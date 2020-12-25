import tweepy
import os

# API Key
consumer_key = os.environ['ConsumerKeyVar']
consumer_secret = os.environ['ConsumerSecretVar']
access_key = os.environ['AccessKeyVar']
access_secret = os.environ['AccessSecretVar']

# Tweepy Auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

noFavRtTweet = []
mentionTweet = []
noDeleteTweet = []

def lambda_handler(event, context):
    # No Favorite No RT Tweet
    print("==========No Favorite No RT Tweet==========")
    for tweet in tweepy.Cursor(api.user_timeline,exclude_replies = True).items(200):
        if tweet.favorite_count == 0 and tweet.retweet_count == 0:
            print(tweet.id,tweet.created_at,tweet.text.replace('\n',''))
            noFavRtTweet.append(tweet.id)

    # Reply Tweet
    print("==========Reply Tweet==========")
    for mentions in tweepy.Cursor(api.mentions_timeline).items(400):
        print(mentions.id,mentions.created_at,mentions.text.replace('\n',''))
        mentionTweet.append(mentions.in_reply_to_status_id)

    print("==========No Favorite No RT Reply Tweet==========")
    # No Favorite No RT Reply Tweet
    for tweet in noFavRtTweet:
        for reptw in mentionTweet:
            if tweet == reptw:
                print(api.get_status(tweet).id,api.get_status(tweet).created_at,api.get_status(tweet).text.replace('\n',''))
                noDeleteTweet.append(tweet)

    # Extraction Delete Tweet
    print("==========Extraction Delete tweet==========")
    perfectList = set(noFavRtTweet) ^ set(noDeleteTweet)
    print(list(perfectList))

    # Delete Tweet
    print("==========delete tweet==========")
    for deltw in perfectList:
        try: 
            print(api.get_status(deltw).id,api.get_status(deltw).created_at,api.get_status(deltw).text)
            api.destroy_status(deltw)
        except Exception as e:
            print("ゴミ屑エラー")
            print(e)