import string
from datetime import datetime
import pytz
from mastodon import Mastodon
from openpyxl import Workbook
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------

# ======================
# Code for API access
# Get the different variables from your mastodon account
# ======================

# Problem 0

mastodon = Mastodon(
    client_id="bN1WW4A0oAyinrc0kzds0ESJ8Qt4sQPgnfMAw7igyZw",
    client_secret="_xmWrG0tCj0VS3W59LCi2oCJ-fAXUe9ovYFBXcRBKSs",
    access_token="awEvsZJughomnKkcisDWPS6ppT_y5UnYxxUbNuebUZc",
    api_base_url="https://mastodon.social"
)

# ======================
# Global variables & functions
# ======================


# Problem 1

# TODO: Object Toot
class Toot:
    def __init__(self, content, account, user_id, hashtags, bookmark, no_replies, url, toot_id, count_replies, pubdate, mentions, media, language, poll):
        self.content = content
        self.account = account
        self.user_id = user_id
        self.hashtags = hashtags
        self.bookmark = bookmark
        self.no_replies = no_replies
        self.url = url
        self.toot_id = toot_id
        self.count_replies = count_replies
        self.pubdate = pubdate
        self.mentions = mentions
        self.media = media
        self.language = language
        self.poll = poll


# Problem 2

# TODO: get_text_content (global function)
# Updated function to work with Toot objects


def get_text_content(toot):
    # Get 'content' from toot, if no 'content' use '' empty
    html_C_toot = getattr(toot, 'content', '')

    # no content return empty
    if not html_C_toot:
        return ""

    # BeautifulSoup to take text from HTML
    soup = BeautifulSoup(html_C_toot, 'html.parser')

    # Get only the text and remove spaces
    clean_text = soup.get_text(separator=' ', strip=True)
    return ' '.join(clean_text.split())


# ======================
# Loading
# ======================

# Problem 3

# TODO: Load function
def load(hashtag):
    # Make an empty list to store the toots
    toots = []

   # Get 10 toots with the hashtag
    result = mastodon.timeline_hashtag(hashtag, limit=10)

    # Iterate through the results and create Toot objects
    for toot_data in result:
        # Get the cleaned text from the toot
        content = get_text_content(toot_data)

       # Make a new Toot object with the information
        toot_object = Toot(
            content=content,
            account=toot_data['account'],
            user_id=toot_data['account']['id'],
            # Hashtags from the toot
            hashtags=toot_data.get('tags', []),
            # No bookmark right now
            bookmark=False,
            no_replies=toot_data['replies_count'] == 0,
            url=toot_data['url'],
            toot_id=toot_data['id'],
            count_replies=toot_data['replies_count'],
            pubdate=toot_data['created_at'],
            mentions=toot_data.get('mentions', []),
            media=toot_data.get('media_attachments', []),
            language=toot_data['language'],
            # Check if theres a poll
            poll=toot_data.get('poll', None)
        )

        # Add this Toot object to the list
        toots.append(toot_object)

    # Return the list of Toot objects
    return toots


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, toot):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# MEDIA TRIGGERS

# Problem 4

# TODO: MediaTrigger
class MediaTrigger(Trigger):
    def evaluate(self, toot):
        # This should be changed in subclasses
        return bool(getattr(toot, 'media', []))

# Problem 5

# TODO: ImageMediaTrigger


class ImageMediaTrigger(MediaTrigger):
    def evaluate(self, toot):
        # Check if the media attribute contains at least one image attachment
        return any(media['type'] == 'image' for media in toot.media)

# Problem 6

# TODO: VideoMediaTrigger


class VideoMediaTrigger(MediaTrigger):
    def evaluate(self, toot):
        return any(media['type'] == 'video' for media in toot.media)

# Problem 7

# TODO: GifMediaTrigger


class GifMediaTrigger(MediaTrigger):
    def evaluate(self, toot):

        # Check if 'media' exists and is a list
        if not hasattr(toot, 'media') or not isinstance(toot.media, list):
            return False

        # Go through media items
        for media in toot.media:
            if isinstance(media, dict):
                # Make sure type is lowercase
                media_type = media.get('type', '').lower()
                # Check if it's a GIF or  GIF-like variants
                if media_type in ['gif', 'gifv']:
                    return True

        return False

# Problem 8

# TODO: AudioMediaTrigger


class AudioMediaTrigger(MediaTrigger):
    def evaluate(self, toot):
        return any(media['type'] == 'audio' for media in toot.media)

# Problem 9

# TODO: LanguageTrigger


class LanguageTrigger(Trigger):
    def __init__(self, language):
        self.language = language

    def evaluate(self, toot):
        return toot.language == self.language


# Problem 10

# TODO: PollTrigger
class PollTrigger(Trigger):
    def evaluate(self, toot):
        return bool(toot.poll)

# Problem 11

# TODO: MentionsTrigger


class MentionsTrigger(Trigger):
    def evaluate(self, toot):
        return bool(toot.mentions)


# Problem 12

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def evaluate(self, toot):
        content = toot.content.lower()
        content = content.translate(str.maketrans('', '', string.punctuation))
        return self.phrase in content


# TIME TRIGGERS

# Problem 13

# TODO: TimeTrigger
class TimeTrigger(Trigger):
    def __init__(self, ptime):

        # Parse ptime directly with timezone (-05:00)
        # info -> Last try with "%Y-%m-%d %H:%M:%S" it didn't work for (Before and After Trigger) but with %z for timezone it work
        self.ptime = datetime.strptime(ptime, "%Y-%m-%d %H:%M:%S%z")


# Problem 14

# TODO: BeforeTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, toot):

        # Check if toot has a pubdate
        if not hasattr(toot, 'pubdate') or not toot.pubdate:
            return False

        # Make sure pubdate has timezone information
        if toot.pubdate.tzinfo is None:
            toot_pubdate = toot.pubdate.replace(tzinfo=timezone(timedelta(hours=-5)))
        else:
            toot_pubdate = toot.pubdate

        # Compare pubdate with ptime
        return toot_pubdate < self.ptime


# Problem 15

# TODO: AfterTrigger
class AfterTrigger(TimeTrigger):
    def evaluate(self, toot):
        # Check if toot has a pubdate
        if not hasattr(toot, 'pubdate') or not toot.pubdate:
            return False

        # Make sure pubdate has timezone information
        if toot.pubdate.tzinfo is None:
            toot_pubdate = toot.pubdate.replace(tzinfo=timezone(timedelta(hours=-5)))
        else:
            toot_pubdate = toot.pubdate

        # Compare pubdate with ptime
        return toot_pubdate > self.ptime


# ======================
# COMPOSITE TRIGGERS
# ======================

# Problem 16

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, toot):
        return not self.trigger.evaluate(toot)

# Problem 17

# TODO: AndTrigger


class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, toot):

        # Return True if both triggers return True
        return self.trigger1.evaluate(toot) and self.trigger2.evaluate(toot)


# Problem 18

# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, toot):
        return self.trigger1.evaluate(toot) or self.trigger2.evaluate(toot)


# ======================
# Filtering
# ======================

# Problem 19

# TODO: Filter_toots
def filter_toots(toots, triggerlist):
    """
    Takes in a list of Toot instances.

    Returns: a list of only the toots for which a trigger in triggerlist fires.
    """
    triggered_toots = []
    for toot in toots:
        if any(trigger.evaluate(toot) for trigger in triggerlist):
            triggered_toots.append(toot)
    return triggered_toots


# ======================
# Loading into Excel
# ======================

# Problem 20
# TODO: Load_to_workbook
def load_to_workbook(toots, MyFile):
    # Create a new Excel workbook and get the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Toots"

    # Add headers to Excel sheet
    sheet.append(["Account Username", "Publication Date", "Content"])

    # Add toot data
    for toot in toots:
        username = toot.account[0]["username"] if toot.account else "N/A"
        pubdate = toot.pubdate.replace(tzinfo=None) if hasattr(
            toot, "pubdate") and toot.pubdate else "N/A"
        content = toot.content if hasattr(toot, "content") else "N/A"
        # Append the data to the sheet
        sheet.append([username, pubdate, content])
    # Save the workbook
    workbook.save(MyFile)

