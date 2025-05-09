import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the supplier CRUD operations
from crud_operations import Insert_Data_Supplier, Read_All_Suppliers, Update_Supplier, Delete_Supplier

# ✅ Test 1: Insert a new supplier
Insert_Data_Supplier(
    firstname="John", 
    lastname="Doe", 
    matricule="12345", 
    phone=987654321, 
    active=True
)

# ✅ Test 2: Read all suppliers
#Read_All_Suppliers()

# ✅ Test 3: Update a supplier with id 1
# Update_Supplier(
#     supplier_id=1, 
#     firstname="Jane", 
#     lastname="Doe", 
#     matricule="67890", 
#     phone=23456789, 
#     active=True
# )

# ✅ Test 4: Delete a supplier with id 1
# Delete_Supplier(supplier_id=1)
