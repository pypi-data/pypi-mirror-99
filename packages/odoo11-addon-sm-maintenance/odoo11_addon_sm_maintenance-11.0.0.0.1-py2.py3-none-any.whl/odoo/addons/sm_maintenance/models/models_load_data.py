# -*- coding: utf-8 -*-

import json
import os


class load_data(object):

  __instance = None

  data = None

  @staticmethod
  def get_instance():
    if load_data.__instance is None:
      load_data()
    return load_data.__instance

  def __init__(self):
    if load_data.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      load_data.__instance = self

  def tariffs_duration(self):
    loaded_data = {
      "welcome": int(os.getenv('SM_TARIFF_MONTH_DURATION_WELCOME')),
      "default": int(os.getenv('SM_TARIFF_MONTH_DURATION_DEFAULT')),
    }

    return loaded_data

  def batch_reservation(self):
    node_sommobilitat = 'sm_partago'
    loaded_data = self.get_batch_data(node_sommobilitat)
    return loaded_data

  def batch_payment(self):
    node_sm_partago = 'sommobilitat'
    loaded_data = self.get_batch_data(node_sm_partago)
    return loaded_data

  def get_batch_data(self, node_specific):
    return {
      'ordenant_name': os.getenv('SM_BATCH_GENERAL_ORDENANT_NAME'),
      'ordenant_address_1': os.getenv('SM_BATCH_GENERAL_ORDENANT_ADDRESS_1'),
      'ordenant_address_2': os.getenv('SM_BATCH_GENERAL_ORDENANT_ADDRESS_2'),
      'ordenant_bic': os.getenv('SM_BATCH_GENERAL_ORDENANT_BIC'),
      'ordenant_id': os.getenv('SM_BATCH_'+node_specific.upper()+'_ORDENANT_ID'),
      'ordenant_iban': os.getenv('SM_BATCH_'+node_specific.upper()+'_ORDENANT_IBAN'),
    }

  def get_user_config(self):
    return {
      'person_group': os.getenv('SM_USER_PERSON_GROUP'),
      'person_group_prepaiment': os.getenv('SM_USER_PERSON_PREPAIMENT'),
      'default_group_config': os.getenv('SM_USER_PERSON_DEFAULT_GROUP_CONFIG'),
      'person_billing_account': os.getenv('SM_USER_PERSON_BILLING_ACCOUNT'),
      'person_billing_account_blocked': os.getenv('SM_USER_PERSON_BILLING_ACCOUNT_BLOCKED'),
      'default_language': os.getenv('SM_USER_PERSON_DEFAULT_LANGUAGE'),
      'person_owner_group': os.getenv('SM_USER_PERSON_OWNER_GROUP'),
      'billing_account_group': os.getenv('SM_USER_BILLING_ACCOUNT_GROUP'),
      'billing_owner_group': os.getenv('SM_USER_BILLING_ACCOUNT_OWNER_GROUP'),
      'allowed_user_langs': {
        "es": os.getenv('SM_USER_ALLWED_USER_LANGS_ES'),
        "ca": os.getenv('SM_USER_ALLWED_USER_LANGS_CA'),
      }
    }

  def zip_api_info(self):
    return {
      'api_key': os.getenv('SM_ZIP_API_KEY')
    }

  def get_email_info(self):
    return {
      'user': os.getenv('SM_EMAIL_ERROR_REPORTS_MAIL_USER'),
      'password': os.getenv('SM_EMAIL_ERROR_REPORTS_MAIL_PASSWORD'),
    }

  def get_server_info(self):
    return {
      'smtp': os.getenv('SM_EMAIL_SERVER_SMTP'),
      'port': int(os.getenv('SM_EMAIL_SERVER_PORT')),
    }
  def get_config_timezone(self):
    return os.getenv('SM_TIMEZONE')

  def get_system_project_id(self):
    return int(os.getenv('SM_SYSTEM_PROJECT_ID'))
