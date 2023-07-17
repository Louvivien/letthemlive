import os
import time
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import LoginRequired
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, root_validator
import faiss
from datetime import datetime, timedelta
import random
from flask import Flask, render_template
from flask_caching import Cache
import threading



# Load .env file
def load_env():
    print("Loading environment variables...")
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
# Load environment variables 
load_env()
username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')
target_username = os.getenv('TARGET_USERNAME')
if not os.getenv('CACHE_REDIS_URL'):
    print("Error: The CACHE_REDIS_URL environment variable is not set.")
    exit(1)   

# Set up Flask and Cache
app = Flask(__name__)
cache = Cache(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.getenv('CACHE_REDIS_URL')
    })

   



 
@app.route('/')
def welcome():
    return render_template('welcome.html', team='Let Them Live')

 
## Tool to clear cache
# http://127.0.0.1:5000/clear_cache   
@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    print("Clearing cache")
    cache.clear()
    return "Cache has been cleared"

# Set a very long timeout (e.g., 30 days)
VERY_LONG_TIMEOUT = 30 * 24 * 60 * 60  # 30 days in seconds



# Langchain input schemas
# https://python.langchain.com/docs/modules/agents/tools/how_to/tool_input_validation

class InstagramReceiveInputSchema(BaseModel):
    optional_arg: Optional[str] = Field(None)

    @root_validator(pre=True)
    def remove_unnecessary_args(cls, values: Dict[str, Any]) -> Dict:
        # Ignore the input and return None
        return None

class InstagramSendInputSchema(BaseModel):
    tool_input: str


# Function to message a user on Instagram
class InstagramTool:
    MAX_FOLLOW_PER_DAY = 150

    def __init__(self, username, password, target_username, proxy=None, cache=None):
        print("Initializing Instagram client...")
        self.client = Client()
        self.client.delay_range = [1, 3]
        self.cache = cache
        self.target_username = target_username
        
        # Initialize last_sent_message as None
        self.last_sent_message = None

        session_file = f"{username}_session.json"

        if os.path.exists(session_file):
            self.client.load_settings(session_file)
            print("Session loaded from file")
        try:
            print("Logging in to Instagram...")
            self.client.login(username, password)
            print('Logged in')
        except LoginRequired:
            print("Session expired. Logging in again...")
            self.client.login(username, password)
            print('Logged in')
        self.client.dump_settings(session_file)

        
        if proxy:
            print("Setting up proxy...")
            self.client.set_proxy(proxy)
            print("Proxy set up")


        print("Getting user ID...")
        user_id_key = f"user_id:{target_username}"
        user_id = cache.get(user_id_key)
        if user_id:
            self.user_id = user_id
            print("User ID retrieved from cache")
        else:
            self.user_id = self.client.user_id_from_username(target_username)
            cache.set(user_id_key, self.user_id, timeout=VERY_LONG_TIMEOUT)  
            print("User ID retrieved from Instagram and saved to cache")
        if user_id is None:
            print("Error: Unable to get the user ID from the cache.")
            exit(1)
        print("User found")

        # Initialize last_message_id and thread_id as None
        self.last_message_id = None
        self.thread_id = None
        # Initialize follow count
        self.follow_count = 0
        self.follow_reset_time = datetime.now() + timedelta(days=1)



    def get_user_id(self, username):
        try:
            return self.client.user_id_from_username(username)
        except Exception as e:
            print(f"Failed to get user ID for {username}: {e}")
            return None

    def send_message(self, tool_input: InstagramSendInputSchema):
        message = tool_input.tool_input
        print(f"Arguments: {tool_input}")

        # Check if the message is empty
        if not message:
            return "You did not write a message to send, in order to use this tool you need to write a message to the user, try again please"

        print(f"Message: {message}")  # Log the message

        # Check if the message is the same as the last sent message
        if message == self.last_sent_message:
            print("Message is the same as the last sent message. Skipping sending.")
            return "Message is the same as the last sent message. Skipping sending."


        try:
            result = self.client.direct_send(message, user_ids=[self.user_id])
            thread_id = result.thread_id
            thread = self.client.direct_thread(thread_id)
            # Store last_message_id, thread_id, last_sent_message, and last_sent_timestamp as instance variables
            self.last_message_id = thread.messages[0].id
            self.thread_id = result.thread_id
            self.last_sent_message = message
            self.last_sent_timestamp = thread.messages[0].timestamp
            print("Message sent successfully")
            return  "Message sent successfully"
        
        except ClientError as e:
            print('Message failed')
            print(e)



    def receive_message(self, tool_input: Optional[InstagramReceiveInputSchema] = None):
        print(f"Arguments: {tool_input}")
        print("Waiting for reply...")
        for i in range(3):  # try 3 times
            print(f"Attempt {i+1}...")
            self.client.delay_range = [27, 30]

            # Check if last_message_id and thread_id are None
            if self.last_message_id is None or self.thread_id is None:
                print("You did not send a message yet. Suggest sending a messsage to the user.")
                return  "You did not send a message yet. Suggest sending a messsage to the user."

            print("Fetching thread...")
            thread = self.client.direct_thread(self.thread_id)
            print("Thread fetched. Checking for new messages...")
            print("Thread : ", thread)
            new_messages = [m for m in thread.messages if m.timestamp > self.last_sent_timestamp and m.item_type != 'placeholder']
            if new_messages:
                print("New messages found:")
                for message in new_messages:
                    print(f"Received message: {message.text}")
                self.last_message_id = thread.messages[0].id
                self.last_sent_timestamp = thread.messages[0].timestamp
                return new_messages
            else:
                print("No new messages found. Waiting again...")
                self.client.delay_range = [57, 60]

        print("No reply received after 3 attempts.")
        return "No reply received yet. Suggest checking again in one hour."




    
def run_autogpt(goal, username, password, target_username, cache):
    print("Setting up tools for AutoGPT")
    
    if cache is None:
        print("Error: Unable to connect to the Redis server.")
        exit(1)
    
    # Set up tools for AutoGPT
    search = SerpAPIWrapper()

    print("Setting up Instagram for AutoGPT")
    # Create an instance of InstagramTool
    instagram_tool = InstagramTool(username, password, target_username, cache=cache)

    print("Retrieving Instagram profile information...")
    profile_info_key = f'profile_info:{username}'
    profile_info = cache.get(profile_info_key)
    if profile_info:
        print("Profile information retrieved from cache")
    else:
        try:
            profile_info = instagram_tool.client.user_info(instagram_tool.client.user_id)
            cache.set(profile_info_key, profile_info, timeout=VERY_LONG_TIMEOUT)  
            print("Profile information retrieved from Instagram and saved to cache")
        except Exception as e:
            print(f"Failed to retrieve profile information: {e}")
            return

    # Set the AI name and role based on the Instagram profile information
    ai_name = profile_info.full_name
    if profile_info.biography:
        ai_role = f"This is your bio: {profile_info.biography}. Act as if you were this person, never say that you are an AI."
    else:
        ai_role = "This is your bio: I am a passionate individual who loves to engage with people and share my thoughts. Act as if you were this person, never say that you are an AI."

    # Add the send_message and receive_message methods as separate tools
    tools = [
            Tool(
                name="search",
                func=search.run,
                description="useful for when you need to answer questions about current events. You should ask targeted questions"
            ),
            WriteFileTool(),
            ReadFileTool(),
            Tool(
                name="instagram_send",
                func=instagram_tool.send_message,
                args_schema=InstagramSendInputSchema,
                description="Tool for sending a message to a user on Instagram. You must write a message to use this tool, it will not work if you do not write a message"
            ),
            Tool(
                name="instagram_receive",
                func=instagram_tool.receive_message,
                args_schema=InstagramReceiveInputSchema,
                description="Tool for receiving messages from a user on Instagram."
            ),
        ]

    # Set up memory for AutoGPT
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

    # Set up model and AutoGPT
    agent = AutoGPT.from_llm_and_tools(
        ai_name=ai_name,
        ai_role=ai_role,
        tools=tools,
        llm=ChatOpenAI(temperature=0),
        memory=vectorstore.as_retriever()
       )
    agent.chain.verbose = True

    # Run AutoGPT with your goal 
    print("Running AutoGPT...")
    agent.run([goal])


if __name__ == "__main__":
    
    # Set your goal as a natural language string
    goal = "Engage in a conversation with an Instagram user"
    
    

    # Create a thread for AutoGPT
    autogpt_thread = threading.Thread(target=run_autogpt, args=(goal, username, password, target_username, cache))
    autogpt_thread.start()

    # Start server
    app.run(debug=False)