from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDockWidget, QTreeView, QPushButton, QMenuBar, QMenu, \
    QAction, QSizePolicy, QStyledItemDelegate, QAbstractItemView, QHBoxLayout, QTableView, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel, QAbstractTableModel, QRect, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QDropEvent, QDragMoveEvent
from pathlib import Path

from actions.Action import Action, NoneAction
from parser import Runner, FileRead, FileWrite

home = str(Path.home())


class CloseDockWidget(QDockWidget):
    closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_closed = False

    def closeEvent(self, event) -> None:
        self.closed.emit()
        self.is_closed = True
        super().closeEvent(event)

    def show(self) -> None:
        self.closed.emit()
        self.is_closed = False
        super().show()


class NewActionTreeNode:
    """Node for ActionsTreeModel class"""

    def __init__(self, data):
        self._data = data
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if column == 0:
            if self._data is None:
                return None
            if type(self._data) == str:
                return self._data
            return self._data.name

    def columnCount(self):
        return 1

    def childCount(self):
        return len(self._children)

    def child(self, row):
        if 0 <= row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
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

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.data(index.column())
        if role == Qt.UserRole:
            return node._data
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # Enable Drag and Drop only for actual items, not titles
        default_flags = QAbstractItemModel.flags(self, index)
        if self.data(self.parent(index), Qt.DisplayRole) == self._root.data(0):
            return default_flags
        return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | default_flags

    @property
    def root(self):
        return self._root


class BoldDelegate(QStyledItemDelegate):
    """Custom item delegate for new_action_tree. Makes headers bold"""

    def __init__(self, model):
        super().__init__()
        self.model = model

    def paint(self, painter, option, index):
        if self.model.data(self.model.parent(index), Qt.DisplayRole) == self.model.root.data(0):
            option.font.setWeight(QFont.Bold)
        QStyledItemDelegate.paint(self, painter, option, index)


def create_table_index(model, row, column):
    return QAbstractTableModel.index(model, row, column)


class ActionsModel(QAbstractTableModel):
    """Model for actions_table"""

    def __init__(self, items: list):
        super().__init__()
        self._data = items

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole:
            if orientation == Qt.PortraitOrientation:
                return ['Action', 'Comment'][section]
            else:
                return section + 1

    def data(self, index: QModelIndex, role: int = ...):
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
                # print('WHY')
                # It goes here while drag and drop inside the table
                return False
            return True
        return QAbstractTableModel.setData(self, index, value, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        last_inserted_row = row + count - 1
        self.beginInsertRows(QModelIndex(), row, last_inserted_row)
        for i in range(count):
            self._data.insert(row + i, NoneAction)
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
        was_changed = False
        for row in rows:
            min_row = max((row - 1, 0))
            if row != min_row:
                self._data[min_row], self._data[row] = self._data[row], self._data[min_row]
                index = create_table_index(self, row, 0)
                index_1 = create_table_index(self, min_row, 0)
                self.dataChanged.emit(index, index_1)
                was_changed = True
        return was_changed

    def move_down(self, rows):
        was_changed = False
        rows.reverse()
        for row in rows:
            max_row = min((row + 1, self.rowCount() - 1))
            if row != max_row:
                self._data[max_row], self._data[row] = self._data[row], self._data[max_row]
                index = create_table_index(self, row, 0)
                index_1 = create_table_index(self, max_row, 0)
                self.dataChanged.emit(index, index_1)
                was_changed = True
        return was_changed

    @property
    def actions(self):
        return self._data


class ActionsTable(QTableView):
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

    def dragEnterEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.source() == self:
            rows = set(self.get_selected_rows())
            targetRow = self.indexAt(event.pos()).row()
            rows.discard(targetRow)
            rows = sorted(rows)
            if not rows:
                return None
            if targetRow == -1:
                targetRow = self.model().rowCount()
            self.model().insertRows(targetRow, len(rows))
            rowMapping = dict()  # Src row to target row.
            for idx, row in enumerate(rows):
                if row < targetRow:
                    rowMapping[row] = targetRow + idx
                else:
                    rowMapping[row + len(rows)] = targetRow + idx
            colCount = self.model().columnCount()
            for srcRow, tgtRow in sorted(rowMapping.items()):
                for col in range(0, colCount):
                    self.model().setData(create_table_index(self.model(), tgtRow, col), self.model().actions[srcRow])
            for row in reversed(sorted(rowMapping.keys())):
                self.model().removeRow(row)
            event.accept()

        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()

            source = event.source()
            source_model = source.model()
            index = source.currentIndex()
            action_class = source_model.data(index, Qt.UserRole)

            action = action_class()
            self.model().insertRow(self.model().rowCount() + 1)
            # noinspection PyTypeChecker
            index = create_table_index(self.model(), self.model().rowCount() - 1, 0)
            self.model().setData(index, action)
            main_window = self.parent().parent()
            main_window.not_saved()
            action.open_edit_dialog(main_window)

    def get_selected_rows(self):
        return list(set(index.row() for index in self.selectedIndexes()))

    def move_selection_up(self):
        selected_rows = self.get_selected_rows()
        for row in selected_rows:
            min_row = max((row - 1, 0))
            if row == min_row and len(selected_rows) == 1:
                return None
            self.clearSelection()
            if row != min_row:
                self.selectRow(min_row)

    def move_selection_down(self):
        selected_rows = self.get_selected_rows()
        selected_rows.reverse()
        for row in selected_rows:
            max_row = min((row + 1, self.model().rowCount() - 1))
            if row == max_row and len(selected_rows) == 1:
                return None
            self.clearSelection()
            if row != max_row:
                self.selectRow(max_row)


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
    """Creates list with ActionTreeNodes for ActionsTreeModel"""
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
        self.default_opened_file = 'untitled.mcrc[*]'
        self.opened_file = self.default_opened_file
        self.init_ui()

        self.is_saved = True

        self.actions_table.doubleClicked.connect(self.open_action_edit_dialog)
        self.new_action_dock.closed.connect(self.sync_dock_and_action)
        self.action_new_action_dock.triggered.connect(self.handle_dock_state)
        self.delete_button.pressed.connect(self.delete)
        self.move_up_button.pressed.connect(self.move_up)
        self.move_down_button.pressed.connect(self.move_down)
        self.run_button.pressed.connect(self.run)
        self.action_new.triggered.connect(self.new_file)
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)

    def open_action_edit_dialog(self):
        selected_rows = self.actions_table.get_selected_rows()
        if len(selected_rows) == 1:
            row = selected_rows[0]
            model = self.actions_table.model()
            index = create_table_index(model, row, 0)
            action = model.data(index, Qt.UserRole)
            was_changed = action.open_edit_dialog(self)
            if was_changed:
                self.not_saved()

    def delete(self):
        selected_rows = self.actions_table.get_selected_rows()
        for i, row in enumerate(selected_rows):
            self.actions_table.model().removeRow(row - i)
        self.not_saved()

    def move_up(self):
        selected_rows = self.actions_table.get_selected_rows()
        was_changed = self.actions_table.model().move_up(selected_rows)
        if was_changed:
            self.actions_table.move_selection_up()
            self.not_saved()

    def move_down(self):
        selected_rows = self.actions_table.get_selected_rows()
        was_changed = self.actions_table.model().move_down(selected_rows)
        if was_changed:
            self.actions_table.move_selection_down()
            self.not_saved()

    def run(self):
        Runner.run(self.actions_table.model().actions)

    def not_saved(self):
        if self.actions_table.model().rowCount():
            if self.opened_file != self.default_opened_file:
                self.setWindowTitle(f'{self.opened_file}[*]')
            self.setWindowModified(True)
            self.is_saved = False
        else:
            self.saved()

    def saved(self):
        if self.opened_file != self.default_opened_file:
            self.setWindowTitle(f'{self.opened_file}[*]')
        self.setWindowModified(False)
        self.is_saved = True

    def new_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Create new file', home, '.mcrc (*.mcrc)')[0]
        if filename:
            if not self.is_saved:
                reply = QMessageBox.warning(self, 'Save changes', 'Do you want to save your changes?',
                                            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Cancel:
                    return None
                if reply == QMessageBox.Save:
                    # If user did not save the file
                    return_code = self.save_file()
                    if return_code == 1:
                        return None

            file = open(filename, 'w')
            file.close()
            self.opened_file = filename
            model = ActionsModel([])
            self.actions_table.setModel(model)
            self.saved()

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', home, '.mcrc (*.mcrc)')[0]
        if filename:
            if not self.is_saved:
                reply = QMessageBox.warning(self, 'Save changes', 'Do you want to save your changes?',
                                            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Cancel:
                    return None
                if reply == QMessageBox.Save:
                    # If user did not save the file
                    return_code = self.save_file()
                    if return_code == 1:
                        return None

            self.opened_file = filename
            actions = FileRead.read_file(filename)
            model = ActionsModel(actions)
            self.actions_table.setModel(model)
            self.saved()

    def save_file(self):
        if self.opened_file == self.default_opened_file:
            filepath = QFileDialog.getSaveFileName(self, 'Create new file', home, '.mcrc (*.mcrc)')[0]
            if filepath:
                file = open(filepath, 'w')
                file.close()
                self.opened_file = filepath
            else:
                return 1

        FileWrite.write_file(self.opened_file, self.actions_table.model().actions)
        self.saved()

    def sync_dock_and_action(self):
        self.action_new_action_dock.setChecked(self.new_action_dock.is_closed)

    def handle_dock_state(self):
        is_checked = self.action_new_action_dock.isChecked()
        if is_checked:
            self.new_action_dock.show()
        else:
            self.new_action_dock.close()

    def init_ui(self):
        self.setWindowTitle(self.opened_file)
        self.setWindowModified(False)
        self.resize(900, 550)
        self.setMinimumSize(600, 300)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)
        self.centralWidget.setLayout(self.layout)

        # New action dock
        self.new_action_dock = CloseDockWidget('New action')
        self.new_action_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.new_action_dock)
        # New action dock content
        self.new_action_dock_content = QWidget()
        self.new_action_dock.setWidget(self.new_action_dock_content)
        # New action layout
        self.new_action_layout = QVBoxLayout()
        self.new_action_layout.setContentsMargins(0, 0, 0, 0)
        self.new_action_dock_content.setLayout(self.new_action_layout)

        # New action tree
        self.new_action_tree = QTreeView()
        self.new_action_layout.addWidget(self.new_action_tree)
        self.new_action_tree.setHeaderHidden(True)
        self.new_action_tree.setRootIsDecorated(False)
        self.new_action_tree.setDragDropMode(QAbstractItemView.DragOnly)
        items = create_action_tree_items()
        model = NewActionTreeModel(items)
        self.new_action_tree.setModel(model)
        self.new_action_tree.setItemDelegate(BoldDelegate(model))
        self.new_action_tree.expandAll()

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 4, 0, 0)
        self.buttons_layout.setSpacing(4)
        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.layout.addLayout(self.buttons_layout)
        button_size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        # Delete button
        self.delete_button = QPushButton(QIcon.fromTheme('edit-delete'), 'Delete')
        self.delete_button.setShortcut('Del')
        self.delete_button.setToolTip('Delete selected actions (Del)')
        self.delete_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.delete_button)
        # Move up button
        self.move_up_button = QPushButton(QIcon('go-up'), 'Move up')
        self.move_up_button.setShortcut('Ctrl+Up')
        self.move_up_button.setToolTip('Move selected actions up (Ctrl+Up)')
        self.move_up_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.move_up_button)
        # Move down button
        self.move_down_button = QPushButton(QIcon('go-down'), 'Move down')
        self.move_down_button.setShortcut('Ctrl+Down')
        self.move_down_button.setToolTip('Move selected actions down (Ctrl+Down)')
        self.move_down_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.move_down_button)
        # Run button
        self.run_button = QPushButton(QIcon('system-run'), 'Run')
        self.run_button.setShortcut('Ctrl+Space')
        self.run_button.setToolTip('Run macro (Ctrl+Space)')
        self.run_button.setSizePolicy(button_size_policy)
        self.buttons_layout.addWidget(self.run_button)

        # Actions table
        self.actions_table = ActionsTable()
        self.layout.addWidget(self.actions_table)
        self.layout.setStretch(0, 0)
        self.layout.setStretch(1, 1)
        self.actions_table.horizontalHeader().resizeSection(0, 150)
        self.actions_table.horizontalHeader().setStretchLastSection(True)
        font = self.actions_table.horizontalHeader().font()
        font.setBold(True)
        self.actions_table.horizontalHeader().setFont(font)

        model = ActionsModel([])
        self.actions_table.setModel(model)

        # Menu bar
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 30))
        self.setMenuBar(self.menubar)

        self.menu_file = QMenu('File', self.menubar)
        self.menubar.addAction(self.menu_file.menuAction())

        self.action_new = QAction('New', self)
        self.action_new.setShortcut('Ctrl+N')
        self.action_open = QAction('Open', self)
        self.action_open.setShortcut('Ctrl+O')
        self.action_save = QAction('Save', self)
        self.action_save.setShortcut('Ctrl+S')

        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)

        self.menu_windows = QMenu('Windows', self.menubar)
        self.menubar.addAction(self.menu_windows.menuAction())
        self.action_new_action_dock = QAction('New action', self)
        self.action_new_action_dock.setCheckable(True)
        self.action_new_action_dock.setChecked(True)
        self.menu_windows.addAction(self.action_new_action_dock)
