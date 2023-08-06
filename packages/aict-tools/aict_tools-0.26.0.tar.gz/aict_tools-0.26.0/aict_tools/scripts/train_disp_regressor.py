import pandas as pd
import click
from sklearn import model_selection
from sklearn import metrics
from tqdm import tqdm
import numpy as np

from fact.io import write_data
from ..io import save_model, read_telescope_data
from ..preprocessing import (
    convert_to_float32, calc_true_disp, convert_units, horizontal_to_camera,
)
from ..feature_generation import feature_generation
from ..configuration import AICTConfig
from ..logging import setup_logging


@click.command()
@click.argument('configuration_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('signal_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('predictions_path', type=click.Path(exists=False, dir_okay=False))
@click.argument('disp_model_path', type=click.Path(exists=False, dir_okay=False))
@click.argument('sign_model_path', type=click.Path(exists=False, dir_okay=False))
@click.option('-k', '--key', help='HDF5 key for h5py hdf5', default='events')
@click.option('-v', '--verbose', help='Verbose log output', is_flag=True)
def main(configuration_path, signal_path, predictions_path, disp_model_path, sign_model_path, key, verbose):
    '''
    Train two learners to be able to reconstruct the source position.
    One regressor for disp and one classifier for the sign of delta.

    Both pmml and pickle format are supported for the output.

    CONFIGURATION_PATH: Path to the config yaml file

    SIGNAL_PATH: Path to the signal data

    PREDICTIONS_PATH : path to the file where the mc predictions are stored.

    DISP_MODEL_PATH: Path to save the disp model to.

    SIGN_MODEL_PATH: Path to save the disp model to.
        Allowed extensions are .pkl and .pmml.
        If extension is .pmml, then both pmml and pkl file will be saved
    '''
    log = setup_logging(verbose=verbose)

    config = AICTConfig.from_yaml(configuration_path)
    model_config = config.disp

    np.random.seed(config.seed)

    disp_regressor = model_config.disp_regressor
    sign_classifier = model_config.sign_classifier

    disp_regressor.random_state = config.seed
    sign_classifier.random_state = config.seed

    log.info('Loading data')
    df = read_telescope_data(
        signal_path, config,
        model_config.columns_to_read_train,
        feature_generation_config=model_config.feature_generation,
        n_sample=model_config.n_signal
    )
    log.info('Total number of events: {}'.format(len(df)))

    log.info(
        'Using coordinate transformations for %s',
        model_config.coordinate_transformation
    )

    df = convert_units(df, model_config)
    source_x, source_y = horizontal_to_camera(df, model_config)

    log.info('Using projected disp: {}'.format(model_config.project_disp))
    df['true_disp'], df['true_sign'] = calc_true_disp(
        source_x, source_y,
        df[model_config.cog_x_column], df[model_config.cog_y_column],
        df[model_config.delta_column],
        project_disp=model_config.project_disp,
    )

    # generate features if given in config
    if model_config.feature_generation:
        feature_generation(df, model_config.feature_generation, inplace=True)

    df_train = convert_to_float32(df[config.disp.features])
    df_train.dropna(how='any', inplace=True)

    log.info('Events after nan-dropping: {} '.format(len(df_train)))

    target_disp = df['true_disp'].loc[df_train.index]
    target_sign = df['true_sign'].loc[df_train.index]

    # load optional columns if available to be able to make performance plots
    # vs true energy / size
    if config.true_energy_column is not None:
        true_energy = df.loc[df_train.index, config.true_energy_column].to_numpy()
    if config.size_column is not None:
        size = df.loc[df_train.index, config.size_column].to_numpy()

    if model_config.log_target is True:
        target_disp = np.log(target_disp)

    log.info('Starting {} fold cross validation... '.format(
        model_config.n_cross_validations
    ))
    scores_disp = []
    scores_sign = []
    cv_predictions = []

    kfold = model_selection.KFold(
        n_splits=model_config.n_cross_validations,
        shuffle=True,
        random_state=config.seed,
    )

    total = model_config.n_cross_validations
    for fold, (train, test) in enumerate(tqdm(kfold.split(df_train.values), total=total)):

        cv_x_train, cv_x_test = df_train.values[train], df_train.values[test]

        cv_disp_train, cv_disp_test = target_disp.values[train], target_disp.values[test]
        cv_sign_train, cv_sign_test = target_sign.values[train], target_sign.values[test]

        disp_regressor.fit(cv_x_train, cv_disp_train)
        cv_disp_prediction = disp_regressor.predict(cv_x_test)

        if model_config.log_target is True:
            cv_disp_test = np.exp(cv_disp_test)
            cv_disp_prediction = np.exp(cv_disp_prediction)

        sign_classifier.fit(cv_x_train, cv_sign_train)
        # scale proba for positive sign to [-1, 1], so it's a nice score for the sign
        # where values close to -1 mean high confidence for - and values close to 1 mean
        # high confidence for +
        cv_sign_score = 2 * sign_classifier.predict_proba(cv_x_test)[:, 1] - 1
        cv_sign_prediction = np.where(cv_sign_score < 0, -1.0, 1.0)

        scores_disp.append(metrics.r2_score(cv_disp_test, cv_disp_prediction))
        scores_sign.append(metrics.accuracy_score(cv_sign_test, cv_sign_prediction))

        cv_df = pd.DataFrame({
            'disp': cv_disp_test,
            'disp_prediction': cv_disp_prediction,
            'sign': cv_sign_test,
            'sign_prediction': cv_sign_prediction,
            'sign_score': cv_sign_score,
            'cv_fold': fold,
        })
        if config.true_energy_column is not None:
            cv_df[config.true_energy_column] = true_energy[test]
        if config.size_column is not None:
            cv_df[config.size_column] = size[test]
        cv_predictions.append(cv_df)

    predictions_df = pd.concat(cv_predictions, ignore_index=True)

    log.info('writing predictions from cross validation')
    write_data(predictions_df, predictions_path, mode='w')

    scores_disp = np.array(scores_disp)
    scores_sign = np.array(scores_sign)
    log.info('Cross validated R^2 scores for disp: {}'.format(scores_disp))
    log.info('Mean R^2 score from CV: {:0.4f} ± {:0.4f}'.format(
        scores_disp.mean(), scores_disp.std()
    ))

    log.info('Cross validated accuracy for the sign: {}'.format(scores_sign))
    log.info('Mean accuracy from CV: {:0.4f} ± {:0.4f}'.format(
        scores_sign.mean(), scores_sign.std()
    ))

    log.info('Building new model on complete data set...')
    # set random seed again to make sure different settings
    # for n_cross_validations don't change the final model
    np.random.seed(config.seed)
    disp_regressor.random_state = config.seed
    sign_classifier.random_state = config.seed

    disp_regressor.fit(df_train.values, target_disp.values)
    sign_classifier.fit(df_train.values, target_sign.values)

    log.info('Pickling disp model to {} ...'.format(disp_model_path))
    save_model(
        disp_regressor,
        feature_names=list(df_train.columns),
        model_path=disp_model_path,
        label_text='abs_disp',
    )
    log.info('Pickling sign model to {} ...'.format(sign_model_path))
    save_model(
        sign_classifier,
        feature_names=list(df_train.columns),
        model_path=sign_model_path,
        label_text='sign_disp',
    )


if __name__ == '__main__':
    main()
