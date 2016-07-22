import os

base_dir = os.environ.get('BASE_DIR')

MMKIT_STORAGES_ROOT_DIR = os.path.normpath(os.path.join(base_dir, '../storages'))
