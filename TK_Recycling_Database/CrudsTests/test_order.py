import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Order cruds from crud_operations
from crud_operations import Insert_Data_Order, Read_All_Orders, Update_Order, Delete_Order

# ✅ Test 1: Insert a new order
Insert_Data_Order(
    client_id=2, 
    product="Product1", 
    quantity=10, 
    total="100.00", 
    status="active", 
    createdAtFormatted="2025-02-02"
)

# ✅ Test 2: Read all orders
#Read_All_Orders()

# ✅ Test 3: Update an order with ID 1
# Update_Order(
#     order_id=2, 
#     product="Updated Product", 
#     quantity=20, 
#     total="200.00", 
#     status="completed"
# )

# ✅ Test 4: Delete an order with ID 2
# Delete_Order(order_id=2)
