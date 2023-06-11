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

# Load .env file
def load_env():
    print("Loading environment variables...")
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)


# Function to message a user on Instagram
class InstagramTool:
    def __init__(self, username, password, proxy=None):
        print("Initializing Instagram client...")
        self.client = Client()
        self.client.delay_range = [1, 3]
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
        print("Session saved to file")
        if proxy:
            print("Setting up proxy...")
            self.client.set_proxy(proxy)
            print("Proxy set up")
        print("Getting user ID...")
        self.user_id = self.client.user_id_from_username('louvivien')
        print("User found")
        # Initialize last_message_id and thread_id as None
        self.last_message_id = None
        self.thread_id = None

    def send_message(self, message):
        print("Sending message...")
        try:
            result = self.client.direct_send(message, user_ids=[self.user_id])
            thread_id = result.thread_id
            thread = self.client.direct_thread(thread_id)
            # Store last_message_id and thread_id as instance variables
            self.last_message_id = thread.messages[0].id
            self.thread_id = result.thread_id
            print("Message sent successfully")
            return  "Message sent successfully"
        
        except ClientError as e:
            print('Message failed')
            print(e)

    def receive_message(self, *args, **kwargs):
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
            new_messages = [m for m in thread.messages if m.id > self.last_message_id]
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


def run_autogpt(goal, username, password):
    print("Setting up tools for AutoGPT")
    # Set up tools for AutoGPT
    search = SerpAPIWrapper()

    print("Setting up Instagram for AutoGPT")
    # Create an instance of InstagramTool
    instagram_tool = InstagramTool(username, password)


    # Add the send_message and receive_message methods as separate tools
    tools = [
        Tool(
            name="search",
            func=search.run,
            description="usefulfor when you need to answer questions about current events. You should ask targeted questions"
        ),
        WriteFileTool(),
        ReadFileTool(),
        Tool(
            name="instagram_send",
            func=instagram_tool.send_message,
            description="Tool for sending messages to a user on Instagram."
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
        ai_name="Tom",
        ai_role="Assistant. Do not say that you are an AI",
        tools=tools,
        llm=ChatOpenAI(temperature=0),
        memory=vectorstore.as_retriever()
       )
    agent.chain.verbose = True

    # Run AutoGPT with your goal and pass the user's reply as an argument
    print("Running AutoGPT...")
    agent.run([goal])

if __name__ == "__main__":
    # Load environment variables
    load_env()
    username = os.getenv('INSTA_USERNAME')
    password = os.getenv('INSTA_PASSWORD')

    # Set your goal as a natural language string
    goal = "Engage in a conversation with an Instagram user"

    # Run AutoGPT with the goal
    run_autogpt(goal, username, password)
