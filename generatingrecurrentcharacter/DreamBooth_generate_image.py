import replicate
import os
from dotenv import load_dotenv

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
VERSION_ID = "3e0a1a4286c8cbe6eeaf0bd5a91a2427b0b208f1cd3ddbaa5f73b927424802c2"

# Run your trained model
print("Running model...")
run_input = {"prompt": "selfy of Nathalie in her bathroom"}
model_version = f"{MODEL_NAME}:{VERSION_ID}"
result = replicate.run(model_version, input=run_input)
print(result)
