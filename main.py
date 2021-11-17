from modules.yt_cfb_processor import Processor

# config = ConfigParser(app_name="SportsYTDL", config_path="config.yaml")

if __name__ == "__main__":
    processor = Processor()
    processor.run()
