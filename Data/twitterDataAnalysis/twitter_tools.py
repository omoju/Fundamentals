import datetime
from datetime import datetime
from datetime import timedelta
from datetime import time

def extract_features(tweet_list):
	returnList = []

	for tweet in tweet_list:

		timeOfDay = extractTimeOfDay(tweet)
		containsMention = extractContainsMention(tweet)
		containsURL = extractContainsURL(tweet)
		tweetLength = extractTweetLength(tweet)
		containsHashtag = extractContainsHashtag(tweet)
		isReply = extractIsReply(tweet)

		featureTuple = (timeOfDay, containsMention, containsURL, tweetLength, containsHashtag, isReply)

		returnList.append(featureTuple)

	return returnList

def extractTimeOfDay(tweet):
	''' Returns: 'morning, afternoon, evening, night' '''

	returnString = None
	createdAtStr = None

	morningLeftEdge = time(11, 0, 0)
	afternoonLeftEdge = time(17, 0, 0) 
	eveningLeftEdge = time(22, 0, 0)
	midnight = time(23, 59, 59)
	nightLeftEdge = time(2, 0, 0)

	if "created_at" in tweet:
		createdAtStr = tweet["created_at"]
		createdDate = datetime.strptime(createdAtStr[:-11], "%a %b %d %H:%M:%S")

		asTime = time(createdDate.hour, createdDate.minute, createdDate.second)

		if morningLeftEdge<=asTime and asTime<=afternoonLeftEdge:
			returnString = "morning"
		elif afternoonLeftEdge<=asTime and asTime<=eveningLeftEdge:
			returnString = "afternoon"
		elif asTime>=eveningLeftEdge and asTime<=midnight:
			returnString = "evening"
		elif asTime<=nightLeftEdge:
			returnString = "evening"
		elif nightLeftEdge<=asTime and asTime<=morningLeftEdge:
			returnString = "night"

	return returnString


def extractContainsMention(tweet):
	
	returnFloat = 0.0

	if "user_mentions" in tweet:
		numMentions = len(tweet["user_mentions"])

		if numMentions>0:
			returnFloat = 1.0

	return returnFloat

def extractContainsURL(tweet):
	
	returnFloat = 0.0

	if "urls" in tweet:
		if len(tweet["urls"])>0:
			returnFloat = 1.0

	return returnFloat

def extractTweetLength(tweet):
	tweetText = tweet["text"]

	return len(tweetText)

def extractContainsHashtag(tweet):
	
	returnFloat = 0.0

	if "hashtags" in tweet:
		if len(tweet["hashtags"])>0:
			returnFloat = 1.0

	return returnFloat

def extractIsReply(tweet):
	returnFloat = 0.0

	if "in_reply_to_screen_name" in tweet:
		if tweet["in_reply_to_screen_name"] is not None:
			returnFloat = 1.0

	return returnFloat