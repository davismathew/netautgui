from ..models import Inventory
import os
import ConfigParser

def project_path(type):
    config = ConfigParser.ConfigParser()
    config.read('netaut.conf')
    if type == 'project':
        path = config.get('paths', 'project_path')
    elif type == 'play':
        path = config.get('paths', 'project_path')
    return os.listdir(path)