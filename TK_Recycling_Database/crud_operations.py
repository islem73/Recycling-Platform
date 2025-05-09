import mysql
import mysql.connector
from mysql.connector import Error
from .connexion_DB import create_connection



##################  1️⃣ CREATING DB & TABLES   ##################
def create_database_and_tables():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Create the database if it does not exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS recycle")
            print("Database created or already exists")

            # Switch to the database
            cursor.execute("USE recycle")

            # Create the tables
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
                    confirmPassword VARCHAR(255) NOT NULL,
                    CHECK (confirmPassword = password)
                )
            """)
            print("Table 'client' created or already exists!")

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



##################  2️⃣ CRUD METHODS FOR CLIENTS TABLE  ##################

# ADD NEW CLIENT
def Insert_Data_Client(name, email, role, pays, mission, matricule, phone, company, password, confirmPasword):
    connection = create_connection()
    if connection:
        try :
            cursor = connection.cursor()
            query = """
            INSERT INTO client (
                name, email, role, pays, mission, matricule, phone, company, password, confirmPasword
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (name, email, role, pays, mission, matricule, phone, company, password, confirmPasword)
            cursor.execute(query, values)
            connection.commit()
            print("Client created successfully!")
        except Error as err:
            print(f"Error: {err}")
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySql Connection is closed!")
               
# GET ALL CLIENTS
def Read_All_Clients():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Important: dictionary cursor
            cursor.execute("USE recycle")  # Ensure using the right database
            query = "SELECT * FROM client"
            cursor.execute(query)
            clients = cursor.fetchall()
            return clients
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return []

# UPDATE CLIENT
def Update_Client(
    client_id, name=None, email=None, role=None, pays=None, mission=None, matricule=None, 
    phone=None, company=None, password=None, confirmPassword=None):
        connection = create_connection()
        if connection:
            try :
                cursor = connection.cursor()
                query = "UPDATE client SET "
                updates = []
                values = []

                if name:
                    updates.append("name = %s")
                    values.append(name)
                if email:
                    updates.append("email = %s")
                    values.append(email)
                if role:
                    updates.append("role = %s")
                    values.append(role)
                if pays:
                    updates.append("pays = %s")
                    values.append(pays)
                if mission:
                    updates.append("mission = %s")
                    values.append(mission)
                if matricule:
                    updates.append("matricule = %s")
                    values.append(matricule)
                if phone:
                    updates.append("phone = %s")
                    values.append(phone)
                if company:
                    updates.append("company = %s")
                    values.append(company)
                if password:
                    updates.append("password = %s")
                    values.append(password)
                if confirmPassword:
                    updates.append("confirmPasword = %s")
                    values.append(confirmPassword)

                query += ", ".join(updates)
                query += " WHERE id = %s"
                values.append(client_id)

                cursor.execute(query, values)
                connection.commit()
                print("Client updated successfully!")

            except Error as e:
                print(f"Error: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed.")

# DELETE CLIENT
def Delete_Client(client_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM client WHERE id = %s"
            values = (client_id,)
            cursor.execute(query, values)
            connection.commit()
            print("Client deleted successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")



##################  3️⃣ CRUD METHODS FOR SUPPLIERS TABLE  ##################

# ADD NEW SUPPLIER
def Insert_Data_Supplier(firstname, lastname, matricule, phone, active=True):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO supplier (firstname, lastname, matricule, phone, active)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (firstname, lastname, matricule, phone, active)
            cursor.execute(query, values)
            connection.commit()
            print("Supplier created successfully!")
        except Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed!")

# GET ALL SUPPLIERS
def Read_All_Suppliers():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM supplier"
            cursor.execute(query)
            suppliers = cursor.fetchall()
            for supplier in suppliers:
                print(supplier)
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")

# UPDATE SUPPLIER
def Update_Supplier(supplier_id, firstname=None, lastname=None, matricule=None, phone=None, active=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE supplier SET "
            updates = []
            values = []

            # Check for each field and append it if provided
            if firstname:
                updates.append("firstname = %s")
                values.append(firstname)
            if lastname:
                updates.append("lastname = %s")
                values.append(lastname)
            if matricule:
                updates.append("matricule = %s")
                values.append(matricule)
            if phone:
                updates.append("phone = %s")
                values.append(phone)
            if active is not None:  # Check if active is passed
                updates.append("active = %s")
                values.append(active)

            # Build the final query
            query += ", ".join(updates)
            query += " WHERE id = %s"
            values.append(supplier_id)

            cursor.execute(query, values)
            connection.commit()
            print("Supplier updated successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")

# DELETE SUPPLIER
def Delete_Supplier(supplier_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM supplier WHERE id = %s"
            values = (supplier_id,)
            cursor.execute(query, values)
            connection.commit()
            print("Supplier deleted successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")



##################  4️⃣ CRUD METHODS FOR ORDERS TABLE  ##################

# ADD NEW ORDER
def Insert_Data_Order(client_id, product, quantity, total, status, createdAtFormatted):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO `order` (client_id, product, quantity, total, status, createdAtFormatted)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (client_id, product, quantity, total, status, createdAtFormatted)
            cursor.execute(query, values)
            connection.commit()
            print("Order created successfully!")
        except Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed!")


# GET ALL ORDERS
def Read_All_Orders():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM `order`"
            cursor.execute(query)
            orders = cursor.fetchall()
            for order in orders:
                print(order)
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")

# UPDATE ORDER
def Update_Order(order_id, client_id=None, product=None, quantity=None, total=None, status=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE `order` SET "
            updates = []
            values = []

            if client_id:
                updates.append("client_id = %s")
                values.append(client_id)
            if product:
                updates.append("product = %s")
                values.append(product)
            if quantity:
                updates.append("quantity = %s")
                values.append(quantity)
            if total:
                updates.append("total = %s")
                values.append(total)
            if status:
                updates.append("status = %s")
                values.append(status)

            query += ", ".join(updates)
            query += " WHERE id = %s"
            values.append(order_id)

            cursor.execute(query, values)
            connection.commit()
            print("Order updated successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")

# DELETE ORDER
def Delete_Order(order_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM `order` WHERE id = %s"
            values = (order_id,)
            cursor.execute(query, values)
            connection.commit()
            print("Order deleted successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")




##################  6️⃣ CRUD METHODS FOR USERS ( TEAM ) TABLE  ##################

#ADD NEW USER
def Insert_Data_User(name, email, role, mission, matricule, phone, company, password, confirmPassword, passwordChangedAt=None, passwordResetToken=None, passwordResetExpires=None, active=True):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO user (
                name, email, role, mission, matricule, phone, company, password, 
                confirmPassword, passwordChangedAt, passwordResetToken, passwordResetExpires, active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, email, role, mission, matricule, phone, company, password, 
                     confirmPassword, passwordChangedAt, passwordResetToken, passwordResetExpires, active)
            cursor.execute(query, values)
            connection.commit()
            print("User created successfully!")
        except Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed!")
 
#GET ALL USERS
def Read_All_Users():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor
            cursor.execute("USE recycle")  # Make sure to select the database
            query = "SELECT * FROM user"
            cursor.execute(query)
            users = cursor.fetchall()
            return users  # Return the list of users
        except Error as e:
            print(f"Error: {e}")
            return []  # Return empty list on error
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return []  # Return empty list if connection fails

#UPDATE USER
def Update_User(user_id, name=None, email=None, role=None, mission=None, matricule=None, phone=None, company=None, password=None, confirmPassword=None, passwordChangedAt=None, passwordResetToken=None, passwordResetExpires=None, active=None):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE user SET "
            updates = []
            values = []

            if name:
                updates.append("name = %s")
                values.append(name)
            if email:
                updates.append("email = %s")
                values.append(email)
            if role:
                updates.append("role = %s")
                values.append(role)
            if mission:
                updates.append("mission = %s")
                values.append(mission)
            if matricule:
                updates.append("matricule = %s")
                values.append(matricule)
            if phone:
                updates.append("phone = %s")
                values.append(phone)
            if company:
                updates.append("company = %s")
                values.append(company)
            if password:
                updates.append("password = %s")
                values.append(password)
            if confirmPassword:
                updates.append("confirmPassword = %s")
                values.append(confirmPassword)
            if passwordChangedAt:
                updates.append("passwordChangedAt = %s")
                values.append(passwordChangedAt)
            if passwordResetToken:
                updates.append("passwordResetToken = %s")
                values.append(passwordResetToken)
            if passwordResetExpires:
                updates.append("passwordResetExpires = %s")
                values.append(passwordResetExpires)
            if active is not None:
                updates.append("active = %s")
                values.append(active)

            query += ", ".join(updates)
            query += " WHERE id = %s"
            values.append(user_id)

            cursor.execute(query, values)
            connection.commit()
            print("User updated successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")

#DELETE USER
def Delete_User(user_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM user WHERE id = %s"
            values = (user_id,)
            cursor.execute(query, values)
            connection.commit()
            print("User deleted successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed.")


##################  7️⃣ COUNTING FUNCTIONS FOR STATISTICS  ##################

def count_employees():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM user")
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Error counting employees: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def count_clients():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM client")
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Error counting clients: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def count_suppliers():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM supplier")
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Error counting suppliers: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def count_products():
    return 4  

def count_orders():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM `order`")  # Note: backticks for reserved word
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Error counting orders: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def count_services():
    return 3            
           
           
           
           
           
           
                
create_database_and_tables()