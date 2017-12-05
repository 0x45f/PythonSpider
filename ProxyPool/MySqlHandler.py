import configparser


class MySqlHandler:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        host = config['mysql']['host0']
        port = int(config['mysql']['port'])
        username = config['mysql']['username']
        password = config['mysql']['password']
        database = config['mysql']['database']
        charset = config['mysql']['charset']
