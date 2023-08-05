from odoo import models, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils


class sm_lopd_cron(models.Model):
  _name = 'sm_lopd.sm_lopd_cron'

  @api.model
  def send_lopd_emails_cron(self):
    self.notify_company_cs_users_about_lopd()
    self.notify_companies_about_lopd()

  def notify_company_cs_users_about_lopd(self):
    members = self.env['res.partner'].search([
      ('cs_user_type', '=', 'organisation'),
      ('lopd_mail_sent', '=', False)
    ])
    if members.exists():
      for member in members:
        if member.parent_id.id:
          if member.exists_on_app_db():
            member.notify_about_lopd()
        else:
          error_msg = _("""We have a company cs user without company defined for member.id: %s""") % (str(member.id))
          sm_utils.create_system_task(self,"CS company user error.",error_msg)
    return True

  def notify_companies_about_lopd(self):
    companies = self.env['res.partner'].search([
      ('member_nr', '>', 0),
      ('is_company', '=', True),
      ('lopd_mail_sent', '=', False)
    ])
    if companies.exists():
      for company in companies:
        company.notify_about_lopd()
    return True