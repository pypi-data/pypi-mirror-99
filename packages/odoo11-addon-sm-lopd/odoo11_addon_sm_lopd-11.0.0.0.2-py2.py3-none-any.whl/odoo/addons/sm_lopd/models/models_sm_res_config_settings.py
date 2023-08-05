# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  lopd_mail_template_id = fields.Many2one(
    related='company_id.lopd_mail_template_id',
    string=_("LOPD notification template"))

  lopd_company_mail_template_id = fields.Many2one(
    related='company_id.lopd_company_mail_template_id',
    string=_("LOPD company notification template"))

  # CARSHARING DATA DEFAULT VALUES
  # default_group_id = fields.Many2one(
  #   related='company_id.default_group_id',
  #   string=_("Default group"))
  # default_group_config_id = fields.Many2one(
  #   related='company_id.default_group_config_id',
  #   string=_("Default group config"))
  # default_billing_account_id= fields.Many2one(
  #   related='company_id.default_billing_account_id',
  #   string=_("Default billing account"))
  # default_billing_account_blocked_id = fields.Many2one(
  #   related='company_id.default_billing_account_blocked_id',
  #   string=_("Default billing account blocked"))
  # default_app_language = fields.Char(
  #   related='company_id.default_app_language',
  #   string=_("Default app language"))
  # default_owner_group_id = fields.Many2one(
  #   related='company_id.default_owner_group_id',
  #   string=_("Default owner group"))
