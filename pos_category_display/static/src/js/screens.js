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
        },
        clear_search: function () {
            this._super();
            var _super = this._super.bind(this);
            var input = this.el.querySelector(".searchbox input");
            input.disabled = false;
            input.style.width = "100px";
            input.style["padding-right"] = "20px";
            input.focus();

            input.onblur = function() {
                if (!input.value) {
                    input.disabled = true;
                    input.style.width = 0;
                    input.style["padding-right"] = "4px";
                    _super();
                }
            };
        },
    });

    screens.ProductScreenWidget.include({
        show: function(){
            this._super();
            var $breadcrumbs = this.$('.breadcrumbs')
            var $categories = this.$('.categories')
            var $searchbox_input = this.$('.searchbox input')
            if (this.pos.config.pos_category_display === 'minimized'){
                $breadcrumbs.hide();
                $categories.hide();
                $searchbox_input.removeAttr("placeholder");
                $searchbox_input.prop("disabled", true);
                $searchbox_input.css({ width: 0, "padding-right": 4 });
            }
        },
    });
});
