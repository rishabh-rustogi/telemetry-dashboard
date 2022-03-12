import time
import pandas as pd
import psutil
import pickle



timeCounter = 0
timeList = []
countCPUList = []
countRAMList = []
procList = []
start = time.time()
fileCPU = "CPUUsage.pkl"
fileRAM = "RAMUsage.pkl"

def processSortedByMemory():
    processList = []
    # Iterate over the list
    for proc in psutil.process_iter():

       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           processList.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    processList = sorted(processList, key=lambda procObj: procObj['vms'], reverse=True)
    #print(processList)
    tempList = set()
    i = 0
    while len(tempList) < 5:
        while True:
            if processList[i]['name'] + ": " + str(round((processList[i]['vms']*0.98/1000000),3)) + "GB" not in tempList:
                tempList.add(processList[i]['name'] + ": " + str(round((processList[i]['vms']*0.98/1000000),3)) + "GB")
                break
            i += 1
    return ",\n".join(list(tempList))

while True:
    if time.time() - start > 0.5:

        timeCounter += 1
        start = time.time()
        timeList.append(timeCounter*0.5)
        countCPUList.append(psutil.cpu_percent())
        countRAMList.append(((psutil.virtual_memory().total - psutil.virtual_memory().available)/psutil.virtual_memory().total)*100)
        procList.append(processSortedByMemory())
        dfCPU = pd.DataFrame(dict(
            x = timeList,
            y = countCPUList
        ))
        f = open(fileCPU,"wb")
        pickle.dump(dfCPU,f)
        f.close()

        dfRAM = pd.DataFrame(dict(
            x = timeList,
            y = countRAMList,
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