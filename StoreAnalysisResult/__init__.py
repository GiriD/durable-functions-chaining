import os, json
from azure.cosmos import CosmosClient
from azure.cosmos.partition_key import PartitionKey

def main(imageAnalysisResult: str) -> str:

    image_analysis_result = json.loads(imageAnalysisResult)

    COSMOS_URI = os.environ['COSMOS_URI']
    COSMOS_KEY = os.environ['COSMOS_KEY']
    DATABASE_ID = os.environ['DATABASE_ID']
    CONTAINER_ID = os.environ['CONTAINER_ID']

    client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)

    # setup database for this sample
    db = client.create_database_if_not_exists(id=DATABASE_ID)

    # setup container for this sample
    container = db.create_container_if_not_exists(id=CONTAINER_ID, partition_key=PartitionKey(path='/image_name'))
    response = container.upsert_item(body=image_analysis_result)
    return response['id']
    