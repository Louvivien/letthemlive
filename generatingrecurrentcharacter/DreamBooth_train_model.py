import os
import requests
import json
from dotenv import load_dotenv
import replicate
import zipfile

# Load .env file
def load_env():
    print("Loading environment variables...")
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

# Set your API token
load_env()
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

# Set your model name
MODEL_NAME = "louvivien/nathalie"

# Set your version ID
VERSION_ID = "a8ba568da0313951a6b311b43b1ea3bf9f2ef7b9fd97ed94cebd7ffd2da66654"

# Set the headers for the API requests
headers = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json"
}

# Zip your data folder
print("Zipping data folder and uploading to Replicate...")
def zip_data_folder(folder_name):
    zipf = zipfile.ZipFile('Training_data.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

zip_data_folder('Training_data')

# Upload the data file
print("Uploading data file to Replicate...")
upload_url = "https://dreambooth-api-experimental.replicate.com/v1/upload/data.zip"
response = requests.post(upload_url, headers=headers)
upload_url = response.json()["upload_url"]
with open("Training_data.zip", 'rb') as data_file:
    requests.put(upload_url, headers={"Content-Type": "application/zip"}, data=data_file)
SERVING_URL = response.json()["serving_url"]

# Start a training job
train_url = "https://dreambooth-api-experimental.replicate.com/v1/trainings"
train_data = {
    "input": {
        "instance_prompt": "a photo of a cjw person",
        "class_prompt": "a photo of a person",
        "instance_data": SERVING_URL,
        "max_train_steps": 2000
    },
    "model": MODEL_NAME,
    "trainer_version": "cd3f925f7ab21afaef7d45224790eedbb837eeac40d22e8fefe015489ab644aa",
    "webhook_completed": "https://example.com/dreambooth-webhook"
}
response = requests.post(train_url, headers=headers, data=json.dumps(train_data))
print(response.json())

# Get the status of the training job
job_id = response.json()["id"]
status_url = f"https://dreambooth-api-experimental.replicate.com/v1/trainings/{job_id}"
response = requests.get(status_url, headers=headers)
print(response.json())


