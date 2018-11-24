# This module will perform simple sentiment analysis on Twitter data
# This was created by Donna Xue, 251025215

# compute_tweets shall be the main function that uses the sub-functions under it
def compute_tweets(tweetsFile, keywordsFile):
    # validate the files from user input
    # keywords is the entire text file for keywords
    keywords = checkFile(keywordsFile)
    # dictionaryKeywords formats the data into a dictionary structure
    dictionaryKeywords = readKeywords(keywords)

    keywords.close()        # close the file

    # tweets is the entire text file of the tweets
    tweets = checkFile(tweetsFile)
    # process tweets by calculating happiness score
    processedTweets = processTweets(dictionaryKeywords, tweets)

    tweets.close()      # close the file

    # store the tweet information according to each timezone
    pacificList = processedTweets[0]
    mountainList = processedTweets[1]
    centralList = processedTweets[2]
    easternList = processedTweets[3]

    # calculate and store happiness of each timezone
    pacificSentiment = timezoneSentiment(pacificList)
    mountainSentiment = timezoneSentiment(mountainList)
    centralSentiment = timezoneSentiment(centralList)
    easternSentiment = timezoneSentiment(easternList)


    # return  list of tuples in order of Eastern , Central, Mountain, Pacific with (average, count)
    return [(easternSentiment, len(easternList)), (centralSentiment, len(centralList)), (mountainSentiment, len(mountainList)),
                                                                    (pacificSentiment, len(pacificList))]

# First, check the file to make sure there is a ".txt" with parameter fileName being the name of entered file
def checkFile(fileName):
    try:
        if ".txt" not in fileName:
            fileName = fileName + ".txt"    # adds .txt if not already included
        inputData = open(fileName, "r", encoding="utf-8")      # opens the file and avoid encoding errors
        return inputData
    # if the file does not exist, the program raises an exception
    except IOError:
        print("Error: file not found")
        emptyList = []
        return emptyList        # return an empty list with the generated exception


# Second, store keywords and associated values into a dictionary structure
def readKeywords(file):     # the parameter "file" is the data from the keywords file
    dictionary = {}         # create an empty dictionary for keywords and values to prepare
    for line in file:       # reading each line
        if line != "":
            line = line.rstrip()        # strip the /n from the end of the line
            seperate = line.split(",")     # split the line into keyword and sentiment value
            keyword = seperate[0]
            value = int(seperate[1])
            dictionary[keyword] = value
    return dictionary


# Third, process tweet data location by formatting and storing the coordinates
def formatCoordinate(x,y):
    formattedCoordinate = []
    formattedCoordinate.append(float(x))
    formattedCoordinate.append(float(y))
    return formattedCoordinate


# Fourth, figure out which timezone the tweet originated from
def determineTimezone(coordinate):
    x = coordinate[0]
    y = coordinate[1]

    yMin = -125.24226
    yMax = -67.444574
    xMin = 24.660845
    xMax = 49.189787
    # use yMax of each region to determine coordinate location as xMax repeats for various zones
    easternYMax = -67.444574
    centralYMax = -87.518395
    mountainYMax = -101.998892
    pacificYMax = -115.236428
    # check to see if the given coordinates are indeed within the max and min ranges
    if (x > xMin and x < xMax) and (y > yMin and y < yMax) :
        if y < pacificYMax :
            return "Pacific"
        elif y < mountainYMax :
            return "Mountain"
        elif y < centralYMax :
            return "Central"
        elif y < easternYMax :
            return "Eastern"


# Fifth, calculate the happiness of the tweet
# parameters are the keywords in dictionary structure and the tweet text
def calculateSentiment(dictionaryKeywords, tweetText):
    sentimentValue = 0
    keywordCount = 0
    if tweetText != "" :    # make sure the tweet is not empty
        tweetWords = tweetText.split()      # split tweet into individual words
        for word in tweetWords:
            word = word.lower()     # formats into lowercase
            for char in word:
                if not char.isalpha():
                    word = word.replace(char, "")   # clears punctuation
            for keyword in dictionaryKeywords:
                if word == keyword:
                    keywordValue = dictionaryKeywords[keyword]     # keyword sentiment value
                    sentimentValue = sentimentValue + keywordValue      # add keyword value to sentiment value of tweet
                    keywordCount = keywordCount + 1     # running count of the keyword count in the tweet

    if keywordCount > 0 :        # makes sure there were actual keywords in the tweet
        sentimentScore = sentimentValue / keywordCount     # calculates the happiness score
        return sentimentScore       # returns the happiness score
    else:
        return 0        # if there were no keywords found, the function returns 0


# Sixth, process tweets and append sentiment values to timezone lists
# parameter "dictionary" is keywords and values and "tweetFile" is the the tweet file
def processTweets(dictionaryKeywords, tweetFile):
    # empty list for each timezone to prepare
    pacificList = []
    mountainList = []
    centralList = []
    easternList = []

    for line in tweetFile:
        if line != "":
            line = line.rstrip()     # removes the "/n" at the front of the line
            line = line.lstrip("[")     # cannot just use line.strip() because some lines are continuations of a previous tweet)
            # format the coordinates from the tweet
            dataList1 = line.split("] ")       # split for the coordinate data

            coordinatePart = dataList1[0].split(", ")     # split for the two portions of coordinates
            coordinates = formatCoordinate(coordinatePart[0], coordinatePart[1])    # the x and y values in the coordinate
            timezone = determineTimezone(coordinates)

            dataList2 = dataList1[1].split(" ")      # split remaining tweet info into the 4 sections
            tweetText = dataList2[3]        # store tweet text into variable
            sentimentScore = calculateSentiment(dictionaryKeywords,tweetText)   # calculate happiness value of tweet
            if sentimentScore != 0 :    # make sure there are keywords existent in tweet
                if timezone == "Pacific":
                    pacificList.append(sentimentScore)
                elif timezone == "Mountain":
                    mountainList.append(sentimentScore)
                elif timezone == "Central":
                    centralList.append(sentimentScore)
                elif timezone == "Eastern":
                    easternList.append(sentimentScore)

    return [easternList, centralList, mountainList, pacificList]    # multi-dimensional list with sentiment scores for each zone


# Seventh, calculate the happiness of each time zone
def timezoneSentiment(listSentimentScores) :
    sum = 0
    sentimentSum = 0
    for value in listSentimentScores:
        if len(listSentimentScores) > 0:
            sum = sum + value
            sentimentSum = sum / len(listSentimentScores)
    return sentimentSum

# refer to compute_tweets function as main function
