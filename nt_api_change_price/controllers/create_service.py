from odoo.http import request, Response
from odoo import http, _


class NtIntegration(http.Controller):

    @http.route('/api/Integration/NT/CreateService', auth='user', csrf=False, methods=['POST'], type='json')
    def create_service(self, **kwargs):
        response = request.jsonrequest
        # return requests.codes.ok
        if response.get('name', False) and response.get('categ_id', False) and response.get('default_code',
                                                                                            False) and response.get(
            'description_sale', False):
            product_category = request.env['product.category'].sudo().search([('name', '=', response.get('categ_id'))],
                                                                             limit=1)
            if product_category:
                categ_id = product_category
            else:
                catigor = {
                    'name': response.get('categ_id'),
                }
                categ_id = request.env['product.category'].sudo().create(catigor)

            product = request.env['product.template'].sudo().search(
                [('name', '=', response.get('name')), ('default_code', '=', response.get('default_code'))], limit=1)
            if product:
                result = {
                    "success": False,
                    "message": "The service has not been created the service is exist .",
                }
            else:
                service = {
                    'sale_ok': True,
                    'purchase_ok': False,
                    'detailed_type': "service",
                    'name': response['name'],
                    'default_code': response['default_code'],
                    'description_sale': response['description_sale'],
                    'categ_id': categ_id.id,
                }
                service = request.env['product.template'].sudo().create(service)

                result = {
                    "success": True,
                    "message": "The service has  been created successfully.",
                }
        else:
            sms = " "
            if not response.get('name'):
                sms += "The Service Name Required,"
            if not response.get('description_sale'):
                sms += "The Service Description Required,"
            if not response.get('default_code'):
                sms += "The Service Code Required,"
            if not response.get('categ_id'):
                sms += "The service Category Required,"
            result = {
                "success": False,
                "message": sms,
            }
        return result
