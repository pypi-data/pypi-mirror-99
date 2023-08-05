# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
  _inherit = 'res.company'

  lopd_mail_template_id = fields.Many2one('mail.template',
    string=_("LOPD notification template"))
  lopd_company_mail_template_id = fields.Many2one('mail.template',
    string=_("LOPD company notification template"))

sm_company()
