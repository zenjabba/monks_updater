from decouple import config

############################################################
# INI SETTINGS
############################################################
# core
DEBUG = config('DEBUG', False, cast=bool)
USER_PATH = config('USER_PATH', "/home/$USER$", cast=str)
