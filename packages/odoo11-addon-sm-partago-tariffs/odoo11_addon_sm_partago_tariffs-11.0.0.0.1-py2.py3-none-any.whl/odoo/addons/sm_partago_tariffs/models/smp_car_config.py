# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class smp_car_config(models.Model):
  _inherit = 'smp.sm_car_config'
  _name = 'smp.sm_car_config'

  related_price_group_id = fields.Many2one('smp.sm_carconfig_price_group', string=_("Related price group"))
  initial_price = fields.Float(string=_("Initial price (sense IVA)"))
  cs_carconfig_ids = fields.One2many(comodel_name='sm_carsharing_structure.cs_carconfig',
    inverse_name='db_carconfig_id', string='CS Carconfigs')