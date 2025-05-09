####### ❌ THIS FILE IS NOT TESTED YET ####### 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the client cruds from crud_operations_factory
from crud_operations_factory import Insert_Record , Read_All_Records , Update_Record, Delete_Record


# Inserting data into client table
Insert_Record('client', name='John Doe', email='john.doe@example.com', role='admin', pays='USA', mission='Management', matricule='12345', phone=1234567890, company='TechCo', password='password', confirmPasword='password')

# Reading all clients
Read_All_Records('client')

# Updating a client
Update_Record('client', 1, name='Jane Doe', email='jane.doe@example.com', role='user')

# Deleting a client
Delete_Record('client', 1)
