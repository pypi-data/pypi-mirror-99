"""Config helper."""

import base64
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Mapping, Optional, Union, cast

import toml
from dotenv import load_dotenv
from outcome.utils import env

ValidPath = Union[str, Path]
ValidConfigType = Union[str, int, float, bool, List['ValidConfigType']]
ConfigDict = Mapping[str, ValidConfigType]


class Sentinel:
    ...


NO_DEFAULT = Sentinel()


class ConfigBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> ValidConfigType:  # pragma: no cover
        ...

    @abstractmethod
    def __contains__(self, key: str) -> bool:  # pragma: no cover
        ...


base_64_protocol = 'base64://'  # noqa: WPS114


class EnvBackend(ConfigBackend):
    def __init__(self):
        dotenv_file = Path.cwd() / '.env'
        load_dotenv(dotenv_path=dotenv_file, verbose=env.is_dev())

    def get(self, key: str) -> ValidConfigType:
        value = os.environ[key]

        # We can define protocols as suffix of the env variable.
        # For instance, if the env variable starts with `base64://` we will decode the rest of the string
        # with b64decode.
        #
        # This can be useful to store RSA keys as env variable since they need to be encoded as base64 strings.
        # This can also be used to specify a path to sensitive data stored in a remote database, and the get function
        # will be able to fetch the corresponding data depending on the specified protocol.
        if value.startswith(base_64_protocol):
            return base64.b64decode(value[len(base_64_protocol) :]).decode('utf-8')

        return value

    def __contains__(self, key: str) -> bool:
        return key in os.environ


class DefaultBackend(ConfigBackend):

    defaults: Mapping[str, ValidConfigType]

    def __init__(self, defaults: Mapping[str, ValidConfigType]):
        self.defaults = defaults

    def get(self, key: str) -> ValidConfigType:
        return self.defaults[key]

    def __contains__(self, key: str) -> bool:
        return key in self.defaults


class TomlBackend(ConfigBackend):

    path: Optional[ValidPath]
    config: Optional[ConfigDict]
    aliases: Optional[Mapping[str, str]]

    def __init__(self, path: Optional[ValidPath] = None, aliases: Optional[Mapping[str, str]] = None):
        self.path = path
        self.aliases = aliases
        self.config = None

    def get(self, key: str) -> ValidConfigType:
        if not self.config:
            self.load_config()
        assert self.config is not None
        return self.config[key]

    def __contains__(self, key: str) -> bool:
        if not self.config:
            self.load_config()
        return key in self.config

    def load_config(self):
        assert self.path
        self.config = self.get_config(self.path, self.aliases)

    @classmethod
    def get_config(  # noqa: WPS615
        cls, path: ValidPath, aliases: Optional[Mapping[str, str]] = None,
    ) -> Mapping[str, ValidConfigType]:
        config = toml.load(path)
        config_flattened = dict(cls.flatten_keys(config))

        if aliases:
            for original, alias in aliases.items():
                config_flattened[alias.upper()] = config_flattened.pop(original.upper())

        return config_flattened

    @classmethod
    def flatten_keys(cls, value: object, key: Optional[str] = None) -> Mapping[str, ValidConfigType]:
        if not isinstance(value, dict):
            if not key:
                raise Exception('Value cannot be a non-dict without a key')

            assert isinstance(value, (str, int, float, bool, list))
            return {key.upper(): cast(ValidConfigType, value)}

        flattened: Mapping[str, ValidConfigType] = {}
        value = cast(Mapping[str, object], value)

        for k, v in value.items():
            prefix = (f'{key}_' if key else '').upper()
            flattened.update({f'{prefix}{skey}': sval for skey, sval in cls.flatten_keys(v, k).items()})

        return flattened


class Config:  # pragma: only-covered-in-unit-tests
    """This class helps with retrieving config values from a project environment.

    You can provide a path to a TOML file, typically the pyproject.toml, or just
    let the class try to extract the values from environment variables.

    Environment variables will always take precedence over the values found in the file.

    The keys from the TOML file will be flattened and transformed to uppercase, following
    environment variable conventions.

    For example:

    ```toml
    [app]
    port = 80
    ```

    Will be transformed into

    ```py
    {
        'APP_PORT': 80
    }
    ```

    If needed you can modify Config backends to change the order of priority, or to add your own backends.
    You can use add_backend method to add your own backend at the desired priority.
    If you wish to add your own backend, it needs to inherit from ConfigBackend abstract class.
    """

    backends: List[ConfigBackend]
    default_backend: DefaultBackend

    def __init__(
        self,
        path: Optional[ValidPath] = None,
        aliases: Optional[Mapping[str, str]] = None,
        defaults: Optional[Mapping[str, ValidConfigType]] = None,
    ) -> None:
        """Initialize the class with an optional config file and set of aliases.

        The aliases dict will rewrite config keys from key to value:

        ```
        aliases = {'ORIGINAL_KEY': 'NEW_KEY'}
        config = Config('some_file.toml', aliases)

        config.get('ORIGINAL_KEY')  # -> raises KeyError
        config.get('NEW_KEY')  # -> returns value
        ```

        The defaults dict is the final fallback.

        Arguments:
            path (ValidPath, optional): The path to the config file.
            aliases (Mapping[str, str], optional): The aliasing dict.
            defaults (Mapping[str, ValidConfigType], optional): A dict of hardcoded values
        """
        self.backends = [EnvBackend()]
        if path:
            self.backends.append(TomlBackend(path=path, aliases=aliases))

        self.default_backend = DefaultBackend(defaults or {})

    def get(self, key: str, default: Union[Optional[ValidConfigType], Sentinel] = NO_DEFAULT) -> Optional[ValidConfigType]:

        for backend in self.backends:
            if key in backend:
                return backend.get(key)

        try:
            return self.default_backend.get(key)
        except KeyError as exc:
            if not isinstance(default, Sentinel):
                return default
            raise exc

    def add_backend(self, backend: ConfigBackend, priority: int):
        self.backends.insert(priority, backend)


class AppConfig(Config):
    # This class wraps Config in order to modify return value of APP_NAME
    #
    # Indeed, in most pyprojecttoml files, the application name is of the form `myproject-api-app`,
    # which maps to the name of its Github repository or Docker image.
    #
    # However, in our application environment, we only want to keep `myproject`.
    # This allows for instance to use APP_NAME to fetch the right service of OTCServices.

    def get(self, key: str, default: Union[Optional[ValidConfigType], Sentinel] = NO_DEFAULT) -> Optional[ValidConfigType]:
        key_value = super().get(key, default)
        if key == 'APP_NAME':
            if key_value is default and not isinstance(default, Sentinel):
                return default
            assert isinstance(key_value, str)
            return key_value.split('-')[0]
        return key_value
