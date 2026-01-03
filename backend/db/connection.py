import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="shazam_db",
        user="postgres",
        password="Bhargav",
        host="localhost",
        port="5432"
    )
