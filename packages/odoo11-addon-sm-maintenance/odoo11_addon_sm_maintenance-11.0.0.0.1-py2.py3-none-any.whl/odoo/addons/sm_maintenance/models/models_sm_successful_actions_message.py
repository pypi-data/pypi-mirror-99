from odoo import api, models, fields, _

class sm_successful_action_message(models.TransientModel):
  _name = 'sm_maintenance.successful_action_message'

  action = fields.Char('Action', readonly=1)
  model = fields.Char('From model', readonly=1)
