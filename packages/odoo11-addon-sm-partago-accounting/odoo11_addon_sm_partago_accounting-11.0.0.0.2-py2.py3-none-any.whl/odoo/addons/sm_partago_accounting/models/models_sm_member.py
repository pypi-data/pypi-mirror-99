from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_partago_db.models.models_smp_db_utils import smp_db_utils

class partago_user(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  # TODO: To be added on the moment of migration
  # cs_accounting_state = fields.Selection([
  #   ('app_managed', 'Prepayment (App)'),
  #   ('erp_managed', 'Postpayment (ERP)')
  # ], default='app_managed', string=_("Carsharing accounting status"))

  personal_billing_account_index = fields.Char(string=_("Personal billingAccount index"))

  related_cs_billing_account_id = fields.Many2one('smp.sm_billing_account',
    string=_("Related cs db billing account"),compute="_get_related_cs_billing_account_id",store=False)
  related_cs_billing_account_mintuesleft = fields.Float(string=_("Related cs db billing account minutes left"),
    compute="_get_related_cs_billing_account_mintuesleft",store=False)
  
  @api.depends('personal_billing_account_index')
  def _get_related_cs_billing_account_id(self):
    for record in self:
      if not record.related_cs_billing_account_id:
        rba = self.env['smp.sm_billing_account'].search([('name','=',record.personal_billing_account_index)])
        if rba.exists():
          record.related_cs_billing_account_id = rba[0]
  @api.depends('related_cs_billing_account_id')
  def _get_related_cs_billing_account_mintuesleft(self):
    for record in self:
      if record.related_cs_billing_account_id:
        record.related_cs_billing_account_mintuesleft = record.related_cs_billing_account_id.minutesLeft

  def add_app_transaction_to_personal_billing_account(self,ttype=False,description=False,credits=False):
    if ttype and description and credits and self.personal_billing_account_index:
      app_db_utils = smp_db_utils.get_instance()
      transaction = app_db_utils.create_app_ba_transaction(self.personal_billing_account_index,ttype,description,credits)
      return transaction
    return False

partago_user()