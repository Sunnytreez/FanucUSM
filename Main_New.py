from time import sleep
import pandas as pd
from openpyxl import load_workbook
import socket
import os
import subprocess

def host_set():
    setup=input("Set New IP Address? Y/else:")
    if setup=="Y" or setup=="y":
        subprocess.call("main2.py", shell=True)
        with open('host.txt', 'r') as f:
            HOST = f.read().strip()
            print(f"HOST environment variable: {HOST}")
    
    else:
            HOST ='192.168.1.10'
    print(f"Using HOST: {HOST}")
    return HOST
    
def read_excel(sheet_name, pdnum):
    df = pd.read_excel('data.xlsx', sheet_name=sheet_name)
    return df.iat[2, pdnum], df

def server_connect(HOST,PORT):
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect((HOST, PORT))
    return Client

def send_data(Client, data):
    Client.send(data.encode())
    received_data = Client.recv(10)
    return received_data.decode()

def main():
    
    PORT = 59002
    totalnumber=input("Total Number of parts to pick:")
    pdnum=1
    setup=input("Set New IP Address? Y/else:")
    if setup=="Y" or setup=="y":
        HOST = host_set()
        print(f"Final HOST: {HOST}")
    else:
        HOST ='192.168.1.10'
        print(f"Using HOST: {HOST}")
        sleep(4)
    i=0    
    while True:
        try:
            
            client = server_connect(HOST,PORT)
            value, df = read_excel("sheet1", pdnum)
            client=server_connect(HOST,PORT)
            print("Try loop", i, "PDNUM", pdnum)
            for i in range(21):
                positionaldata = str(df.iat[i, pdnum]).ljust(10)
                print(positionaldata)
                received_data = send_data(client, positionaldata)
                print(f"Received: {received_data}")
        except Exception as e:
            print("Waitng to connect", {e})
            if i==20:
                pdnum=pdnum+1
                print(f"PDNUM incremented to {pdnum}")
                i=0
         #   sleep(.25)
            else:
                print("Col not incremented waiting on robot data request")
            pass
        #print(f"socket error: {e}")
        
        finally:
            sleep(10)
            if i==20:
                client.close()
            else:
                print("restart program and wait for request again", "i=", i )
if __name__ == "__main__":
    main()
                    