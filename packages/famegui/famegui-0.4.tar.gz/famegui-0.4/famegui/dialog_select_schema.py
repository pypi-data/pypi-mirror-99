import typing
import logging

from PySide2 import QtWidgets
from .generated.ui_dialog_select_schema import Ui_DialogSelectSchemas
from famegui.appworkingdir import AppWorkingDir


class DialogSelectSchemas(QtWidgets.QDialog):

    def __init__(self, working_dir: AppWorkingDir, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_DialogSelectSchemas()
        self._working_dir = working_dir
        self._ui.setupUi(self)
        # init
        self.setWindowTitle(self.tr("Select schema file"))
        self._ui.comboBoxSchemas.addItems(
            self._working_dir.list_existing_schema_files())

    def selected_schema_path(self) -> str:
        selected_schema = self._ui.comboBoxSchemas.currentText()
        logging.info("selected schema: {}".format(selected_schema))
        return self._working_dir.make_full_path(selected_schema)
