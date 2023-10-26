import psycopg2
import os


class DataBase(object):
    def __init__(self):
        self.__conn = psycopg2.connect(dbname='satellite', user=os.environ.get('DB_USER'),
                                       password=os.environ.get('DB_PASSWORD'), host='localhost')
        self.__cursor = self.__conn.cursor()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataBase, cls).__new__(cls)
        return cls.instance




if __name__ == "__main__":
    db = DataBase()
