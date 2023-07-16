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
import faiss
from datetime import datetime, timedelta
import random
from flask import Flask
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
   

# Set up Flask and Cache
app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('CACHE_REDIS_URL')
})
 
## Tool to clear cache
# http://127.0.0.1:5000/clear_cache   
@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    print("Clearing cache")
    cache.clear()
    return "Cache has been cleared"

# Set a very long timeout (e.g., 30 days)
VERY_LONG_TIMEOUT = 30 * 24 * 60 * 60  # 30 days in seconds

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

        # Check if session is cached
        session = self.cache.get(f'{username}_session')
        if session:
            self.client.set_settings(session)
            print("Session loaded from cache")
        else:
            self.login(username, password)

        if proxy:
            print("Setting up proxy...")
            self.client.set_proxy(proxy)
            print("Proxy set up")

        print("Getting user ID...")
        # Check if user_id is cached
        user_id = self.cache.get(f'{username}_user_id')
        if user_id:
            self.user_id = user_id
            print("User ID loaded from cache")
        else:
            self.user_id = self.get_user_id(username)
            print("User found")
            # Cache user_id with timeout
            self.cache.set(f'{username}_user_id', self.user_id, timeout=VERY_LONG_TIMEOUT)
            print(f"Cached {username}_user_id with timeout {VERY_LONG_TIMEOUT} seconds")
            # Check if user_id is cached
            user_id = self.cache.get(f'{username}_user_id')
            if user_id:
                self.user_id = user_id
                print("User_id is cached")
            else:
                print("User_id is not cached")

        # Initialize last_message_id and thread_id as None
        self.last_message_id = None
        self.thread_id = None
        # Initialize follow count
        self.follow_count = 0
        self.follow_reset_time = datetime.now() + timedelta(days=1)



    def login(self, username, password):
        try:
            print("Logging in to Instagram...")
            self.client.login(username, password)
            print('Logged in')
            # Cache session with timeout
            self.cache.set(f'{username}_session', self.client.settings, timeout=VERY_LONG_TIMEOUT)
            print(f"Cached {username}_session with timeout {VERY_LONG_TIMEOUT} seconds")
            # Check if session is cached
            session = self.cache.get(f'{username}_session')
            if session:
                self.client.set_settings(session)
                print("Session is cached")
            else:
                print("Session is not cached")
        except LoginRequired:
            print("Session expired. Logging in again...")
            self.client.login(username, password)
            print('Logged in')
            # Cache session with timeout
            self.cache.set(f'{username}_session', self.client.settings, timeout=VERY_LONG_TIMEOUT)
            print(f"Cached {username}_session with timeout {VERY_LONG_TIMEOUT} seconds")
            # Check if session is cached
            session = self.cache.get(f'{username}_session')
            if session:
                self.client.set_settings(session)
                print("Session is cached")
            else:
                print("Session is not cached")
        except Exception as e:
            print(f"Failed to login: {e}")
            raise e

    def get_user_id(self, username):
        try:
            return self.client.user_id_from_username(username)
        except Exception as e:
            print(f"Failed to get user ID for {username}: {e}")
            return None

    def send_message(self, message):
        print("Preparing to send message...")
        print(f"Message: {message}")  # Log the message

        # Check if the message is the same as the last sent message
        if message == self.last_sent_message:
            print("Message is the same as the last sent message. Skipping sending.")
            return "Message is the same as the last sent message. Skipping sending."

        try:
            result = self.client.direct_send(message, user_ids=[self.user_id])
            thread_id = result.thread_id
            thread = self.client.direct_thread(thread_id)
            # Store last_message_id, thread_id, and last_sent_message as instance variables
            self.last_message_id = thread.messages[0].id
            self.thread_id = result.thread_id
            self.last_sent_message = message
            print("Message sent successfully")
            return  "Message sent successfully"
        
        except ClientError as e:
            print('Message failed')
            print(e)


    def receive_message(self, tool_input=None):
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
            new_messages = [m for m in thread.messages if m.id > self.last_message_id and m.item_type != 'placeholder']
            if new_messages:
                print("New messages found:")
                for message in new_messages:
                    print(f"Received message: {message.text}")
                self.last_message_id = thread.messages[0].id
                return new_messages
            else:
                print("No new messages found. Waiting again...")
                self.client.delay_range = [57, 60]

        print("No reply received after 3 attempts.")
        return "No reply received yet. Suggest checking again in one hour."

    

    # def make_post():
    #         # Create this function
    #        # Ask chatGPT to create this function using this: https://github.com/adw0rd/instagrapi
                # it should handle delays, errors and add prints
       
       
    
    def follow_users(self, topic):
        # Check if the follow limit has been reached
        if self.follow_count >= self.MAX_FOLLOW_PER_DAY:
            print("Follow limit is reached for today. Can't proceed. Try again tomorrow.")
            return

        # Check if the follow count should be reset
        if datetime.now() >= self.follow_reset_time:
            print("Resetting follow count for the new day.")
            self.follow_count = 0
            self.follow_reset_time = datetime.now() + timedelta(days=1)

        print("Searching for users related to the topic...")
        try:
            users = self.client.search_users(topic, count=50)  # Search for 50 users related to the topic
            print(f"Found {len(users)} users related to {topic}")
        except ClientError as e:
            print(f"Failed to search users: {e}")
            return

        for user in users:
            # Check if the follow limit has been reached
            if self.follow_count >= self.MAX_FOLLOW_PER_DAY:
                print("Follow limit is reached for today. Can't proceed. Try again tomorrow.")
                return

            try:
                print(f"Following user {user.username}...")
                self.client.user_follow(user.pk)  # Follow the user
                self.follow_count += 1  # Increment the follow count
                print(f"Followed user {user.username}")
                time.sleep(random.uniform(2, 4))  # Random delay to mimic human behavior and avoid rate limits
            except ClientError as e:
                print(f"Failed to follow user {user.username}: {e}")

        print("Finished following users.")


# # Function to train a model on Replicate and generate images
# class ReplicateTool:

#     def __init__():
        
#     def train_model():
# You can ask Chat GPT to create this from /letthemlive/DreamBooth_train_model.py

#     def generate_image():
# You can ask Chat GPT to create this from /letthemlive/DreamBooth_generate_image.py
  
    
    
def run_autogpt(goal, username, password, target_username, cache):
    print("Setting up tools for AutoGPT")

    # Set up tools for AutoGPT
    search = SerpAPIWrapper()

    print("Setting up Instagram for AutoGPT")
    # Create an instance of InstagramTool
    instagram_tool = InstagramTool(username, password, target_username, cache=cache)


    print("Retrieving Instagram profile information...")
    # Check if profile_info is cached
    profile_info = cache.get(f'{username}_profile_info')
    if profile_info:
        print("Profile information loaded from cache")
    else:
        try:
            profile_info = instagram_tool.client.user_info(instagram_tool.user_id)
            print("Profile information retrieved successfully")
            # Cache profile_info with timeout
            cache.set(f'{username}_profile_info', profile_info, timeout=VERY_LONG_TIMEOUT)
            print(f"Cached {username}_profile_info with timeout {VERY_LONG_TIMEOUT} seconds")
            # Check if user_id is cached
            profile_info = cache.get(f'{username}_profile_info')
            if profile_info:
                print("profile_info is cached")
            else:
                print("profile_info is not cached")

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
                description="Tool for sending messages to a user on Instagram. Requires a message as input. Make sure tool_input is not empty, it must contain your message to the user."
            ),
            Tool(
                name="instagram_receive",
                func=instagram_tool.receive_message,
                description="Tool for receiving messages from a user on Instagram."
            ),
        

            # Tool(
            #     name="instagram_follow",
            #     func=instagram_tool.follow_users,
            #     description="Tool for following users on Instagram related to a specific topic."
            # ),

            # Tool(
            #     name="instagram_make_post",
            #     func=instagram_tool.make_post
            #     description="Tool for making a post on Instagram"
            # ),


            # Tool(
            #     name="replicate_train",
            #     func=replicate_tool.train_model,
            #     description="Tool for training a model on Replicate from a dataset."
            # ),
            # Tool(
            #     name="replicate_generate",
            #     func=replicate_tool.generate_image,
            #     description="Tool for generating images from a model on Replicate"
            # ),
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






