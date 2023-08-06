import pinject
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ..columns import Columns
import os
from ..environment import Environment
from ..secrets import Secrets
import datetime
import inspect
from .binding_config import BindingConfig


class BindingSpec(pinject.BindingSpec):
    object_graph = None
    _bind = None

    def __init__(self, **kwargs):
        self._bind = kwargs

    def build_from_binding_config(self, binding_name):
        binding = self._bind[binding_name]
        # we have 3 options of what was bound: an actual object, which we just return, a Class name, which we
        # ask the object graph to build, or a dictionary with three keys: ['class', 'args', 'kwargs'].  For the
        # latter we as the object graph to build the class and then pass args and kwargs to the build_configure
        # method.
        object_graph = self.provide_object_graph()
        if isinstance(binding, BindingConfig):
            instance = self.object_graph.provide(binding.object_class)
            if not hasattr(instance, 'configure'):
                raise ValueError(
                    f"Requested to build binding '{binding_name}' but the class '{binding.object_class.__name__}' " + \
                    "does not have the necessary 'configure' method"
                )
            instance.configure(*binding.args, **binding.kwargs)
            return instance
        if inspect.isclass(binding):
            return self.object_graph.provide(binding)
        return binding

    def provide_requests(self):
        if 'requests' in self._bind:
            return self.build_from_binding_config('requests')

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            method_whitelist=['GET', 'POST', 'DELETE', 'OPTIONS', 'PATCH']
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        return http

    def provide_object_graph(self):
        """
        This is very hacky.

        The object graph is the dependency injection container, which is never supposed to be
        injected.  However, there are some cases where it is just easier this way, so I'm cheating
        and making it injectable.  Unfortunately, pinject doesn't natively support this, so instead
        the startup of the given service will inject the object graph it builds into the binding spec
        so that we can provide it here.
        """
        if self.object_graph is None:
            raise ValueError("You must manually provide the object graph before requesting it!")

        return self.object_graph

    def provide_columns(self):
        return Columns(self.provide_object_graph())

    def provide_secrets(self):
        if 'secrets' in self._bind:
            return self.build_from_binding_config('secrets')
        return {}

    def provide_environment(self, secrets):
        if 'environment' in self._bind:
            return self._bind['environment']
        return Environment(os.getcwd() + '/.env', os.environ, secrets)

    def provide_cursor(self, environment):
        if 'cursor' in self._bind:
            return self.build_from_binding_config('cursor')
        import mariadb
        connection = mariadb.connect(
            user=environment.get('db_username'),
            password=environment.get('db_password'),
            host=environment.get('db_host'),
            database=environment.get('db_database'),
            autocommit=True,
        )
        return connection.cursor(dictionary=True)

    def provide_now(self):
        if 'now' in self._bind:
            return self.build_from_binding_config('now')
        return datetime.datetime.now()

    def provide_input_output(self):
        if 'input_output' in self._bind:
            return self.build_from_binding_config('input_output')
        raise AttributeError('The dependency injector requested an InputOutput but none has been configured')

    def provide_authentication(self):
        if 'authentication' in self._bind:
            return self.build_from_binding_config('authentication')
        raise AttributeError('The dependency injector requested an Authenticaiton method but none has been configured')

    @classmethod
    def init_application(cls, handler, handler_config, *args, **kwargs):
        object_graph = cls.get_object_graph(*args, **kwargs)
        handler = object_graph.provide(handler)
        handler.configure(handler_config)
        return handler

    @classmethod
    def get_object_graph(cls, *args, **kwargs):
        binding_spec = cls(*args, **kwargs)
        object_graph = pinject.new_object_graph(binding_specs=[binding_spec])
        binding_spec.object_graph = object_graph
        return object_graph
