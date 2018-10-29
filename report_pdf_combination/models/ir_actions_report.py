# Copyright 2018 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ReportAction(models.Model):
    _inherit = 'ir.actions.report'

    report_type = fields.Selection(
        selection_add=[("pdf-combination", "Combine multiple PDFs")])
    combination_line_ids = fields.One2many(
        'ir.actions.report.combination.line', 'action_report_id',
        string='Combination lines')

    def render_pdf_combination(self, docids, data):
        report_model_name = 'report.%s' % self.report_name
        report_model = self.env.get(report_model_name)
        if report_model is None:
            report_model = self.env['report.report_pdf_combination.abstract']
        return report_model.with_context({
            'active_model': self.model,
            'current_report_to_use': self.id
        }).create_pdf_combination_report(docids, data)

    @api.model
    def _get_report_from_name(self, report_name):
        res = super(ReportAction, self)._get_report_from_name(report_name)
        if res:
            return res
        report_obj = self.env['ir.actions.report']
        qwebtypes = ['pdf-combination']
        conditions = [('report_type', 'in', qwebtypes),
                      ('report_name', '=', report_name)]
        context = self.env['res.users'].context_get()
        return report_obj.with_context(context).search(conditions, limit=1)
