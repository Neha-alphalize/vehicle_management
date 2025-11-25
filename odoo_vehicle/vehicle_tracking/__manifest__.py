{
    'name': 'Vehicle Tracking',
    'version': '1.0',
    'summary': 'Track vehicle movement, trips and driver logs',
    'description': """
Odoo 19 Vehicle Tracking Module
--------------------------------
Manage vehicle trip details, driver, KM readings, invoices, and durations.
    """,
    'author': 'Danat Oman',
    'company': 'DANAT OMAN',
    'category': 'Fleet',
    'depends': ['base', 'fleet'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_tracking_view.xml',
        'views/vehicle_tracking_actions.xml', 
        'views/vehicle_tracking_menus.xml',
        'data/vehicle_tracking_sequence.xml',
    ],

    'application': True,
    'installable': True,
}
