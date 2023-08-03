import json
import requests
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
from langchain_experimental.autonomous_agents import AutoGPT
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, root_validator
import faiss
from datetime import datetime, timedelta
import random
from flask import Flask, send_from_directory, request, jsonify, session
from flask_cors import CORS

from flask_caching import Cache
import threading
import random
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus








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

# Get MongoDB connection string and password from environment variables
db_host_original = os.getenv('DB_HOST')
db_password = os.getenv('DB_PASSWORD')

# Check if db_password is None
if db_password is None:
    print("DB_PASSWORD is not set in the environment variables.")
    # Handle this situation as needed, e.g., by setting a default password, raising an error, etc.
else:
    # URL-encode the password
    db_password_encoded = quote_plus(db_password)

    # Replace <password> placeholder in the connection string with the URL-encoded password
    db_host = db_host_original.replace("<password>", db_password_encoded)


# setup mongoDB connection
client = MongoClient(db_host)

# Check if connected to MongoDB
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected to MongoDB")
except ConnectionError:
    print("Failed to connect to MongoDB")

db = client['letthemlive']
users_collection = db['users']



# Set up Flask server and Cache
app = Flask(__name__, static_folder=os.path.abspath("./client/build"))
app.config['SECRET_KEY'] = 'random_key_for_now'
CORS(app)
cache = Cache(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.getenv('CACHE_REDIS_URL')
    })


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    fullname = data.get('fullname')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'email and password are required.'}), 400

    user = users_collection.find_one({'email': email})
    if user:
        return jsonify({'error': 'email already exists. Please try logging in.'}), 400

    hashed_password = generate_password_hash(password)
    new_user = {'email': email, 'password': hashed_password, 'fullname': fullname}
    users_collection.insert_one(new_user)

    return jsonify({'message': 'Signup successful.'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'email and password are required.'}), 400

    user = users_collection.find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    # If login successful, store user information in session
    session['logged_in'] = True
    session['email'] = email
    return jsonify({
        'message': 'Login successful.',
        'user': {
            'fullname': user.get('fullname', ''), # Return user's full name
            'avatar': user.get('avatar', '') # Return user's avatar image URL
        }
    }), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful.'}), 200



@app.route('/create_influencer', methods=['POST'])
def create_influencer():
    if not session.get('logged_in'):
        return jsonify({'error': 'You must log in first.'}), 401

    data = request.get_json()
    full_name = data.get('full_name')
    insta_username = data.get('insta_username')
    insta_password = data.get('insta_password')
    gender = data.get('gender')
    description = data.get('description')

    influencer = {
        'user_email': session['email'],
        'full_name': full_name,
        'insta_username': insta_username,
        'insta_password': insta_password,
        'gender': gender,
        'description': description,
        # TODO fetch total no of posts and followers of this user from insta and store it
        'total_posts': 0,
        'total_followers': 0
    }

    influencers_collection = db['influencers']
    influencers_collection.insert_one(influencer)

    return jsonify({'message': 'Virtual influencer created successfully.'}), 201

@app.route('/fetch_influencers', methods=['GET'])
def fetch_influencers():
    if not session.get('logged_in'):
        return jsonify({'error': 'You must log in first.'}), 401

    email = session['email']
    influencers_collection = db['influencers']
    influencers = list(influencers_collection.find({'user_email': email}, {'_id': 0}))

    return jsonify({'influencers': influencers}), 200


@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'email' not in session:
        return jsonify({'error': 'User is not logged in.'}), 401

    data = request.get_json()
    email = session['email']
    new_email = data.get('new_email')
    new_fullname = data.get('new_fullname')
    new_password = data.get('new_password')
    new_avatar = data.get('new_avatar')

    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    if new_email:
        user['email'] = new_email
        session['email'] = new_email
    if new_fullname:
        user['fullname'] = new_fullname
    if new_password:
        user['password'] = generate_password_hash(new_password)
    if new_avatar:
        user['avatar'] = new_avatar

    users_collection.update_one({'email': email}, {'$set': user})

    return jsonify({'message': 'Profile updated successfully.'}), 200



## Routes for frontend
@app.route('/api')
def api():
    return 'Hello World from Flask!'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        print(f"Serving index.html from {app.static_folder}")
        return send_from_directory(app.static_folder, 'index.html')
    
    

# Task to keep the server active
def do_nothing():
    print("Keeping server awake...")
    # This is where you'd put the task you want to run.
    # Since you want to do nothing, we'll just pass.
    pass

def schedule_do_nothing():
    # Schedule do_nothing to be called after 12 minutes (720 seconds)
    threading.Timer(720, schedule_do_nothing).start()

    # Call the function
    do_nothing()


## Tool to clear cache
# http://127.0.0.1:5000/clear_cache
@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    print("Clearing cache")
    cache.clear()
    return "Cache has been cleared"
# Set how long the data will stay in the cache
VERY_LONG_TIMEOUT = 30 * 24 * 60 * 60  # 30 days in seconds



# Functions for editing profile and reading images content

def run_profile_edit(username, password, target_username, cache, **kwargs):
    print("Editing Account Details")

    if cache is None:
        print("Error: Unable to connect to the Redis server.")
        exit(1)

    instagram_tool = InstagramTool(username, password, target_username, cache=cache)
    instagram_tool.edit_account(**kwargs)

def read_image(image_url: str) -> str:
    try:
        HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
        API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        response = requests.post(API_URL, headers=headers, data=image_url)
        response_json = response.json()
        return response_json[0]["generated_text"]
    except Exception as e:
        print(f"Image description from Hugging Face failed due to error: {e}")
        print("Getting Image description from image-to-caption.io endpoint")
        try:
            return read_image_by_io_endpoint(image_url)
        except Exception as e:
            print(f"Image description from io endpoint failed due to error: {e}")

    return ""

def read_image_by_io_endpoint(image_url: str) -> str:

    ENDPOINT_URL = "https://image-to-caption.io/api/v1/description"

    payload = json.dumps({
        "imageUrl": image_url
    })

    headers = {
        'authority': 'image-to-caption.io',
        'accept': '/',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': '_ga=GA1.1.991307832.1690024023; _ga_9ELLC7L1NQ=GS1.1.1690024022.1.1.1690026865.0.0.0',
        'origin': 'https://image-to-caption.io',
        'pragma': 'no-cache',
        'referer': 'https://image-to-caption.io/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-csrftoken': 'Ud7UiwLDNHWqiFTwFW1vukOJcMYEULIL'
    }

    response = requests.request("POST", ENDPOINT_URL, headers=headers, data=payload)

    response_json = json.loads(response.text)

    return response_json["description"]

def generate_instagram_caption(image_description: str, use_emoji: bool = True) -> list:

    ENDPOINT_URL = "https://image-to-caption.io/api/v1/captions"

    payload = json.dumps({
        "description": image_description,
        "useEmoji": use_emoji
    })
    headers = {
        'authority': 'image-to-caption.io',
        'accept': '/',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': '_ga=GA1.1.991307832.1690024023; _ga_9ELLC7L1NQ=GS1.1.1690024022.1.1.1690026865.0.0.0',
        'origin': 'https://image-to-caption.io',
        'pragma': 'no-cache',
        'referer': 'https://image-to-caption.io/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-csrftoken': 'Ud7UiwLDNHWqiFTwFW1vukOJcMYEULIL'
    }

    response = requests.request("POST", ENDPOINT_URL, headers=headers, data=payload)

    response_json = json.loads(response.text)

    return response_json["captions"]



# Langchain input schemas for checking inputs to tools
# https://python.langchain.com/docs/modules/agents/tools/how_to/tool_input_validation
class InstagramSendInputSchema(BaseModel):
    tool_input: str = Field(...)

    @root_validator
    def validate_input(cls, values: Dict[str, Any]) -> Dict:
        tool_input = values["tool_input"]
        if not tool_input:
            raise ValueError("You are using the send_message tool without providing a message to send. To make this work you first need to write the message then use this tool. Do not write the message in a file or it will not work")

        if tool_input.endswith('.txt'):
            raise ValueError("You are using the send_message tool with a file. This tool does not work with files, you need to write a regular message, not provide a file")

        return values

class InstagramGetPostsSchema(BaseModel):
    tool_input: int = Field(description="count of numbers to posts to return")


class InstagramLikePostsSchema(BaseModel):
    tool_input: list = Field(description="list of posts that needs to be liked.")
    
    @root_validator
    def validate_input(cls, values: Dict[str, Any]) -> Dict:
        tool_input = values["tool_input"]
        if type(tool_input) != list:
            raise ValueError("You are using the like_post tool without providing a list type argument. To make this work you need to provide list of integers. For example: [3052787801845186036, 2877751288856163701]")
              
        return values


class InstagramCommentInputSchema(BaseModel):
    post_id: str
    comment_text: str

# Functions for Instagram using instagrapi methods
# https://github.com/adw0rd/instagrapi/

# Custom instagrapi client to load and dump settings from and to an object
class CustomClient(Client):
    def load_settings_from_object(self, settings):
        self.set_settings(settings)

    def dump_settings_to_object(self):
        return self.get_settings()

class InstagramTool:
    MAX_FOLLOW_PER_DAY = 150

    def __init__(self, username, password, target_username, proxy=None, cache=None):
        try:
            print("Initializing Instagram client...")
            self.client = CustomClient()
        except Exception as e:
            print(f"Error while initializing Instagram client: {e}")
            return
        self.client.delay_range = [1, 3]
        self.cache = cache
        self.target_username = target_username
        self.posts = None
        self.llm = OpenAI(model_name="text-davinci-003", openai_api_key=os.getenv('OPENAI_API_KEY'))

        # Load session from cache
        session_key = f"{username}_session"
        session_data = self.cache.get(session_key)

        if session_data:
            self.client.load_settings_from_object(session_data)
            print("Session loaded from cache")
        else:
            try:
                print("Logging in to Instagram...")
                self.client.login(username, password)
                print('Logged in')
            except LoginRequired:
                print("Session expired. Logging in again...")
                self.client.login(username, password)
                print('Logged in')
            session_data = self.client.dump_settings_to_object()
            self.cache.set(session_key, session_data, timeout=VERY_LONG_TIMEOUT)
        time.sleep(random.uniform(2, 4))  # Random delay to mimic human behavior and avoid rate limits

        if proxy:
            print("Setting up proxy...")
            self.client.set_proxy(proxy)
            print("Proxy set up")

        # Find user ID of the target
        print("Getting user ID...")
        user_id_key = f"user_id:{target_username}"
        user_id = cache.get(user_id_key)
        if user_id:
            self.user_id = user_id
            print("User ID retrieved from cache")
        else:
            self.user_id = self.client.user_id_from_username(target_username)
            cache.set(user_id_key, self.user_id, timeout=VERY_LONG_TIMEOUT)
            cache.set(user_id_key, self.user_id, timeout=VERY_LONG_TIMEOUT)  
            user_id = cache.get(user_id_key)
            print("User ID retrieved from Instagram and saved to cache")
        if user_id is None:
            print("Error: Unable to get the user ID from the cache.")
            exit(1)
        print("User found")
        time.sleep(random.uniform(2, 4))  # Random delay to mimic human behavior and avoid rate limits

        # Initialize last_sent_message as None
        self.last_sent_message = None
        # Initialize last_message_id and thread_id as None
        self.last_message_id = None
        self.thread_id = None

        # Initialize follow count
        self.follow_count = 0
        self.follow_reset_time = datetime.now() + timedelta(days=1)

        # Check if the target user is already followed
        follow_status_key = f"{username}_follows_{target_username}_true"
        follow_status = self.cache.get(follow_status_key)
        if follow_status:
            print("User already followed. Skipping follow.")
        else:
            # Check if the follow limit has been reached
            if self.follow_count >= self.MAX_FOLLOW_PER_DAY:
                print("Follow limit is reached for today. Can't proceed. Try again tomorrow.")
                return
            # Check if the follow count should be reset
            if datetime.now() >= self.follow_reset_time:
                print("Resetting follow count for the new day.")
                self.follow_count = 0
                self.follow_reset_time = datetime.now() + timedelta(days=1)

            # Follow target_username
            result = self.client.user_follow(self.user_id)
            # Check if the follow was successful
            if result == True:
                print('Followed successfully')
                # Save follow status to cache
                self.cache.set(follow_status_key, True, timeout=VERY_LONG_TIMEOUT)
                self.follow_count += 1  # Increment the follow count
                time.sleep(random.uniform(2, 4))  # Random delay to mimic human behavior and avoid rate limits
            else:
                print('Follow failed')

    def send_message(self, tool_input: InstagramSendInputSchema):
        if isinstance(tool_input, str):
            tool_input = InstagramSendInputSchema(tool_input=tool_input)
        message = tool_input.tool_input
        print(f"Arguments: {tool_input}")

        # Check if the message is empty
        if not message:
            return "You did not write a message to send, in order to use this tool you need to write a message to the user, try again please"
        print(f"Message: {message}")  # Log the message

        # Check if the message is the same as the last sent message
        if message == self.last_sent_message:
            print("Message is the same as the last sent message. Skipping sending. Did you wait for the user reply? Suggest using instagram_receive")
            return "Message is the same as the last sent message. Skipping sending. Did you wait for the user reply? Suggest using instagram_receive"

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

    def receive_message(self, tool_input: Optional[str] = None):
        print("Waiting for reply...")

        # Check if last_message_id and thread_id are None
        if self.last_message_id is None or self.thread_id is None:
            print("You did not send a message yet. Suggest sending a messsage to the user.")
            return  "You did not send a message yet. Suggest sending a messsage to the user."

        for i in range(3):  # try 3 times
            print(f"Attempt {i+1}...")
            self.client.delay_range = [27, 30]

            try:
                print("Fetching thread...")
                thread = self.client.direct_thread(self.thread_id)
                print("Thread fetched. Checking for new messages...")
                print("Thread : ", thread)
                new_messages = [m for m in thread.messages if m.timestamp > self.last_sent_timestamp and m.item_type != 'placeholder']
            except Exception as e:
                print(f"Error while fetching thread or checking for new messages: {e}")
                return f"Error while fetching thread or checking for new messages: {e}"

            if new_messages:
                print("New messages found:")
                for message in new_messages:
                    print(f"Received message: {message.text}")
                try:
                    self.last_message_id = thread.messages[0].id
                    self.last_sent_timestamp = thread.messages[0].timestamp
                except Exception as e:
                    print(f"Error while updating last_message_id or last_sent_timestamp: {e}")
                    return f"Error while updating last_message_id or last_sent_timestamp: {e}"
                return f"Command instagram_receive returned: the user replied: '{new_messages[0].text}. Suggest sending a new messsage to the user to continue the discussion.'"
            else:
                print("No new messages found. Waiting again...")
                self.client.delay_range = [57, 60]

        print("No reply received after 3 attempts.")
        return "No reply received yet. Suggest checking again in one hour."

    def edit_account(self, **kwargs):
        print(f"Changing following account data: {', '.join(kwargs.keys())}")
        try:
            self.client.account_edit(**kwargs)
            print("Account data changed successfully")
        except Exception as e:
            print(f"Error while changing account details: {e}")

    def search_and_follow(self, tool_input):
        query = tool_input
        users = self.client.search_users(query)
        followed = 0
        users = users[:3]
        for user in users:
            try:
                self.client.user_follow(user.pk)
                followed += 1
            except Exception as e:
                print(f"Failed to follow {user.username}: {e}")

        return f"Followed {followed} user(s) from the search results."

    def search_posts_by_keywords(self, tool_input, count=1):
        try:
            results = self.client.search(tool_input, 'posts', count)
            return results
        except Exception as e:
            return f"Error searching posts: {e}"
        
    def generate_comment(self, caption_text):
        prompt = f"Write a unique and engaging comment based on the following Instagram caption: {caption_text}"
        comment = self.llm(prompt, max_tokens=30)
        return comment
    
    def get_posts_from_followers(self, tool_input=3):
        try:
            count = int(tool_input)
            following_users = self.client.user_following(self.client.user_id)
            following_users_ids = [i for i in following_users.keys()]
            posts = []

            # get 1 random post from count(default=3) number of followers
            following_users_ids = random.sample(following_users_ids, count)
            for user in following_users_ids:
                # fetch 10 recent posts and pick 1 random post.
                user_posts = self.client.user_medias(user, 10)
                posts.append(random.choice(user_posts))
            self.posts = posts
            post_ids = [int(p.pk )for p in posts]
            # like all the collected posts
            self.like_post(post_ids)
            print(f'{count} post(s) found from your followers. Their ids are as followes: {post_ids}')

            return {int(p.pk):p.caption_text for p in self.posts}
        except Exception as e:
            return f"Error getting posts from following: {e}"
    
    def like_post(self, tool_input):
        ## TODO chache all the ids of the already liked post to avoid them in next loop
        try:
            post_ids = tool_input
            for post_id in post_ids:
                self.client.media_like(post_id)
                print (f"Post {post_id} liked successfully.")
        except Exception as e:
            return f"Error liking post: {e}"

    def comment_on_post(self, tool_input: Optional[str] = None):
        '''
        fetches posts from self.posts and add comments to those posts. Make sure to call 
        self.posts is not empty.
        '''
        try:
            if self.posts:
                for post in self.posts:
                    # generate a comment using the text in post.caption_text
                    comment_text = self.generate_comment(post.caption_text)
                    self.client.media_comment(post.pk, comment_text)
                    return "Comment posted successfully."
        except Exception as e:
            return f"Error commenting on post: {e}"

# AutoGPT lauched by Langchain
def run_autogpt(goal, username, password, target_username, cache):
    print("Setting up tools for AutoGPT")

    if cache is None:
        print("Error: Unable to connect to the Redis server.")
        exit(1)

    # Set up tools for AutoGPT
    search = SerpAPIWrapper()

    print("Setting up Instagram for AutoGPT")
    # Create an instance of InstagramTool so to access instagrapi methods
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
        ai_role = f"This is your bio: {profile_info.biography}. Act as if you were this person, never say that you are an AI. Do not write in a commercial way, write as if you were a real person not a salesperson."
    else:
        ai_role = "This is your bio: I am a passionate individual who loves to engage with people and share my thoughts. Act as if you were this person, never say that you are an AI."

    # Langchain: set the tools that AutoGPT can use
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
                description="Tool for sending a message that you have previously written to a user on Instagram. Do not write the message you want to send in a file or it will not work."
            ),
            Tool(
                name="instagram_receive",
                func=instagram_tool.receive_message,
                description="Tool for receiving messages from a user on Instagram."
            ),
            Tool(
                name="instagram_search_follow",
                func=instagram_tool.search_and_follow,
                description="Tool for searching Instagram accounts by query and following a specified number of them."
            ),
            Tool(
                name="instagram_get_posts_from_followers",
                func=instagram_tool.get_posts_from_followers,
                args_schema=InstagramGetPostsSchema,
                description="Tool for getting a specified number of posts from users the account is following on Instagram."
            ),
            # commenting out this tool to prevent autoGPT from making additional call to 
            # like_post tool. The posts would be automatcally liked as a part of get_posts_from_followers tool.
            # Tool(
            #     name="instagram_like",
            #     func=instagram_tool.like_post,
            #     args_schema=InstagramLikePostsSchema,
            #     description="Tool for liking posts on Instagram given their post_ids as a list."
            # ),
            Tool(
                name="instagram_comment",
                func=instagram_tool.comment_on_post,
                description="Tool for commenting on a post on Instagram. Use text returned from instagram_get_posts_from_followers and write a comment using that.  Make sure to call get_posts_from_followers_and_like before it."
            ),
        ]

    # Langchain: set up memory for AutoGPT
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
    #Use Model gpt-4 because gpt-3.5 don't follow well the system message and generated "" empty input
    # Langchain: set up model and AutoGPT
    agent = AutoGPT.from_llm_and_tools(
        ai_name=ai_name,
        ai_role=ai_role,
        tools=tools,
        llm=ChatOpenAI(model="gpt-4",temperature=0.5),
        memory=vectorstore.as_retriever()
       )
    agent.chain.verbose = True

    # Run AutoGPT with your goal
    print("Running AutoGPT...")
    agent.run([goal])


if __name__ == "__main__":

    # Start the scheduling
    schedule_do_nothing()
        

######## All in one prompt (works/commented for now because i dont want it to run alone on the server)
    
    # Set the goal for AutoGPT
    goal = "'I want to engage with my Instagram followers. Firstly, I aim to send a message to a specific user. Before sending the message, I will check if I have any previous conversations with this user. If there is an existing conversation, I will verify its stage to see if I have already sent a message. If a message has been sent, I will patiently wait for their response before sending another one.\n\nOnce I receive a reply, I will continue the conversation with the user. I will also regularly check for any new responses and respond promptly. Engaging in a meaningful and respectful conversation is a priority.\n\nWhile having a conversation or after, when waiting for a reply, I would like to search for 5 profiles related to my interests (do this only once) and follow them to expand my network.\n\nNext, I will retrieve the 2 most recent posts from the users (do this only once) I am following and actively like those posts to show appreciation and support.\n\nLastly, I intend to leave thoughtful comments on those posts (do this only once) to foster a sense of community and connection with my followers. I will patiently wait for the response for the discussion'"

    # Create a thread for AutoGPT
    autogpt_thread = threading.Thread(target=run_autogpt, args=(goal, username, password, target_username, cache))
    autogpt_thread.start()



    # Start server
    app.run(debug=False)
    
    
    
    
    
    
    
    
######## Specific prompts 

                    # Set your goal as a natural language string
                    #goal = "Engage in a conversation with an Instagram user"
                    
                    ######## Conversation

                    # # Set your goal as a natural language string
                    # goal = "Engage in a conversation with an Instagram user"
                    
                    # # Create a thread for AutoGPT
                    # autogpt_thread = threading.Thread(target=run_autogpt, args=(goal, username, password, target_username, cache))
                    # autogpt_thread.start()
                    
                    ######## Edit profile

                    # Creating a thread to test changing account details
                    # profile_edit_thread = threading.Thread(target=run_profile_edit, args=(username, password, target_username, cache), kwargs={'biography': "Whatever to put here", 'full_name': "Any new name", 'external_url': "http://feedlink.io/"})
                    # profile_edit_thread.start()

                    # ######## search and follow
                    # # Set your goal as a natural language string
                    # goal = "Search for 5 profiles related to fashion account and follow them."
                    

                    ######## find posts from people you follow.
                    # Set your goal as a natural language stringf
                    # goal = "Find 2 recents posts from among your followers and leave a comment"
                    
                    ######## Work in progress
                    #Test image reading functions
                    # img_url = "./cat.jpg"
                    # print(read_image(img_url))
                    # image_desc = read_image_by_io_endpoint(img_url)
                    # print(image_desc)
                    # print(generate_instagram_caption(image_desc))
    
