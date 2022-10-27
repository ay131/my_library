from odoo.http import request, Response
from odoo import http, _


class NtChangePrice(http.Controller):

    @http.route('/api/Integration/NT/Visit', auth='user', csrf=False, methods=['POST'], type='json')
    def change_price(self, **kwargs):
        response = request.jsonrequest

        if response.get('action_type') == 'update_price':
            print(response)
            product = request.env['product.product'].sudo().search(
                [('name', '=', response['service'].get('name')),
                 ('default_code', '=', response['service'].get('default_code'))], limit=1)
            print(product)
            mov_line = request.env['account.move.line'].sudo().search(
                [('accession_number', '=', response.get('accession_number')), ('product_id', '=', product.id)], limit=1)
            print(mov_line)
            # mov_line = request.env['account.move.line'].sudo().search([('accession_number', '=', response.get('accession_number'))],limit=1)
            if mov_line:
                if mov_line.move_id.state == 'draft':
                    print('1111111111111111111111111111', mov_line.move_id.state)
                    mov_line.move_id.write({'invoice_line_ids': [(1, mov_line.id, {
                        'price_unit': response.get('cash'),
                    })]})
                if mov_line.move_id.state == 'posted':
                    deff_amount = response.get('cash') - mov_line.price_unit
                    print(deff_amount)
                    if deff_amount > 0:
                        # print(deff_amount,'+++++++++++++++')
                        request.env["account.move"].sudo().create(
                            {
                                "partner_id": mov_line.move_id.partner_id.id,
                                "move_type": "out_invoice",
                                "journal_id": mov_line.move_id.journal_id.id,
                                "invoice_line_ids": [(0, 0, {
                                    'accession_number': mov_line.accession_number,
                                    'contract_id': mov_line.contract_id,
                                    'product_id': mov_line.product_id,
                                    'name': mov_line.name,
                                    'price_unit': deff_amount,
                                    'quantity': mov_line.quantity,
                                })]
                            }
                        )
                    if deff_amount < 0:
                        inv_cr_note = request.env["account.move"].search(
                            [('partner_id', '=', mov_line.move_id.partner_id.id), ('move_type', '=', 'out_refund'),
                             ('state', '=', 'draft')], limit=1)

                        print('inv_cr_note', inv_cr_note, '************************', mov_line)
                        if inv_cr_note and inv_cr_note.state == 'draft':
                            print(inv_cr_note)
                            inv_cr_note.write({
                                "invoice_line_ids": [(0, 0, {
                                    'accession_number': mov_line.accession_number,
                                    'contract_id': mov_line.contract_id,
                                    'product_id': mov_line.product_id,
                                    'name': mov_line.name,
                                    'price_unit': abs(deff_amount),
                                    'quantity': mov_line.quantity,
                                })]})
                        else:
                            request.env["account.move"].sudo().create(
                                {
                                    "partner_id": mov_line.move_id.partner_id.id,
                                    "move_type": "out_refund",
                                    'ref': _('Reversal of: %(move_name)s', move_name=mov_line.move_id.name),
                                    "journal_id": mov_line.move_id.journal_id.id,
                                    "invoice_line_ids": [(0, 0, {
                                        'accession_number': mov_line.accession_number,
                                        'contract_id': mov_line.contract_id,
                                        'product_id': mov_line.product_id,
                                        'name': mov_line.name,
                                        'price_unit': abs(deff_amount),
                                        'quantity': mov_line.quantity,
                                    })]
                                }
                            )
                        print(deff_amount, '---------------')


        return 'aaaaaaa'
