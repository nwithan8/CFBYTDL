from modules.yt_cfb_processor import Processor
from modules.config_parser import ConfigParser

config = ConfigParser(app_name="CFBYTDL", config_path="config.yaml")

if __name__ == "__main__":
    processor = Processor(cfbd_api_key=config.cfbd_api_key)
    processor.run()
