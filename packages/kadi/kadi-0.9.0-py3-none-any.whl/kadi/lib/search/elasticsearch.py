# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from elasticsearch import Elasticsearch as _Elasticsearch
from elasticsearch.exceptions import ImproperlyConfigured
from flask import _app_ctx_stack
from flask import current_app
from flask.globals import _app_ctx_err_msg


class Elasticsearch:
    """Elasticsearch client for use in a Flask application.

    Wraps the official client for ease of use in a Flask application. Requires an
    application context, as it uses the application's configuration value
    ``ELASTICSEARCH_HOSTS`` to specifiy one or more Elasticsearch nodes to connect to.

    :param app: (optional) The application object. Will only be used to call
        :meth:`init_app`, which may also be called manually afterwards instead.
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the application's configuration.

        Will initialize ``ELASTICSEARCH_HOSTS`` to ``"http://localhost:9200"`` if not
        present already in the application's configuration.

        :param app: The application object.
        """
        app.config.setdefault("ELASTICSEARCH_HOSTS", "http://localhost:9200")

    def __getattr__(self, attr):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "elasticsearch"):
                hosts = current_app.config["ELASTICSEARCH_HOSTS"]

                if isinstance(hosts, str):
                    hosts = [hosts]
                elif not hosts:
                    hosts = []

                try:
                    ctx.elasticsearch = _Elasticsearch(hosts=hosts)
                except ImproperlyConfigured as e:
                    raise RuntimeError("Elasticsearch is disabled.") from e

            return getattr(ctx.elasticsearch, attr)

        raise RuntimeError(_app_ctx_err_msg)


es = Elasticsearch()
