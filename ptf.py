'''
    Performance Test Framework

    Using this script you will be able to send a defined number of requests
    to a specific url with a specific method.
    As output you will receive:
        the avg time for each request,
        the total time needed from the requests
        the fastest and the slowest request
'''

''' libraryes import'''
import requests
import time
from threading import Thread
import threading

'''max number of parallel threads'''
threadLimiter = threading.BoundedSemaphore(5)

domain = "_INSERT_DOMAIN_HERE_"
endpoint = "_INSERT_ENDPOINT_HERE_"
method = "_INSERT_METHOD_HERE_"



''' THREAD CLASS ===============================================================================================
    A new Thread is create every time the program need to send a new request
    in this wai all the request wil be sended in a different thread
'''
class MyThread(Thread):
    def __init__(self, val, url, delay):
        Thread.__init__(self)
        self.val = val
        self.url = url
        self.delay = delay

    def run(self):
        time.sleep(self.delay)

    def send(self):
        threadLimiter.acquire()
        ''' We will try to:
            crete a session, prepare the request and send it over the session.
            We will print the microseconds between the request and the response(delta time)
            and return it in order to compute the average time
        '''
        try:
            sess = requests.Session()
            req = requests.Request(method, url)
            prepared = req.prepare()
            resp = sess.send(prepared)
            print("Request #" + str(self.val) + " - Time: " + str(
                resp.elapsed.microseconds) + " μs" + " - Status: " + str(resp.status_code))

            return int(resp.elapsed.microseconds)

        finally:
            threadLimiter.release()


''' METHOD INPUT FUNCTION ===========================================================================================
    Function for the input of the method.
    In case of not valid input the function will be recursive
'''


def MethodInput(inMethod):

    if (not inMethod) or (inMethod == "_INSERT_METHOD_HERE_"):
        inMethod = input("Insert the method you want to use in the requests: ")

    # check formatting
    inMethod = inMethod.upper().replace(" ", "")

    # check if it is a valid method
    if inMethod in ("GET", "POST", "HEAD", "PUT", "OPTIONS", "DELETE"):
        print("The Method inserted is valid and it is: " + inMethod)
        # ask to continue in case the method is DELETE
        if inMethod == "DELETE":
            print("The DELETE method could delete the requested file.")
            checkDel = input("Insert YES to continue: ")
            if checkDel.upper() != "YES":
                print("You did not insert YES")
                print("Return at the start of the Method Input")
                print(" ")
                return MethodInput("")
    else:
        print("The value inserted is not valid.")
        print("Return at the start of the Method Input")
        return MethodInput("")

    return inMethod


''' DELAY INPUT FUNCTION ===========================================================================================
    Function for the input of the delay.
    The dalay will be in second.
    In case of not valid input the function will be recursive
'''
def DelayInput():
    print(" ")
    print("How much delay do you want between each request?")
    try:
        inDelay = float(input("Insert the second do you prefer: (0 is no delay) "))
        return inDelay
    except:
        print("the value inserted is not valid.")
        return DelayInput()


''' NUMBER OF REQUEST INPUT FUNCTION ===========================================================================================
    Function for the input of how many request the program will send.
    In case of not valid input the function will be recursive
'''
def NRequestInput():
    print(" ")
    print(" ")
    try:
        InNReq = int(input("How many requests do you want to send?"))
        return InNReq
    except:
        print("The value is not allowed")
        return NRequestInput()


''' DOMAIN FORMATTING '''
def FormatDomain(inDomain):
    inDomain = inDomain.replace("/", "").replace(" ", "")

    return inDomain


''' ENDPOINT FORMATTING '''
def FormatEndpoint(inEndpoint):

    inEndpoint = inEndpoint.replace(" ", "")
    # add the / if there isn't yet
    if inEndpoint[0] != "/":
        inEndpoint = "/" + inEndpoint

    return inEndpoint


# end of the definitions =============================================================================================

url = ""
while True:

    ''' check if the domain is not set yet or it needs to be inserted '''
    if (not domain) or (domain == "_INSERT_DOMAIN_HERE_"):
        print(" ")
        domain = input("Insert the domain to use in the requests: ")
    # formatting check
    domain = FormatDomain(domain)

    ''' check if the endpoint is not set yet or it needs to be inserted '''
    if (not endpoint) or (endpoint == "_INSERT_ENDPOINT_HERE_"):
        print(" ")
        endpoint = input("Insert the endpoint to use in the requests: ")
    # check string formatting
    endpoint = FormatEndpoint(endpoint)

    '''define the url that will be used for the requests'''
    url = "http://" + domain + endpoint
    print(" ")
    print("URL used ---> " + url)

    '''choose the method to use in the request '''
    method = MethodInput(method)

    '''Check the connection once to know the server response ================================================='''
    ''' As in the Thread, we will try to:
        crete a session, prepare the request and send it over the session.
        We will print the microseconds between the request and the response(delta time)
        and return it in order to compute the average time  '''
    print(" ")
    print("Sending a test Request")
    s = requests.Session()
    req = requests.Request(method, url)
    prepped = req.prepare()
    resp = s.send(prepped)

    if resp.status_code / 100 >= 4:
        print("There is an error in the request -> Error:" + str(resp.status_code))
        print("URL used: " + url + " - Method used: " + method)
        checkContinue = input("Do you want to proceed anyway? (Y/N) ").upper()
        if checkContinue != "Y":
            print("Restarting the program and all variables...")
            domain = endpoint = method = ""
            continue
    else:
        print("Status:" + str(resp.status_code))


    ''' check if the user want to add a delay between each request '''
    delay = DelayInput()

    '''ask the user hoy many request he want to send ========================================'''
    nReq = NRequestInput()

    '''variables used in the while loop and to show the avg time'''
    print(" ")
    # index for the loop
    i = 0
    # total of the time of each requests
    sum = 0
    # returned time of the request
    temp = 0
    # variable for the longest and shortest time
    # at the start they are  set to 0
    minTime = maxTime = 0
    # threads array
    threads = []

    ''' 
        Start of the loop ===========================================================================================
        The program will create thread and send request until the number is lesser than nReq.
        Then add to the total time the rime of the last thread.
        After that, check if that time is longer or shorter than the other's time.
        At the end check if the user set a delay between each request,
        it is made waiting the end of the previous thread(join()).    '''
    while i < int(nReq):
        # create the i-th thread
        threads.append(MyThread(i, url, delay))
        threads[i].start()
        temp = threads[i].send()

        # add the time to total and check for max and min time
        sum += temp

        if minTime == 0:
            maxTime = temp
            minTime = temp
        elif temp > maxTime:
            maxTime = temp
        elif temp < minTime:
            minTime = temp

        # check for delay
        if int(delay) != 0:
            threads[i].join()
        i += 1

    '''formatting and print the result ==========================================================================='''
    print(" ")
    print(" ")
    print("*********************RESULT***********************************")
    print(" ")
    print("URL used: " + url + " - Method used: " + method)
    print("Number of requests: " + str(len(threads)))
    print("Total time took from the requests is: " + str(format(sum / 1000, ".3f")) + " ms")
    print(" ")
    sum /= (int(nReq) * 1000)
    print("The average time for each request is: " + str(format(sum, ".3f")) + " ms")
    print(" ")
    print("Slowest Request took " + str(maxTime / 1000) + " mSeconds.")
    print("Fastest Request took " + str(minTime / 1000) + " mSeconds.")


    '''Ask for continue or not the program'''
    print(" ")
    checkEnd = input("Do you want to send any other request? (Y/N) ").upper()
    if checkEnd == "N":
        print("Closing the program...")
        break
    else:
        print("Do you want to use the previous domain, endpoint and method?")
        checkForChange = input("You will insert every variable. (Y/N) ").upper()
        if checkForChange == "N":
            domain = endpoint = method = ""

