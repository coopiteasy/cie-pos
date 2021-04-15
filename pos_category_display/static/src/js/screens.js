odoo.define('pos_category_display.screens', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    screens.ProductCategoriesWidget.include({
        renderElement: function() {
            this._super();
            if (this.pos.config.pos_category_display === 'minimized') {
                var buttons = this.el.querySelectorAll('.js-category-switch');
                for (var i = 0; i < buttons.length; i++) {
                    buttons[i].removeEventListener('click', this.switch_category_handler);
                }
            }
        }
    })

    screens.ProductScreenWidget.include({
        show: function(){
            this._super();
            var $breadcrumbs = this.$('.breadcrumbs')
            var $categories = this.$('.categories')
            var $searchbox_input = this.$('.searchbox input')
            if (this.pos.config.pos_category_display === 'minimized'){
                $breadcrumbs.hide();
                $categories.hide();
                $searchbox_input.removeAttr('placeholder');
                // TODO toggle class to expand/reduce input

            }
        },
    });
});
