from random import randint
from collections import deque
import time
import google_image_grabber
import praw

# By default, look for 'source' and reply with an image of 'sauce'
r = praw.Reddit(user_agent='A bot that searches for search term and comments a picture of specified images created by /u/bustylasercannon')

cache = deque(maxlen=200)

# Log in to reddit as account to post from
def redditLogin():
	r.login('', '') 

# Get all comments from subreddit specified
def getAllComments(subreddit = 'all'):
	comments = r.get_comments(subreddit, limit = 100)
	return comments

# Check comment for specified term
def checkComment(comment):
	if comment.body.find("sauce") == -1:
		print 'No source found'
		return False
	else:
		print 'Found source!'
		return True
		
def scrape(comments):
	# Loop through all comments pulled
	for c in comments:
		# Ensure comment hasn't already been replied to in session
		if c.id in cache:
			break
		cache.append(c.id)
		# Check for source
		sourceFound = checkComment(c)
		if sourceFound:
			try:
				postReply(c)
			except KeyboardInterrupt:
				global running
				running = False
			except praw.errors.APIException, e:
				print "[ERROR]:", e
				print "Sleeping 30 seconds:"
				time.sleep(600)
				try: 
					postReply(c)
				except:
					continue
			except Exception, e:
				print "[ERROR]:", e
				continue

def postReply(comment):
	# Build a reply and send
	SauceResponse = buildReply()
	try:
		comment.reply(SauceResponse)
		time.sleep(2)
	except praw.errors.APIException, e:
		print "Reddit Exception: Sleeping for 5 minutes"
		time.sleep(300)

def buildReply():
	# Build the lists of variables used in the reply
	replies = ["Here's your sauce!", "Sauce for you!", "Sauce provided.", "Sauce time!", "Sauce.", "Sauce is great.", "Did someone say Sauce?!",
				 "Knock knock, who's there? SAUCE.","SAUCE REQUESTED? SAUCE PROVIDED", "Source.", "Found a sauce for you."]
	images = google_image_grabber.main('sauce', 7)
	# Select random value from each list
	reply = replies[randint(0, len(replies))]
	imageURL = images[randint(0,len(images))]
	# Build reply and return
	finalReply = "[%(textResponse)s](%(sauceURL)s)" % {'textResponse': reply, "sauceURL": imageURL}
	print finalReply
	return finalReply


redditLogin()
running = True
while running:
	#Run indefinitely
	comments = r.get_comments('all',limit = 3000)
	scrape(comments)
	print 'Sleeping until next iteration'
	time.sleep(30)
	print 'Commencing next iteration'
