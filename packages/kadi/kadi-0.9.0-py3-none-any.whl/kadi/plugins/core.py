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
from flask import current_app
from jinja2 import Markup


def run_hook(name, **kwargs):
    r"""Run the plugin hook with the given name for all registered plugins.

    :param name: The name of the hook.
    :param \**kwargs: Additional keyword arguments that will be passed to the hook.
    :return: A single result, if ``firstresult`` is set to ``True`` in the hook spec, or
        a list of results.
    :raises ValueError: If no valid hook with the given name was found.
    """
    hook = getattr(current_app.plugin_manager.hook, name, None)

    if hook is None:
        raise ValueError(f"No valid hook with the name '{name}' was found.")

    return hook(**kwargs)


def template_hook(name, **kwargs):
    r"""Run the plugin hook with the given name inside a template.

    Uses :func:`run_hook` and joins multiple results together as a string ready to be
    inserted into a template.

    :param name: The name of the hook.
    :param \**kwargs: Additional keyword arguments that will be passed to the hook.
    :return: The template string, which may be empty if the given hook was not found or
        raised an exception.
    """
    try:
        result = run_hook(name, **kwargs)
    except:
        result = ""

    if isinstance(result, list):
        result = "\n".join([r if r is not None else "" for r in result])
    elif result is None:
        result = ""

    return Markup(result)


def get_plugin_config(name):
    """Get the configuration of a plugin.

    For each plugin, configuration can be specified by mapping the name of the plugin to
    the configuration that the plugin expects in the ``PLUGIN_CONFIG`` value as
    configured in the application's configuration.

    :param name: The name of the plugin.
    :return: The plugin configuration or an empty dictionary if no valid configuration
        could be found.
    """
    return current_app.config["PLUGIN_CONFIG"].get(name, {})
