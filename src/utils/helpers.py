import os

from dotenv import load_dotenv


load_dotenv()


def get_env_data(key):
    return os.environ.get(key)


TEST_EMAIL = get_env_data('TEST_EMAIL')
TEST_PASS = get_env_data('TEST_PASS')
