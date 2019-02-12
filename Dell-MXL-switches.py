import paramiko
import time # For adding delays in the code
import sys
#import json

#for attaching the date to the file name : filename-Month-day-Year-Hours-minutes
timestr = time.strftime(" - %m-%d-%Y-%H-%M")
#print (timestr)

#logs to see if the authentication went through or not
#Use it only when you want to see the logs, say why the SSH conenction to the device fails
'''
import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
'''

#paramiko exceptions to handle at the end of the script
exceptions          =          (paramiko.ssh_exception.BadAuthenticationType, paramiko.ssh_exception.AuthenticationException,
                                paramiko.ssh_exception.NoValidConnectionsError, TimeoutError, ConnectionAbortedError,
                                paramiko.ssh_exception.SSHException)


# Read the switches IP info from the text file
with open ('Dell-MXL-switches.txt') as f:
    lines = f.read().splitlines()

#print (lines)

# *************** Code starts here **********************

#Admin credentials - DONOT * USE * THESE. Always use the service account credentials
#username = ''
#password = ''
#Update admin credentials to the latest one always

#Service Account credentials
username = ''
password = ''

for line in lines:
    #try: #exception handling; if one of the devices fail, the next ones will be executed in order.
    try:
        print ('~'*80)

        #calling the SSH client from Paramiko Library
        ssh_client = paramiko.SSHClient()

        #Accept the public key from the switch. Automatically add untrusted hosts (make sure okay for security policy in your environment)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=line, username=username, password=password)

        #print ('\n\n\t', ssh_client, '\n\t') #Connection Object
        print ('\n\t ***********  Successful connection to ***********\n\t\t\t\t', line)

        time.sleep(1)         #add delays in the script to get more control. This allows us to wait for a second before outputting the session info
        #Requests interactive shell session on this channel
        remote_connection = ssh_client.invoke_shell()
        time.sleep(2)
        remote_connection.send('en\n')
        remote_connection.send('<password>\n') #Enable password
        time.sleep(1)
        remote_connection.send('terminal length 0\n') #Disables Paging. Need not press space-bar/Enter for viewing the output.
        time.sleep(1)
        remote_connection.send('show running-config\n')
        time.sleep(1)

        # Print the output of the session
        if remote_connection.recv_ready():
            output = remote_connection.recv(65534)
        #print(output)
        time.sleep(1)

        # Flush the interactive shell output to the buffer
        sys.stdout.flush()

        line = line + timestr
        # Open a file and write the output to it
        with open(line+'.txt', 'wb') as write_output:
            write_output.write(output)

        #Close the file
        write_output.close

        #Close the SSH connection
        ssh_client.close
        #print (ssh_client.close)

        #Adding a second delay to the loop before moving onto the next iteration i.e., next switch
        time.sleep(1)

    except exceptions as e:
        print ('+-'*40)
        print ('Failed to connect to : ', line, '\nReason: ', e, '\n', '+-'*40)
