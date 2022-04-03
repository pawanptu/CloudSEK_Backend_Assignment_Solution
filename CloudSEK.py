import threading
import requests
import sys
import os
import time

ipturl = str()
Word = str()
WordL = list()
errorC = list()
SCD = dict()

threads = []

def urlGenerator(inputS, word):
    return "https://" + inputS + "/" + word

def Broute_Force(url):
    global SCD
    try:
        response = requests.get(url)
        SCD[url] = int(response.status_code)
    except:
        print("URL error for : " + url)
        SCD[url] = 404

def inputP():
    try:
        global ipturl
        global WordF
        global errorC
        global WordL

        ipturl = sys.argv[1]
        WordF = sys.argv[2]

        for x in range(3, len(sys.argv)):
            errorC.append(int(sys.argv[x]))

        if not(os.path.isfile(WordF)):
            raise Exception("The input of word file does not exist or accessing from wrong location(path)")

        WordL = open(WordF, 'r').readlines()

        for x in range(len(WordL)):
            WordL[x] = WordL[x].strip()
    except Exception as e:
        print(e)
        sys.exit()


def actionHandler():
    global WordL
    global ipturl
    urls = []
    global SCD
    global threads

    for word in WordL:
        urls.append(urlGenerator(ipturl, word))

    for url in urls:
        threads.append(threading.Thread(
            target=Broute_Force, args=(url,)))

    for x in range(len(threads)):
        threads[x].start()


def outputGeneration():
    global SCD
    global errorC
    global threads

    for x in range(len(threads)):
        threads[x].join()

    file = open('ans.txt', 'w')

    print("Printing and writing require one in ans.txt file !")

    for key, value in SCD.items():
        print(key + " [Status code " + str(value) + "]" +"\n")
        if value in errorC:
            to_write = key + " [Status code " + str(value) + "]" + "\n"
            file.write(to_write)

    file.close()


if __name__ == "__main__":
    start_time = time.time()
    inputP()
    actionHandler()
    outputGeneration()
    print("%s sec" % (time.time() - start_time))
