##############################################################################
#
#    Copyright (C) 2017- Coop IT Easy.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "POS Products Display Customization",
    "version": "12.0.1.0.0",
    "depends": ["point_of_sale", "beesdoo_product"],
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "website": "https://coopiteasy.be",
    "summary": """
        Adds information on POS product card.
        - display weight
        - producers
    """,
    "data": ["views/assets.xml"],
    "qweb": ["static/src/xml/pos_products.xml"],
    "installable": True,
}
