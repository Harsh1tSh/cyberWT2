import psycopg2
import pandas as pd

def fetch_data():
    try:
        connection = psycopg2.connect(
            dbname="maritime_voyage",
            user="postgres",
            password="HIslandH",
            host="localhost"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM voyages;"
        data = pd.read_sql_query(query, connection)
        return data

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    data = fetch_data()
    print(data.head())
