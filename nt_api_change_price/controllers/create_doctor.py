from odoo.http import request, Response
from odoo import http, _


class NtIntegration(http.Controller):
    @http.route('/api/Integration/NT/CreateDoctor', auth='user', csrf=False, methods=['POST'], type='json')
    def create_doctor(self, **kwargs):
        response = request.jsonrequest
        # return requests.codes.ok
        if response.get('doctor_code', False) and response.get('name', False):
            res_partner = request.env['res.partner'].sudo().search([('name', '=', response.get('name')),
                                                                    ('doctor_code', '=', response.get('doctor_code')),
                                                                    ('doctor', '=', True)
                                                                    ], limit=1)
            if res_partner:
                result = {
                    "success": False,
                    "message": "The doctor has not been created the doctor is exist .",
                }

            else:
                doctor = {
                    'name': response.get('name'),
                    'doctor_code': response.get('doctor_code'),
                    'doctor': True,
                    'company_type': 'person',
                }
                request.env['res.partner'].sudo().create(doctor)
                result = {
                    "success": True,
                    "message": "The doctor has been created successfully.",
                }
        else:
            sms = " "
            if not response.get('name'):
                sms += "there is no doctor name ,"
            if not response.get('doctor_code'):
                sms += "there is no  doctor_code ,"

            result = {
                "success": False,
                "message": sms,
            }
        return result
