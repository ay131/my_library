# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api


# =========================[ const vals  ]===================
stat=[('draft', 'Not Available'),('available', 'Available'),('lost', 'Lost')]
# ============================================================
# =========================[ Library Book model ]===================
class LibraryBook(models.Model):
    # =========================[ model defination ]===================
    _name = 'library.book'
    _description = 'library book info'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    # =================================================================

    # =========================[SQL costrains======]===================
    # =================================================================

    # =========================[main field]===================
    short_name = fields.Char('Short Title', required=True)
    name = fields.Char(string='Title', required=True)
    date_release = fields.Date(string='release date')
    notes = fields.Text(string='Internal Notes')
    state = fields.Selection(selection=stat,string='State',default="draft")
    description = fields.Html(string='Description',sanitize=True, strip_style=False)
    cover = fields.Binary(string='Book Cover')
    out_of_print = fields.Boolean(string='Out of Print?')
    date_updated = fields.Datetime(string='Last Updated')
    pages = fields.Integer(string='Number of Pages',groups='base.group_user',states={'lost': [('readonly', True)]},
                           help='Total book page count', company_dependent=False)
    reader_rating = fields.Float(string='Reader Average Rating',digits=(14, 4))
    active = fields.Boolean(string='Active', default=True)
    cost_price = fields.Float('Book Cost', digits='Product Price')
    retail_price = fields.Monetary(string='Retail Price',currency_field='currency_id')
    # =================================================================

    # =========================[relashional fields ]===================
    author_ids = fields.Many2many('res.partner', string='author')
    currency_id = fields.Many2one('res.currency', string='Currency')
    publisher_id = fields.Many2one('res.partner', string='Publisher',ondelete='set null')
    # ================================================================

    # =========================[computed fields ]=====================
    # =================================================================

    # =========================[computed functions ]===================
    # =======[....................]==========
    # @api.depends('')
    # =================================================================


    # #=================[onchange functions ]===================
    # ========[................. ]========
    # @api.onchange("")
    # ================================================================

    # =========================[action functions]===================
    # ========[............... ]========
    # ================================================================

    # =========================[Python costrains======]===================
    # @api.constrains('')
    # =================================================================
