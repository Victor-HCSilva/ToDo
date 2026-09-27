from django.db import models
import smtplib
from logging import getLogger 
import os
from django.contrib.auth.models import User
from email.message import EmailMessage
from api.models import DispatchLog


logger = getLogger("__main__")


class SendEmail:
	server_type = os.getenv("SERVER_TYPE")
	port = os.getenv("EMAIL_PORT")
	link = os.getenv("LINK_PAGINA")
	email = os.getenv("TEST_EMAIL_FROM")
	password = os.getenv("EMAIL_PASSWORD")

	def __init__(self, to_user: User,content: str,title: str):
		self.to_user = to_user
		self.content = content
		self.title = title
		
	def _template(self, username: str, content: str):
		return f"""
		<div style="border 2px solid gray; background-color: azure;;">
		<h1 style="text-align: center;"> Olá, {username}!</h1>
			<div style="border 2px solid gray;">
				
				<p 
				style="
				text-align:center; 
				color: darkcyan;border: 1px; 
				padding: 0px; 
				margin: 0px;
				border: 1px solid gray;
				border-radius: 10px; background-color: #D1FFD1;">Sua notificação<p>

			<p style="color: #2b2d31; text-align: center;">
			{content}
			</p>
		<a style="color: green; border: 2px solid darkcyan; border-radius: 10px; text-align: center" href={self.link} target="_blank">Visite a página</a>	
		</div>	
	</div>
		"""

	def send(self):
		try:
			if not self.to_user.email or not self.email:
				raise("Algum erro ocorreu sobre emails") 

			from_ = self.email
			msg = EmailMessage()
			msg['Subject'] = self.title
			msg['From'] = from_
			msg['To'] = self.to_user.email 
			msg.set_content(
			    self._template(content=self.content, username=self.to_user.username), 
			    subtype='html'
			)

			with smtplib.SMTP(self.server_type, self.port) as smtp:
				smtp.starttls()
				smtp.login(from_, self.password)
				smtp.send_message(msg)

				obj = DispatchLog.objects.create(
						to=self.to_user,
						title=self.title,
						content=self.content
					)
				logger.info(f'E-mail de {from_} para {self.to_user.email} enviado com sucesso!')

		except Exception as e:
			logger.info(f"Erro ao enviar o email: {e}")
		


		 