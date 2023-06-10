import os
import time
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import ClientError
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
def instagrapi_message(username, password):
    print("Initializing Instagram client...")
    # Create a client object
    client = Client()
    # Login to Instagram
    print("Logging in to Instagram...")
    client.login(username, password)
    print('Logged in')

    # Get the user id of louvivien
    print("Getting user ID...")
    user_id = client.user_id_from_username('louvivien')
    print("User found")                      

    # Send a direct message
    print("Sending message...")                      
    message = 'Hello, this is a test message using instagrapi and autogpt'
    try:
        result = client.direct_send(message, user_ids=[user_id])
        print('Message sent successfully')

        # Get the thread_id from the result
        thread_id = result.thread_id

        # Get the thread with the user
        thread = client.direct_thread(thread_id)

        # Keep track of the last message you sent
        last_message_id = thread.messages[0].id

        # Wait for the user to reply
        print("Waiting for reply...")
        for _ in range(3):  # try 3 times
            # Refresh the thread
            thread = client.direct_thread(thread_id)

            # Check for new messages
            new_messages = [m for m in thread.messages if m.id > last_message_id]

            if new_messages:
                # Process new messages
                for message in new_messages:
                    print(f"Received message: {message.text}")

                # Update the last message id
                last_message_id = thread.messages[0].id
                return message.text  # Return the text of the last received message
            else:
                print("No reply received yet. Waiting again...")
                time.sleep(60)  # wait for another 60 seconds
        print("No reply received after 3 attempts.")
        return None
    except ClientError as e:
        print('Message failed')
        print(e)

class InstagramTool:
    def __init__(self, username, password):
        self.client = Client()
        self.client.login(username, password)
        self.user_id = self.client.user_id_from_username('louvivien')

    def send_message(self, message):
        result = self.client.direct_send(message, user_ids=[self.user_id])
        thread_id = result.thread_id
        thread = self.client.direct_thread(thread_id)
        last_message_id = thread.messages[0].id
        return last_message_id, thread_id

    def receive_message(self, last_message_id, thread_id):
        thread = self.client.direct_thread(thread_id)
        new_messages = [m for m in thread.messages if m.id > last_message_id]
        return new_messages


def run_autogpt(goal, reply):
    # Set up tools for AutoGPT
    search = SerpAPIWrapper()

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
            description="Tool for sending messages to a user on Instagram"
        ),
        Tool(
            name="instagram_receive",
            func=instagram_tool.receive_message,
            description="Tool for receiving messages from a user on Instagram"
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
        ai_role="Assistant",
        tools=tools,
        llm=ChatOpenAI(temperature=0),
        memory=vectorstore.as_retriever()
    )
    agent.chain.verbose = True

    # Run AutoGPT with your goal and pass the user's reply as an argument
    agent.run([goal, reply])

if __name__ == "__main__":
    # Load environment variables
    load_env()
    username = os.getenv('INSTA_USERNAME')
    password = os.getenv('INSTA_PASSWORD')

    # Set your goal as a natural language string
    goal = "Send a message to an Instagram user and then use Auto-GPT to engage in a conversation based on their reply"
    
    # Get the reply from the Instagram user
    reply = instagrapi_message(username, password)
    goal2 = "User's reply :"+reply

    # If there is no reply after 3 attempts, tell AutoGPT to wait for one hour
    if reply is None:
        print("No reply received yet. Waiting for one hour before checking again...")
        time.sleep(3600)  # wait for one hour
        reply = instagrapi_message(username, password)

    # Run AutoGPT with the goal and the reply (as a second goal)
    run_autogpt(goal, goal2)
