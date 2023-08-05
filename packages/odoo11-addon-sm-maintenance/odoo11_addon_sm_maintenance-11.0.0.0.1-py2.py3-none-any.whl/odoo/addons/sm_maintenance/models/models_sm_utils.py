# -*- coding: utf-8 -*-

import base64
import hashlib
import pytz
from datetime import datetime
from odoo.tools.translate import _
from lxml import etree
from schwifty import IBAN
from odoo.addons.sm_maintenance.models.models_load_data import load_data


class sm_utils(object):

  @staticmethod
  def get_today_date():
    timezone = pytz.timezone('Europe/Madrid')
    date_time = datetime.now(tz=timezone)
    return datetime.date(date_time)

  @staticmethod
  def send_email_from_template(parent, template):
    company = parent.env.user.company_id
    mail_template = getattr(company, template)
    email_values = {'send_from_code': True}
    mail_template.with_context(email_values).send_mail(parent.id,True)

  @staticmethod
  def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

  @staticmethod
  def record_exists(parent, child_model, relation_name, name_query):
    if relation_name:
      relation = getattr(parent, relation_name)
      if relation.id:
        return True
    else:
      existing_model = parent.env[child_model].sudo().search(
        [('name', '=', name_query)])
      if existing_model.id:
        return True
    return False

  @staticmethod
  def get_create_existing_model(model_env, query, creation_data=False):
    existing_model = model_env.search(query)
    create_model = True
    if existing_model:
      if existing_model.exists():
        model = existing_model
        create_model = False
    if create_model:
      if creation_data:
        model = model_env.create(creation_data)
    return model

  @staticmethod
  def delete_existing_model(model_env, query):
    existing_model = model_env.search(query)
    if existing_model:
      if existing_model.exists():
        existing_model.unlink()
        return True
    return False

  @staticmethod
  def create_system_task(parent,task_name=False,task_description=False):
    loader = load_data.get_instance()
    parent.env['project.task'].create({
      'name': task_name,
      'description': task_description,
      'project_id': loader.get_system_project_id()
    })

  @staticmethod
  def is_module_active(contextself, module_name):
    module = contextself.env['ir.module.module'].search(
      [('name', '=', module_name), ('state', '=', 'installed')])
    return module.exists()

  #TODO: move out from here
  @staticmethod
  def generate_iban_check_digits(iban):
    iban_str = str(iban)
    iban_str = iban_str[:2] + '00' + iban_str[4:]
    new_iban = IBAN(iban_str, allow_invalid=True)
    number_iban = new_iban.numeric
    return '{:0>2}'.format(98 - (int(number_iban) % 97))

  #TODO: move out from here
  @staticmethod
  def valid_iban(iban):
    number_iban = iban.numeric
    return int(number_iban) % 97 == 1

  #TODO: deprecated, must remove
  @staticmethod
  def sepa_file_parser(sepa_data):

    # ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
    # a = hashlib.md5()
    str1 = "payment"
    str2 = sepa_data['serial_id']
    str3 = sepa_data['payment_date_long']
    MsgId_text = hashlib.md5((str2 + str3).encode("utf-8")).hexdigest()
    PmtInfId_text = hashlib.md5((str1 + str2 + str3).encode("utf-8")).hexdigest()

    if sepa_data['total_invoices'] == '0' or sepa_data['total_amount'] == '0':
      return True

    Document = etree.Element(
      'Document', xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02")

    CstmrDrctDbtInitn = etree.Element('CstmrDrctDbtInitn')

    GrpHdr = etree.Element('GrpHdr')

    MsgId = etree.Element('MsgId')
    MsgId.text = MsgId_text
    GrpHdr.append(MsgId)

    CreDtTm = etree.Element('CreDtTm')
    CreDtTm.text = sepa_data['payment_date_long']
    GrpHdr.append(CreDtTm)

    NbOfTxs = etree.Element('NbOfTxs')
    NbOfTxs.text = sepa_data['total_invoices']
    GrpHdr.append(NbOfTxs)

    CtrlSum = etree.Element('CtrlSum')
    CtrlSum.text = sepa_data['total_amount']
    GrpHdr.append(CtrlSum)

    InitgPty = etree.Element('InitgPty')

    Nm = etree.Element('Nm')
    Nm.text = sepa_data['ordenant_name']
    InitgPty.append(Nm)

    Id = etree.Element('Id')

    OrgId = etree.Element('OrgId')

    Othr = etree.Element('Othr')

    Id_Id = etree.Element('Id')
    Id_Id.text = sepa_data['ordenant_id']
    Othr.append(Id_Id)

    SchmeNm = etree.Element('SchmeNm')

    Prtry = etree.Element('Prtry')
    Prtry.text = 'SEPA'
    SchmeNm.append(Prtry)

    Othr.append(SchmeNm)

    OrgId.append(Othr)

    Id.append(OrgId)

    InitgPty.append(Id)

    GrpHdr.append(InitgPty)

    CstmrDrctDbtInitn.append(GrpHdr)

    PmtInf = etree.Element('PmtInf')

    PmtInfId = etree.Element('PmtInfId')
    PmtInfId.text = PmtInfId_text
    PmtInf.append(PmtInfId)

    PmtMtd = etree.Element('PmtMtd')
    PmtMtd.text = 'DD'
    PmtInf.append(PmtMtd)

    NbOfTxs_2 = etree.Element('NbOfTxs')
    NbOfTxs_2.text = sepa_data['total_invoices']
    PmtInf.append(NbOfTxs_2)

    CtrlSum_2 = etree.Element('CtrlSum')
    CtrlSum_2.text = sepa_data['total_amount']
    PmtInf.append(CtrlSum_2)

    PmtTpInf = etree.Element('PmtTpInf')

    SvcLvl = etree.Element('SvcLvl')

    Cd = etree.Element('Cd')
    Cd.text = 'SEPA'
    SvcLvl.append(Cd)

    PmtTpInf.append(SvcLvl)

    LclInstrm = etree.Element('LclInstrm')

    Cd_2 = etree.Element('Cd')
    Cd_2.text = 'CORE'
    LclInstrm.append(Cd_2)

    PmtTpInf.append(LclInstrm)

    SeqTp = etree.Element('SeqTp')
    SeqTp.text = 'OOFF'
    PmtTpInf.append(SeqTp)

    PmtInf.append(PmtTpInf)

    ReqdColltnDt = etree.Element('ReqdColltnDt')
    ReqdColltnDt.text = sepa_data['payment_date']
    PmtInf.append(ReqdColltnDt)

    Cdtr = etree.Element('Cdtr')

    Nm_2 = etree.Element('Nm')
    Nm_2.text = sepa_data['ordenant_name']
    Cdtr.append(Nm_2)

    PstlAdr = etree.Element('PstlAdr')

    Ctry = etree.Element('Ctry')
    Ctry.text = 'ES'
    PstlAdr.append(Ctry)

    AdrLine = etree.Element('AdrLine')
    AdrLine.text = sepa_data['ordenant_address_1']
    PstlAdr.append(AdrLine)

    AdrLine_2 = etree.Element('AdrLine')
    AdrLine_2.text = sepa_data['ordenant_address_2']
    PstlAdr.append(AdrLine_2)

    Cdtr.append(PstlAdr)

    PmtInf.append(Cdtr)

    CdtrAcct = etree.Element('CdtrAcct')

    CdtrAcct_Id = etree.Element('Id')

    IBAN = etree.Element('IBAN')
    IBAN.text = sepa_data['ordenant_iban']
    CdtrAcct_Id.append(IBAN)

    CdtrAcct.append(CdtrAcct_Id)

    PmtInf.append(CdtrAcct)

    CdtrAgt = etree.Element('CdtrAgt')

    FinInstnId = etree.Element('FinInstnId')

    BIC = etree.Element('BIC')
    BIC.text = sepa_data['ordenant_bic']

    FinInstnId.append(BIC)

    CdtrAgt.append(FinInstnId)

    PmtInf.append(CdtrAgt)

    ChrgBr = etree.Element('ChrgBr')
    ChrgBr.text = 'SLEV'
    PmtInf.append(ChrgBr)

    CdtrSchmeId = etree.Element('CdtrSchmeId')

    CdtrSchmeId_Id = etree.Element('Id')

    PrvtId = etree.Element('PrvtId')

    PrvtId_Othr = etree.Element('Othr')

    Id_Id_2 = etree.Element('Id')
    Id_Id_2.text = sepa_data['ordenant_id']
    PrvtId_Othr.append(Id_Id_2)

    Othr_SchmeNm = etree.Element('SchmeNm')

    Prtry_2 = etree.Element('Prtry')
    Prtry_2.text = 'SEPA'
    Othr_SchmeNm.append(Prtry_2)

    PrvtId_Othr.append(Othr_SchmeNm)

    PrvtId.append(PrvtId_Othr)

    CdtrSchmeId_Id.append(PrvtId)

    CdtrSchmeId.append(CdtrSchmeId_Id)

    PmtInf.append(CdtrSchmeId)

    if not sepa_data['invoices']:
      # reports
      iterator = sepa_data['reports']
      inv_type = 'test'
    else:
      # invoices
      iterator = sepa_data['invoices']
      inv_type = 'prod'

    for it in iterator:

      DrctDbtTxInf = etree.Element('DrctDbtTxInf')

      PmtId = etree.Element('PmtId')

      EndToEndId = etree.Element('EndToEndId')
      EndToEndId.text = hashlib.md5(
        (str2 + str(it.id) + sepa_data['payment_date']).encode('utf-8')).hexdigest()
      PmtId.append(EndToEndId)

      DrctDbtTxInf.append(PmtId)

      InstdAmt = etree.Element('InstdAmt', Ccy="EUR")
      # price here
      if inv_type == 'test':
        InstdAmt.text = '1'
      else:
        InstdAmt.text = str(it.amount_total)

      DrctDbtTxInf.append(InstdAmt)

      DrctDbtTx = etree.Element('DrctDbtTx')

      MndtRltdInf = etree.Element('MndtRltdInf')

      MndtId = etree.Element('MndtId')

      if inv_type == 'test':
        MndtId.text = str(it.id)
      else:
        MndtId.text = str(it.number)

      MndtRltdInf.append(MndtId)

      DtOfSgntr = etree.Element('DtOfSgntr')
      DtOfSgntr.text = sepa_data['payment_date']
      MndtRltdInf.append(DtOfSgntr)

      DrctDbtTx.append(MndtRltdInf)

      DrctDbtTxInf.append(DrctDbtTx)

      DbtrAgt = etree.Element('DbtrAgt')
      FinInstnId_2 = etree.Element('FinInstnId')
      DbtrAgt.append(FinInstnId_2)

      DrctDbtTxInf.append(DbtrAgt)

      Dbtr = etree.Element('Dbtr')

      Dbtr_Nm = etree.Element('Nm')

      Dbtr_Nm.text = it.partner_id.get_sepa_name()
      Dbtr.append(Dbtr_Nm)

      DrctDbtTxInf.append(Dbtr)

      DbtrAcct = etree.Element('DbtrAcct')

      DbtrAcct_Id = etree.Element('Id')

      Id_IBAN = etree.Element('IBAN')
      Id_IBAN.text = it.partner_id.get_bank_nr()
      DbtrAcct_Id.append(Id_IBAN)

      DbtrAcct.append(DbtrAcct_Id)

      DrctDbtTxInf.append(DbtrAcct)

      RmtInf = etree.Element('RmtInf')

      Ustrd = etree.Element('Ustrd')
      Ustrd.text = sepa_data['payment_concept']
      RmtInf.append(Ustrd)

      DrctDbtTxInf.append(RmtInf)

      PmtInf.append(DrctDbtTxInf)
    # END ADD USER

    CstmrDrctDbtInitn.append(PmtInf)

    Document.append(CstmrDrctDbtInitn)

    s = etree.tostring(Document, pretty_print=True,
               xml_declaration=True, encoding='UTF-8')
    file = base64.encodestring(s)

    return file