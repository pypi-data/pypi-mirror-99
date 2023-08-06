# -*- coding: utf-8 -*-
import logging

from flasgger import swag_from
from pathlib import Path
from http import HTTPStatus
from vantage6.common import logger_name
from vantage6.server.resource import ServicesResources


module_name = logger_name(__name__)
log = logging.getLogger(module_name)


def setup(api, api_base, services):

    path = "/".join([api_base, module_name])
    log.info(f'Setting up "{path}" and subdirectories')

    api.add_resource(
        Test,
        path,
        endpoint='test',
        methods=('GET',),
        resource_class_kwargs=services
    )


# ------------------------------------------------------------------------------
# Resources / API's
# ------------------------------------------------------------------------------
class Test(ServicesResources):

    @swag_from(str(Path(r"swagger/websocket-test.yaml")),
               endpoint='websocket_test')
    def get(self):
        """Return something."""
        self.socketio.send("you're welcome!", room='all_nodes')
        return self.socketio.server.manager.rooms, HTTPStatus.OK
