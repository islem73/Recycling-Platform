####### ❌ THIS FILE IS NOT TESTED YET ####### 

# 💡💡💡
# This file demonstrates an approach in Python using a factory-like pattern 
# to handle CRUD operations for different tables. 
# The key idea is to create reusable functions that perform generic CRUD operations, 
# reducing repetitive code and making the process more efficient.
# These functions dynamically handle database queries by accepting parameters such as table names, 
# column names, and values, allowing for flexible and reusable code to interact with any table.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from mysql.connector import Error
from connexion_DB import create_connection

# INSERTING RECORD
def Insert_Record(table, **kwargs):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            columns = ', '.join(kwargs.keys())
            values = ', '.join(['%s'] * len(kwargs))
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(kwargs.values()))
            connection.commit()
            print(f"{table.capitalize()} created successfully!")
        except Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# READ ALL RECORDS
def Read_All_Records(table):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# UPDATE RECORD
def Update_Record(table, record_id, **kwargs):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            updates = [f"{col} = %s" for col in kwargs.keys()]
            query = f"UPDATE {table} SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, tuple(kwargs.values()) + (record_id,))
            connection.commit()
            print(f"{table.capitalize()} updated successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# DELETE RECORD
def Delete_Record(table, record_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"DELETE FROM {table} WHERE id = %s"
            cursor.execute(query, (record_id,))
            connection.commit()
            print(f"{table.capitalize()} deleted successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


