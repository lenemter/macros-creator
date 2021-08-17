from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QDockWidget, QTreeView, QPushButton, \
    QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QAction, QSizePolicy, QAbstractItemView
from PyQt5.QtCore import Qt, QModelIndex, QRect
from PyQt5.QtGui import QDropEvent, QFont
from PyQt5.Qt import QAbstractItemModel, QStyledItemDelegate

from actions.Action import Action
import actions
from gui.Widgets import ReadOnlyDelegate, VerticalLine


class BoldDelegate(QStyledItemDelegate):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def paint(self, painter, option, index):
        if self.model.data(self.model.parent(index), Qt.DisplayRole) == self.model.root.data(0):
            option.font.setWeight(QFont.Bold)
        QStyledItemDelegate.paint(self, painter, option, index)


class ActionsTreeNode:
    def __init__(self, data):
        self._data_ = data
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if column == 0:
            if self._data_ is None:
                return None
            if type(self._data_) == str:
                return self._data_
            return self._data_.name

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

    @property
    def data_(self):
        return self._data_


class ActionsTreeModel(QAbstractItemModel):
    def __init__(self, nodes):
        super().__init__()
        self._root = ActionsTreeNode(None)
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
            return node.data_
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


class ActionsTree(QTreeView):
    def __init__(self):
        super().__init__()

        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.setDragDropMode(QAbstractItemView.DragOnly)

        # Tree items
        self.items = []
        # Create dict with categories as keys and classes as values
        categories = dict()
        for cls in Action.__subclasses__():
            category = cls.category
            if category in categories:
                categories[category].append(cls)
            else:
                categories[category] = [cls]
        # Use this dict to create Tree items
        for category in categories.keys():
            self.items.append(ActionsTreeNode(category))
            for cls in categories[category]:
                self.items[-1].addChild(ActionsTreeNode(cls))

        model = ActionsTreeModel(self.items)
        self.setModel(model)
        self.setItemDelegate(BoldDelegate(self.model()))
        self.expandAll()


class TableWidget(QTableWidget):
    """Custom TableWidget with drag event support and actions tracking"""

    def __init__(self):
        super().__init__()
        self.actions_list = []

        self.setItemDelegate(ReadOnlyDelegate())
        self.setColumnCount(2)
        self.setAcceptDrops(True)
        self.verticalHeader().setVisible(True)
        self.setHorizontalHeaderLabels(['Action', 'Comment'])
        self.horizontalHeader().resizeSection(0, 150)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        font = self.horizontalHeader().font()
        font.setBold(True)
        self.horizontalHeader().setFont(font)

    def fill_table(self, actions: list = None):
        if actions is not None:
            self.actions_list = actions
        self.setRowCount(0)  # Clear
        self.setRowCount(len(self.actions_list))
        for row, action in enumerate(self.actions_list):
            self.setItem(row, 0, QTableWidgetItem(action.name))
            self.setItem(row, 1, QTableWidgetItem(action.comment))

    def add_action(self, action_class):
        action = action_class()
        self.actions_list.append(action)

        self.setRowCount(len(self.actions_list))
        self.setItem(len(self.actions_list) - 1, 0, QTableWidgetItem(action.name))
        self.setItem(len(self.actions_list) - 1, 1, QTableWidgetItem(action.comment))

        action.open_edit_dialog(self.parent().parent())

        self.setItem(len(self.actions_list) - 1, 1, QTableWidgetItem(action.comment))

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()

            source = event.source()
            model = source.model()
            index = source.currentIndex()
            action_class = model.data(index, Qt.UserRole)
            self.add_action(action_class)


class MainWindowUI:
    def init_ui(self, main_window: QMainWindow):
        main_window.setWindowTitle('Macros Creator')
        main_window.resize(900, 550)
        main_window.setMinimumSize(600, 300)

        self.central_widget = QWidget()
        main_window.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setStretch(1, 4)

        # Actions dock
        self.actions_dock = QDockWidget()
        self.actions_dock.setWindowTitle('Actions')
        self.actions_dock.setMinimumWidth(190)
        self.actions_dock.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        self.actions_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.actions_dock_content = QWidget()
        self.actions_dock_layout = QVBoxLayout(self.actions_dock_content)
        self.actions_dock_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_dock.setWidget(self.actions_dock_content)
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.actions_dock)

        # Actions tree
        self.actions_tree = ActionsTree()
        self.actions_dock_layout.addWidget(self.actions_tree)

        # Buttons
        self.table_layout = QVBoxLayout()
        self.table_layout.setSpacing(6)
        self.layout.addLayout(self.table_layout)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.table_layout.addLayout(self.buttons_layout)

        buttons_size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.button_delete = QPushButton('Delete')
        self.button_delete.setShortcut('Del')
        self.button_delete.setToolTip('Deleted selected actions (Del)')
        self.button_delete.setSizePolicy(buttons_size_policy)
        self.buttons_layout.addWidget(self.button_delete)

        self.divider_1 = VerticalLine()
        self.buttons_layout.addWidget(self.divider_1)

        self.button_move_up = QPushButton('Move up')
        # self.button_move_up.setShortcut('')  # todo: Make shortcut
        # self.button_move_up.setToolTip('')  # todo: Make tooltip
        self.button_move_up.setSizePolicy(buttons_size_policy)
        self.buttons_layout.addWidget(self.button_move_up)

        self.button_move_down = QPushButton('Move down')
        # self.button_move_down.setShortcut('')  # todo: Make shortcut
        # self.button_moce_down.setToolTip('')  # todo: Make tooltip
        self.button_move_down.setSizePolicy(buttons_size_policy)
        self.buttons_layout.addWidget(self.button_move_down)

        self.divider_2 = VerticalLine()
        self.buttons_layout.addWidget(self.divider_2)

        self.button_run = QPushButton('Run')
        self.button_run.setShortcut('Ctrl+Space')
        self.button_run.setToolTip('Run program (Ctrl+Space)')
        self.button_run.setSizePolicy(buttons_size_policy)
        self.buttons_layout.addWidget(self.button_run)

        # Table
        self.table = TableWidget()
        self.table_layout.addWidget(self.table)

        # Menubar
        self.menubar = QMenuBar(main_window)
        self.menubar.setGeometry(QRect(0, 0, 800, 30))
        main_window.setMenuBar(self.menubar)

        self.menu_file = QMenu(self.menubar)
        self.menu_file.setTitle('File')

        self.action_new = QAction(self)
        self.action_new.setText('New')
        self.action_new.setShortcut('Ctrl+N')
        self.action_open = QAction(self)
        self.action_open.setText('Open')
        self.action_open.setShortcut('Ctrl+O')
        self.action_save = QAction(self)
        self.action_save.setText('Save')
        self.action_save.setShortcut('Ctrl+S')

        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menubar.addAction(self.menu_file.menuAction())

        self.menu_windows = QMenu(self.menubar)
        self.menu_windows.setTitle('Windows')
        # todo create toggle for Actions dock
