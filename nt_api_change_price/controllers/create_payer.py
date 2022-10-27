from odoo.http import request, Response
from odoo import http, _


class NtIntegration(http.Controller):
    @http.route('/api/Integration/NT/CreatePayer', auth='user', csrf=False, methods=['POST'], type='json')
    def create_payer(self, **kwargs):
        response = request.jsonrequest
        # return requests.codes.ok
        if response.get('name', False) and response.get('ref', False) and response.get('vat', False):
            res_partner = request.env['res.partner'].sudo().search([('name', '=', response.get('name'))], limit=1)

            if res_partner:
                result = {
                    "success": False,
                    "message": "The payer has not been created the payer is exist .",
                }
            else:
                payer = {
                    'name': response.get('name'),
                    'ref': response.get('ref'),
                    'vat': response.get('vat'),
                    'company_type': 'company',
                    'customer_rank': 1,
                }
                request.env['res.partner'].sudo().create(payer)
                result = {
                    "success": True,
                    "message": "The payer has  been created successfully.",
                }
        else:
            sms = " "
            if not response.get('name'):
                sms += "there is no payer name ,"
            if not response.get('vat'):
                sms += "there is no payer vat ,"
            if not response.get('ref'):
                sms += "there is no payer ref ,"

            result = {
                "success": False,
                "message": sms,
            }
        return result
