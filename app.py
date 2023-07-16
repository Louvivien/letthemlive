import os
import time
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import ClientError, LoginRequired
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
import redis
from flask import Flask, render_template
import logging


# Configuring logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


# Load .env file
def load_env():
    logging.info("Loading environment variables...")
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    redis_url = os.getenv('CACHE_REDIS_URL')
    if redis_url:
        return redis_url
    else:
        logging.error("Redis URL is not specified in environment variables.")
        raise ValueError("Redis URL is not specified in environment variables.")


# Load environment variables
load_env()
username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')
target_username = os.getenv('TARGET_USERNAME')


# Set up Flask and Cache
app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': load_env()
})

@app.route('/')
def welcome():
    return render_template('welcome.html', team='Let Them Live')


# Tool to clear cache
@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    logging.info("Clearing cache")
    cache.clear()
    return "Cache has been cleared"






# Set a very long timeout (e.g., 30 days)
#VERY_LONG_TIMEOUT = 30 * 24 * 60 * 60  # 30 days in seconds
#Cambiando el set pues ahora en Redis 7 se usa expire
VERY_LONG_TIMEOUT = 30 * 24 * 60 * 60  # 30 days in seconds
VERY_LONG_TIMEOUT_MS = VERY_LONG_TIMEOUT * 1000  # 30 days in milliseconds



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
            # Cache session in Redis with timeout
            self.cache.set(f'{username}_session', self.client.settings)
            self.cache.expire(f'{username}_session', VERY_LONG_TIMEOUT_MS)
            print(f"Cached {username}_session in Redis with timeout {VERY_LONG_TIMEOUT} seconds")
            # Check if session is cached in Redis
            session = self.cache.get(f'{username}_session')
            if session:
                self.client.set_settings(session)
                print("Session is cached in Redis")
            else:
                print("Session is not cached in Redis")
        except LoginRequired:
            print("Session expired. Logging in again...")
            self.client.login(username, password)
            print('Logged in')
            # Cache session in Redis with timeout
            self.cache.set(f'{username}_session', self.client.settings, timeout=VERY_LONG_TIMEOUT)
            print(f"Cached {username}_session in Redis with timeout {VERY_LONG_TIMEOUT} seconds")
            # Check if session is cached in Redis
            session = self.cache.get(f'{username}_session')
            if session:
                self.client.set_settings(session)
                print("Session is cached in Redis")
            else:
                print("Session is not cached in Redis")
        except Exception as e:
            print(f"Failed to login: {e}")
            raise e

    def get_user_id(self, username):
        try:
            user_id = self.cache.get(f'{username}_user_id')
            if user_id:
                print("User ID loaded from cache in Redis")
                return user_id
            else:
                user_id = self.client.user_id_from_username(username)
                print("User found")
                # Cache user_id in Redis with timeout
                self.cache.set(f'{username}_user_id', user_id)
                self.cache.expire(f'{username}_user_id', VERY_LONG_TIMEOUT_MS)
                print(f"Cached {username}_user_id in Redis with timeout {VERY_LONG_TIMEOUT} seconds")
                # Check if user_id is cached in Redis
                user_id = self.cache.get(f'{username}_user_id')
                if user_id:
                    print("User_id is cached in Redis")
                else:
                    print("User_id is not cached in Redis")
                return user_id
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
            return "Message sent successfully"

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
                return "You did not send a message yet. Suggest sending a messsage to the user."

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


def run_autogpt(goal, username, password, target_username, cache):
    print("Setting up tools for AutoGPT")

    # Set up tools for AutoGPT
    search = SerpAPIWrapper()

    print("Setting up Instagram for AutoGPT")
    # Create an instance of InstagramTool with Redis cache
    #redis_cache = redis.Redis.from_url(cache)
    # Cargar la URL de Redis desde la variable de entorno
    redis_url = os.getenv('CACHE_REDIS_URL')

    # Crear una instancia de Redis utilizando la URL correcta
    redis_cache = redis.Redis.from_url(redis_url)

    instagram_tool = InstagramTool(username, password, target_username, cache=redis_cache)

    print("Retrieving Instagram profile information...")
    # Check if profile_info is cached
    profile_info = cache.get(f'{username}_profile_info')
    if profile_info:
        print("Profile information loaded from cache")
    else:
        try:
            profile_info = instagram_tool.client.user_info(instagram_tool.user_id)
            print("Profile information retrieved successfully")

            # Cache profile_info and set timeout
            cache.set(f'{username}_profile_info', profile_info)
            cache.expire(f'{username}_profile_info', VERY_LONG_TIMEOUT)

            print(f"Cached {username}_profile_info with timeout {VERY_LONG_TIMEOUT} seconds")

            # Check if profile_info is cached
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
    app.run(debug=True, host='0.0.0.0')





