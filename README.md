# cabsploit

<h1>This is a pentesting tool. "CABSPLOIT"</h1>

this tools allows you to scan for devices and
to put yourself in the middle of the connection between router and a device in the same network.
after that you can sniff their network traffic and alter it but it doesnot work for hsts or https sites
this tool is made for linux so some libraries and functionalities may not be available for windows users.

it uses scapy to send false ARP (adress resolution packets).
This basically tricks the router to think that you are the victim device and tricks the victim device to think you're the router.
