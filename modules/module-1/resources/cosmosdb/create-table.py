import json
import os
from optparse import Values
import time
from urllib.parse import urljoin
import uuid
from azure.cosmos import CosmosClient, PartitionKey

# ✅ FIX: Read from environment variables instead of terraform.tfstate
host       = os.environ["COSMOS_ENDPOINT"]
primarykey = os.environ["COSMOS_PRIMARYKEY"]

print("Cosmos Endpoint:", host)
print("Connecting to CosmosDB...")

# Initialize the Cosmos client
url = str(host)
primarykey = str(primarykey)

client = CosmosClient(url, primarykey)

# Create a database
database_name = 'ine-cosmos-sql-db'
database = client.create_database_if_not_exists(id=database_name)

# Create blog-users container
container_name = 'blog-users'
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id")
)

db_file_json_1 = open('./modules/module-1/resources/cosmosdb/blog-users.json')
db_file_1 = json.loads(db_file_json_1.read())
for db_item_1 in db_file_1:
    container.upsert_item(body=db_item_1)

# Create blog-posts container
container_name = 'blog-posts'
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id")
)

db_file_json_2 = open('./modules/module-1/resources/cosmosdb/blog-posts.json')
db_file_2 = json.loads(db_file_json_2.read())
for db_item_2 in db_file_2:
    container.upsert_item(body=db_item_2)

print("Items Updated")