{
    'name': "Only Vendor's Product",
    'summary': "Purchase Order will only show our vendor's products",
    'version': '12.0.0.0.1',
    'depends': ['purchase'],
    'author': "Coopdevs Treball SCCL",
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'description': """
    Customization to only show the vendor's products in the purchase_order_form.
    """,
    "license": "AGPL-3",
    'data': [
        "views/purchase_order_view.xml",
    ]

}
