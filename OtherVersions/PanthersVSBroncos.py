### This is based on the original PuppiesVSKittens.py, but adapted to not use
### the lights and not reset at midnight. 

import time
import datetime
import praw
import os

# Assign terms to groups
thingGroupA = ['Broncos']
thingGroupB = ['Panthers']

thingGroups = thingGroupA + thingGroupB 

def countAndSumThings(resultsSet, currentCounts):
    resultsSet = resultsSet.lower()
    for thing in currentCounts:
        thingLower = thing.lower()
        searchThing = ' '+thingLower+' '
        thingCount = resultsSet.count(searchThing)
        currentCounts[thing]+=thingCount
    return currentCounts

while True:

    try:
        if not 'totalThingsCounts' in locals(): 
            totalThingsCounts = {thingGroups[i]:0 for i in range(0,len(thingGroups))}

        try:
            r = praw.Reddit('Term tracker by u/mechanicalreddit') # Change 'yourname' to your Reddit username
            # Rough estimates suggest that there are around 20 new comments per second
            allComments = r.get_comments('all', limit=750) # The maximum number of comments that can be fetched at a time is 1000
            commentDetails = [comment for comment in allComments]
            
        except:
            print("Something didn't work right in fetching the comments")
        
        else:
            [print(comment.created) for comment in commentDetails[0:5]] 

            if 'timeBoundary' in locals(): # To prevent counting comments twice
                allCommentBodies = [str(comment.body) for comment in commentDetails if comment.created > timeBoundary]
                timeBoundary = commentDetails[0].created
                
            else:
                allCommentBodies = [str(comment.body) for comment in commentDetails]
                timeBoundary = commentDetails[0].created
                
            singleCommentCorpus = ' '.join(allCommentBodies)
            singleCommentCorpusCleaned = singleCommentCorpus.replace('\n',' ')
            
            totalThingsCounts=countAndSumThings(singleCommentCorpusCleaned, totalThingsCounts)

            sumThingGroupA = sum([totalThingsCounts[thing] for thing in thingGroupA])
            sumThingGroupB = sum([totalThingsCounts[thing] for thing in thingGroupB])

            sumOfThings = sumThingGroupA + sumThingGroupB

            if sumOfThings == 0:
                sumOfThings = 1 # Temporarily deal with cases where there are no things
        
        # Temporary loop management and output
        print('GroupA (Broncos): ' + str(sumThingGroupA))
        print('GroupB (Panthers): ' + str(sumThingGroupB))
        print('Total Counts: ' + str(totalThingsCounts))
        time.sleep(120)
        
    except KeyboardInterrupt:
        quit()





