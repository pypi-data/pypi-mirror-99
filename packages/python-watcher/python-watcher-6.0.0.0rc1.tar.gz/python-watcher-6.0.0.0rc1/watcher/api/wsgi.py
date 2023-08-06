# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""WSGI script for Watcher API, installed by pbr."""

import sys

from oslo_config import cfg
import oslo_i18n as i18n
from oslo_log import log

from watcher.api import app
from watcher.common import service


CONF = cfg.CONF
LOG = log.getLogger(__name__)


def initialize_wsgi_app(show_deprecated=False):
    i18n.install('watcher')

    service.prepare_service(sys.argv)

    LOG.debug("Configuration:")
    CONF.log_opt_values(LOG, log.DEBUG)

    if show_deprecated:
        LOG.warning("Using watcher/api/app.wsgi is deprecated and it will "
                    "be removed in U release. Please use automatically "
                    "generated watcher-api-wsgi instead.")

    return app.VersionSelectorApplication()
