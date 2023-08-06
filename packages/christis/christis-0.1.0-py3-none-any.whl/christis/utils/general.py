import os

def set_env(ldapConfig):
    for k,v in ldapConfig.items():
        os.environ[k] = v