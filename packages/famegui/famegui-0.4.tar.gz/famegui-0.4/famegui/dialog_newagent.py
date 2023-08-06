import logging
import os
import typing
from PySide2 import QtCore, QtGui, QtWidgets

from .generated.ui_dialog_newagent import Ui_DialogNewAgent
from famegui import models
from famegui.appworkingdir import AppWorkingDir


class FileChooserWidget(QtWidgets.QWidget):
    selected_path_changed = QtCore.Signal(str)

    def __init__(self, working_dir: AppWorkingDir, parent: QtWidgets.QWidget = None):
        QtWidgets.QWidget.__init__(self, parent)
        self._working_dir = working_dir
        # layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        # line edit (file path)
        self._line_edit = QtWidgets.QLineEdit(self)
        self._line_edit.setPlaceholderText(self.tr("Please enter file path"))
        self._line_edit.textChanged.connect(self._on_text_edit_changed)
        layout.addWidget(self._line_edit)
        # button (to open dialog box)
        button = QtWidgets.QPushButton("...", self)
        button.setToolTip(self.tr("Select file..."))
        button.setFixedWidth(button.fontMetrics().width(button.text()) + 10)
        layout.addWidget(button)
        # connect
        button.clicked.connect(self._on_button_clicked)

    def _on_button_clicked(self):
        open_location = self._working_dir.timeseries_dir
        if self._line_edit.text() != "":
            full_edit_path = self._working_dir.make_full_path(
                self._line_edit.text())
            if os.path.isfile(full_edit_path):
                open_location = full_edit_path

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open time series file"),
            open_location,
            self.tr("Time series (*.csv);;All files (*.*)"))
        if file_path != "":
            file_path = self._working_dir.make_relative_path(file_path)
            self._line_edit.setText(file_path)

    def _on_text_edit_changed(self, value: str):
        self.selected_path_changed.emit(value)


class AttributeTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent: QtWidgets.QTreeWidget, attr: models.SchemaAttribute, working_dir: AppWorkingDir):
        self._attr = attr
        self._working_dir = working_dir
        self._attr_value = None
        self._display_error = (lambda has_error: None)

        QtWidgets.QTreeWidgetItem.__init__(
            self, parent, [self._attr.name])

        if self._attr.is_mandatory:
            font = self.font(0)
            font.setBold(True)
            self.setFont(0, font)
            self.setToolTip(0, "{} (mandatory)".format(
                self._attr.type_name))
        else:
            self.setToolTip(0, self._attr.type_name)

        parent.setItemWidget(
            self, 1, self._create_edit_widget(self._attr))

    @property
    def attr_name(self) -> str:
        return self._attr.name

    @property
    def attr_value(self):
        return self._attr_value

    @property
    def validation_error(self) -> str:
        if self._attr.is_mandatory:
            if self._attr_value is None:
                return "mandatory attribute {} is not defined".format(self.attr_name)
        return None

    def _create_edit_widget(self, attr_type: models.SchemaAttribute) -> QtWidgets.QWidget:
        if attr_type.type == models.AttributeType.ENUM:
            comboBox = QtWidgets.QComboBox()
            enums = [""]
            enums.extend(attr_type.enum_values)
            comboBox.addItems(enums)
            if len(enums) == 2:
                comboBox.setCurrentIndex(1)
                self._attr_value = enums[1]
            comboBox.currentTextChanged.connect(self._on_enum_value_changed)
            return comboBox
        elif attr_type.type == models.AttributeType.TIME_SERIES:
            file_chooser = FileChooserWidget(self._working_dir)
            file_chooser.selected_path_changed.connect(
                self._on_time_series_path_changed)
            return file_chooser
        elif attr_type.type == models.AttributeType.INTEGER:
            line_edit = self._create_line_edit(
                "0", self._on_integer_value_changed)
            line_edit.setValidator(QtGui.QIntValidator())
            return line_edit
        elif attr_type.type == models.AttributeType.DOUBLE:
            line_edit = self._create_line_edit(
                "0.0", self._on_double_value_changed)
            validator = QtGui.QDoubleValidator()
            # accept '.' as decimal separator
            validator.setLocale(QtCore.QLocale.English)
            line_edit.setValidator(validator)
            return line_edit
        elif attr_type.type == models.AttributeType.DOUBLE_LIST:
            return self._create_line_edit("1.0, 3.5, 5", self._on_double_list_changed)
        else:
            logging.error(
                "can't create editor: unknown attribute type '{}'".format(attr_type.type))
            return None

    def _create_line_edit(self, placeholder_text: str, handler) -> QtWidgets.QLineEdit:
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.textChanged.connect(handler)
        self._display_error = (lambda has_error: line_edit.setStyleSheet(
            "QLineEdit { background: '#F66257'; }") if has_error else line_edit.setStyleSheet(""))
        return line_edit

    def _on_enum_value_changed(self, value: str):
        assert value == "" or value in self._attr.enum_values
        self._attr_value = value if value != "" else None

    def _on_time_series_path_changed(self, value: str):
        if value == "":
            self._attr_value = None
        else:
            self._attr_value = value
            if self._working_dir.find_existing_child_file(value) is None:
                logging.warning("invalid time series file path '{}' for attribute '{}'".format(
                    value, self._attr.name))

    def _on_integer_value_changed(self, value: str):
        try:
            self._attr_value = int(value) if value != "" else None
            self._display_error(False)
        except:
            self._display_error(True)
            logging.warning("invalid integer value '{}' for attribute '{}'".format(
                value, self._attr.name))
            self._attr_value = None

    def _on_double_value_changed(self, value: str):
        try:
            self._attr_value = float(value) if value != "" else None
            self._display_error(False)
        except:
            self._display_error(True)
            logging.warning("invalid double value '{}' for attribute '{}'".format(
                value, self._attr.name))
            self._attr_value = None

    def _on_double_list_changed(self, value: str):
        self._attr_value = None
        self._display_error(False)
        if value == "":
            return

        try:
            self._attr_value = []
            for str in value.split(","):
                self._attr_value.append(float(str.strip()))
        except:
            self._attr_value = None
            self._display_error(True)
            logging.warning("invalid double list value '{}' for attribute '{}'".format(
                value, self._attr.name))


class DialogNewAgent(QtWidgets.QDialog):

    def __init__(self, schema: models.Schema, working_dir: AppWorkingDir, parent=None):
        QtWidgets.QDialog.__init__(self, parent=None)
        self._ui = Ui_DialogNewAgent()
        self._ui.setupUi(self)
        self._schema = schema
        self._working_dir = working_dir
        self._tree_items = []
        # init
        self.setWindowTitle(self.tr("New agent"))
        self._ui.comboBoxType.addItems(self._schema.agent_types.keys())

        # tree view
        self._ui.treeWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self._ui.treeWidget.setRootIsDecorated(False)
        self._ui.treeWidget.setColumnCount(2)
        self._ui.treeWidget.setHeaderLabels(
            [self.tr("Attribute"), self.tr("Value")])
        self._ui.treeWidget.setColumnWidth(0, 200)
        self._ui.treeWidget.setAlternatingRowColors(True)
        self._reset_attributes()

        # connect slots
        self._ui.comboBoxType.currentTextChanged.connect(
            self._reset_attributes)

    def accept(self):
        if self._confirm_attributes_are_valid():
            super().accept()

    def _reset_attributes(self):
        self._ui.treeWidget.clear()
        self._tree_items.clear()

        current_agent_type = self._ui.comboBoxType.currentText()
        for attr in self._schema.agent_types[current_agent_type].attributes.values():
            item = AttributeTreeItem(
                self._ui.treeWidget, attr, self._working_dir)
            self._tree_items.append(item)

    def _confirm_attributes_are_valid(self) -> bool:
        errors = ""
        for item in self._tree_items:
            if item.validation_error != None:
                errors += "- {}\n".format(item.validation_error)

        if errors == "":
            return True

        choice = QtWidgets.QMessageBox.warning(
            self,
            self.tr("All attributes are not valid"),
            self.tr(
                "The new agent won't be valid:\n{}\nDo you want to continue?".format(errors)),
            QtWidgets.QMessageBox.StandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
            QtWidgets.QMessageBox.No
        )
        return choice == QtWidgets.QMessageBox.Yes

    def make_new_agent(self, agent_id) -> models.Agent:
        agent_type = self._ui.comboBoxType.currentText()
        agent = models.Agent(agent_id, agent_type)
        for item in self._tree_items:
            if item.attr_value != None:
                agent.add_attribute(item.attr_name, item.attr_value)
        return agent
