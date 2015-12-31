import time
import datetime
import praw
import os


## Useful resources
# https://learn.sparkfun.com/tutorials/resistors/example-applications
# https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds
# https://en.wikipedia.org/wiki/LED

# The RPi/Python/LED interface
import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BCM) ## Use internal pin numbering

# Initialize LEDs
# Green light
GPIO.setup(22, GPIO.OUT) ## Setup GPIO pin 25 to OUT

# Initialize Pulse width modulation on GPIO 25. Frequency=100Hz and OFF
pG = GPIO.PWM(22, 100)
pG.start(0)

# Red light
GPIO.setup(25, GPIO.OUT) ## Setup GPIO pin 22 to OUT

# Initialize Pulse width modulation on GPIO 22. Frequency=100Hz and OFF
pR = GPIO.PWM(25, 100)
pR.start(0)

# Test light dimming and relative brightnesses
# testLights = True
#
# if testLights == True:
#     i = 0
#     while True:
#         try:
#             if (i == 100): direction = -1
#             if (i == 1): direction = 1
#             pR.ChangeDutyCycle(i*.2)
#             pG.ChangeDutyCycle(100-i)
#             i += direction
#             time.sleep(.2)
# 
#         except KeyboardInterrupt:
#             pG.stop()
#             pR.stop()
#             GPIO.cleanup()
#             quit()

    
    

# Assign terms to groups
thingGroupA = red = ['kittens', 'kitty', 'cat']
thingGroupB = green = ['puppies', 'puppy', 'dog']

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

            # Determine the relative LED brightnesses based on the term frequencies
            redIntensity = (sumThingGroupA/sumOfThings) * 100
            greenIntensity = (sumThingGroupB/sumOfThings) * 100

            # Red appears brighter because of how it is percieved by the eye,
            # so decrease it to make the brightnesses seem more equal
            # https://learn.sparkfun.com/tutorials/light/visible-light
            # http://www.ledsmagazine.com/articles/print/volume-10/issue-6/features/understand-rgb-led-mixing-ratios-to-realize-optimal-color-in-signs-and-displays-magazine.html
            # http://www.gizmology.net/LEDs.htm
            # The differnece in level of brightness is more perceptable at lower levels.
            # Therefore, square the intensity to change the brightness distribution. 
            redIntensity = ((redIntensity**2)/10000) * 100 * .25
            greenIntensity = ((greenIntensity**2)/10000) * 100

            # Reset the counts at midnight
            if 'previousHour' in locals():
                if previousHour > datetime.datetime.now().hour:
                    sumThingGroupA = sumThingGroupB = redIntensity = greenIntensity = 0
                    totalThingsCounts = {thingGroups[i]:0 for i in range(0,len(thingGroups))}
                    previousHour = datetime.datetime.now().hour
                    
                else:
                    previousHour = datetime.datetime.now().hour
            else:
                previousHour = datetime.datetime.now().hour
       

        # Update lighting
        pG.ChangeDutyCycle(greenIntensity)
        pR.ChangeDutyCycle(redIntensity)

        
        # Temporary loop management
        print('sumThingGroupA (Cats): ' + str(sumThingGroupA))
        print('sumThingGroupB (Dogs): ' + str(sumThingGroupB))
        print('totalThingsCounts: ' + str(totalThingsCounts))
        print('redIntensity: ' + str(redIntensity))
        print('greenIntensity: ' + str(greenIntensity))
        print('timeBoundary: ' + str(timeBoundary))
        print('previousHour: ' + str(previousHour))
        print('current hour: ' + str(datetime.datetime.now().hour))
        time.sleep(120)
        
    except KeyboardInterrupt:
        pG.stop()
        pR.stop()
        GPIO.cleanup()
        quit()





