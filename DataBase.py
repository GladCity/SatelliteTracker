import psycopg2
import os
from satellite import Satellite
from typing import List


class DataBase(object):
    def __init__(self):
        self.__conn = psycopg2.connect(dbname='satellite', user=os.environ.get('DB_USER'),
                                       password=os.environ.get('DB_PASSWORD'), host='localhost')
        self.__cursor = self.__conn.cursor()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataBase, cls).__new__(cls)
        return cls.instance

    def get_satellite(self) -> List[Satellite]:
        self.__cursor.execute("SELECT * FROM satellite")
        out = []
        for row in self.__cursor:
            out.append(Satellite(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        return out

    def add_satellite(self, satellite: Satellite):
        self.__cursor.execute(
            f"""INSERT INTO satellite(name, start_pos, start_time, period, height, photo_bounds, detalis, photo_size)
        VALUES('{satellite.name}', '{satellite.start_pos}', '{satellite.start_time}', {satellite.period}, {satellite.height},
         '{str(satellite.photo_bounds).replace('[', '{').replace(']', '}')}', {satellite.detalis}, {satellite.photo_size});""")
        self.__conn.commit()


if __name__ == "__main__":
    db = DataBase()
    db.add_satellite(db.get_satellite()[0])
