# -*- coding: utf-8 -*-
from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("order_line")
    def onchange_order_line(self):
        if len(self.order_line):
            for prod in self.order_line:
                if len(prod.product_id.seller_ids):
                    if not self.partner_id:
                        # Autofill the vendor's field from the product's first provider
                        self.partner_id = prod.product_id.seller_ids[0].name
                    vendors = [v.name for v in prod.product_id.seller_ids]
                    if self.partner_id not in vendors:
                        return {
                            "warning": {
                                "title": "Warning!",
                                "message": "Your order contains products from different vendors.",
                            }
                        }
