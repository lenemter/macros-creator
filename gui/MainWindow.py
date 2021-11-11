import traceback
from pathlib import Path
from typing import Optional, Any, Union

from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel, QAbstractTableModel, QRect, QSize, \
    pyqtSignal, QDir, QItemSelectionModel
from PyQt5.QtGui import QFont, QIcon, QDropEvent, QDragMoveEvent, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTreeView, QPushButton, QMenuBar, \
    QMenu, QAction, QSizePolicy, QStyledItemDelegate, QAbstractItemView, QHBoxLayout, QTableView, \
    QFileDialog, QMessageBox, QSpacerItem

import runner
from actions.Action import Action
from gui.SettingsDialog import SettingsDialog
from gui.icons_handler import get_action_icon
from utils import get_path

HOME = str(Path.home())
DEFAULT_OPENED_FILE = 'untitled.mcrc'
DEFAULT_SETTINGS = {
    'time_between': 0.0
}
FILE_FILTERS = '.mcrc XML (*.mcrc);; .mcrc CSV (*.mcrc);; .mcrc DB (*.mcrc)'


class NewActionTreeNode:
    """Node for NewActionTreeModel class"""

    def __init__(self, data):
        self._data = data
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column) -> Optional[str]:
        if column == 0:
            if self._data is None:
                return None
            if type(self._data) == str:
                return self._data
            return self._data.name

    @staticmethod
    def columnCount() -> int:
        return 1

    def childCount(self) -> int:
        return len(self._children)

    def child(self, row):
        if 0 <= row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self) -> int:
        return self._row

    def addChild(self, child) -> None:
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)


class NewActionTreeModel(QAbstractItemModel):
    """Model for new_action_tree"""

    def __init__(self, nodes):
        super().__init__()
        self._root = NewActionTreeNode(None)
        for node in nodes:
            self._root.addChild(node)

    @property
    def root(self) -> NewActionTreeNode:
        return self._root

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, node, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        parent.addChild(node)

    def index(self, row: int, column: int, _parent: QModelIndex = None) -> QModelIndex:
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QModelIndex()

        child = parent.child(row)
        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        return QModelIndex()

    def parent(self, child: QModelIndex) -> QModelIndex:
        if child.isValid():
            parent = child.internalPointer().parent()
            if parent:
                return QAbstractItemModel.createIndex(self, parent.row(), 0, parent)
            return QModelIndex()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.data(index.column())
        if role == Qt.DecorationRole:
            if not isinstance(node._data, str):
                return QIcon(get_path(get_action_icon(node._data)))
        if role == Qt.UserRole:
            return node._data
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # Enable Drag and Drop only for actual items, not titles
        default_flags = QAbstractItemModel.flags(self, index)
        if self.data(self.parent(index), Qt.DisplayRole) == self._root.data(0):
            return default_flags
        return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | default_flags


class BoldDelegate(QStyledItemDelegate):
    """Custom item delegate for new_action_tree. Makes headers bold"""

    def __init__(self, model):
        super().__init__()
        self.model = model

    def paint(self, painter, option, index):
        if self.model.data(self.model.parent(index), Qt.DisplayRole) == self.model.root.data(0):
            option.font.setWeight(QFont.Bold)
        QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index: QModelIndex) -> QSize:
        return QSize(100, 24)


def create_table_index(model: Union[QAbstractItemModel, QAbstractTableModel], row: int,
                       column: int) -> QModelIndex:
    return QAbstractTableModel.index(model, row, column)


class ActionsModel(QAbstractTableModel):
    """Model for ActionsTable"""

    def __init__(self, items: list):
        super().__init__()
        self._data = items

    @property
    def actions(self) -> list:
        return self._data.copy()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Union[
        int, str]:
        if role == Qt.DisplayRole:
            if orientation == Qt.PortraitOrientation:
                return ['Action', 'Comment'][section]
            else:
                return section + 1

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._data[index.row()].name
            else:
                return self._data[index.row()].comment
        if role == Qt.UserRole:
            return self._data[index.row()]

    def setData(self, index: QModelIndex, value, role=Qt.EditRole) -> bool:
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            if column == 0:
                self._data[row] = value
                self.dataChanged.emit(index, index)
            else:
                print('WHY')
                return False
            return True
        return QAbstractTableModel.setData(self, index, value, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        last_inserted_row = row + count - 1
        self.beginInsertRows(QModelIndex(), row, last_inserted_row)
        for i in range(count):
            self._data.insert(row + i, None)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        last_removed_row = row + count - 1
        self.beginRemoveRows(QModelIndex(), row, last_removed_row)
        for i, j in enumerate(range(count)):
            del self._data[row + j - i]
        self.endRemoveRows()
        return True

    def move_up(self, rows):
        # if rows in the start and go in a row
        if rows[-1] - rows[0] + 1 == len(rows) and rows[0] == 0:
            return None

        for row in rows:
            next_row = max(row - 1, 0)
            if row != next_row:
                self._data[next_row], self._data[row] = self._data[row], self._data[next_row]
                index = create_table_index(self, row, 0)
                index_1 = create_table_index(self, next_row, 0)
                self.dataChanged.emit(index, index_1)

    def move_down(self, rows):
        # if rows in the end and go in a row
        if rows[-1] - rows[0] + 1 == len(rows) and rows[-1] == self.rowCount() - 1:
            return None

        for row in reversed(rows):
            next_row = min(row + 1, self.rowCount() - 1)
            if row != next_row:
                self._data[next_row], self._data[row] = self._data[row], self._data[next_row]
                index = create_table_index(self, row, 0)
                index_1 = create_table_index(self, next_row, 0)
                self.dataChanged.emit(index, index_1)


class ActionsTable(QTableView):
    """Table with drag-and-drop and move up/down functions"""

    addActionSignal = pyqtSignal()
    actionAddedSignal = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.horizontalHeader().resizeSection(0, 150)
        self.horizontalHeader().setStretchLastSection(True)
        font = self.horizontalHeader().font()
        font.setBold(True)
        self.horizontalHeader().setFont(font)

        self.setModel(ActionsModel([]))

    @property
    def selected_rows(self) -> list:
        return sorted(set(index.row() for index in self.selectedIndexes()))

    def dragEnterEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.source() == self:
            model = self.model()
            rows = self.selected_rows
            target_row = self.indexAt(event.pos()).row()

            if rows[0] == target_row:
                return None
            if rows[-1] - rows[0] == len(
                    rows) and target_row == -1:  # if rows in the end and go in a row
                return None
            if target_row == -1:
                target_row = model.rowCount()
            if len(rows) == 1 and rows[0] == target_row - 1:
                return None

            row_mapping = dict()  # Source rows to target rows
            offset = target_row - rows[0]
            max_row = model.rowCount() + len(rows)
            for row in rows:
                new_row = row + offset
                if row + offset >= max_row:
                    new_row -= 1
                if row < target_row:
                    row_mapping[row] = new_row
                else:
                    row_mapping[row + len(rows)] = new_row
            for row in row_mapping.values():
                model.insertRow(row)
            for source_row, target_row in sorted(row_mapping.items()):
                index = create_table_index(model, target_row, 0)
                model.setData(index, model.actions[source_row])
            for row in sorted(row_mapping.keys(), reverse=True):
                model.removeRow(row)
            event.accept()

        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
            self.addActionSignal.emit()

    def create_action(self, action_cls, row=-1):
        model = self.model()
        if row == -1:
            row = model.rowCount()
        action = action_cls()
        model.insertRow(row)
        index = create_table_index(model, row, 0)
        model.setData(index, action)
        self.actionAddedSignal.emit(row)

    def move_items_up(self):
        rows = self.selected_rows
        self.model().move_up(rows)
        self.move_selection_up(rows)

    def move_items_down(self):
        rows = self.selected_rows
        self.model().move_down(rows)
        self.move_selection_down(rows)

    def move_selection_up(self, rows):
        # if rows in the start and go in a row
        if rows[-1] - rows[0] + 1 == len(rows) and rows[0] == 0:
            return None

        self.clearSelection()
        model = self.model()
        selection_model = self.selectionModel()
        for row in rows:
            next_row = max(row - 1, 0)
            selection_model.select(create_table_index(model, next_row, 0),
                                   QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def move_selection_down(self, rows):
        model = self.model()
        row_count = model.rowCount()

        # if rows in the end and go in a row
        if rows[-1] - rows[0] + 1 == len(rows) and rows[-1] == row_count - 1:
            return None

        self.clearSelection()
        selection_model = self.selectionModel()
        for row in rows:
            next_row = min(row + 1, row_count - 1)
            selection_model.select(create_table_index(model, next_row, 0),
                                   QItemSelectionModel.Select | QItemSelectionModel.Rows)


def create_actions_categories_dict() -> dict:
    """Creates dict with categories as keys and classes as values"""
    categories = dict()
    for cls in Action.__subclasses__():
        category = cls.category
        if category in categories:
            categories[category].append(cls)
        else:
            categories[category] = [cls]
    return categories


def create_action_tree_items() -> list:
    """Creates list with NewActionTreeNodes for NewActionTreeModel"""
    items = []
    categories = create_actions_categories_dict()
    # Use this dict to create Tree items
    for category in categories.keys():
        items.append(NewActionTreeNode(category))
        for cls in categories[category]:
            items[-1].addChild(NewActionTreeNode(cls))
    return items


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._opened_file = None
        self.opened_file = DEFAULT_OPENED_FILE
        self.opened_file_filter = None
        self.settings = DEFAULT_SETTINGS

        self.init_ui()

        # Signals
        self.actions_table.addActionSignal.connect(self.add_new_action)
        self.new_action_tree.doubleClicked.connect(self.add_new_action)
        self.actions_table.actionAddedSignal.connect(self.action_added)

        self.run_button.clicked.connect(self.run)
        self.move_up_button.clicked.connect(self.actions_table.move_items_up)
        self.move_down_button.clicked.connect(self.actions_table.move_items_down)
        self.delete_button.clicked.connect(self.delete)
        self.settings_button.clicked.connect(self.open_settings_dialog)

        self.actions_table.doubleClicked.connect(self.open_action_edit_dialog)

        self.action_new.triggered.connect(self.file_new)
        self.action_open.triggered.connect(self.file_open)
        self.action_save.triggered.connect(self.file_save)
        self.action_save_as.triggered.connect(self.file_save_as)
        self.action_close.triggered.connect(self.file_close)

    @property
    def opened_file(self):
        return self._opened_file

    @opened_file.setter
    def opened_file(self, value):
        if not isinstance(value, str):
            raise ValueError('Opened file is not a string')
        self._opened_file = value
        self.setWindowTitle(f'{self._opened_file}[*]')

        if hasattr(self, 'action_save'):
            if value == DEFAULT_OPENED_FILE:
                self.action_save.setText('Save...')
            else:
                self.action_save.setText('Save')

    # Qt methods

    def closeEvent(self, event: QCloseEvent) -> None:
        """Ask user to save his work before closing"""
        reply = self.ask_save_question()
        if reply == QMessageBox.AcceptRole:
            return_code = self.file_save()
            if return_code == 1:  # If user did not save the file
                event.ignore()
            else:
                event.accept()
        elif reply == QMessageBox.DestructiveRole:
            event.accept()
        else:
            event.ignore()

    # Utility methods

    def handle_exception(self, exception: Exception):
        """Handles exceptions in run() and open_file()"""
        self.show_error(
            f'An error occurred: {getattr(exception, "message", repr(exception))}',
            str(traceback.format_exc())
        )

    def ask_save_question(self) -> QMessageBox.ButtonRole:
        """Asks user to save his work. Used in new_file() and open_file()"""
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText('Do you want to save your changes?')
        message_box.setWindowTitle('Save changes')
        close_button = QPushButton(QIcon(get_path('gui/icons/edit-delete.svg')),
                                   'Close without saving')
        message_box.addButton(close_button, QMessageBox.DestructiveRole)
        cancel_button = QPushButton(QIcon(get_path('gui/icons/dialog-cancel.svg')),
                                    'Cancel')
        message_box.addButton(cancel_button, QMessageBox.RejectRole)
        save_button = QPushButton(QIcon(get_path('gui/icons/document-save.svg')),
                                  'Save' if self.opened_file != DEFAULT_OPENED_FILE else 'Save...')
        message_box.addButton(save_button, QMessageBox.AcceptRole)
        message_box.setDefaultButton(save_button)

        message_box.exec()
        return message_box.buttonRole(message_box.clickedButton())

    def show_error(self, message: str, detailed_text=None):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Error")
        message_box.setIcon(QMessageBox.Critical)
        message_box.setText(message)
        if detailed_text is not None:
            message_box.setDetailedText(detailed_text)
        ok_button = QPushButton(QIcon(get_path('gui/icons/dialog-ok-apply.svg')),
                                'Ok')
        message_box.addButton(ok_button, QMessageBox.AcceptRole)
        message_box.setDefaultButton(ok_button)

        message_box.exec()

    # New action methods

    def add_new_action(self):
        model = self.new_action_tree.model()
        index = self.new_action_tree.currentIndex()
        action_cls = model.data(index, Qt.UserRole)
        if not isinstance(action_cls, str):
            self.actions_table.create_action(action_cls)

    def action_added(self, row):
        model = self.actions_table.model()
        index = create_table_index(model, row, 0)
        action = model.data(index, Qt.UserRole)  # get selected action
        action.open_edit_dialog(self)

    # Buttons methods

    def run(self):
        try:
            runner.run(self.actions_table.model().actions, self.settings)
        except Exception as e:
            self.handle_exception(e)

    def delete(self):
        selected_rows = self.actions_table.selected_rows
        if selected_rows:
            for i, row in enumerate(selected_rows):
                self.actions_table.model().removeRow(row - i)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self, self.settings)
        dialog.exec()
        self.settings = dialog.get_settings()

    # Table methods

    def open_action_edit_dialog(self):
        row = self.actions_table.selected_rows[0]
        model = self.actions_table.model()
        index = create_table_index(model, row, 0)
        action = model.data(index, Qt.UserRole)  # get selected action
        action.open_edit_dialog(self)

    # Menubar methods

    def file_new(self):
        file_dialog = QFileDialog(self,
                                  'Create new file',
                                  HOME,
                                  FILE_FILTERS)
        file_dialog.setFilter(file_dialog.filter() | QDir.Hidden)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix('mcrc')
        if file_dialog.exec() == QFileDialog.Accepted:
            reply = self.ask_save_question()
            if reply == QMessageBox.Accepted:
                return_code = self.file_save()
                if return_code == 1:  # If user did not save the file
                    return
            elif reply == QMessageBox.NoButton:
                pass
            else:
                return

            self.opened_file = file_dialog.selectedFiles()[0]
            self.opened_file_filter = file_dialog.selectedMimeTypeFilter()
            with open(self.opened_file, mode='w', encoding='UTF-8') as _:
                pass
            self.actions_table.setModel(ActionsModel([]))

    def file_open(self):
        file_dialog = QFileDialog(self,
                                  'Open file',
                                  HOME,
                                  FILE_FILTERS)
        file_dialog.setFilter(file_dialog.filter())
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setDefaultSuffix('mcrc')
        if file_dialog.exec() == QFileDialog.Accepted:
            reply = self.ask_save_question()
            if reply == QMessageBox.AcceptRole:
                return_code = self.file_save()
                if return_code == 1:  # If user did not save the file
                    return
            elif reply == QMessageBox.DestructiveRole:
                pass
            else:
                return

            self.opened_file = file_dialog.selectedFiles()[0]
            self.opened_file_filter = file_dialog.selectedNameFilter()

            if self.opened_file_filter == '.mcrc XML (*.mcrc)':
                try:
                    actions, self.settings = runner.read_file_xml(self.opened_file)
                except Exception as e:
                    self.handle_exception(e)
                    return
            elif self.opened_file_filter == '.mcrc CSV (*.mcrc)':
                try:
                    actions, self.settings = runner.read_file_csv(self.opened_file)
                except Exception as e:
                    self.handle_exception(e)
                    return
            elif self.opened_file_filter == '.mcrc DB (*.mcrc)':
                try:
                    actions, self.settings = runner.read_file_db(self.opened_file)
                except Exception as e:
                    self.handle_exception(e)
                    return
            else:
                raise ValueError('Unknown file format')

            self.actions_table.setModel(ActionsModel(actions))

    def file_save(self, always_open_dialog: bool = False) -> Optional[int]:
        """always_open_dialog is only used in self.file_save_as()"""
        if self.opened_file == DEFAULT_OPENED_FILE or always_open_dialog:
            file_dialog = QFileDialog(self,
                                      'Create new file',
                                      HOME,
                                      FILE_FILTERS)
            file_dialog.setFilter(file_dialog.filter() | QDir.Hidden)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setDefaultSuffix('mcrc')
            if file_dialog.exec() == QFileDialog.Accepted:
                self.opened_file = file_dialog.selectedFiles()[0]
                self.opened_file_filter = file_dialog.selectedNameFilter()
                with open(self.opened_file, mode='w', encoding='UTF-8') as _:
                    pass
            else:
                return 1

        if self.opened_file_filter == '.mcrc XML (*.mcrc)':
            runner.write_file_xml(self.opened_file,
                                  self.actions_table.model().actions,
                                  self.settings)
        elif self.opened_file_filter == '.mcrc CSV (*.mcrc)':
            runner.write_file_csv(self.opened_file,
                                  self.actions_table.model().actions,
                                  self.settings)
        elif self.opened_file_filter == '.mcrc DB (*.mcrc)':
            runner.write_file_db(self.opened_file,
                                 self.actions_table.model().actions,
                                 self.settings)
        else:
            raise ValueError('Unknown file format')

    def file_save_as(self):
        old_file = self.opened_file
        return_code = self.file_save(always_open_dialog=True)
        if return_code == 1:
            self.opened_file = old_file

    def file_close(self):
        reply = self.ask_save_question()
        if reply == QMessageBox.AcceptRole:
            return_code = self.file_save()
            if return_code == 1:
                return
        elif reply == QMessageBox.RejectRole:
            return
        elif reply == QMessageBox.DestructiveRole:
            pass

        self.opened_file = DEFAULT_OPENED_FILE
        self.actions_table.setModel(ActionsModel([]))  # Clear data

    # UI init

    def init_ui(self):
        self.setWindowModified(False)
        self.resize(900, 550)
        self.setMinimumSize(600, 300)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(4)
        self.centralWidget.setLayout(self.layout)

        # New action tree
        self.new_action_tree = QTreeView()
        self.layout.addWidget(self.new_action_tree)
        self.new_action_tree.setHeaderHidden(True)
        self.new_action_tree.setDragDropMode(QAbstractItemView.DragOnly)
        items = create_action_tree_items()
        model = NewActionTreeModel(items)
        self.new_action_tree.setModel(model)
        self.new_action_tree.setItemDelegate(BoldDelegate(model))
        self.new_action_tree.expandAll()

        # Right layout
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(4)
        self.layout.addLayout(self.right_layout)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setObjectName('buttons_layout')
        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.right_layout.addLayout(self.buttons_layout)
        button_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Run button
        self.run_button = QPushButton(QIcon(get_path('gui/icons/system-run.svg')),
                                      'Run')
        self.run_button.setShortcut('Ctrl+Space')
        self.run_button.setToolTip('Run macro (Ctrl+Space)')
        self.run_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.run_button)
        # Move up button
        self.move_up_button = QPushButton(QIcon(get_path('gui/icons/go-up.svg')),
                                          'Move up')
        self.move_up_button.setShortcut('Ctrl+Up')
        self.move_up_button.setToolTip('Move selected actions up (Ctrl+Up)')
        self.move_up_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.move_up_button)
        # Move down button
        self.move_down_button = QPushButton(QIcon(get_path('gui/icons/go-down.svg')),
                                            'Move down')
        self.move_down_button.setShortcut('Ctrl+Down')
        self.move_down_button.setToolTip('Move selected actions down (Ctrl+Down)')
        self.move_down_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.move_down_button)
        # Delete button
        self.delete_button = QPushButton(QIcon(get_path('gui/icons/edit-delete.svg')),
                                         'Delete')
        self.delete_button.setShortcut('Del')
        self.delete_button.setToolTip('Delete selected actions (Del)')
        self.delete_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.delete_button)
        # Spacer
        self.vertical_spacer = QSpacerItem(100, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttons_layout.addItem(self.vertical_spacer)
        # Settings button
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(get_path('gui/icons/configure.svg')))
        self.settings_button.setToolTip('Settings')
        self.settings_button.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.buttons_layout.addWidget(self.settings_button)

        # Actions table
        self.actions_table = ActionsTable()
        self.right_layout.addWidget(self.actions_table)

        # Layouts stretch
        self.right_layout.setStretch(0, 0)
        self.right_layout.setStretch(1, 1)
        self.layout.setStretch(0, 0)
        self.layout.setStretch(1, 1)

        # Menu bar
        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 800, 30))
        self.setMenuBar(self.menubar)

        self.menu_file = QMenu('File')
        self.menubar.addAction(self.menu_file.menuAction())

        self.action_new = QAction(QIcon(get_path('gui/icons/document-new.svg')), 'New...')
        self.action_new.setShortcut('Ctrl+N')
        self.action_open = QAction(QIcon(get_path('gui/icons/document-open.svg')), 'Open...')
        self.action_open.setShortcut('Ctrl+O')
        self.action_save = QAction(QIcon(get_path('gui/icons/document-save.svg')), 'Save...')
        self.action_save.setShortcut('Ctrl+S')
        self.action_save_as = QAction(QIcon(get_path('gui/icons/document-save.svg')), 'Save as...')
        self.action_save_as.setShortcut('Ctrl+Shift+S')
        self.action_close = QAction(QIcon(get_path('gui/icons/dialog-cancel.svg')), 'Close file')

        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addAction(self.action_close)
