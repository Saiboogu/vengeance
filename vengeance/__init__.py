
# Standard Imports
from tweepy import OAuthHandler, Stream, StreamListener

# Vengeance Imports
from config import Config

v_config = Config('../config.ini')
v_config.debug()

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = v_config.oauth['ConsumerKey']
consumer_secret = v_config.oauth['ConsumerSecret']

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = v_config.oauth['AccessToken']
access_token_secret = v_config.oauth['AccessTokenSecret']


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.

    This is a basic listener that just prints received tweets to stdout.

    """
    def on_status(self, status):
        tweet = status.text.lower()
        print tweet
        if 'on sale now' in tweet:
            return False
        else:
            return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['basketball'])