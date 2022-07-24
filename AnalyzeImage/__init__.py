import os, requests, json, hashlib
from azure.storage.blob import ContainerClient

def main(imageName: str) -> str:
    storage_connection_string = os.environ["AzureWebJobsStorage"]
    container = ContainerClient.from_connection_string(conn_str=storage_connection_string, container_name="images")
    blob_client = container.get_blob_client(imageName)
    
    headers = {'Ocp-Apim-Subscription-Key': os.environ["COMPUTER_VISION_API_KEY"], 'Content-Type': 'application/octet-stream'}
    response = requests.post('https://'+os.environ["COMPUTER_VISION_RESOURCE_NAME"]+'.cognitiveservices.azure.com/vision/v3.2/analyze?visualFeatures=Categories,Tags,Adult,Brands,Color,Description,Faces,ImageType,Objects&language=en&model-version=latest', headers=headers, data=blob_client.download_blob().readall())
    analysis_result = json.loads(response.text)
    analysis_result['image_name'] = imageName
    analysis_result['id'] = hashlib.md5((imageName).encode()).hexdigest()
    
    return json.dumps(analysis_result)