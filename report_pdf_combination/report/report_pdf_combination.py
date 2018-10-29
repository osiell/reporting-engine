# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from io import BytesIO
from base64 import b64decode

from odoo import models

import logging
_logger = logging.getLogger(__name__)


try:
    from PyPDF2 import PdfFileMerger
except ImportError:
    _logger.debug('Can not import PyPDF2.PdfFileMerger.')


class ReportXlsxAbstract(models.AbstractModel):
    _name = 'report.report_pdf_combination.abstract'

    def create_pdf_combination_report(self, docids, data):
        objs = self.env[self.env.context.get('active_model')].browse(docids)
        file_list = self.get_files_for_pdf_combination_report(data, objs)
        merger = PdfFileMerger()
        self.configure_merger(merger)
        for f in file_list:
            merger.append(f)
        file_data = BytesIO()
        merger.write(file_data)
        file_data.seek(0)
        return file_data.read(), 'pdf-combination'

    def configure_merger(self, merger):
        # For posible configurations
        # see https://pythonhosted.org/PyPDF2/PdfFileMerger.html
        pass

    def get_files_for_pdf_combination_report(self, data, objs):
        report_id = self.env.context.get('current_report_to_use', False)
        if not report_id:
            raise NotImplementedError()
        report = self.env['ir.actions.report'].browse(report_id)
        if not report.combination_line_ids:
            raise NotImplementedError()
        file_list = []
        for line in report.combination_line_ids:
            if line.type == 'static_pdf_file':
                file_list.append(BytesIO(b64decode(line.static_pdf_file)))
            elif line.type == 'action_report':
                file_list.append(
                    BytesIO(line.report_id.render(objs.ids, data=data)[0]))
        return file_list
