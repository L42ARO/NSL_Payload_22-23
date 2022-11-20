import random
print("Running emma")
with open('emma.txt', 'w') as f:
    f.write(str(random.randint(0, 100)))