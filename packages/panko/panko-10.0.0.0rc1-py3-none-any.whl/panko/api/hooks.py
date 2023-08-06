#
# Copyright 2012 New Dream Network, LLC (DreamHost)
#
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

from pecan import hooks

from panko import storage


class ConfigHook(hooks.PecanHook):
    """Attach the configuration object to the request.

    That allows controllers to get it.
    """

    def __init__(self, conf):
        super(ConfigHook, self).__init__()
        self.conf = conf

    def before(self, state):
        state.request.cfg = self.conf


class DBHook(hooks.PecanHook):

    def __init__(self, conf):
        self.connection = storage.get_connection_from_config(
            conf)

    def before(self, state):
        state.request.conn = self.connection


class TranslationHook(hooks.PecanHook):

    def after(self, state):
        # After a request has been done, we need to see if
        # ClientSideError has added an error onto the response.
        # If it has we need to get it info the thread-safe WSGI
        # environ to be used by the ParsableErrorMiddleware.
        if hasattr(state.response, 'translatable_error'):
            state.request.environ['translatable_error'] = (
                state.response.translatable_error)
