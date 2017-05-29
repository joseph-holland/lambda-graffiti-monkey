# -*- coding: utf-8 -*-

from __future__ import print_function
from graffiti_monkey import cli as gm_cli
from pprint import pprint

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def envvar_to_list(envvar):
    return os.environ[envvar].split(',')


def handler(event, context):
    log.info('Loading function')
    try:
        gm = gm_cli.GraffitiMonkeyCli()
        gm.region = os.environ['REGION']
        gm.config = {"_instance_tags_to_propagate": envvar_to_list('INSTANCE_TAGS_TO_PROPAGATE'),
                     "_volume_tags_to_propagate": envvar_to_list('VOLUME_TAGS_TO_PROPAGATE'),
                     "_volume_tags_to_be_set": envvar_to_list('VOLUME_TAGS_TO_BE_SET'),
                     "_snapshot_tags_to_be_set": envvar_to_list('SNAPSHOT_TAGS_TO_BE_SET'),
                     "_instance_filter": envvar_to_list('INSTANCE_FILTER'),
                     }
        gm.initialize_monkey()
        gm.start_tags_propagation()

        return 'Graffiti Monkey completed successfully!'

    except KeyError, e:
        log.error('Error: Environment variable not set: ' + str(e))
    except Exception, e:
        log.error('Error: Graffiti Monkey encountered the following error: ' + str(e))
