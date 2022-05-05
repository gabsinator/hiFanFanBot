#twitter bot using twitter api v2
import time
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
consumer_key = os.getenv("API_key")
consumer_secret_key = os.getenv("API_secret_key")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
bearer_token = os.getenv("bearer_token")

last_tweet = int(os.getenv("last_tweet"))

exclude_list = ["retweets", "replies"]
tweet = "Hello World"
FILE_NAME = "last.txt"
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

def get_user_id(username):
    response = client.get_user(username=username)
    return response


#read ID of last tweet the bot has replied to
def read_last(FILE_NAME):
    file = open(FILE_NAME, "r")
    last_id = int(file.read().strip())
    file.close()

    return last_id

#store ID of the last tweet the bot replied to
def store_last(FILE_NAME, last_id):
    file = open(FILE_NAME, "w")
    file.write(str(last_id))
    file.close()

    return

def reply():
    tweets = client.get_users_tweets(id=USER_ID, exclude= exclude_list, since_id= last_tweet)

    count = 0

    try:
        for tweet in reversed(tweets.data):
            tweet = dict(tweet)
            tweet_id = tweet["id"]

            client.like(tweet_id=tweet_id)
            client.create_tweet(text= "hi fanfan", in_reply_to_tweet_id= tweet_id)
            count += 1

            os.environ["last_tweet"] = str(tweet_id)

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