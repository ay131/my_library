from odoo.http import request, Response
from odoo import http, _


class NtIntegration(http.Controller):
    @http.route('/api/Integration/NT/CreateCenter', auth='user', csrf=False, methods=['POST'], type='json')
    def create_doctor(self, **kwargs):
        response = request.jsonrequest
        # return requests.codes.ok
        if response.get('center_code', False) and response.get('name', False) :
            res_partner = request.env['res.partner'].sudo().search([('name', '=', response.get('name')),
                                                                     ('center_code', '=', response.get('center_code')),
                                                                     ('center', '=', True)
                                                                     ],limit=1)
            if res_partner:
                result = {
                    "success": False,
                    "message": "The center has not been created the center is exist .",
                }

            else:
                center = {
                    'name': response.get('name'),
                    'center_code': response.get('center_code'),
                    'center':True,
                    'company_type':'company',
                }
                request.env['res.partner'].sudo().create(center)
                result = {
                    "success": True,
                    "message": "The center has been created successfully.",
                }
        else:
            sms = " "
            if not response.get('name'):
                sms += "there is no center name ,"
            if not response.get('center_code'):
                sms += "there is no  center_code ,"

            result = {
                "success": False,
                "message": sms,
            }
        return result
