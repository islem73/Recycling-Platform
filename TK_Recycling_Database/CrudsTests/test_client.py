import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the client cruds from crud_operations
from crud_operations import Insert_Data_Client, Read_All_Clients, Update_Client, Delete_Client



# ✅ Test 1: Insert a new client

Insert_Data_Client(
    name="John Doe", 
    email="johndoe@example.com", 
    role="Admin", 
    pays="USA", 
    mission="Recycling", 
    matricule="12345", 
    phone=1234567890, 
    company="Eco Corp", 
    password="password123", 
    confirmPasword="password123"
)

# ✅ Test 2: Read all clients
#Read_All_Clients()

# ✅ Test 3: Update a client with id 1
# Update_Client(
#     client_id=1, 
#     name="Jane Doe", 
#     email="janedoe@example.com", 
#     role="Manager", 
#     pays="Canada", 
#     mission="Waste Management", 
#     matricule="54321", 
#     phone=98765432, 
#     company="Green Corp", 
#     password="newpassword", 
#     confirmPassword="newpassword"
# )

# ✅ Test 4: Delete a client with id 2
#Delete_Client(client_id=2)
