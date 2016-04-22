import contextlib
import datetime
import pymysql
import dbconfig


class DBHelper:

    @staticmethod
    def connect(database='crimemap'):
        return pymysql.connect(host='localhost',
                               user=dbconfig.db_user,
                               passwd=dbconfig.db_password,
                               db=database)

    def get_all_crimes(self):
        connection = self.connect()
        try:
            query = "SELECT category, date, latitude, longitude,\
                    description FROM crimes;"
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(query)
            named_crimes = []
            for crime in cursor:
                named_crime = {
                    'category': crime[0],
                    'date': datetime.datetime.strftime(
                        crime[1], '%Y-%m-%d'),
                    'latitude': crime[2],
                    'longitude': crime[3],
                    'description': crime[4]
                }
                named_crimes.append(named_crime)

            return named_crimes
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (\
            category, date, latitude, longitude, description)\
            VALUES (%s, %s, %s, %s, %s)"
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(query, (
                    category, date, latitude, longitude, description))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
