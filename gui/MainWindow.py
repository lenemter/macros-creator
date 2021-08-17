from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QAbstractItemView
from PyQt5.QtCore import Qt
from pathlib import Path

import actions.Action
from gui.MainWindowUI import MainWindowUI
from parser import FileRead, FileWrite, Runner

home = str(Path.home())


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        QMainWindow.__init__(self)
        MainWindowUI.init_ui(self, self)

        self.new_action_tree.doubleClicked.connect(self.add_item_to_table)
        self.table.itemChanged.connect(self.not_saved)
        self.table.doubleClicked.connect(self.open_edit_dialog)
        self.delete_button.pressed.connect(self.delete)
        self.move_up_button.pressed.connect(self.move_up)
        self.move_down_button.pressed.connect(self.move_down)
        self.run_button.pressed.connect(self.run)
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)

        self.opened_file = None
        self.is_saved = True

    def get_selected_rows(self):
        return list(set(item.row() for item in self.table.selectedIndexes()))

    def add_item_to_table(self):
        model = self.new_action_tree.model()
        index = self.new_action_tree.currentIndex()
        action_class = model.data(index, Qt.UserRole)
        if type(action_class) != str:
            self.table.add_action(action_class)

    def open_edit_dialog(self):
        selected_rows = self.get_selected_rows()
        if len(selected_rows) == 1:
            selected_row = selected_rows[0]
            selected_action = self.table.actions_list[selected_row]
            selected_action.open_edit_dialog(self)
            self.table.fill_table()

    def delete(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.information(self, 'No rows', 'No rows selected', QMessageBox.Ok)
        else:
            answer = QMessageBox.question(self, 'Are you sure', f'Do you want to delete {len(selected_rows)} actions?',
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                for i, row in enumerate(selected_rows):
                    self.table.removeRow(row - i)
                    del self.table.actions_list[row - i]
                self.not_saved()

    def move_up(self):
        selected_rows = list(set(item.row() for item in self.table.selectedItems()))
        if len(selected_rows) == 0:
            QMessageBox.information(self, 'No rows', 'No rows selected', QMessageBox.Ok)
        else:
            old_actions = self.table.actions_list.copy()
            for row in selected_rows:
                min_row = max((row - 1, 0))
                if row == min_row:
                    continue
                self.table.actions_list[min_row], self.table.actions_list[row] = \
                    self.table.actions_list[row], self.table.actions_list[min_row]

            if old_actions == self.table.actions_list:
                return None

            self.table.fill_table()
            self.table.clearSelection()
            self.table.setSelectionMode(QAbstractItemView.MultiSelection)
            for row in selected_rows:
                min_row = max((row - 1, 0))
                self.table.selectRow(min_row)
            self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def move_down(self):
        selected_rows = list(set(item.row() for item in self.table.selectedItems()))
        if len(selected_rows) == 0:
            QMessageBox.information(self, 'No rows', 'No rows selected', QMessageBox.Ok)
        else:
            selected_rows.reverse()
            old_actions = self.table.actions_list.copy()
            for row in selected_rows:
                max_row = min((row + 1, len(self.table.actions_list) - 1))
                if row == max_row:
                    continue
                self.table.actions_list[max_row], self.table.actions_list[row] = \
                    self.table.actions_list[row], self.table.actions_list[max_row]

            if old_actions == self.table.actions_list:
                return None

            self.table.fill_table()
            self.table.clearSelection()
            self.table.setSelectionMode(QAbstractItemView.MultiSelection)
            for row in selected_rows:
                max_row = min((row + 1, len(self.table.actions_list) - 1))
                self.table.selectRow(max_row)
            self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def run(self):
        if self.opened_file is None:
            return_code = self.save()
            if return_code == 1:
                return None

        self.hide()
        Runner.run(self.opened_file)
        self.show()

    def not_saved(self):
        self.is_saved = False
        self.setWindowTitle('Macros Creator*')

    def saved(self):
        self.is_saved = True
        self.setWindowTitle('Macros Creator')

    def new(self):
        filename = QFileDialog.getSaveFileName(self, 'Create new file', home, '.mcrc (*.mcrc)')[0]
        if filename:
            if not self.is_saved:
                answer = QMessageBox.warning(self, 'Save changes', 'Do you want to save your changes?',
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if answer == QMessageBox.Cancel:
                    return None
                if answer == QMessageBox.Save:
                    # If user did not save the file
                    return_code = self.save()
                    if return_code == 1:
                        return None

            file = open(filename, 'w')
            file.close()
            self.opened_file = filename
            self.table.setRowCount(0)
            self.table.actions_list.clear()
            self.saved()

    def open(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', home, '.mcrc (*.mcrc)')[0]
        if filename:
            if not self.is_saved:
                answer = QMessageBox.warning(self, 'Save changes', 'Do you want to save your changes?',
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if answer == QMessageBox.Cancel:
                    return None
                if answer == QMessageBox.Save:
                    # If user did not save the file
                    return_code = self.save()
                    if return_code == 1:
                        return None

            self.opened_file = filename
            actions = FileRead.read_file(filename)
            self.table.fill_table(actions)
            self.saved()

    def save(self):
        if self.opened_file is None:
            filepath = QFileDialog.getSaveFileName(self, 'Create new file', home, '.mcrc (*.mcrc)')[0]
            if filepath:
                file = open(filepath, 'w')
                file.close()
                self.opened_file = filepath
            else:
                return 1

        FileWrite.write_file(self.opened_file, self.table.actions_list)
        self.saved()

    def closeEvent(self, event) -> None:
        if not self.is_saved:
            answer = QMessageBox.warning(self, 'Save changes', 'Do you want to save your changes?',
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if answer == QMessageBox.Discard:
                event.accept()
            if answer == QMessageBox.Save:
                # If user did not save the file
                return_code = self.save()
                if return_code == 1:
                    event.ignore()
                else:
                    event.accept()
            if answer == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()
