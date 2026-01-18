import mysql.connector


def dbconfig():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="piokl",
            passwd="Neoiki_PIOKI@123",
            database="pio_db"
        )
        return db

    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e