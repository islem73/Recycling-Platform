import mysql.connector
from connexion_DB import create_connection

def create_database_and_tables():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            ##### ❌ CREATING DATABASE IF DOESNT EXIST
            cursor.execute("CREATE DATABASE IF NOT EXISTS recycle")
            print("Database created or already exists")

            ##### ❌ SWITCHING TO RECYCLE DATABASE
            cursor.execute("USE recycle")

            ##### ✅ CREATING CLIENT TABLE 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS client (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    pays VARCHAR(255) NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    mission VARCHAR(255) NOT NULL,
                    matricule VARCHAR(255) NOT NULL,
                    phone INT NOT NULL,
                    company VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    confirmPasword VARCHAR(255) NOT NULL,
                    CHECK (confirmPasword = password)
                )
            """)
            print("Table 'client' created or already exists!")

            
            ##### ✅ CREATING SUPPLIER TABLE 
            ##### ❎ MUST BE CREATED BEFORE STOCK TABLE 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS supplier (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    firstname VARCHAR(255) NOT NULL,
                    lastname VARCHAR(255) NOT NULL,
                    matricule VARCHAR(255) NOT NULL UNIQUE,
                    phone INT NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("Table 'supplier' created or already exists!")

            
            ##### ✅ CREATING ORDER TABLE 
            ##### ❎ THIS TABLE DEPENDS ON CLIENT TABLE 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `order` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    client_id INT NOT NULL,
                    product VARCHAR(255) NOT NULL,
                    quantity INT NOT NULL,
                    total VARCHAR(255) NOT NULL,
                    status ENUM('active', 'inactive', 'completed') DEFAULT 'active',
                    active BOOLEAN DEFAULT TRUE,
                    createdAtFormatted VARCHAR(255),
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES client(id)
                )
            """)
            print("Table 'order' created or already exists!")

            ##### ✅ CREATING PRODUCT TABLE 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    reference VARCHAR(255) NOT NULL UNIQUE,
                    category VARCHAR(255) NOT NULL,
                    description TEXT,
                    prix DECIMAL(10, 2) NOT NULL,
                    resistanceChaleur INT,
                    resistanceChimique INT,
                    resistanceChock INT,
                    faciliteFaconnage INT,
                    minStock INT NOT NULL,
                    stock INT NOT NULL,
                    stockAlert ENUM('Bas', 'Moyen', 'Haut'),
                    image VARCHAR(255),
                    active BOOLEAN DEFAULT TRUE,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("Table 'products' created or already exists!")

       
            ##### ✅ CREATING STOCK TABLE 
            ##### ❎ THIS TABLE DEPENDS ON SUPPLIER TABLE 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stocks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reference VARCHAR(255) NOT NULL UNIQUE,
                    quantity INT NOT NULL,
                    status ENUM('Payé', 'Non Payé') NOT NULL,
                    supplier INT NOT NULL,
                    total DECIMAL(10, 2) NOT NULL,
                    creationDate VARCHAR(255),
                    active BOOLEAN DEFAULT TRUE,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (supplier) REFERENCES supplier(id)
                )
            """)
            print("Table 'stocks' created or already exists!")

            ##### ✅ CREATING USERS ( TEAM ) TABLE 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `user` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                role VARCHAR(50) DEFAULT 'user',
                mission VARCHAR(255) NOT NULL,
                matricule VARCHAR(255) NOT NULL,
                phone INT NOT NULL,
                company VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                confirmPassword VARCHAR(255) NOT NULL,
                passwordChangedAt DATETIME,
                passwordResetToken VARCHAR(255),
                passwordResetExpires DATETIME,
                active BOOLEAN DEFAULT TRUE,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CHECK (confirmPassword = password)
            )
            """)
            
            print("Table 'user' created or already exists!")


        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed!")


##### ✅ CALLING THE FUNCTION TO CREATE THE DB AND TABLES
create_database_and_tables()
