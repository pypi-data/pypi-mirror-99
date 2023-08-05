import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from odoo.addons.sm_maintenance.models.models_load_data import load_data


class Mail_service:
  __instance = None

  @staticmethod
  def getInstance():
    if Mail_service.__instance is None:
      Mail_service()
    return Mail_service.__instance

  def __init__(self):
    if Mail_service.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      Mail_service.__instance = self

    server_configuration = self.get_server_from_loaded_data()
    self.server = smtplib.SMTP(server_configuration)
    self.user_data = load_data.get_instance().get_email_info()

  def get_server_from_loaded_data(self):
    server_data = load_data.get_instance().get_server_info()
    return str(server_data['smtp']) + ": " + str(server_data['port'])

  def send_email(self, subject, body):
    msg = MIMEMultipart()

    msg['From'] = "admin@sommobilitat.coop"
    msg['To'] = "admin@sommobilitat.coop"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    self.open_connexion()
    self.login()
    self.prepare_to_send(msg)
    self.close_connexion()

  def login(self):
    address = str(self.user_data['address'])
    password = str(self.user_data['password'])

    self.server.login(address, password)

  def prepare_to_send(self, msg):
    self.server.sendmail(msg['From'], msg['To'], msg.as_string())

  def open_connexion(self):
    self.server.starttls()

  def close_connexion(self):
    self.server.quit()
