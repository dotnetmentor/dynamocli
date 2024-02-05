import configparser
from appdirs import user_config_dir
from os import mkdir
import os.path

CREDENTIALS_FILE_PATH = os.path.expanduser('~/.aws/credentials')


class Configuration:
  def __init__(self) -> None:
    self.application_config = configparser.ConfigParser()
    self.aws_config = configparser.ConfigParser()
    self.aws_config.read(CREDENTIALS_FILE_PATH)
    config_dir = user_config_dir('dynocli')
    config_name = '.config.ini'
    if not os.path.exists(config_dir):
      mkdir(config_dir)
    self.local_config_file_path = os.path.join(config_dir, config_name)
    if not os.path.isfile(self.local_config_file_path):
      self.application_config['Connection'] = {
      }
      self.set_authentication_type('local')
      self.set_port('8000') 
      self.set_verbose('False')
      self.set_profile('default')
      self.set_region(self.get_region())
      self.save_config()
    else:
      with open(self.local_config_file_path, 'r') as configuration_file:
        self.application_config.read_file(configuration_file)
  
  def has_option(self, option) -> bool:
    section = 'Connection'
    return self.application_config.has_option(section, option)

  def get_connection(self) -> dict:
    return self.application_config['Connection']

  def get_table_name(self) -> str:
    if self.has_option('tablename'):
      return self.get_connection()['tablename']
    return ''

  def get_authentication_type(self) -> str:
    return self.get_connection().get('authentication', fallback='')

  def get_region(self) -> str:
    if self.get_connection().get('region'):
      return self.get_connection()['region']
    if os.environ.get('AWS_DEFAULT_REGION'):
      return os.environ.get('AWS_DEFAULT_REGION')
    
    if self.aws_config.has_option(self.get_profile(), 'region'):
      return self.aws_config[self.get_profile()]['region']
    return 'eu-west-1'

  def get_profile(self) -> str:
    conn = self.get_connection()
    if conn.get('profile'):
      return conn['profile']
    return 'default'

  def get_port(self) -> str:
    return self.get_connection().get('port')

  def get_verbose(self) -> str:
    return self.get_connection().get('verbose')
  
  def set_table_name(self, table_name) -> None:
    self.get_connection()['tablename'] = table_name

  def set_authentication_type(self, authentication_type) -> None:
    self.get_connection()['authentication'] = authentication_type

  def set_value(self, key, value) -> None:
    if key == 'tablename':
      self.set_table_name(value)
    elif key == 'authentication':
      self.set_authentication_type(value)
    elif key == 'region':
      self.set_region(value)
    elif key == 'profile':
      self.set_profile(value)
    elif key == 'port':
      self.set_port(value)
    elif key == 'verbose':
      self.set_verbose(value)
    else:
      raise ValueError(f'No such key: {key}')
  def set_region(self, region) -> None:
    self.get_connection()['region'] = region

  def set_profile(self, profile) -> None:
    self.get_connection()['profile'] = profile

  def set_port(self, port) -> None:
    self.get_connection()['port'] = port

  def set_verbose(self, verbose) -> None:
    self.get_connection()['verbose'] = verbose
     
  def __print_aws_config(self):
    for section in self.aws_config.sections():
      print(f'[{section}]')
      for key in self.aws_config[section]:
        print(f'{key}: {self.aws_config[section][key]}')

  def print_config(self) -> None:
      """Prints the current configuration to the console"""
      conn = self.get_connection()
      for key in conn:
          print(f'{key}: {conn[key]}')
  
  def save_config(self) -> None:
    """Saves the current configuration to the configuration file"""
    with open(self.local_config_file_path, 'w') as configuration_file:
        self.application_config.write(configuration_file)
  
  def export(self) -> dict:
    """Exports the current configuration to a dictionary
    
    Returns:
        The current configuration"""
    o = {}
    for section in self.application_config.sections():
      for key in self.application_config[section]:
        o[key] = self.application_config[section][key]
    
    o['profile'] = self.get_profile()
    o['region'] = self.get_region()
    return o    

    
        