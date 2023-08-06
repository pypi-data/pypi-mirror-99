"""
(c) Copyright 2016 Hewlett-Packard Enterprise Development Company, L.P.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import sys

from oslo_config import cfg
from paste import deploy
from paste import urlmap

from freezer_api.cmd import api
from freezer_api.common import config

CONF = cfg.CONF


def root_app_factory(loader, global_conf, **local_conf):
    """Freezer can manage multiple versions, but
    only launch one version at a time, Otherwise it is
     easy to cause confusion. If there is a demand in the future
    for a single freezer-api instance to support both v1 and v2 at a time,
    you need to add a new patch to implement it.
    """
    if CONF.enable_v1_api and '/v1' in local_conf:
        del local_conf['/v2']
    else:
        del local_conf['/v1']
    return urlmap.urlmap_factory(loader, global_conf, **local_conf)


def freezer_appv1_factory(global_conf, **local_conf):
    return api.build_app_v1()


def freezer_appv2_factory(global_conf, **local_conf):
    return api.build_app_v2()


def initialize_app(conf=None, name='main'):
    """ initializing app for paste to deploy it """

    # register and parse arguments
    config.parse_args(args=sys.argv[1:])
    # register logging opts
    config.setup_logging()
    # locate and load paste file
    conf = config.find_paste_config()
    app = deploy.loadapp('config:%s' % conf, name=name)
    return app
