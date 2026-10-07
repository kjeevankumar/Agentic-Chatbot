from configparser import ConfigParser
from pathlib import Path


class Config:
    def __init__(self, config_file=None):
        self.config = ConfigParser()
        if config_file is None:
            config_file = Path(__file__).with_name('uniconfigfile.ini')
        self.config.read(config_file)

    def get_page_title(self):
        return self.config.get('DEFAULT', 'PAGE_TITLE')

    def get_llm_options(self):
        return [option.strip() for option in self.config.get('DEFAULT', 'LLM_OPTIONS').split(',')]

    def get_usecase_options(self):
        return [option.strip() for option in self.config.get('DEFAULT', 'USECASE_OPTIONS').split(',')]

    def get_groq_model_options(self):
        return [option.strip() for option in self.config.get('DEFAULT', 'Groq_model_options').split(',')]


config = Config()