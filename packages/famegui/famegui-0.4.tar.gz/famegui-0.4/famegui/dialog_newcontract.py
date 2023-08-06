from PySide2.QtWidgets import QDialog, QDialogButtonBox

from .generated.ui_dialog_newcontract import Ui_DialogNewContract

from famegui import models
from famegui.agent_controller import AgentController


class DialogNewContract(QDialog):

    def __init__(self, sender: AgentController, receiver: AgentController, schema: models.Schema, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_DialogNewContract()
        self._ui.setupUi(self)
        self._sender = sender
        self._receiver = receiver

        self.setWindowTitle(self.tr("New contract"))
        self._ui.labelDescr.setText(self.tr(
            '<html><head/><body>'
            '<p>Create new contract between:</p>'
            '<ul>'
            '<li>Sender: agent <b>{}</b> of type <b>{}</b></li>'
            '<li>Receiver: agent <b>{}</b> of type <b>{}</b></li>'
            '</ul>'
            '</body></html>').format(sender.id_str, sender.type_name, receiver.id_str, receiver.type_name))

        # fill possible products to select based on the sender SchemaAgentType
        sender_type = schema.agent_type_from_name(sender.type_name)
        assert sender_type is not None
        self._ui.comboBoxProduct.addItems(sender_type.products)

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(
            self._update_ok_button_status)
        self._update_ok_button_status()

    def make_new_contract(self) -> models.Contract:
        return models.Contract(
            self._sender.id,
            self._receiver.id,
            self._ui.comboBoxProduct.currentText(),
            self._ui.spinBoxDeliveryInterval.value(),
            self._ui.spinBoxFirstDelivery.value()
        )

    def _update_ok_button_status(self):
        all_fields_ok = self._ui.comboBoxProduct.currentText() != ""
        self._ui.buttonBox.button(
            QDialogButtonBox.Ok).setEnabled(all_fields_ok)
