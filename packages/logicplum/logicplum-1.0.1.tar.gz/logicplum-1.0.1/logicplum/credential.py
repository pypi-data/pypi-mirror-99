import yaml
import base64
import pathlib

from . import config


class ClientBase:
    def __init__(self, token: str, config_path: str) -> None:
        """
        token from class argument or yaml configuration (token) file.
        """
        if token is None and config_path is None:
            raise NameError(
                "Please pass a token or yaml configuration file (token as a key).")
        
        if token is None:
            if not pathlib.Path(config_path).is_file():
                raise ValueError("config_path: File does not exist.")
            with open(config_path, "r") as file:
                token_config: dict = yaml.load(file, Loader=yaml.FullLoader)

            if config.YAML_TOKEN_KEY not in token_config.keys():
                raise KeyError(f"token: token key required in {config_path} file")

            token: str = token_config[config.YAML_TOKEN_KEY]
        try:
            token_str: str = base64.b64decode(token.encode()).decode()
        except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError):
            raise UnicodeError(
                "Invalid Token. Please login to LogicPlum platform to get a new token.")
        except:
            raise ValueError("Unknown Error.")

        token_split: str = token_str.split("||")
        if len(token_split) != 3 or token_split[0] not in config.ALLOWED_ENVIRONMENTS.keys():
            raise ValueError(
                "Invalid token. Please login to LogicPlum platform to get a new token.")

        self.token: str = token
        self.endpoint: str = config.ALLOWED_ENVIRONMENTS[token_split[0]]


class Client(ClientBase):
    def __init__(self, token: str = None, config_path: str = None) -> None:
        super().__init__(token=token, config_path=config_path)
