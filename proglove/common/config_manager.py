import configparser


class ConfigManager:
    _config_folder = '/data'
    _irk_config = None
    _carriage_config = None
    _led_mapping_config = None

    def __init__(self, config_folder):
        ConfigManager._config_folder = config_folder

    @staticmethod
    def get_config_folder():
        return ConfigManager._config_folder

    @staticmethod
    def get_proglove_cfg():
        if ConfigManager._carriage_config:
            return ConfigManager._carriage_config
        else:
            ConfigManager._carriage_config = configparser.ConfigParser()
            ConfigManager._carriage_config.read(ConfigManager._config_folder + '/proglove.ini')
            return ConfigManager._carriage_config
