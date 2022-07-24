import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import ssl

class Messaging:
	def __init__(self,username,password,to_mail,subject,text):
		"""
		This is a class to send emails. It can be used from other
		scripts very easily.

		username: The email of the sender
		password: Either the password of the sender or an app password token
		to_mail: Email of the recipient. This script can only send a msg
		to one person, so the parameter must be a string. It can be a list
		subject: subject of the email
		text: body of the email

		"""
		self.username=username
		self.password=password
		self.to_mail=to_mail
		self.subject=subject
		self.text=text
		self.all_mails=["@gmail.com","@outlook.com","@hotmail.com","@ymail.com","@googlemail.com",
		"@msn.com","@yahoo.com"]
		self.intermediate()

	def intermediate(self):	
		self.simple_counter=False
		msg=MIMEMultipart()
		msg["From"]=self.username
		msg["To"]=self.to_mail
		msg["Subject"]=self.subject
		msg.attach(MIMEText(self.text,"plain"))
		self.texto=msg.as_string()
		for i in self.to_mail:
			if i=="@":
				self.simple_counter=True

	def Send_it(self):	
		"""
		When called, sends the email once the class is instantiated
		"""
		print("Sending...")
		context = ssl.create_default_context()
		if self.simple_counter:
			try:
				server = smtplib.SMTP('smtp.gmail.com:587')
				server.ehlo()
				server.starttls()
				server.login(self.username,self.password)
				server.sendmail(self.username, self.to_mail, self.texto)

				print("Success! Message sent to {}\n\n".format(self.to_mail))
				return True
			except Exception as e:
				print("Error!")
				print(e,"\n\n")
				return False	
			finally:
				server.quit()	
		else:
			#if it falls in the else, it means the recipient address did not have
			#an @, so it will try to send it to everyone. For example if the reci-
			#pient was example, the email will be sent to example@gmail.com,
			#example@yahoo.com,example@outlook.com, etc if they exist.
			self.mails_counter=0
			try:
				for i in self.all_mails:
					server = smtplib.SMTP('smtp.gmail.com:587')
					server.ehlo()
					server.starttls()
					server.login(self.username,self.password)
					self.mails_counter+=1
					server.sendmail(self.username,"{}{}".format(self.to_mail,i), self.texto)
					
					print("Success! Message sent to {}{}\n\n".format(self.to_mail,i))
					return True
			except Exception as e:
				if self.mails_counter!=len(self.all_mails):
					pass
				else:	
					print("Error!")
					print(e,"\n\n")
					return False	
			finally:
				server.quit()		

if __name__=="__main__":				
	body="Testing script {}".format(__file__) #body of the msg

	username=os.environ["EMAIL_USER"] 
	#this line gets the value of the environment variable EMAIL_USER

	password=os.environ["EMAIL_TOKEN"]
	#this line gets the value of the environment variable which stores
	#a token to the email of the sender, it could also be a password
	#but it will likely have issues with less secure apps if gmail is
	#used

	msg=Messaging(username=username,password=password,to_mail=username,
	subject="This is a test",text=body)

	msg.Send_it()
