# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _

class cs_car(models.Model):
  _name = 'fleet.vehicle'
  _inherit = 'fleet.vehicle'

  battery_fee = fields.Selection([
    ('rent', _("Lloguer")),
    ('bougth', _("Compra")),
    ('no-quota', _("Sense Quota"))
  ], string=_("Bateria propietat"), default="rent")
  car_type = fields.Selection([
    ('fp', _("FP")),
    ('renting', _("Renting")),
    ('cic', _("CiC")),
    ('p2p', _("P2P")),
  ], string=_("Modalitat"), default="fp")
  bougth_km = fields.Integer(string=_("Km en la compra"))
  bougth_date = fields.Date(string=_("Data de la compra"))
  r_link_update = fields.Boolean(string=_("R-Link update"))
  key_number = fields.Char(string=_("Número clau"))
  insurance_company = fields.Char(string=_("Asseguradora"))
  insurance_age = fields.Char(string=_("Edat assegurança"))
  insurance_policy = fields.Char(string=_("Polissa assegurança"))
  insurance_expiricy = fields.Date(string=_("Venciment Assegurança"))
  insurance_extras = fields.Text(string=_("Garanties Extres"))
  battery_size = fields.Integer(string=_("Tamany de la bateria"))
  next_tech_revision = fields.Date(string=_("Propera ITV"))
  next_revision = fields.Date(string=_("Propera revisió"))
  viat_applies = fields.Boolean(string=_("Aplica Via-T"))
  viat_pan = fields.Char(string=_("PAN Via-T"))
  viat_expiricy = fields.Date(string=_("Caducitat Via-T"))
  viat_onplace = fields.Boolean(string=_("Via-T col.locat?"))
  viat_eco_accepted = fields.Boolean(string=_("Eco Via-T acceptat?"))
  viat_eco_approved_date = fields.Date(string=_("Data aprovació Eco Via-T"))
  ivtm_status = fields.Selection([
    ('no', _("No")),
    ('no_apply', _("No aplica")),
    ('presented', _("Instància presentada")),
    ('yes', _("IVTM BONIFICAT"))
  ], string=_("Tramitada bonificacio IVTM"), default="no")
  live_card = fields.Char(string=_("Targeta Live"))
  live_card_status = fields.Char(string=_("Estat Targeta Live"))
  live_smou = fields.Char(string=_("Live a SMOU"))
  smou_email_id = fields.Many2one("mail.alias",string=_("Email (SMOU)"),compute="_get_car_email")
  electromaps_code = fields.Char(string=_("Codi electromaps"))
  garagekey_code = fields.Char(string=_("Mando garatge"))
  secondary_key_location = fields.Char(string=_("Ubicacio segona clau"))
  battery_rental = fields.Float(_("Quota bateria (sense IVA)"))
  contact_person_txt = fields.Char(string=_("Contacte"))
  vinyl = fields.Char(string=_("Vinil"))
  origin = fields.Char(string=_("Origen"))
  drive_docs = fields.Char(string=_("Documentació DRIVE"))

  @api.depends('project_id')
  def _get_car_email(self):
    for record in self:
      if record.project_id:
        if record.project_id.alias_id:
          record.smou_email_id = self.project_id.alias_id





