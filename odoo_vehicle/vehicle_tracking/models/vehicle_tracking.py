# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

class VehicleTracking(models.Model):
    _name = 'vehicle.tracking'
    _description = 'Vehicle Tracking'
    _rec_name = 'vehicle_id'

    # Header info
    ref = fields.Char(string='Ref', readonly=True, copy=False, default='New')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    driver_id = fields.Many2one('res.partner', string='Driver',
                                domain="[('is_company','=',False)]")
    number_plate = fields.Char(string='Number Plate')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 readonly=True)

    # Tracking Details
    source = fields.Selection([
        ('head_office', 'Head Office'),
        ('branch', 'Branch'),
        ('warehouse', 'Warehouse'),
        ('customer_site', 'Customer Site'),
        ('others', 'Others'),
    ], string='Source')

    destination = fields.Selection([
        ('head_office', 'Head Office'),
        ('branch', 'Branch'),
        ('warehouse', 'Warehouse'),
        ('customer_site', 'Customer Site'),
        ('others', 'Others'),
    ], string='Destination')

    start_km = fields.Integer(string='Start Km', default=0)
    end_km = fields.Integer(string='End Km', default=0)
    km_travelled = fields.Integer(string='KM Travelled', compute='_compute_km_travelled', store=True)
    purpose_of_visit = fields.Selection([
        ('delivery', 'Delivery'),
        ('collection', 'Collection'),
        ('inspection', 'Inspection'),
        ('official', 'Official'),
        ('personal', 'Personal'),
    ], string='Purpose of Visit')

    start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Time')
    duration = fields.Float(string='Duration (Hrs)', compute='_compute_duration', store=True)
    invoice_number = fields.Char(string='Invoice Number')
    invoice_match = fields.Boolean(string="Invoice Match", readonly=True)
    invoice_message = fields.Char(string="Invoice Message", readonly=True)

    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    estimated_time = fields.Float(string='Estimated Time (Hrs)', default=00.00)

    coolant_water = fields.Boolean(string='Coolant Water')
    oil_checking = fields.Boolean(string='Oil Checking')
    tyre_checking = fields.Boolean(string='Tyre Checking')
    battery_checking = fields.Boolean(string='Battery Checking')
    daily_checks = fields.Boolean(string='Daily Checks')

    invoice_line_ids = fields.One2many(
        'vehicle.tracking.invoice',   # child model name
        'tracking_id',     
        string='Invoice Details'
    )

    #info section
    start_trip = fields.Boolean(string='Start Trip')
    end_trip = fields.Boolean(string='End Trip')
    trip_cancel = fields.Boolean(string='Trip Cancel')


    start_latitude = fields.Char(string='Start Latitude')
    start_longitude = fields.Char(string='Start Longitude')
    end_latitude = fields.Char(string='End Latitude')
    end_longitude = fields.Char(string='End Longitude')

    image_url = fields.Char(string='Image URL')
    remarks = fields.Text(string='Remarks')


    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
    ], default='draft', string='Status', readonly=True)

    # Compute fields
    @api.depends('start_km', 'end_km')
    def _compute_km_travelled(self):
        for rec in self:
            rec.km_travelled = max(rec.end_km - rec.start_km, 0)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                delta = rec.end_time - rec.start_time
                rec.duration = round(delta.total_seconds() / 3600, 2)
            else:
                rec.duration = 0.0

    @api.depends('km_travelled', 'duration')
    def _compute_amount(self):
        # You can use any logic to calculate the amount, here we assume a rate per km
        rate_per_km = 10  # Example: 10 units per kilometer
        rate_per_hour = 5  # Example: 5 units per hour of duration

        for rec in self:
            # Calculate the amount based on the distance traveled and duration
            rec.amount = (rec.km_travelled * rate_per_km) + (rec.duration * rate_per_hour)

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.number_plate = self.vehicle_id.license_plate

        
    @api.model_create_multi
    def create(self, vals_list):
        # DO NOT assign sequence here - let it remain as 'New'
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New' or not vals.get('ref'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('vehicle.tracking.seq')
        records = super(VehicleTracking, self).create(vals_list)
        return records
        
    @api.onchange('invoice_number')
    def _onchange_invoice_number(self):
        if not self.invoice_number:
            self.invoice_match = False
            self.invoice_message = ""
            return

        # check invoice in account.move with move_type='out_invoice'
        invoice = self.env['account.move'].search([
            ('name', '=', self.invoice_number),
            ('move_type', '=', 'out_invoice')
        ], limit=1)

        if invoice:
            self.invoice_match = True
            self.invoice_message = "Invoice number matches ✓"
        else:
            self.invoice_match = False
            self.invoice_message = "Invoice number doesn’t match ✗"



    # Buttons
    def action_validate(self):
        for rec in self:
            if rec.invoice_number:
                invoice = rec.env['account.move'].search([
                    ('name', '=', rec.invoice_number),
                    ('move_type', '=', 'out_invoice')
                ], limit=1)

                if not invoice:
                    # Invoice does NOT exist → block validation
                    rec.invoice_match = False
                    rec.invoice_message = "Invoice number doesn’t match ✗"
                    raise UserError("Invoice number doesn’t match any existing invoice!")

                # Invoice exists → allow validation
                rec.invoice_match = True
                rec.invoice_message = "Invoice number matches ✓"

            # Continue your normal validation logic
            rec.state = 'validated'
    

    

    # def action_discard_custom(self):
    #     """Custom discard button — shows confirmation and redirects to list view."""
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Vehicle Tracking',
    #         'res_model': 'vehicle.tracking',
    #         'view_mode': 'list,form',
    #         'target': 'current',
    #         'views': [(False, 'list'), (False, 'form')],
    #     }
    
    def action_discard_custom(self):
        """Custom discard button – only delete if record has ref='New' (not saved properly)"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicle Tracking',
            'res_model': 'vehicle.tracking',
            'view_mode': 'list',
            'view_id': False,
            'target': 'current',
            'context': self.env.context,
        }

    def action_custom_save(self):
        # Save the record (Odoo does this automatically when you save a form)
        self.ensure_one()  # Ensure only one record is processed at a time
        if self.ref == 'New' and self.state == 'draft':
            self.ref = self.env['ir.sequence'].next_by_code('vehicle.tracking.seq') or 'New'
        # Return to the list view after saving
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicle Tracking',
            'res_model': 'vehicle.tracking',
            'view_mode': 'list', # Use the default list view
            'target': 'current',
            'context': self.env.context,
        }


    # def action_custom_save(self):
    #     return True
