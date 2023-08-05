# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools.translate import _


class smp_car(models.Model):
  _name = 'smp.sm_car'

  name = fields.Char(string=_("Name"), required=True)
  home = fields.Char(string=_("Home"))
  car_name = fields.Char(string=_("name (car)"))
  license_plate = fields.Char(string=_("licensePlate"))
  invers_qnr = fields.Char(string=_("invers_qnr"))
  invers_type = fields.Char(string=_("invers_type"))
  invers_lomo_adapter = fields.Boolean(string=_("lomo_adapter"))
  swap_group = fields.Char(string=_("swapGroup"))
  owner_group_index = fields.Char(string=_("Owner Group Index"))
  owner_group_id = fields.Many2one('smp.sm_group', string=_("Owner Group"),compute="_get_owner_group_id")

  #TODO: bring to fleet
  car_model = fields.Char(string=_("Model"))
  location = fields.Char(string=_("Location"))
  car_brand = fields.Char(string=_("Brand"))
  registration = fields.Date(string=_("Registration"))
  vin = fields.Char(string=_("Vehicle identification number"))
  car_owner = fields.Many2one('res.partner', string=_("Owner"))
  kilometre_marker = fields.Float(string=_("Kilometre marker"))
  car_color = fields.Char(string=_("Color"))
  has_gps = fields.Boolean(string=_("Has GPS?"))
  vehicle_type = fields.Selection([
    ('cotxe', 'Cotxe'),
    ('bicicleta', 'Bicicleta'),
    ('furgoneta', 'Furgoneta')
  ], string='Vehicle type')

  carconfigs_id = fields.One2many('smp.sm_car_config', 'rel_car_id', string=_('Carconfigs'))

  _order = "name asc"

  @api.depends('owner_group_index')
  def _get_owner_group_id(self):
    for record in self:
      if record.owner_group_index:
        existing_group = self.env['smp.sm_group'].search([('name','=',record.owner_group_index)])
        if existing_group.exists():
          record.owner_group_id = existing_group[0].id

  def fetch_db_data(self, data):
    update_data = {}

    if "name" in data:
      update_data['car_name'] = data['name']
    else:
      update_data['car_name'] = False

    if "home" in data:
      update_data['home'] = data['home']
    else:
      update_data['home'] = False

    if "licensePlate" in data:
      update_data['license_plate'] = data['licensePlate']
    else:
      update_data['license_plate'] = False

    if "invers" in data:
      if "qnr" in data["invers"]:
        update_data['invers_qnr'] = data['invers']['qnr']
      else:
        update_data['invers_qnr'] = False
      if "type" in data["invers"]:
        update_data['invers_type'] = data['invers']['type']
      else:
        update_data['invers_type'] = False
      if "lomo_adapter" in data["invers"]:
        update_data['invers_lomo_adapter'] = data['invers']['lomo_adapter']
      else:
        update_data['invers_lomo_adapter'] = False
    else:
      update_data['invers_qnr'] = False
      update_data['invers_type'] = False
      update_data['invers_lomo_adapter'] = False

    if "swapGroup" in data:
      update_data['swap_group'] = data['swapGroup']
    else:
      update_data['swap_group'] = False

    if "ownerGroup" in data:
      update_data['owner_group_index'] = data['ownerGroup']
    else:
      update_data['owner_group_index'] = False

    self.write(update_data)
