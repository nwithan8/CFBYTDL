import confuse


class ConfigParser:
    def __init__(self, app_name: str, config_path: str):
        self.config = confuse.Configuration(app_name)
        self.config.set_file(filename=config_path)

    @property
    def _cfbd_config(self):
        return self.config['CFBD'].get()

    @property
    def _ytdl_config(self):
        return self.config['YTDL'].get()

    @property
    def cfbd_api_key(self) -> str:
        return self._cfbd_config.get('APIKey', '')
