###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import click
import logging
import os
from pathlib import Path
from urllib.parse import urlparse

from wis2box import cli_helpers
from wis2box.util import yaml_load
from wis2box.log import setup_logger

LOGGER = logging.getLogger(__name__)

with (Path(__file__).parent / 'resources' / 'data-mappings.yml').open() as fh:
    DATADIR_DATA_MAPPINGS = yaml_load(fh)

try:
    DATADIR = Path(os.environ.get('WIS2BOX_DATADIR'))
    DATADIR_INCOMING = DATADIR / 'data' / 'incoming'
    DATADIR_PUBLIC = DATADIR / 'data' / 'public'
    DATADIR_ARCHIVE = DATADIR / 'data' / 'archive'
    API_CONFIG = Path(os.environ.get('WIS2BOX_API_CONFIG'))
except (OSError, TypeError):
    import traceback
    print(traceback.format_exc())
    msg = 'Configuration filepaths do not exist!'
    LOGGER.error(msg)
    raise EnvironmentError(msg)

API_TYPE = os.environ.get('WIS2BOX_API_TYPE')
API_URL = os.environ.get('WIS2BOX_API_URL')
API_BACKEND_TYPE = os.environ.get('WIS2BOX_API_BACKEND_TYPE')
API_BACKEND_URL = os.environ.get('WIS2BOX_API_BACKEND_URL').rstrip('/')
OSCAR_API_TOKEN = os.environ.get('WIS2BOX_OSCAR_API_TOKEN')
URL = os.environ.get('WIS2BOX_URL')

BROKER = os.environ.get('WIS2BOX_BROKER')
broker_url = urlparse(BROKER)
if broker_url.port is not None:
    broker_url_port = f':{broker_url.port}'
else:
    broker_url_port = ''

MQP_URL = f'{broker_url.scheme}://{broker_url.hostname}{broker_url_port}/'

try:
    DATA_RETENTION_DAYS = int(os.environ.get('WIS2BOX_DATA_RETENTION_DAYS'))
except TypeError:
    DATA_RETENTION_DAYS = None


LOGLEVEL = os.environ.get('WIS2BOX_LOGGING_LOGLEVEL', 'ERROR')
LOGFILE = os.environ.get('WIS2BOX_LOGGING_LOGFILE', 'stdout')

if 'WIS2BOX_DATADIR_DATA_MAPPINGS' in os.environ:
    LOGGER.debug('Overriding WIS2BOX_DATADIR_DATA_MAPPINGS')
    try:
        with open(os.environ.get('WIS2BOX_DATADIR_DATA_MAPPINGS')) as fh:
            DATADIR_DATA_MAPPINGS = yaml_load(fh)
            assert DATADIR_DATA_MAPPINGS is not None
    except Exception as err:
        DATADIR_DATA_MAPPINGS = None
        msg = f'Missing data mappings: {err}'
        LOGGER.error(msg)
        raise EnvironmentError(msg)


if None in [
    DATADIR,
    DATADIR_INCOMING,
    DATADIR_PUBLIC,
    OSCAR_API_TOKEN,
    API_TYPE,
    API_URL,
    MQP_URL,
    URL
]:
    msg = 'Environment variables not set!'
    LOGGER.error(msg)
    raise EnvironmentError(msg)


@click.group()
def environment():
    """Environment management"""
    pass


@click.command()
@click.pass_context
@cli_helpers.OPTION_VERBOSITY
def create(ctx, verbosity):
    """Creates baseline data/metadata directory structure"""

    click.echo(f'Setting up logging (loglevel={LOGLEVEL}, logfile={LOGFILE})')
    setup_logger(LOGLEVEL, LOGFILE)

    click.echo(f'Creating baseline directory structure in {DATADIR}')
    DATADIR.mkdir(parents=True, exist_ok=True)
    DATADIR_INCOMING.mkdir(parents=True, exist_ok=True)
    DATADIR_PUBLIC.mkdir(parents=True, exist_ok=True)
    (DATADIR / 'cache').mkdir(parents=True, exist_ok=True)
    (DATADIR / 'config').mkdir(parents=True, exist_ok=True)
    (DATADIR / 'metadata' / 'discovery').mkdir(parents=True, exist_ok=True)
    (DATADIR / 'metadata' / 'station').mkdir(parents=True, exist_ok=True)


@click.command()
@click.pass_context
@cli_helpers.OPTION_VERBOSITY
def show(ctx, verbosity):
    """Displays wis2box environment variables"""

    for key, value in os.environ.items():
        if key.startswith('WIS2BOX'):
            click.echo(f'{key} => {value}')


environment.add_command(create)
environment.add_command(show)
