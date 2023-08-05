"""
heliopy configuration utility
"""
import configparser
import os
import pymms
from pathlib import Path


def get_config_file():
    """
    Find the configuration file. Locations are{}

    1. ~/.pymmsrc/pymmsrc
    2. <installation folder>/config.ini
    3. <installation folder>/template_config.ini

    Returns
    -------
    config_file : str
        Filepath of the ``pymms`` configuration file
    """
    # Get user configuration location
    config_files = [Path('~/.pymmsrc/pymmsrc').expanduser(),
                    Path(pymms.__file__).parent / 'config.ini',
                    Path(pymms.__file__).parent / 'config_template.ini']
    
    for f in config_files:
        if f.is_file():
            return str(f)


def load_config():
    """
    Read the configuration file. Locations are:

    1. <installation folder>/template_config.ini
    2. <installation folder>/config.ini

    Returns
    -------
    config : dict
        Dictionary containing configuration options.
    """    
    config_location = get_config_file()
    config = configparser.ConfigParser()
    config.read(config_location)
    config_dict = {}
    
    # Set data download directory
    for dirname in ('data_root', 'dropbox_root', 'mirror_root'):
        root = os.path.expanduser(config['DIRS'][dirname])
        if root == 'None':
            config_dict[dirname] = None
            continue
        
        # Make any default directories system-independent
        if os.name == 'nt':
            root = root.replace('/', '\\')
        config_dict[dirname] = root
        
        # Create data download if not created
        if not os.path.isdir(root):
            print('Creating root data directory {}'.format(root))
            os.makedirs(root)

    # login credentials
    for cred in ('username', 'password'):
        config_dict[cred] = config['SDCLOGIN'][cred]
        if config_dict[cred] == 'None':
            config_dict[cred] = None

    config_dict['gls_root'] = config['GLS']['gls_root']
    if config_dict['gls_root'] == 'None':
        config_dict['gls_root'] = None

    return config_dict
