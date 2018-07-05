# PerformanceTestFramework

Using this script you will be able to send a defined number of requests to a specific url with a specific method.
As output you will receive: the avg time for each request, the total time needed from the requests, the fastest and the slowest request.

### Prerequisites

In order to use this file you will need:

A version of Python installed, that you will find at the link below
```
https://www.python.org/downloads/
```
The HTTP library for python Requests, that you will find at the link below
```
https://www.python.org/downloads/

```

### Installing

Once the zip has been downloaded or the repository has been cloned you will be ready to start using the command
```
py ptf.py
```
or
```
python ptf.py
```

### General Explanation
In order to start the program you have to run the file "ptf.py".

The idea is:
  - take an URL (http:// + domain + endpoint)
  - take the chosen method 
  - send a defined number of requests using the url and the selected method 

Every time a request is sent the program will print the time needed to complete the request (microseconds) and the status (2xx,3xx...) of the request.
At the end,  the output on screen will be:
a recap of the URL and the  used method
the number of requests
the time needed to complete all the requests (without the delay time)
the average time
the fastest and slowest time 

At that point, it will be asked if you want to continue with new requests or not.

### More information
The program can obtain the domain, the endpoint and the method by user's input or modifying the variables at the start of the script. The variable will be named domain, endpoint, method.

In case the selected method will be “DELETE” the program will warn the user about the possibility to delete the resource if allowed, and he will be asked to confirm the will to continue or not.

After set the URL and the method, the program will send a test request to know which status will be expected in the following requests (at least in theory).

In case the status will be an error status, the program will ask the user if he wants to continue anyway or restart the program. The URL and method will be showed in order to allow the user to check for possible errors in the input.

At the end, the program will ask the user if he want a delay between each request and after that he will be asked to insert the number of requests the user wants to send.
