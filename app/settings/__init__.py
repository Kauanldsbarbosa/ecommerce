import os
from app.settings.local import LocalSettings
from app.settings.test import TestSettings
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('ENVIRONMENT', 'local')

environment_map = {
    'local': LocalSettings,
    'test': TestSettings,
}

def get_environment():
    environment = environment_map.get(env, LocalSettings)
    return environment()