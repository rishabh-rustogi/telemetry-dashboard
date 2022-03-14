import time
import pandas as pd
import psutil
import pickle


#initialize variables to get cpu usage percentage and ram usage percentage over time
timeCounter = 0
timeList = []
countCPUList = []
countRAMList = []
procList = []
start = time.time()
fileCPU = "CPUUsage.pkl"
fileRAM = "RAMUsage.pkl"

# Return top 5 process consuming most Memory
def processSortedByMemory():
    processList = []

    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dictinary to list
           processList.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    # Sort the list by virtual memory usage in reverse order
    processList = sorted(processList, key=lambda procObj: procObj['vms'], reverse=True)

    tempList = set()
    i = 0

    # Get top 5 unique processes
    while len(tempList) < 5:
        while True:
            if processList[i]['name'] + ": " + str(round((processList[i]['vms']*0.98/1000000),3)) + "GB" not in tempList:
                tempList.add(processList[i]['name'] + ": " + str(round((processList[i]['vms']*0.98/1000000),3)) + "GB")
                break
            i += 1
    
    # Return a comma seperated string of the processes with RAM usage
    return ", ".join(list(tempList))

#get cpu usage percentage every 0.5 secs and write the dataframe to fileCPU
#get RAM usage percentage every 0.5 secs, as well as the top 5 processes using the most RAM and write this dataframe to fileRAM
while True:
    if time.time() - start > 0.5:

        timeCounter += 1
        start = time.time()
        timeList.append(timeCounter*0.5)
        countCPUList.append(psutil.cpu_percent())
        countRAMList.append(((psutil.virtual_memory().total - psutil.virtual_memory().available)/psutil.virtual_memory().total)*100)
        procList.append(processSortedByMemory())
        dfCPU = pd.DataFrame(dict(
            timeList = timeList,
            countCPUList = countCPUList
        ))
        f = open(fileCPU,"wb")
        pickle.dump(dfCPU,f)
        f.close()

        dfRAM = pd.DataFrame(dict(
            timeList = timeList,
            countRAMList = countRAMList,
            processes = procList
        ))
        f = open(fileRAM,"wb")
        pickle.dump(dfRAM,f)
        f.close()

        if timeCounter > 175:
            countCPUList.pop(0)
            countRAMList.pop(0)
            procList.pop(0)
            timeList.pop(0)
