import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the User CRUD operations
from crud_operations import Insert_Data_User, Read_All_Users, Update_User, Delete_User

# ✅ Test 1: Insert a new user
Insert_Data_User(
    name="John", 
    email="exemple@gmail.com",
    role="user",
    orders=2,
    pays="tunisie",
    mission="fhjff",
    matricule="34re001",
    phone=28999888,
    company="comp x",
    password="abc1",
    confirmPassword="abc1"
)

# ✅ Test 2: Read all suppliers
#Read_All_Users()

# ✅ Test 3: Update a supplier with id 1
# Update_User(
#     user_id=1,
#     name="John", 
#     email="exemple@gmail.com",
#     role="user",
#     orders=2,
#     pays="Tunisie",
#     mission="fhjff",
#     matricule="34re001",
#     phone=33888777,
#     company="comp y",
#     password="abc2",
#     confirmPassword="abc2"
# )

# ✅ Test 4: Delete a supplier with id 1
# Delete_Supplier(supplier_id=1)
