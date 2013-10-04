# -*- encoding: utf-8 -*-
"""twitter demo for PiFace CAD.
Call with no arguments to pull latest tweets from home timeline.
Call with string argument to search for that term
"""
from time import sleep
import threading
import sys
import os
try:
    import twitter  # http://mike.verdone.ca/twitter/
except ImportError:
    print("You need to install Python Twitter Tools "
          "(http://mike.verdone.ca/twitter/).")
    sys.exit(1)
import pifacecommon
import pifacecad


UPDATE_INTERVAL = 60
PAGE_WIDTH = pifacecad.lcd.LCD_WIDTH * 2

CONSUMER_KEY = "6eMHbsNHcxRLIzF4wZWf6g"
CONSUMER_SECRET = "BDL5j87310UBqOtRzMLo2wP93xc8BZ3xh3IGAIjzB0A"
# CONSUMER_KEY = ""
# CONSUMER_SECRET = ""

OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


class NoTweetsError(Exception):
    pass


class TwitterTicker(object):
    def __init__(self, cad, oauth_token, oauth_secret, search_term=None):
        self.twitter = twitter.Twitter(
            auth=twitter.OAuth(
                oauth_token, oauth_secret,
                CONSUMER_KEY, CONSUMER_SECRET)
        )
        self.search_term = search_term
        self.cad = cad
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()
        self.cad.lcd.backlight_on()
        try:
            self.current_tweet = self.get_latest_tweet()
        except NoTweetsError:
            self.current_tweet = None
        self.display_tweet(self.current_tweet)
        self.timer = None

    @property
    def page(self):
        return self._current_page

    @page.setter
    def page(self, new_page):
        num_pages = 1 + int(len(self.current_tweet['text']) / PAGE_WIDTH)
        new_page %= num_pages
        self.display_tweet(self.current_tweet, new_page)

    def get_latest_tweet(self):
        if self.search_term is None:
            return self.twitter.statuses.home_timeline()[0]

        try:
            latest_tweets = self.twitter.search.tweets(
                q=self.search_term,
                since_id=self.current_tweet['id'])['statuses']
        except AttributeError:
            latest_tweets = self.twitter.search.tweets(
                q=self.search_term)['statuses']

        try:
            return latest_tweets[0]
        except IndexError:
            raise NoTweetsError()

    def update(self, event=None):
        """Updated the screen with the latest tweet."""
        print("Updating...")
        try:
            latest_tweet = self.get_latest_tweet()
        except NoTweetsError:
            return
        else:
            if self.current_tweet is None or \
                    latest_tweet['id'] != self.current_tweet['id']:
                self.current_tweet = latest_tweet
                self.display_tweet(self.current_tweet)

    def auto_update(self):
        self.update()
        # update again soon
        self.timer = threading.Timer(UPDATE_INTERVAL, self.auto_update)
        self.timer.start()

    def display_tweet(self, tweet, page=0):
        self._current_page = page
        text = tweet['text']
        self.cad.lcd.clear()
        start = PAGE_WIDTH * page
        end = PAGE_WIDTH * (page + 1)
        top_line = text[start:start+pifacecad.lcd.LCD_WIDTH].ljust(
            pifacecad.lcd.LCD_WIDTH)
        bottom_line = text[start+pifacecad.lcd.LCD_WIDTH:end].ljust(
            pifacecad.lcd.LCD_WIDTH)
        self.cad.lcd.set_cursor(0, 0)
        self.cad.lcd.write(top_line)
        self.cad.lcd.set_cursor(0, 1)
        self.cad.lcd.write(bottom_line)

    def close(self):
        if self.timer is not None:
            self.timer.cancel()
        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()

    def next_page(self, event=None):
        self.page += 1

    def previous_page(self, event=None):
        self.page -= 1


if __name__ == "__main__":
    try:
        search_term = sys.argv[1]
    except IndexError:
        search_term = None
        print("Using home timeline.")
    else:
        print("Searching for", search_term)

    twitter_creds = os.path.expanduser('~/.twitter_piface_demo_credentials')
    if not os.path.exists(twitter_creds):
        twitter.oauth_dance(
            "PiFace Demo", CONSUMER_KEY, CONSUMER_SECRET, twitter_creds)

    oauth_token, oauth_secret = twitter.read_token_file(twitter_creds)

    cad = pifacecad.PiFaceCAD()

    global twitterticker
    twitterticker = TwitterTicker(cad, oauth_token, oauth_secret, search_term)
    twitterticker.auto_update()  # start the updating process

    # listener cannot deactivate itself so we have to wait until it has
    # finished using a barrier.
    global end_barrier
    end_barrier = threading.Barrier(2)

    # wait for button presses
    switchlistener = pifacecad.SwitchEventListener(chip=cad)
    switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
    switchlistener.register(5, pifacecad.IODIR_ON, twitterticker.update)
    switchlistener.register(6, pifacecad.IODIR_ON, twitterticker.previous_page)
    switchlistener.register(7, pifacecad.IODIR_ON, twitterticker.next_page)

    switchlistener.activate()
    end_barrier.wait()  # wait unitl exit

    # exit
    twitterticker.close()
    switchlistener.deactivate()
