import typer, os, pathlib, errno

from .schema import Config
from ..utils import APP_NAME
from .utils import TextEnum


def create_path_if_not_exists(path: pathlib.Path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


class ConfigController:

    class HandlerMode(TextEnum):
        WRITE = "w"
        READ = "r"

    def __init__(self, mode: HandlerMode):
        app_dir = typer.get_app_dir(APP_NAME)
        self.file_path = pathlib.Path(app_dir) / "config.json"
        self.mode = mode
        self.file = None

    def __enter__(self):
        create_path_if_not_exists(self.file_path)
        if not self.file_path.is_file():
            with open(self.file_path, "w", encoding='utf8') as file:
                raw_data = Config.default().json()
                file.write(raw_data)
        self.file = open(self.file_path, mode=self.mode, encoding="utf8")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    @classmethod
    def parse_config(cls):
        with cls(cls.HandlerMode.READ) as file:
            file_content = file.read()
        return Config.parse_raw(file_content)

    @classmethod
    def write_config(cls, config: Config):
        file_content = config.json()
        with cls(cls.HandlerMode.WRITE) as file:
            file.write(file_content)
