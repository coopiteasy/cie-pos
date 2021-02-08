import logging
import os

from checksumdir import dirhash

from odoo import api, fields, models
from odoo.tools.config import config

_logger = logging.getLogger(__name__)

CERT_DIR = config.get("certified_modules_directory", "pos_certified_modules")
USER_DIR = os.path.expanduser("~")


class ModuleHash(models.Model):
    _inherit = "ir.module.module"

    hash = fields.Char(compute="_compute_hash", help="Module hash")

    @api.multi
    def _compute_hash(self):

        _logger.info("[pos_hash_cert] USER_DIR = %s" % USER_DIR)
        start_dir = os.path.dirname(os.path.realpath(__file__))
        _logger.info("[pos_hash_cert] start_DIR = %s" % start_dir)

        last_root = start_dir
        current_root = start_dir
        found_cert_dir = None

        while found_cert_dir is None and current_root != os.path.dirname(
            USER_DIR
        ):
            pruned = False
            for root, dirs, _ in os.walk(current_root):
                if not pruned:
                    try:
                        # Remove the part of the tree we already searched
                        del dirs[dirs.index(os.path.basename(last_root))]
                        pruned = True
                    except ValueError:
                        pass
                if CERT_DIR in dirs:
                    # found the directory, stop
                    found_cert_dir = os.path.join(root, CERT_DIR)
                    break
                # Otherwise, pop up a level, search again
            last_root = current_root
            current_root = os.path.dirname(last_root)

        if found_cert_dir:
            _logger.info(
                "[pos_hash_cert] found_cert_dir = %s" % found_cert_dir
            )
            certified_modules = [
                name
                for name in os.listdir(found_cert_dir)
                if os.path.isdir(os.path.join(found_cert_dir, name))
            ]

            for record in self:
                if record.name in certified_modules:
                    record.hash = dirhash(
                        found_cert_dir, "sha256", excluded_extensions=["pyc"]
                    )
                    _logger.info(
                        "[pos_hash_cert] '%s' with hash '%s'"
                        % (record.name, record.hash)
                    )
        else:
            _logger.info(
                "[pos_hash_cert] no certified modules directory found"
            )
            pass
