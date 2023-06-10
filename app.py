import os
from dotenv import load_dotenv

from instagrapi import Client
from instagrapi.exceptions import ClientError


# Load .env file
def load_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)


def instagrapi_follow_and_message(username, password):
    # Create a client object
    client = Client()
    # Login to Instagram
    client.login(username, password)
    print('logged in')

    # Get the user id of louvivien
    user_id = client.user_id_from_username('louvivien')
                            # # Follow louvivien
                            # result = client.user_follow(user_id)
                            # # Check if the follow was successful
                            # if result == True:
                            #     print('Followed successfully')
                            # else:
                            #     print('Follow failed')
    print("user found")                      
    # Send a direct message
    print("sending message")                      
    message = 'Hello, this is a test message usingf instagrapi'
    try:
        result = client.direct_send(message, [user_id])
        print('Message sent successfully')
    except ClientError as e:
        print('Message failed')
        print(e)


if __name__ == "__main__":
    load_env()
    username = os.getenv('INSTA_USERNAME')
    password = os.getenv('INSTA_PASSWORD')
    driver_path = os.getenv('CHROME_DRIVER_PATH')
    # print(username, password, driver_path)
    

    instagrapi_follow_and_message(username, password)




# Tested non working solutions:

# from instapy import InstaPy
# from instabot import Bot
# from instaclient import InstaClient
# from instaclient.errors.common import NotLoggedInError, PrivateAccountError

# # Instaclient
# def instaclient_follow_and_message(username, password, driver_path):
#     client = InstaClient(driver_path=driver_path)
#     try:
#         client.login(username=username, password=password)
#     except NotLoggedInError:
#         print('Could not log in')
#     try:
#         client.follow('louvivien')
#     except PrivateAccountError:
#         print('The account is private')
#     try:
#         client.message('louvivien', 'Hello, this is me with Instaclient')
#     except Exception as e:
#         print(f'Error occurred: {str(e)}')

# pb with chromdriver

# InstaPy
# def instapy_follow(username, password):
#     session = InstaPy(username=username, password=password)
#     session.login()
#     session.follow_by_list(["louvivien"], times=1, sleep_delay=600, interact=False)


#Instapy can't send messages to user

# # Instabot
# def instabot_follow_and_message(username, password):
#     bot = Bot()
#     bot.login(username=username, password=password)
#     print('logged in')
#     bot.follow("louvivien")
#     print('followed')
#     message = "Hello, this is me with Instabot"
#     bot.send_message(message, "louvivien")
#     print('message sent')

# 2023-06-10 15:35:03,523 - instabot version: 0.117.0 - ERROR - Request returns 429 error!