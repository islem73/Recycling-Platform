import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Stock cruds from crud_operations
from crud_operations import Insert_Data_Stock, Read_All_Stocks, Update_Stock, Delete_Stock


# ✅ Test 1: Insert a new stock
Insert_Data_Stock(
    reference="Ref1",
    quantity=23,
    status="Payé",
    supplier=1,
    total=23.00,
    creationDate="2/3/2025",
)

# ✅ Test 2: Read all stocks
#Read_All_Products()

# ✅ Test 3: Update an stock with ID 1
# Update_Stock(
#     stock_id = 1, 
#     reference="Ref2", 
#     quantity=55, 
#     status="Non Payé", 
#     supplier=1, 
#     total=44.00, 
#     creationDate="1/3/2025", 
#     active=True
# )

# ✅ Test 4: Delete an stock with ID 1
#Delete_Product(product_id=1)