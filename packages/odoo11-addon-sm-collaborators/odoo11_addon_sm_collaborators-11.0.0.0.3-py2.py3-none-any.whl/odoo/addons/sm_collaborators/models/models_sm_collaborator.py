# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources


class sm_collaborator(models.Model):
  _name = 'sm_collaborators.sm_collaborator'

  # Data
  name = fields.Char(string=_("Name"), required=True)
  date = fields.Date(string=_("Date"))
  member_name = fields.Char(string=_("Member name"))
  member_email = fields.Char(string=_("Member email"))
  collaborator_info = fields.Char(string=_("Info"))
  collaborator_type = fields.Selection([('www', 'Socis Colaboradors (web)')],
    string=_("Type"))

  # Computed
  completed = fields.Date(string=_("Completed"))
  end = fields.Date(string=_("Collaboration end"))
  related_member_id = fields.Many2one('res.partner', string=_("Partner"))

  _order = "date desc"

  @api.multi
  def find_rel_partner(self):
    cols = self.env['sm_collaborators.sm_collaborator'].browse(self.env.context['active_ids'])
    if cols.exists():
      for col in cols:
        rel_member = self.env['res.partner'].sudo().search([
          ('name', 'like', col.member_name.lower().title())])
        if len(rel_member) > 0:
          if len(rel_member) > 1:
            for member in rel_member:
              if member.email == col.member_email:
                col.sudo().write({'related_member_id': member.id})
          else:
            col.sudo().write({'related_member_id': rel_member[0].id})

    return sm_resources.getInstance().get_successful_action_message(self,
      _('Find relative partner done successfully'),
      self._name)
