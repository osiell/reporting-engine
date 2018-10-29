# Copyright 2018 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ReportCombinationLine(models.Model):
    _name = 'ir.actions.report.combination.line'
    _description = "Line composing a report combination"
    _rec_name = 'report_id'

    action_report_id = fields.Many2one(
        'ir.actions.report', "Combination report")
    sequence = fields.Integer(default=99)
    report_id = fields.Many2one(
        'ir.actions.report', "Report",
        domain=lambda self: self._get_report_id_domain())
    static_pdf_file_name = fields.Char("Static PDF file name")
    static_pdf_file = fields.Binary(
        "Static PDF file", attachment=True)
    type = fields.Selection(
        selection=[
            ('action_report', 'Report'),
            ('static_pdf_file', 'Static PDF file')],
        required=True)

    @api.model
    def _get_report_id_domain(self):
        domain = [('report_type', '!=', 'pdf-combination')]
        params = self.env.context.get('params')
        if params:
            report = self.env['ir.actions.report'].browse(params.get('id'))
            if report:
                domain.append(('model', '=', report.model))
        return domain

    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'action_report':
            self.static_pdf_file = False
        elif self.type == 'static_pdf_file':
            self.report_id = False
