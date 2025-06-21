import pymysql
import json
import os


def connect_to_db():
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.json'))
    with open(config_file_path) as config_file:
        config = json.load(config_file)

    try:
        conn = pymysql.connect(host=config["host"], port=config["port"], user=config["user"], password=config["password"], database=config["db"])
        return conn
    except pymysql.MySQLError as err:
        print(err)
        return None
    except Exception as e:
        print(e)
        return None


