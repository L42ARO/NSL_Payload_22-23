import matplotlib.pyplot as plt

# Open the file for reading
with open("data.txt", "r", encoding='UTF-16') as f:
    # Read all lines in the file and remove the last three lines
    lines = f.readlines()[:-3]
# Convert each line to a number and store ink a list
numbers = []
for line in lines:
    if line=='\n':
        pass
    line = line.rstrip('\n')  # Remove newline and whitespace characters
    #print(line)
    try:
        number=int(line)
        numbers.append(number)
        
    except ValueError:
        # Ignore lines that cannot be converted to a float
        #print(line)
        pass

# Plot the numbers on a graph
plt.plot(numbers)
plt.show()