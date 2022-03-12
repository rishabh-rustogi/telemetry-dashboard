from kafka import KafkaConsumer
import time
import pickle
import pandas as pd

consumer = KafkaConsumer(
    'movielog3',
    bootstrap_servers=['localhost:9092']
    # Read from the start of the topic; Default is latest
    # auto_offset_reset='earliest'
)

userSet = set()
countRecurrUsers = 0
total = 0 
countRecurrList = []
timeList = []
timeCounter = 0
timeInterval = 180
start = time.time()


fileRecurrUser = "RecurrUser.pkl"

for message in consumer:

    if 'recommendation' in message.value.decode('UTF-8'):
        user = message.value.decode('UTF-8').split(',')[1]
        total += 1
        if user in userSet:
            countRecurrUsers += 1
        userSet.add(user)
    
    if time.time() - start > timeInterval:
        timeCounter += 1
        start = time.time()
        timeList.append(timeCounter*timeInterval)
        countRecurrList.append((countRecurrUsers/total)*100)
        
        countRecurrUsers = 0
        total = 0

        dfUserRecurr = pd.DataFrame(dict(
            x = timeList,
            y = countRecurrList
        ))

        f = open(fileRecurrUser,"wb")
        pickle.dump(dfUserRecurr,f)
        f.close()


        


        
