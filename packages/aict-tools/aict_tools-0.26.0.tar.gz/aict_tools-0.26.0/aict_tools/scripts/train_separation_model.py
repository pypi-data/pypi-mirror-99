import pandas as pd
import click
from sklearn import model_selection
from sklearn.calibration import CalibratedClassifierCV
from tqdm import tqdm
import numpy as np
from sklearn import metrics
from fact.io import check_extension, write_data

from ..configuration import AICTConfig
from ..io import save_model, read_telescope_data
from ..preprocessing import convert_to_float32
from ..logging import setup_logging


@click.command()
@click.argument('configuration_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('signal_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('background_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('predictions_path', type=click.Path(exists=False, dir_okay=False))
@click.argument('model_path', type=click.Path(exists=False, dir_okay=False))
@click.option('-v', '--verbose', help='Verbose log output', is_flag=True)
def main(configuration_path, signal_path, background_path, predictions_path, model_path, verbose):
    '''
    Train a classifier on signal and background monte carlo data and write the model
    to MODEL_PATH in pmml or pickle format.

    CONFIGURATION_PATH: Path to the config yaml file

    SIGNAL_PATH: Path to the signal data

    BACKGROUND_PATH: Path to the background data

    PREDICTIONS_PATH : path to the file where the mc predictions are stored.

    MODEL_PATH: Path to save the model to. Allowed extensions are .pkl and .pmml.
        If extension is .pmml, then both pmml and pkl file will be saved
    '''
    log = setup_logging(verbose=verbose)

    check_extension(predictions_path)
    check_extension(model_path, allowed_extensions=['.pmml', '.pkl', '.onnx'])

    config = AICTConfig.from_yaml(configuration_path)
    model_config = config.separator
    label_text = model_config.output_name

    log.info('Loading signal data')
    df_signal = read_telescope_data(
        signal_path, config, model_config.columns_to_read_train,
        feature_generation_config=model_config.feature_generation,
        n_sample=model_config.n_signal
    )
    df_signal['label_text'] = 'signal'
    df_signal['label'] = 1

    log.info('Loading background data')
    df_background = read_telescope_data(
        background_path, config, model_config.columns_to_read_train,
        feature_generation_config=model_config.feature_generation,
        n_sample=model_config.n_background
    )
    df_background['label_text'] = 'background'
    df_background['label'] = 0

    df = pd.concat([df_background, df_signal], ignore_index=True)

    df_train = convert_to_float32(df[model_config.features])
    log.debug('Total training events: {}'.format(len(df_train)))

    df_train.dropna(how='any', inplace=True)
    log.debug('Training events after dropping nans: {}'.format(len(df_train)))

    label = df.loc[df_train.index, 'label']

    # load optional columns if available to be able to make performance plots
    # vs true energy / size
    if config.true_energy_column is not None:
        true_energy = df.loc[df_train.index, config.true_energy_column].to_numpy()
    if config.size_column is not None:
        size = df.loc[df_train.index, config.size_column].to_numpy()

    n_gammas = len(label[label == 1])
    n_protons = len(label[label == 0])
    log.info('Training classifier with {} background and {} signal events'.format(
        n_protons, n_gammas
    ))
    log.debug(model_config.features)

    # save prediction_path for each cv iteration
    cv_predictions = []

    # iterate over test and training sets
    X = df_train.values
    y = label.values
    n_cross_validations = model_config.n_cross_validations
    classifier = model_config.model

    log.info('Starting {} fold cross validation... '.format(n_cross_validations))

    stratified_kfold = model_selection.StratifiedKFold(
        n_splits=n_cross_validations, shuffle=True, random_state=config.seed
    )

    aucs = []
    cv_it = stratified_kfold.split(X, y)
    for fold, (train, test) in enumerate(tqdm(cv_it, total=n_cross_validations)):
        # select data
        xtrain, xtest = X[train], X[test]
        ytrain, ytest = y[train], y[test]

        # fit and predict
        classifier.fit(xtrain, ytrain)

        y_probas = classifier.predict_proba(xtest)[:, 1]

        cv_df = pd.DataFrame({
            'label': ytest,
            model_config.output_name: y_probas,
            'cv_fold': fold,
        })
        if config.true_energy_column is not None:
            cv_df[config.true_energy_column] = true_energy[test]
        if config.size_column is not None:
            cv_df[config.size_column] = size[test]
        cv_predictions.append(cv_df)
        aucs.append(metrics.roc_auc_score(ytest, y_probas))

    aucs = np.array(aucs)
    log.info('Cross-validation ROC-AUCs: {}'.format(aucs))
    log.info('Mean AUC ROC : {:.3f} ± {:.3f}'.format(aucs.mean(), aucs.std()))

    predictions_df = pd.concat(cv_predictions, ignore_index=True)
    log.info('Writing predictions from cross validation')
    write_data(predictions_df, predictions_path, mode='w')

    # set random seed again to make sure different settings
    # for n_cross_validations don't change the final model
    np.random.seed(config.seed)
    classifier.random_state = config.seed

    if model_config.calibrate_classifier:
        log.info('Training calibrated classifier')
        classifier = CalibratedClassifierCV(classifier, cv=2, method='sigmoid')
        classifier.fit(X, y)
    else:
        log.info('Training model on complete dataset')
        classifier.fit(X, y)

    log.info('Saving model to {} ...'.format(model_path))
    save_model(
        classifier,
        model_path=model_path,
        label_text=label_text,
        feature_names=list(df_train.columns)
    )


if __name__ == '__main__':
    main()
