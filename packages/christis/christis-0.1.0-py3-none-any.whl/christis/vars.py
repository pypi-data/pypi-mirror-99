import os

def get_christis_config_location():
    home = os.getenv("HOME")
    return "{0}{1}".format(home,"/.christisCLI/")

def get_mongo_configuration_location():
    return "{0}{1}".format(get_christis_config_location(),"mongo.yaml")

def get_christis_api_config_location():
    return "{0}{1}".format(get_christis_config_location(),"ldap.yaml")

def get_christis_cli_config_location():
    return "{0}{1}".format(get_christis_config_location(),"cli.yaml")