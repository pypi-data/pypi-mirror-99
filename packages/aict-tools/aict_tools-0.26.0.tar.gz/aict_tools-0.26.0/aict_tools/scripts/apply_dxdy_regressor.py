import click
import numpy as np
from tqdm import tqdm

from ..io import (
    append_column_to_hdf5,
    read_telescope_data_chunked,
    get_column_names_in_file,
    remove_column_from_file,
    load_model,
)
from ..apply import predict_dxdy
from ..configuration import AICTConfig
from ..logging import setup_logging
from ..preprocessing import calc_true_disp


@click.command()
@click.argument('configuration_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('data_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('dxdy_model_path', type=click.Path(exists=False, dir_okay=False))
@click.option('-n', '--n-jobs', type=int, help='Number of cores to use')
@click.option('-y', '--yes', help='Do not prompt for overwrites', is_flag=True)
@click.option('-v', '--verbose', help='Verbose log output', is_flag=True)
@click.option(
    '-N', '--chunksize', type=int,
    help='If given, only process the given number of events at once',
)
def main(configuration_path, data_path, dxdy_model_path, chunksize, n_jobs, yes, verbose):
    '''
    Apply given model to data. Three columns are added to the file, source_x_prediction, source_y_prediction
    and disp_prediction

    CONFIGURATION_PATH: Path to the config yaml file
    DATA_PATH: path to the FACT data in a h5py hdf5 file, e.g. erna_gather_fits output
    DXDY_MODEL_PATH: Path to the pickled dxdy model.
    '''
    log = setup_logging(verbose=verbose)

    config = AICTConfig.from_yaml(configuration_path)
    model_config = config.dxdy

    columns_to_delete = [
        'source_x_prediction',
        'source_y_prediction',
        'theta',
        'theta_deg',
        'theta_rec_pos',
        'disp_prediction',
    ]
    for i in range(1, 6):
        columns_to_delete.extend([
            'theta_off_' + str(i),
            'theta_deg_off_' + str(i),
            'theta_off_rec_pos_' + str(i),
        ])

    n_del_cols = 0

    for column in columns_to_delete:
        if column in get_column_names_in_file(data_path, config.telescope_events_key):
            if not yes:
                click.confirm(
                    'Dataset "{}" exists in file, overwrite?'.format(column),
                    abort=True,
                )
                yes = True
            remove_column_from_file(data_path, config.telescope_events_key, column)
            log.warn("Deleted {} from the feature set.".format(column))
            n_del_cols += 1

    if n_del_cols > 0:
        log.warn("Source dependent features need to be calculated from the predicted source possition. "
                 + "Use e.g. `fact_calculate_theta` from https://github.com/fact-project/pyfact.")

    log.info('Loading model')
    dxdy_model = load_model(dxdy_model_path)
    log.info('Done')

    if n_jobs:
        dxdy_model.n_jobs = n_jobs

    df_generator = read_telescope_data_chunked(
        data_path, config, chunksize, model_config.columns_to_read_apply,
        feature_generation_config=model_config.feature_generation
    )

    log.info('Predicting on data...')
    for df_data, start, stop in tqdm(df_generator):

        dxdy = predict_dxdy(
            df_data[model_config.features], dxdy_model,
            log_target=model_config.log_target,
        )

        source_x = df_data[model_config.cog_x_column] + dxdy[:,0]
        source_y = df_data[model_config.cog_y_column] + dxdy[:,1]
        
        key = config.telescope_events_key
        append_column_to_hdf5(data_path, source_x, key, 'source_x_prediction')
        append_column_to_hdf5(data_path, source_y, key, 'source_y_prediction')


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
