import time 

def intro():
    for i in range(15):
        print("\n")
        time.sleep(.10)
    with open("banner.txt", 'r') as fin:
        print(fin.read())