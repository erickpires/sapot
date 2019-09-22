from appdirs import user_config_dir
from configparser import ConfigParser
from getpass import getpass
from pkg_resources import get_distribution
import os

def get_module_version(module):
    return module + ' ' + get_distribution(module).version

def get_env_vars(env_vars):
    values = []
    for var in env_vars:
        values.append(os.environ[var] if var in os.environ else None)
    return values

def get_default_config_file(dirname, filename):
    boto_config_dir = user_config_dir(dirname)
    if not os.path.exists(boto_config_dir):
        os.makedirs(boto_config_dir)
    return os.path.join(boto_config_dir, filename)

def read_config_file(config_file, default='LOGIN'):
    config = ConfigParser(default_section=default)
    config.read(config_file)
    return config

def write_config_file(config, config_file):
    with open(config_file, 'w') as f:
        config.write(f)

def input_login_info(config, config_file, operation='atualizado'):
    user_id = config['LOGIN']['MINERVA_ID']
    config['LOGIN']['MINERVA_ID'] = str(
        input('ID/CPF%s: ' % (' [%s]' % user_id if user_id else '')) or user_id)
    config['LOGIN']['MINERVA_PASS'] = getpass('Senha: ')

    write_config_file(config, config_file)
    print('Arquivo %s. Continuando...\n' % operation)

    return config['LOGIN']['MINERVA_ID'], config['LOGIN']['MINERVA_PASS']

def get_info_from_config(config):
    login = config['LOGIN']
    for required_key in ['MINERVA_ID', 'MINERVA_PASS']:
        if not required_key in login: login[required_key] = ''
    return [login['MINERVA_ID'], login['MINERVA_PASS']]

def config_first_run(config, config_file):
    ans = input('Não encontramos o arquivo de configurações. Deseja ' +
                'inserir os dados para login aqui? [s/N] ')

    if not ans.lower().strip() in ['s', 'sim']:
        print('Tudo bem. Por favor, insira seu ID e senha em: \n\t[%s]' %
              config_file)
        write_config_file(config, config_file)
        return False

    get_info_from_config(config)
    input_login_info(config, config_file, 'salvo')
    return True
