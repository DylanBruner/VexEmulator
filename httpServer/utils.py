from urllib import request
from httpServer import classes

"""
GET / HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36\r\nAccept-Language: en-US\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-GPC: 1\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nAccept-Encoding: gzip, deflate, br\r\n\r\n
"""

def RequestCodeToMessage(code):
    if code == 200:
        return 'OK'
    elif code == 404:
        return 'Not Found'
    
    return ""

def DecodeRequest(data: bytes):
    resp = classes.Request()

    data = data.decode()

    resp.method = data.split('/')[0].strip()
    resp.url    = data.split('HTTP/')[0].split('GET ')[1].strip()

    for line in data.split('\n'):
        if ":" in line:
            headerName  = line.split(":")[0].strip()
            headerValue = line.split(":")[1].strip()
            resp.headers[headerName] = headerValue

    return resp

def DoesRequestMatchRoute(string1, string2) -> bool:
    """
    Check if each character in string1 is equal to string2, when it finds a < or > return if everything up to that point is equal 
    """
    SplitString1 = string1.split('/')
    SplitString2 = string2.split('/')

    matches = True
    try:
        for i in range(len(SplitString1)):
            if "<" in SplitString1[i] or ">" in SplitString1[i]:
                break
            elif SplitString1[i] == SplitString2[i]:
                pass
            else:
                matches = False
    except IndexError:
        matches = False
        
    return matches

def getArgsFromRequest(route: str, request: str) -> list:
    requestSplit = request.split('/')
    routeSplit = route.split('/')

    newRequest = ""
    
    for i in range(len(routeSplit)):
        if routeSplit[i] == requestSplit[i]:
            pass
        else:
            newRequest += '/' + requestSplit[i]

    newRequest = newRequest.split('/')
    if '' in newRequest:
        newRequest.remove('')

    return newRequest