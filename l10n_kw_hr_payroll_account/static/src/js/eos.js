odoo.define('l10n_kw_hr_payroll_account.eos.tree', function (require) {
"use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');

    var QWeb = core.qweb;

    var EOSListController = ListController.extend({
        /**
         * Extends the renderButtons function of ListView by adding a button
         * on the payslip list.
         *
         * @override
         */
        renderButtons: function () {
            this._super.apply(this, arguments);
            this.$buttons.append($(QWeb.render("EOSListView.print_button", this)));
            var self = this;
            this.$buttons.on('click', '.o_button_eos', function () {
                /*if (self.getSelectedIds().length == 0) {
                    return;
                }*/
                var action = {
                type: 'ir.actions.act_window',
                name: 'New Report of End of service and leave',
                res_model: 'eos.leaves.report',
                views: [[false, 'form']],
                view_mode: 'form',
                target: 'new',
                context: {}
            }
                return self.do_action(
                                action, {
                                on_close: function () {
                                    self.update({}, {reload: true});
                                }
                            });
                
            });
        }
    });

    var EOSListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: EOSListController,
        }),
    });

    viewRegistry.add('js_eos_tree', EOSListView);

    return EOSListController;
});
