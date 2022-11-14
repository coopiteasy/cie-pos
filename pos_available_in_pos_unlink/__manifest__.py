# Copyright 2017 - 2020 BEES coop SCRLfs
#   - Elouan Lebars <elouan@coopiteasy.be>
#   - Rémy Taymans <remy@coopiteasy.be>
#   - Vincent Van Rossem <vincent@coopiteasy.be>
#   - Elise Dupont
#   - Thibault François
#   - Grégoire Leeuwerck
#   - Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "POS - Unavailable for Sale",
    "summary": """Maintains "Available in POS" (`available_in_pos`)
    value when unchecking "Can be Sold" (`sale_ok`).""",
    "author": "BEES coop - Cellule IT, Coop IT Easy SC",
    "website": "https://coopiteasy.be",
    "category": "Point Of Sale",
    "version": "12.0.2.0.1",
    "depends": ["point_of_sale"],
    "qweb": ["static/src/xml/templates.xml"],
    "installable": True,
    "license": "AGPL-3",
}
