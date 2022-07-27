import enum
import yaml


#Given string config_file pointing to the file, string service, and list of strings keys, 
#Returns a list of values for the given keys for the given service.

#Now with exceptions and better sanitizing!
#Rewritten with dict to be much better in every way bc dicts are magic!
def get_keys(config_file, service, keys):
    with open(config_file, 'r') as stream:
        cfg = yaml.safe_load(stream)
    cfg = cfg[service]
    ret = []
    for key in (keys):
        if key not in cfg.keys():
            raise Exception('Missing key: ' + key)
        ret.append(cfg[key])
    return ret