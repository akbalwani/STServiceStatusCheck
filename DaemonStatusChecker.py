import datetime
from email import message
from email.mime import multipart
import json
import multiprocessing
from multiprocessing.resource_sharer import stop
import os
import requests
import ssl
import string
import sys

from requests_toolbelt.multipart import decoder

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

import testsmtp
import testsmtp_multipart



receiver_email = "arpit.balwani@state.co.us"
# receiver_email = "arpitbalwani.ab@gmail.com"
message =[]


def writeLog(logString, severity):
    # This is the logfile for our python script
    global logFile
    # print( logString)


    tstamp = datetime.datetime.now()
    if severity == 'SUCCESS':
        inString = str(tstamp) + ' ' +  severity + '     ' + logString + '\n'
    elif severity == 'WARNING':
        inString = str(tstamp) + ' ' +  severity + '     ' + logString + '\n'
    elif severity == 'INFO':
        inString = str(tstamp) + ' ' +  severity + '     ' + logString + '\n'
    else:
        inString = str(tstamp) + ' ' +  severity + ' ' + logString + '\n'
    try:
        fHandle = open(logFile,'a+')
        fHandle.write(inString)
        fHandle.close()
    except:
        print( 'Problem writing to log' )
        return

    return




def getServerDaemonsStatus(basicAuth, stUrl, protocol):

    global referer
    global stTimeout
    
    # url = stUrl + 'servers?fields=isActive&protocol=' + protocol
    # print(url)
    # url = 'https://10.17.43.102:444/api/v2.0/servers?protocol=http&isActive=true'
    # print(url)
    # url = stUrl + 'daemons'
    authString = 'Basic ' + basicAuth
    headers = {'Referer': referer,
              'Accept': 'application/json',
              'Authorization': authString}    

    try:
        response = sessionMgt.get(stUrl, headers=headers, verify=False, timeout=stTimeout)
    except requests.ConnectionError as ec:
        writeLog('I cannot connect to ' + stUrl,'FATAL')
        writeLog(str(ec),'FATAL')
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        writeLog('HTTP Error','FATAL')
        raise SystemExit(eh)
    except requests.exceptions.Timeout as et:
        writeLog('Timeout Error:' + str(et), 'FATAL')
        raise SystemExit(et)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        writeLog(f'Get Daemon Status for {protocol}','SUCCESS')
        # print( response.status_code )
        # print( response.json())
        jsonResponse = response.json()
        dStatus = jsonResponse["result"]
        
        daemonRunning = False
        for item in dStatus:
            protocol = item.get("protocol")
            status = item.get("isActive")   
            if status:
                t = protocol + ' is still running'
                # print(t)
                daemonRunning = True



        
        return daemonRunning

def getTmStatus(basicAuth, stUrl):
    tm_running = False
    authString = 'Basic ' + basicAuth
    headers = {'Referer': referer,
              'Accept': 'application/json',
              'Authorization': authString}  
    
    try:
        response = sessionMgt.get(stUrl, headers=headers, verify=False, timeout=stTimeout)
    except requests.ConnectionError as ec:
        writeLog('I cannot connect to ' + stUrl,'FATAL')
        writeLog(str(ec),'FATAL')
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        writeLog('HTTP Error','FATAL')
        raise SystemExit(eh)
    except requests.exceptions.Timeout as et:
        writeLog('Timeout Error:' + str(et), 'FATAL')
        raise SystemExit(et)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        writeLog(f'Get Daemon Status for TM','SUCCESS')
        # print( response.status_code )
        # print( response.json())
        jsonResponse = response.json()
        # print(jsonResponse["status"])
        if(jsonResponse["status"] == "Running."):
            tm_running = True
            
        
    return tm_running


stTimeout = 120

logFile='C:\\PSO\\PSOPROJECTS\\STATE_OF_COLORADO\\DaemonStatus\\run\\script-logs.log'
referer = 'somebody'
# stUrl = 'https://10.128.133.207:444/api/v2.0/'
# stUrl='https://10.17.43.102:444/api/2.0/'
stHost= "10.17.43.102"
# stHost= "st-lab"
stPort="444"

# basicAuth = 'YWRtaW46YWRtaW4=' # from echo -n user:pass | base6
basicAuth= 'YWEwMDIzNTk6QXh3YXlAMTAwMQ=='
# basicAuth='YWRtaW46YWRtaW4='
pkeyfile = 'exportedPrivateKey'

sessionMgt = requests.Session()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


protocols = ["ssh", "ftp", "http", "pesit", "as2", "tm"]

for prot in protocols: 
    if prot != "tm":
        stUrl = f'https://{stHost}:{stPort}/api/v2.0/servers?protocol={prot}&isActive=true'
        if getServerDaemonsStatus(basicAuth,stUrl, prot):
            print(f'{prot} is running')
            message.append(prot)
        else:
            print(f'{prot} is not running')
    else:
        stUrl = f'https://{stHost}:{stPort}/api/v2.0/transactionManager'
        if getTmStatus(basicAuth,stUrl):
            print(f'{prot} is running')
            message.append(prot)



print(len(message))
print(message)
writeLog(f'Services : {message} are running','INFO')
#At a time SOC have ssh , ftp and http running in addition to TM service so total 4 , if the count is lower, notify
if len(message)<4:
    #implement send mail here
    # testsmtp.send_email(receiver_email,' '.join(message))'
    testsmtp_multipart.send_mail(receiver_email,message)
    writeLog(f'email sent successfully to {receiver_email}, because less than 4 services active : {message}','SUCCESS')
else:
    # testsmtp.send_email(receiver_email,' '.join(message))
    # testsmtp_multipart.send_mail(receiver_email,message)
    writeLog(f'All Services Running Fine , no mails triggered :)','SUCCESS')


