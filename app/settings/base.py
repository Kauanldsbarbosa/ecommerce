import os

class BaseConfig:
    def __init__(self):
        self.PROJECT_NAME = os.getenv('PROJECT_NAME', 'My Project')