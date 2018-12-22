#!/usr/bin/python
import praw
import time
import datetime
import requests.packages.urllib3
import reply
from string import punctuation

requests.packages.urllib3.disable_warnings() # disables stupid warnings at the beginning

reddit = praw.Reddit('bot2') # reads bot info from praw.ini

# open list of comments/posts already processed
processed = [] 
with open("processed.txt", "r") as f:
    processed = f.read()
    processed = processed.split("\n")
    processed = list(filter(None, processed))


# open a list of comments already replied to
repliedto = []
with open("repliedto.txt", "r") as f :
    repliedto = f.read()
    repliedto = repliedto.split("\n")
    repliedto = list(filter(None, repliedto))
    

subreddit = reddit.subreddit("pewdiepiesubmissions+pewdiepie+pewdiepie_submissions+tseries") # the subreddits i want to draw from
comments = subreddit.stream.comments() # stream of comments from subrredits


def main() :
    
    # grab each individual comment
    for comment in comments :
        try :
            if comment.id not in processed and comment.link_id not in processed and comment.author.name.lower() != "pewdiesubbot": # check if comment has already been processed/is authored by the bot itself
                
                # process and format the text of the comment
                text = (comment.body).encode('utf-8').lower().split() 
                text = [''.join(c for c in s if c not in punctuation) for s in text]
                text = [s for s in text if s]
                
                # date + time of comment
                date = datetime.datetime.fromtimestamp(comment.created_utc) 
                dif = datetime.datetime.utcnow() - date
                
                # print relevant info
                print(str(date) + " by " + comment.author.name)
                print(text)
                print(" ")
                 
                # check if comment has PewDiePie/T-Series in it and comment if so
                if ("pewdiepie" in text or "tseries" in text) :
                    reply.commentreply(comment)
                    print("\n \n \n FOUND ONE!!! \n \n \n") # notify console that a match has been found
                    repliedto.append(comment.id) # append the comment to the list of comments replied to 
               
                processed.append(comment.id) # mark the comment as processed
                processed.append(comment.link_id)
               
        # catch exception where bot has commented too often too recently       
        except praw.exceptions.APIException: 
            print("\tSleeping for 10 minutes")
            time.sleep(600)
                    

if (__name__ == "__main__") :
    
    try :
        
        main() # run the bot!
        
    # catch keyboard interruptions or any errors during runtime
    except (Exception, KeyboardInterrupt) as e :
        
        # print the caught error
        print("ERROR!")
        print(e) 
       
        # quickly save all the processed files 
        with open('processed.txt', "w") as outfile:
            for comment in processed :
                outfile.write(comment + "\n")
        
        #quickly save all the replied files   
        with open('repliedto.txt', "w") as outfile:
            for comment in repliedto :
                outfile.write(comment + "\n")
                
        # exit cleanly
        exit(0)
        
    
    
    
    '''
for submission in subreddit.new(limit=5):
    print("Title: ", submission.title)
    print("Score: ", submission.score)
    print("---------------------------------\n")
'''