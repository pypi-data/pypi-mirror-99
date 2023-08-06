"""
Tool for analyzing satellite telemetry
"""
import logging

import click

from polaris import __version__
from polaris.batch.batch import batch
from polaris.fetch.data_fetch_decoder import data_fetch_decode_normalize
from polaris.learn.analysis import cross_correlate, feature_extraction
from polaris.viz.server import launch_webserver

# Logger configuration

# Set the logger name explicitly to 'polaris'; if we use __name__
# here, we get 'polaris.polaris', which is redundant. It also allows
# modules to use the parent logger, as their __name__ begins with
# 'polaris', not 'polaris.polaris'.
LOGGER = logging.getLogger('polaris')
CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)
CH.setFormatter(FORMATTER)
LOGGER.addHandler(CH)


@click.version_option(version=__version__)
@click.group()
def cli():
    """
    Tool for analyzing satellite telemetry
    """
    return


@click.command('fetch',
               context_settings={"ignore_unknown_options": True},
               short_help='Download data set(s)')
@click.argument('sat', nargs=1, required=True)
@click.argument('output_file',
                required=True,
                type=click.Path(resolve_path=True))
@click.option('--start_date',
              '-s',
              is_flag=False,
              help='Start date of the fetching period.'
              ' Default: set to 1h ago from now.')
@click.option('--end_date',
              '-e',
              is_flag=False,
              help='End date of fetching period.'
              ' Default: 1h period from start date.')
@click.option('--cache_dir',
              '-c',
              required=False,
              is_flag=False,
              default='/tmp',
              type=click.Path(resolve_path=True),
              help='Directory to save temporary downloaded files.')
@click.option('--import_file',
              '-i',
              required=False,
              default=None,
              is_flag=False,
              help='Import data frames downloaded from db.satnogs.org.')
@click.option('--existing-output-file-strategy',
              type=click.Choice(['merge', 'overwrite', 'error']),
              default='merge',
              show_default=True,
              help='How to handle already-existing output file: ' +
              'merge with it, overwrite it, or exit with an error.')
@click.option('--fetch_from_influxdb',
              is_flag=True,
              help='Fetch space weather data from influxdb')
@click.option('--store_in_influxdb',
              is_flag=True,
              help='Store data in influxdb')
@click.option('--skip_normalizer',
              is_flag=True,
              help='Skip normalizing. Returns data as decoded')
@click.option('--ignore_errors',
              is_flag=True,
              default=False,
              help=' '.join(
                  ['Ignore errors when decoding frames (Default: False)']))
# pylint: disable-msg=too-many-arguments
def cli_fetch(sat, start_date, end_date, output_file, cache_dir, import_file,
              existing_output_file_strategy, store_in_influxdb,
              fetch_from_influxdb, skip_normalizer, ignore_errors):
    """ Obtain telemetry data

    Retrieve and decode the telemetry corresponding to
    SAT (satellite name or NORAD ID) and stores in
    OUTPUT_FILE (path to the output folder)
    """
    data_fetch_decode_normalize(
        sat, start_date, end_date, output_file, cache_dir, import_file,
        existing_output_file_strategy, skip_normalizer, ignore_errors, **{
            "store_in_influxdb": store_in_influxdb,
            "fetch_from_influxdb": fetch_from_influxdb,
        })


@click.command('learn', short_help='Analyze data')
@click.argument('input_file', nargs=1, required=True)
@click.option('--output_graph_file',
              '-g',
              is_flag=False,
              help='Output json graph file')
@click.option('--learn_config_file',
              '-l',
              is_flag=False,
              default=None,
              help='Path to a learn configuration file')
@click.option('--graph_link_threshold',
              '-t',
              default=0.1,
              is_flag=False,
              help='Threshold of influence to show edges')
@click.option('--col',
              '-c',
              is_flag=False,
              help='Target column to extract features for')
@click.option('--use_gridsearch',
              '-d',
              is_flag=True,
              help='Using gridsearch to perform predictions')
@click.option('--csv_sep',
              '-s',
              is_flag=False,
              help='The separator used in the input csv file')
@click.option('--force_cpu',
              is_flag=True,
              help='For force running on CPU (on machines with NVIDIA GPUs)')
# pylint: disable-msg=too-many-arguments
def cli_learn(input_file,
              output_graph_file=None,
              learn_config_file=None,
              graph_link_threshold=0.1,
              col=None,
              use_gridsearch=False,
              csv_sep=',',
              force_cpu=False):
    """ Analyze telemetry data

    Apply machine learning and feature engineering
    to analyse data from INPUT_FILE (path to input json or CSV file)
    """
    if col is not None:
        feature_extraction(input_file, col)
    elif output_graph_file is not None:
        cross_correlate(input_file,
                        output_graph_file,
                        xcorr_configuration_file=learn_config_file,
                        graph_link_threshold=graph_link_threshold,
                        use_gridsearch=use_gridsearch,
                        csv_sep=csv_sep,
                        force_cpu=force_cpu)
    else:
        LOGGER.warning(" ".join([
            "You must provide either --col",
            "or --output-graph-file arguments!"
        ]))


@click.command('viz', short_help='Display results')
@click.argument('graph_file', nargs=1, required=True)
def cli_viz(graph_file):
    """ Visualize the results of the learn command

    Serves HTML5 visualization of GRAPH_FILE (JSON data
    file with graph information about nodes and edges)
    """
    launch_webserver(graph_file)


@click.command('batch', short_help='Run polaris commands in batch mode')
@click.option('--config_file',
              is_flag=False,
              required=False,
              default='polaris_config.json',
              type=click.Path(resolve_path=True),
              help='Config file for polaris batch.')
@click.option('--dry-run/--no-dry-run',
              required=False,
              default=False,
              help='Show what would be run in batch mode')
def cli_batch(config_file, dry_run):
    """ Run polaris from batch: runs polaris commands non-interactively

        :param config_file: path to configuration file
        :param dry_run: Bool for dry run mode
    """
    batch(config_file, dry_run)


# click doesn't automagically add the commands to the group
# (and thus to the help output); you have to do it manually.
cli.add_command(cli_fetch)
cli.add_command(cli_learn)
cli.add_command(cli_viz)
cli.add_command(cli_batch)
