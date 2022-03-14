from kafka import KafkaConsumer
import time
import pickle
import pandas as pd

consumer = KafkaConsumer(
    'movielogXXX',
    bootstrap_servers=['localhost:9092']
)

#initiate the variables for counting recurrent users over time
userSet = set()
countRecurrUsers = 0
total = 0 
countRecurrList = []
timeList = []
timeCounter = 0
timeInterval = 180
startTime = time.time()

#output file where data frame of recurrent users over time will be written to
fileRecurrUser = "RecurrUser.pkl"

#loop through every message received from the Kafka Stream
#Check if the message requests for a reccomendation
#If it does, check if the userID making the request exists in the userSet
#If he/she does, increment countRecurrUsers by 1
#Else add his/her userID to userSet
for message in consumer:

    if 'recommendation' in message.value.decode('UTF-8'):
        user = message.value.decode('UTF-8').split(',')[1]
        total += 1
        if user in userSet:
            countRecurrUsers += 1
        userSet.add(user)
    
    if time.time() - startTime > timeInterval:
        timeCounter += 1
        startTime = time.time()
        timeList.append(timeCounter*timeInterval)
        countRecurrList.append((countRecurrUsers/total)*100)
        
        countRecurrUsers = 0
        total = 0

        dfUserRecurr = pd.DataFrame(dict(
            timeList = timeList,
            countRecurrList = countRecurrList
        ))

        f = open(fileRecurrUser,"wb")
        pickle.dump(dfUserRecurr,f)
        f.close()


        


        
