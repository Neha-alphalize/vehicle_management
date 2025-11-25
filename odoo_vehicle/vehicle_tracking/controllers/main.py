from odoo import http

class VehicleTrackingController(http.Controller):
    @http.route('/vehicle_tracking', auth='public')
    def index(self, **kw):
        return "Vehicle Tracking Module Active"
