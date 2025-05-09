import mysql.connector

def create_connection():
    try:
        MyDb = mysql.connector.connect(
            host="localhost",      
            user="root",          
            password="",          
            database="recycle"     
        )
        if MyDb.is_connected():
            print("Connected to MySQL database successfully!")
            return MyDb
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

if __name__ == "__main__":
    create_connection()
