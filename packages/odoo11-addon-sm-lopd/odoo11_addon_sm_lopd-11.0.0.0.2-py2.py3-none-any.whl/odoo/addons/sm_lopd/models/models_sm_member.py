# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

class sm_member(models.Model):

  _inherit = 'res.partner'
  _name = 'res.partner'

  lopd_mail_sent = fields.Boolean(string=_("LOPD mail"))
  report_address = fields.Char(string=_("Report address"),compute="_get_report_address",store=False)

  @api.depends('street', 'street2', 'zip', 'city')
  def _get_report_address(self):
    report_address = ''
    for record in self:
      if record.street:
        report_address += record.street
      if record.street2:
        report_address += ' '+record.street2
      if record.zip:
        report_address += ' '+record.zip
      if record.city:
        report_address += record.city
      record.report_address = report_address

  @api.model
  def notify_about_lopd_action(self):
    if self.env.context:
       if 'active_ids' in self.env.context:
         members = self.env['res.partner'].browse(self.env.context['active_ids'])
         if members.exists():
           for member in members:
            error = member.notify_about_lopd()
            if error != False:
              return self._resources.get_successful_action_message(self, error, self._name)
    return self._resources.get_successful_action_message(self, _('Notify about lopd done successfully'), self._name)

  def notify_about_lopd(self):
    if not self.lopd_mail_sent:
      if self.is_company:
        sm_utils.send_email_from_template(self, 'lopd_company_mail_template_id')
        self.write({'lopd_mail_sent': True})
      else:
        sm_utils.send_email_from_template(self, 'lopd_mail_template_id')
        self.write({'lopd_mail_sent': True})
    return False
