import logging
import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

load_dotenv()


class DB:
    # TODO: Use psycop3 with all its async features, security features, etc.
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            # Use environment variables for database connection parameters
            dbname = "leads_db"
            user = os.environ["DB_USER"]
            password = os.environ["DB_PASSWORD"]
            host = "localhost"
            port = "5432"

            # Establish the connection
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )

            # Create a cursor to execute SQL queries
            self.cursor = self.connection.cursor()

            logging.info("Connected to the database.")

        except Exception as e:
            logging.exception(f"Error: Unable to connect to the database - {e}")

    def insert_data(self, table: str, data):
        try:
            # Build the SQL query dynamically
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                sql.SQL(', ').join(map(sql.Placeholder, data.keys()))
            )

            # Execute the query
            self.cursor.execute(query, data)

            # Commit the changes
            self.connection.commit()

            logging.info("Data inserted successfully.")

        except Exception as e:
            logging.exception(f"Error: Unable to insert data - {e}")

    def query_data(self, table, columns="*", condition="1=1"):
        try:
            # Build the SQL query dynamically
            query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.Identifier(table),
                sql.SQL(condition)
            ) if columns != "*" else sql.SQL("SELECT * FROM {} WHERE {}").format(
                sql.Identifier(table),
                sql.SQL(condition)
            )

            # Execute the query
            self.cursor.execute(query)

            # Fetch all the results
            rows = self.cursor.fetchall()

            return rows

        except Exception as e:
            logging.exception(f"Error: Unable to query data - {e}")
            return None

    def update_data(self, table, data, condition="1=1"):
        try:
            # Build the SQL query dynamically
            query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
                sql.Identifier(table),
                sql.SQL(', ').join(
                    map(lambda x: sql.SQL("{} = {}").format(sql.Identifier(x), sql.Placeholder(x)), data.keys())
                ),
                sql.SQL(condition)
            )

            # Execute the query
            self.cursor.execute(query, data)

            # Commit the changes
            self.connection.commit()

            logging.info("Data updated successfully.")

        except Exception as e:
            logging.exception(f"Error: Unable to update data - {e}")

    def delete_data(self, table, condition="1=1"):
        try:
            # Build the SQL query dynamically
            query = sql.SQL("DELETE FROM {} WHERE {}").format(
                sql.Identifier(table),
                sql.SQL(condition)
            )

            # Execute the query
            self.cursor.execute(query)

            # Commit the changes
            self.connection.commit()

            logging.info("Data deleted successfully.")

        except Exception as e:
            logging.exception(f"Error: Unable to delete data - {e}")

    def close_connection(self):
        try:
            # Close the cursor and connection
            self.cursor.close()
            self.connection.close()

            logging.info("Connection closed.")

        except Exception as e:
            logging.exception(f"Error: Unable to close connection - {e}")


if __name__ == "__main__":
    db = DB()
    db.connect()
    db.insert_data("searches", {"source": "google", "searchterm": "new york economic development organization", "searchdate": datetime.now(), "results": "test"})
    result = db.query_data("searches", columns=["searchterm", "searchdate"])
    print(result)
    db.update_data("searches", {"source": "bing"}, condition="searchterm = 'new york economic development organization'")
    db.delete_data("searches", condition="id = 1")
    db.close_connection()