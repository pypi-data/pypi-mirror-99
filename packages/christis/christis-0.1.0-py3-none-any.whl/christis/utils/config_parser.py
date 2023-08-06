import yaml
import os
import sys

def get_configuration(configPath):
    if os.path.exists(configPath):
        try:
            with open(configPath) as file:
                configuration = {}
                configuration = yaml.load(file, Loader=yaml.FullLoader)
        except IOError as e:
            Error = {"ErrorCode":"805","ErrorMsg":"I/O error({0}): {1}".format(e.errno, e.strerror)}
        except:
            Error = {"ErrorCode":"805","ErrorMsg":sys.exc_info()[1]}
            return Error
        else:       
            return configuration
    else:
        Error = {"ErrorCode":"804","ErrorMsg":"Config File not found"}
        return Error