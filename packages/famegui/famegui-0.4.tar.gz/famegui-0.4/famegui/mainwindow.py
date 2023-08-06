# This Python file uses the following encoding: utf-8
import os
import logging
import getpass

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore, QtGui, QtWidgets

from famegui import models
import famegui.generated.qt_resources_rc
from famegui.generated.ui_mainwindow import Ui_MainWindow
from famegui.dialog_scenario_properties import DialogScenarioProperties
from famegui.dialog_newagent import DialogNewAgent
from famegui.dialog_newcontract import DialogNewContract
from famegui.dialog_select_schema import DialogSelectSchemas
from famegui.scenario_graph_view import ScenarioGraphView
from famegui.agent_controller import AgentController
from famegui.maincontroller import MainController
from famegui.appworkingdir import AppWorkingDir
from famegui.protobuf_generation import generate_protobuf_from_scenario_yaml_file


class PropertyTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, name, value):
        QtWidgets.QTreeWidgetItem.__init__(self, parent, [name, value])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    def setData(self, column, role, value):
        """ Override QTreeWidgetItem.setData() """
        if (role == QtCore.Qt.EditRole):
            # logging.info("new value: {}".format(value))
            pass

        QtWidgets.QTreeWidgetItem.setData(self, column, role, value)


class MainWindow(QMainWindow):
    def __init__(self, working_dir: AppWorkingDir):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._working_dir = working_dir
        self._tree_items_for_agent_types = {}
        self._controller = MainController(self._working_dir)
        # init
        self._init_ui()
        self._connect_actions()
        self._connect_slots()
        self._on_project_closed()

    def _init_ui(self):
        logging.debug("initializing main window UI")
        # create an attach the scene
        self._graph_view = ScenarioGraphView(self)
        self._graph_view.setSceneRect(0, 0, 2000, 2000)
        self.ui.graphicsView.setScene(self._graph_view)
        # customize main window
        self.ui.labelUserName.setText(getpass.getuser())
        self.ui.graphicsView.setBackgroundBrush(QtGui.QColor(230, 230, 230))
        self.setWindowTitle(
            QtWidgets.QApplication.instance().applicationDisplayName())
        # status bar
        self._status_label_icon = QtWidgets.QLabel()
        self.statusBar().addWidget(self._status_label_icon)
        # project struture tree view
        self.ui.treeProjectStructure.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.treeProjectStructure.setColumnCount(1)
        self.ui.treeProjectStructure.setHeaderLabels(["Agents"])
        # attributes tree view
        self.ui.treeAttributes.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.treeAttributes.setRootIsDecorated(False)
        self.ui.treeAttributes.setColumnCount(2)
        self.ui.treeAttributes.setHeaderLabels(["Attribute", "Value"])
        self.ui.treeAttributes.setColumnWidth(0, 140)
        self.ui.treeAttributes.setAlternatingRowColors(True)
        self.ui.treeAttributes.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

    def _connect_actions(self):
        logging.debug("conecting main window actions")
        # new
        self.ui.actionNewProject.triggered.connect(self.new_project)
        # open
        self.ui.actionOpenProject.triggered.connect(
            self.show_open_scenario_file_dlg)
        # save (enabled only when a change has been done)
        self.ui.actionSaveProject.triggered.connect(self.save_project)
        # save as
        self.ui.actionSaveProjectAs.triggered.connect(self.save_project_as)
        # close
        self.ui.actionCloseProject.triggered.connect(self.close_project)
        # generate protobuf
        self.ui.actionMakeRunConfig.triggered.connect(self.make_run_config)
        # exit
        self.ui.actionExit.triggered.connect(self.close)
        # edit
        self.ui.actionScenarioProperties.triggered.connect(
            self._on_edit_scenario_properties)

    def _connect_slots(self):
        logging.debug("initializing main window slots")
        # ui
        self.ui.sliderZoomFactor.valueChanged.connect(
            self._on_zoom_value_changed)
        self._graph_view.selected_agent_changed.connect(
            self._controller.set_selected_agent_id)
        self._graph_view.contract_creation_requested.connect(
            self._on_contract_creation_requested)
        self._graph_view.agent_creation_requested.connect(
            self._on_agent_creation_requested)
        self.ui.treeProjectStructure.currentItemChanged.connect(
            self._on_tree_view_current_item_changed)
        self.ui.lineFilterPattern.textChanged.connect(
            self._filter_pattern_changed)
        # controller
        self._controller.project_properties.changed.connect(
            self._on_scenario_status_changed)
        self._controller.agent_added.connect(self._on_agent_added)
        self._controller.contract_added.connect(self._on_contract_added)
        self._controller.selected_agent_changed.connect(
            self._on_selected_agent_changed)

    def _on_zoom_value_changed(self):
        zoomFactor = self.ui.sliderZoomFactor.value()
        assert zoomFactor > 0
        scaleFactor = zoomFactor * 0.01
        self.ui.graphicsView.setTransform(
            QtGui.QTransform.fromScale(scaleFactor, scaleFactor))
        self.ui.labelZoomFactor.setText("{} %".format(zoomFactor))

    def _on_tree_view_current_item_changed(self):
        assert self._controller.is_open

        selected_agent_id = None

        tree_item = self.ui.treeProjectStructure.currentItem()
        if tree_item is not None:
            # note: the given id value can be None
            selected_agent_id = tree_item.data(0, QtCore.Qt.UserRole)

        self._controller.set_selected_agent_id(selected_agent_id)

    def _on_agent_creation_requested(self, x: int, y: int):
        assert self._controller.is_open

        dlg = DialogNewAgent(self._controller.schema,
                             self._working_dir, self)
        if dlg.exec_() != 0:
            new_agent = dlg.make_new_agent(
                self._controller.generate_new_agent_id())
            self._controller.add_new_agent(new_agent, x, y)

    def _on_contract_creation_requested(self, sender_id: int, receiver_id: int):
        sender = self._controller.agent_from_id(sender_id)
        receiver = self._controller.agent_from_id(receiver_id)
        dlg = DialogNewContract(
            sender, receiver, self._controller.schema, self)
        if dlg.exec_() != 0:
            self._controller.add_new_contract(dlg.make_new_contract())

    def _on_selected_agent_changed(self, agent_ctrl: AgentController):
        if agent_ctrl is None:
            # clear selection
            self.ui.treeProjectStructure.clearSelection()
            self._graph_view.clearSelection()
            self.ui.treeAttributes.clear()
            return

        # block signals
        self.ui.treeProjectStructure.blockSignals(True)
        self._graph_view.blockSignals(True)

        # update graph view
        self._graph_view.clearSelection()
        agent_ctrl.scene_item.setSelected(True)
        # update tree view
        self.ui.treeProjectStructure.setCurrentItem(agent_ctrl.tree_item)
        # update agent view
        self.ui.treeAttributes.clear()
        item_type = QtWidgets.QTreeWidgetItem(self.ui.treeAttributes, [
            "Type", agent_ctrl.type_name])
        item_type.setBackgroundColor(1, agent_ctrl.svg_color)
        QtWidgets.QTreeWidgetItem(self.ui.treeAttributes, [
                                  "ID", agent_ctrl.id_str])
        for k, v in agent_ctrl.attributes.items():
            PropertyTreeItem(self.ui.treeAttributes, k, str(v))

        # unblock signals
        self.ui.treeProjectStructure.blockSignals(False)
        self._graph_view.blockSignals(False)

    def _filter_pattern_changed(self):
        pattern = self.ui.lineFilterPattern.text().lower()
        for a in self._controller.agent_list:
            hide = (a.type_name.lower().find(pattern) == -1)
            a.tree_item.setHidden(hide)

    def _tree_item_parent_for_agent(self, agent_ctrl) -> QtWidgets.QTreeWidgetItem:
        # return existing if it already exists
        if agent_ctrl.type_name in self._tree_items_for_agent_types:
            return self._tree_items_for_agent_types[agent_ctrl.type_name]
        item = QtWidgets.QTreeWidgetItem(
            self.ui.treeProjectStructure, [agent_ctrl.type_name])
        item.setExpanded(True)
        item.setBackgroundColor(0, agent_ctrl.svg_color)
        self._tree_items_for_agent_types[agent_ctrl.type_name] = item
        return item

    def _create_agent_tree_item(self, agent_ctrl: AgentController):
        parent_item = self._tree_item_parent_for_agent(agent_ctrl)
        # create tree item
        item = QtWidgets.QTreeWidgetItem(parent_item, [agent_ctrl.id_str])
        item.setBackgroundColor(0, agent_ctrl.svg_color)
        item.setData(0, QtCore.Qt.UserRole, agent_ctrl.id)
        item.setToolTip(0, agent_ctrl.tooltip_text)
        # add item
        agent_ctrl.tree_item = item
        self.ui.treeProjectStructure.addTopLevelItem(item)

    def _on_agent_added(self, agent_ctrl: AgentController):
        self._graph_view.add_agent(agent_ctrl)
        self._create_agent_tree_item(agent_ctrl)

    def _on_contract_added(self, sender: AgentController, receiver: AgentController, contract: models.Contract):
        # update scene graph
        self._graph_view.add_contract(sender, receiver)
        # update tree view
        sender_tree_item = QtWidgets.QTreeWidgetItem(
            sender.tree_item, ["{} ({})".format(receiver.id_str, contract.product_name)])
        sender_tree_item.setIcon(0, QtGui.QIcon(u":/icons/16px-login.png"))
        receiver_tree_item = QtWidgets.QTreeWidgetItem(
            receiver.tree_item, ["{} ({})".format(sender.id_str, contract.product_name)])
        receiver_tree_item.setIcon(0, QtGui.QIcon(u":/icons/16px-logout.png"))

    def _confirm_current_project_can_be_closed(self) -> bool:
        if self._controller.has_unsaved_changes:
            choice = QtWidgets.QMessageBox.warning(
                self,
                self.tr("Modifications will be lost"),
                self.tr(
                    "Modifications done to the current scenario have not been saved!\n\nWhat do you want to do?"),
                QtWidgets.QMessageBox.StandardButtons(
                    QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel),
                QtWidgets.QMessageBox.Cancel
            )
            if choice == QtWidgets.QMessageBox.Save:
                return self.save_project()
            elif choice == QtWidgets.QMessageBox.Discard:
                return True
            else:
                return False
        return True

    def _on_project_closed(self):
        self._graph_view.clear()
        # reset zoom
        self.ui.sliderZoomFactor.setValue(50)
        # reset attributes
        self._tree_items_for_agent_types = {}
        # reset scenario
        self._controller.reset()
        # reset ui
        self.ui.treeProjectStructure.clear()
        self.ui.treeAttributes.clear()
        self.ui.lineFilterPattern.clear()
        self.ui.labelProjectName.clear()

    def new_project(self):
        if not self._confirm_current_project_can_be_closed():
            return
        self._on_project_closed()

        # ask user to choose which schema to use for that new scenario
        dlg = DialogSelectSchemas(self._working_dir, self)
        if dlg.exec_() != 0:
            schema_path = dlg.selected_schema_path()
            schema = models.SchemaLoader.load_yaml_file(schema_path)
            self._controller.create_new_scenario(schema)

    def save_project(self) -> bool:
        if not self._controller.is_open:
            return False
        return self._do_save_project_as(self._controller.project_properties.file_path)

    def save_project_as(self) -> bool:
        if not self._controller.is_open:
            return False
        return self._do_save_project_as("")

    def _do_save_project_as(self, file_path: str) -> bool:
        assert self._controller.is_open

        if file_path == "":
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                self.tr("Save scenario file"),
                self._working_dir.scenarios_dir,
                "Scenario file (*.yaml *.yml)")
            if file_path == "":
                return False

        self._controller.save_to_file(file_path)
        return True

    def close_project(self) -> bool:
        if not self._confirm_current_project_can_be_closed():
            return
        self._on_project_closed()

    def show_open_scenario_file_dlg(self):
        if not self._confirm_current_project_can_be_closed():
            return

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open scenario file"),
            self._working_dir.scenarios_dir,
            self.tr("Scenario (*.yaml *.yml)"))
        if file_path != "":
            self.load_scenario_file(file_path)

    def _on_scenario_status_changed(self):
        logging.debug(
            "scenario status changed: agents={}, contracts={}".format(self._controller.agent_count, self._controller.contract_count))

        is_open = self._controller.is_open
        self.ui.treeProjectStructure.setEnabled(is_open)
        self.ui.treeAttributes.setEnabled(is_open)
        self.ui.lineFilterPattern.setEnabled(is_open)
        self.ui.graphicsView.setEnabled(is_open)
        self.ui.sliderZoomFactor.setEnabled(is_open)

        props = self._controller.project_properties
        if is_open:
            if props.file_path != "":
                self.ui.labelProjectName.setText(props.file_path)
            else:
                self.ui.labelProjectName.setText(self.tr("Unnamed scenario"))
        else:
            self.ui.labelProjectName.setText("")

        self.ui.actionSaveProject.setEnabled(props.has_unsaved_changes)
        self.ui.actionScenarioProperties.setEnabled(is_open)
        self.ui.actionMakeRunConfig.setEnabled(
            self._controller.can_export_protobuf)

        # update status bar
        if self._controller.agent_count > 0:
            if props.is_validation_successful:
                self._status_label_icon.setPixmap(":/icons/success-16px.png")
                self._status_label_icon.setToolTip(
                    self.tr("Schema validation succeeded"))
            else:
                self._status_label_icon.setPixmap(":/icons/warning-16px.png")
                self._status_label_icon.setToolTip(
                    self.tr("Schema validation failed"))
        else:
            self._status_label_icon.clear()

    def _ask_user_to_select_new_schema(self, title: str, reason_msg: str) -> str:
        QtWidgets.QMessageBox.warning(self, title, reason_msg)
        dlg = DialogSelectSchemas(self._working_dir, self)
        if dlg.exec_() != 0:
            return dlg.selected_schema_path()
        return ""

    def _confirm_schema_file_to_use(self, schema_path: str, scenario_path: str) -> str:
        assert os.path.isabs(scenario_path)

        if schema_path == "":
            logging.info("no schema file specified, asking user to select one")
            return self._ask_user_to_select_new_schema(
                self.tr("No schema defined"),
                self.tr("This scenario does not define any schema file.\n\n"
                        "Please select an existing schema to be used for that scenario.")
            )

        # if not absolute, the schema path is relative to the scenario file itself, and NOT the working dir
        original_schema_path = schema_path
        if not os.path.isabs(schema_path):
            scenario_dir = os.path.dirname(scenario_path)
            schema_path = os.path.join(scenario_dir, schema_path)
            schema_path = os.path.abspath(schema_path)
            logging.info("schema relative file path '{}' was resolved to '{}'".format(
                original_schema_path, schema_path))

        if not os.path.isfile(schema_path):
            logging.error(
                "failed to locate schema file '{}', asking user to select a new one".format(schema_path))
            return self._ask_user_to_select_new_schema(
                self.tr("Unknown schema"),
                self.tr("This scenario is linked to the schema file '{}' which could not be located.\n\n"
                        "Please select an existing schema for that scenario.".format(original_schema_path))
            )

        return schema_path

    def load_scenario_file(self, file_path):
        self._on_project_closed()
        file_path = os.path.abspath(file_path)
        try:
            logging.info("opening scenario file {}".format(file_path))
            scenario_model = models.ScenarioLoader.load_yaml_file(file_path)

            # make sure to attach a valid schema
            schema_path = self._confirm_schema_file_to_use(
                scenario_model.schema_path, file_path)
            if schema_path == "":
                logging.warning(
                    "no schema specified: can't finalize the load of {}".format(file_path))
                self._on_project_closed()
                return

            logging.info("opening schema file '{}'".format(schema_path))
            schema = models.SchemaLoader.load_yaml_file(schema_path)

            self._controller.open_scenario(
                scenario_model, file_path, schema)
        except:
            self._on_project_closed()
            raise

        props = self._controller.project_properties
        if not props.is_validation_successful:
            QtWidgets.QMessageBox.warning(self,
                                          self.tr("Validation failure"),
                                          self.tr("The loaded scenario does not fulfill the schema:\n\n") +
                                          "\n".join(props.validation_errors))

    def _on_edit_scenario_properties(self):
        dlg = DialogScenarioProperties(
            self._controller.scenario.properties, self._working_dir, self)
        dlg.setWindowTitle(self.tr("Scenario properties"))
        if dlg.exec_() != 0:
            self._controller.set_scenario_properties(dlg.make_properties())

    def make_run_config(self):
        assert self._controller.can_export_protobuf
        scenario_name = os.path.basename(
            self._controller.project_properties.file_path).replace(".yaml", "")
        output_path = "{}/{}.pb".format(
            self._working_dir.protobuf_dir, scenario_name)
        output_path = self._working_dir.make_relative_path(output_path)

        dlg = DialogScenarioProperties(
            self._controller.scenario.properties, self._working_dir, self)
        dlg.setWindowTitle(self.tr("Make run config"))
        dlg.enable_outputfile_selection(output_path)
        if dlg.exec_() != 0:
            self._controller.set_scenario_properties(dlg.make_properties())
            self.save_project()
            output_path = self._working_dir.make_full_path(
                dlg.get_output_file_path())

            progressDlg = QtWidgets.QProgressDialog(self)
            progressDlg.setLabelText(self.tr("Generating protobuf file..."))
            progressDlg.setRange(0, 0)
            progressDlg.setCancelButton(None)

            try:
                progressDlg.show()
                QApplication.processEvents()
                generate_protobuf_from_scenario_yaml_file(self._working_dir.root_dir,
                                                          self._controller.project_properties.file_path,
                                                          output_path)
            finally:
                progressDlg.close()

            QtWidgets.QMessageBox.information(
                self,
                self.tr("Operation succeeded"),
                self.tr("The following file was successfully generated:\n{}").format(output_path))

    # prevent data loss when closing the main window
    def closeEvent(self, event):
        if not self._confirm_current_project_can_be_closed():
            event.ignore()
        else:
            event.accept()
