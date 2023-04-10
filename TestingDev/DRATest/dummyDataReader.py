#Read a file called DummyData.txt
#EAch line in file has format timestamp:value
#Find max and min timestamps which are in microseconds
maxTime = 0
minTime = 10000000000000000
linesNum = 0
timestamps = set()
duplicates = 0
with open("./DummyData5.txt", "r") as f:
  lines = f.readlines()
  linesNum = len(lines)
  for l in lines:
    time = int(l.split(":")[0])
    if time in timestamps:
      duplicates += 1
    else:
      timestamps.add(time)
    if time > maxTime:
      maxTime = time
    if time < minTime:
      minTime = time
print("Max time: " + str(maxTime))
print("Min time: " + str(minTime))
#Calculate how many lines were read in 1 sec
totalTime = maxTime - minTime
#Convert to seconds
totalTime = totalTime / 1000000
print("Total time: " + str(totalTime))
#Frequecy of data
print("Duplicates: " + str(duplicates))
print("Frequency: " + str((linesNum-duplicates) / totalTime))
