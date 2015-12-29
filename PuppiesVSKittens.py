import time
import datetime
import praw
import os

# The RPi/Python/LED interface
# import RPi.GPIO as GPIO ## Import GPIO library
# GPIO.setmode(GPIO.BOARD) ## Use board pin numbering

thingGroupA = red = ['puppies', 'puppy', 'dog']
thingGroupB = green = ['kittens', 'kitty', 'cat']

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

    if not 'totalThingsCounts' in locals(): 
        totalThingsCounts = {thingGroups[i]:0 for i in range(0,len(thingGroups))}
        
    r = praw.Reddit('Term tracker by u/mechanicalreddit') # Change 'yourname' to your Reddit username

    try:
        # Rough estimates suggest that there are around 20 new comments per second
        allComments = r.get_comments('all', limit=1000) # The maximum number of comments that can be fetched at a time is 1000
        
    except:
        print("Something didn't work right in fetching the comments")
    
    else:
        commentDetails = [comment for comment in allComments]

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

        if (sumOfThings == 0): sumOfThings = 1 # Temporarily deal with cases where there are no things
        redIntensity = sumThingGroupA/sumOfThings
        greenIntensity = sumThingGroupB/sumOfThings

        # Reset the counts at midnight
        if previousHour > datetime.datetime.now().hour:
            sumThingGroupA = sumThingGroupB = redIntensity = greenIntensity = 0
            totalThingsCounts = {thingGroups[i]:0 for i in range(0,len(thingGroups))}

    # Lighting management
    # GPIO.setup(12, GPIO.OUT) ## Setup GPIO pin 12 to OUT
    # GPIO.output(12,True) ## Turn on GPIO pin 12

    # p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
    # p.start(0)

    
    # Temporary loop management
    i += 1
    print('Working')
    print('sumThingGroupA (Dogs): ' + str(sumThingGroupA))
    print('sumThingGroupB (Cats): ' + str(sumThingGroupB))
    print('totalThingsCounts: ' + str(totalThingsCounts))
    time.sleep(120)
    
print('All done!')
print(totalThingsCounts)





