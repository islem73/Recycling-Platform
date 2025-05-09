import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Product cruds from crud_operations
from crud_operations import Insert_Data_Product, Read_All_Products, Update_Product, Delete_Product


# ✅ Test 1: Insert a new product
Insert_Data_Product(
    name="Product1", 
    reference="abc",
    category="cat1",
    description="product 1",
    prix=220.00,
    resistanceChaleur=1,
    resistanceChimique=1,
    resistanceChock=1,
    faciliteFaconnage=1,
    minStock=23,
    stock=123,
    stockAlert="Bas",
    image="sdksjn",
)

# ✅ Test 2: Read all products
#Read_All_Products()

# ✅ Test 3: Update an product with ID 1
# Update_Product(
#     product_id=1,
#     name="Product1", 
#     reference="dfgfd",
#     category="cat2",
#     description="product 2",
#     prix=234.00,
#     resistanceChaleur=2,
#     resistanceChimique=2,
#     resistanceChock=2,
#     faciliteFaconnage=2,
#     minStock=40,
#     stock=455,
#     stockAlert="Haut",
#     image="image 1",
# )

# ✅ Test 4: Delete an product with ID 1
#Delete_Product(product_id=1)