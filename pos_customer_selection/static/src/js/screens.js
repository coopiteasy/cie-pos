odoo.define('pos_customer_selection.screens', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    screens.ClientListScreenWidget.include({
        show: function () {
            this._super();
            this.$('.searchbox input').focus();
        },

        line_select: function (event, $line, id) {
            this._super(event, $line, id);
            this.$('.next').click();
        },
    });
});
