#twitter bot using twitter api v2
import time
import tweepy
import os
from github import Github
from dotenv import load_dotenv

load_dotenv()
consumer_key = os.getenv("API_key")
consumer_secret_key = os.getenv("API_secret_key")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
bearer_token = os.getenv("bearer_token")

github_token = os.getenv("github_token")


exclude_list = ["retweets", "replies"]
tweet = "Hello World"
FILE_NAME = "/last.txt"
USER_ID = 1337072139216670723 #id for fanfan
#735765478845489157 #id for gabsinatorrr




# Authenticate to Twitter
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret_key,
    access_token,
    access_token_secret
)

github = Github(github_token)
repo = github.get_user().get_repo("hiFanFanBot")

def get_user_id(username):
    response = client.get_user(username=username)
    return response


#read ID of last tweet the bot has replied to
def read_last(FILE_NAME):

    print("reading ID...")
    file = repo.get_contents(FILE_NAME)
    last_id = file.decoded_content.decode()
    
    return int(last_id)

#store ID of the last tweet the bot replied to
def store_last(last_id):

    print("saving ID...")
    contents = repo.get_contents(FILE_NAME)
    repo.update_file(contents.path, "more tests", str(last_id), contents.sha, branch="master")

    return

def reply():
    tweets = client.get_users_tweets(id=USER_ID, exclude= exclude_list, since_id= read_last(FILE_NAME= FILE_NAME))

    count = 0

    try:
        for tweet in reversed(tweets.data):
            tweet = dict(tweet)
            tweet_id = tweet["id"]

            client.like(tweet_id=tweet_id)
            client.create_tweet(text= "hi fanfan", in_reply_to_tweet_id= tweet_id)
            count += 1

            store_last(last_id= tweet_id)

        print("replied to {0} tweets".format(count))

    except:
        print("nothing to reply to.")
        return

def run():
    while True:
        reply()
        
        time.sleep(180)

if __name__ == "__main__":
    run()