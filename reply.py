import praw
from urllib2 import urlopen
import json

key = "[redacted]" # Google Youtube API key
pewdielink = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=pewdiepie&key="+key
tserieslink = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=tseries&key="+key


def commentreply (comment) :
    
    pewdiedata = urlopen(pewdielink).read()
    tseriesdata = urlopen(tserieslink).read() 
    
    pewdiesubs = int( json.loads(pewdiedata)["items"][0]["statistics"]["subscriberCount"] )
    tseriessubs = int( json.loads(tseriesdata)["items"][0]["statistics"]["subscriberCount"] )
    
    if (pewdiesubs > tseriessubs) :
        comment.reply("PewDiePie currently has **" + ("{:,d}".format( int(pewdiesubs) - int(tseriessubs) )) + "** more subscribers than T-Series! \n *** \n ^(I'm just a student's CS project, please don't hurt me! If there's an issue, please PM me. Have a nice day!)")
    elif (tseriessubs > pewdiesubs) :
        comment.reply("T-Series currently has " + ("{:,d}".format( tseriessubs - pewdiesubs )) + " more subscribers than PewDiePie!")
    
    comment.upvote()

