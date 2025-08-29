import sys
import os
import shutil
import subprocess
from PySide6.QtWidgets import (
    QApplication, QDialog, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsView, QGraphicsRectItem, QGraphicsDropShadowEffect,
    QGroupBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QDockWidget,
    QListWidget, QPushButton, QLabel, QLineEdit,
    QMessageBox, QToolBar, QMenu, QMenuBar, QFrame, QAbstractItemView,
    QStatusBar, QCheckBox, QFileDialog, QListWidgetItem, QPlainTextEdit,
    QColorDialog, QComboBox, QRadioButton, QGridLayout
)
from PySide6.QtGui import QPixmap, QResizeEvent, QColor, QAction, QIcon, QShowEvent, QImage, QFont, QBrush
from PySide6.QtCore import Qt, QRectF, QSize, QTimer, QDateTime, QStandardPaths

# تلاش برای وارد کردن کلاس طراحی UI
try:
    from ui_sinamanager import Ui_LoginDialog
except ImportError as e:
    print(f"Error: Could not import Ui_LoginDialog. Please ensure ui_sinamanager.py is in the correct path and generated correctly. Details: {e}")
    sys.exit(1)

# --- کلاس BackupDialog ---
class BackupDialog(QDialog):
    def __init__(self, projects, parent=None):
        super().__init__(parent)
        self.setWindowTitle("پشتیبان‌گیری پروژه‌ها")
        self.setGeometry(200, 200, 600, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        main_layout = QVBoxLayout(self)
        project_groupbox = QGroupBox("انتخاب پروژه‌ها")
        project_layout = QVBoxLayout(project_groupbox)
        
        self.project_table = QTableWidget()
        self.project_table.setColumnCount(3)
        self.project_table.setHorizontalHeaderLabels(["انتخاب", "ID", "نام پروژه"])
        self.project_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.project_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.project_table.setAlternatingRowColors(True)
        header = self.project_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        project_layout.addWidget(self.project_table)
        main_layout.addWidget(project_groupbox)
        self.project_table.setRowCount(len(projects))
        for row_index, project in enumerate(projects):
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox = QCheckBox()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.project_table.setCellWidget(row_index, 0, checkbox_widget)
            checkbox.stateChanged.connect(self.update_selected_projects_display)
            id_item = QTableWidgetItem(project[0])
            id_item.setTextAlignment(Qt.AlignCenter)
            self.project_table.setItem(row_index, 1, id_item)
            name_item = QTableWidgetItem(project[1])
            name_item.setTextAlignment(Qt.AlignCenter)
            self.project_table.setItem(row_index, 2, name_item)
        selected_projects_groupbox = QGroupBox("پروژه‌های انتخاب‌شده")
        selected_projects_layout = QVBoxLayout(selected_projects_groupbox)
        self.selected_projects_table = QTableWidget()
        self.selected_projects_table.setColumnCount(2)
        self.selected_projects_table.setHorizontalHeaderLabels(["ID", "نام پروژه"])
        self.selected_projects_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.selected_projects_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.selected_projects_table.setAlternatingRowColors(True)
        header_selected = self.selected_projects_table.horizontalHeader()
        header_selected.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_selected.setSectionResizeMode(1, QHeaderView.Stretch)
        selected_projects_layout.addWidget(self.selected_projects_table)
        main_layout.addWidget(selected_projects_groupbox)
        location_groupbox = QGroupBox("محل ذخیره و نام فایل")
        location_layout = QVBoxLayout(location_groupbox)
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("مسیر و نام فایل پشتیبان را انتخاب کنید...")
        browse_button = QPushButton("انتخاب مسیر")
        browse_button.clicked.connect(self.select_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        location_layout.addLayout(path_layout)
        main_layout.addWidget(location_groupbox)
        compress_layout = QHBoxLayout()
        compress_layout.addStretch()
        self.compress_checkbox = QCheckBox("فشرده سازی")
        compress_layout.addWidget(self.compress_checkbox)
        compress_layout.addStretch()
        main_layout.addLayout(compress_layout)
        sections_groupbox = QGroupBox("بخش ها")
        sections_layout = QVBoxLayout(sections_groupbox)
        self.sections_list = QListWidget()
        self.sections_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sections_list.setAlternatingRowColors(True)
        section_items = ["مشخصات پیمان", "ریز متره", "خلاصه متره"]
        for section in section_items:
            item = QListWidgetItem(section)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            self.sections_list.addItem(item)
        sections_layout.addWidget(self.sections_list)
        main_layout.addWidget(sections_groupbox)
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("تأیید")
        self.cancel_button = QPushButton("لغو")
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        self.ok_button.clicked.connect(self.perform_backup)
        self.cancel_button.clicked.connect(self.reject)
        self.selected_projects = []
        self.selected_sections = []
        self.save_path = ""
        self.file_suffix = ""
        self.is_compressed = False
    def update_selected_projects_display(self):
        self.selected_projects_table.setRowCount(0)
        checked_projects = []
        for row in range(self.project_table.rowCount()):
            widget = self.project_table.cellWidget(row, 0)
            checkbox = widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                project_id = self.project_table.item(row, 1).text()
                project_name = self.project_table.item(row, 2).text()
                checked_projects.append((project_id, project_name))
        self.selected_projects_table.setRowCount(len(checked_projects))
        for row_index, project in enumerate(checked_projects):
            id_item = QTableWidgetItem(project[0])
            id_item.setTextAlignment(Qt.AlignCenter)
            name_item = QTableWidgetItem(project[1])
            name_item.setTextAlignment(Qt.AlignCenter)
            self.selected_projects_table.setItem(row_index, 0, id_item)
            self.selected_projects_table.setItem(row_index, 1, name_item)
    def select_path(self):
        default_filename = os.path.join(os.path.expanduser("~"), "backup.cmra")
        file_path, _ = QFileDialog.getSaveFileName(self, "ذخیره فایل پشتیبان", default_filename, "(*.cmra);;All Files (*)")
        if file_path:
            if not file_path.lower().endswith('.cmra'):
                file_path += '.cmra'
            self.path_input.setText(file_path)
            self.save_path = file_path
    def perform_backup(self):
        self.selected_projects = []
        for row in range(self.project_table.rowCount()):
            widget = self.project_table.cellWidget(row, 0)
            checkbox = widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                project_name = self.project_table.item(row, 2).text()
                self.selected_projects.append(project_name)
        self.selected_sections = []
        for i in range(self.sections_list.count()):
            item = self.sections_list.item(i)
            if item.checkState() == Qt.Checked:
                self.selected_sections.append(item.text())
        self.save_path = self.path_input.text()
        self.is_compressed = self.compress_checkbox.isChecked()
        if not self.selected_projects:
            QMessageBox.warning(self, "خطا", "لطفاً حداقل یک پروژه را انتخاب کنید.")
            return
        if not self.save_path:
            QMessageBox.warning(self, "خطا", "لطفاً محل ذخیره را مشخص کنید.")
            return
        try:
            if self.is_compressed:
                project_names = self.selected_projects
                try:
                    subprocess.run(['rar', '-v'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except FileNotFoundError:
                    QMessageBox.critical(self, "خطا", "نرم‌افزار RAR در سیستم شما یافت نشد. لطفاً آن را نصب کرده و به PATH سیستم اضافه کنید.")
                    return
                output_file = self.save_path
                source_paths = [os.path.join("D:\\Projects", p) for p in project_names] 
                command = ['rar', 'a', output_file] + source_paths
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                QMessageBox.information(self, "پشتیبان‌گیری موفق", f"عملیات فشرده‌سازی با موفقیت انجام شد:\n{result.stdout}")
            else:
                for project in self.selected_projects: pass
                QMessageBox.information(self, "پشتیبان‌گیری موفق", "پشتیبان‌گیری بدون فشرده‌سازی انجام شد.")
            self.accept()
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "خطا در فشرده‌سازی", f"خطا در اجرای دستور RAR:\n{e.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "خطای نامشخص", f"یک خطای نامشخص رخ داد: {e}")
    def get_stylesheet(self):
        return """
            QDialog { background-color: #f0f0f0; } QGroupBox { border: 1px solid #c0c0c0; border-radius: 5px; margin-top: 10px; font-weight: bold; background-color: #ffffff; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; } QTableWidget { border: 1px solid #d0d0d0; background-color: #ffffff; gridline-color: #c0c0c0; } QTableWidget::item:alternate { background-color: #f2f2f2; } QTableWidget::item:selected { background-color: #a0c4ff; color: black; } QHeaderView::section { background-color: #d8e0c9; padding: 5px; border: 1px solid #c0c0c0; font-weight: bold; } QLineEdit { border: 1px solid #d0d0d0; padding: 5px; } QLineEdit::selection { color: black; background-color: #a0c4ff; } QPushButton { background-color: #4CAF50; color: white; border: 1px solid #4CAF50; padding: 8px 16px; border-radius: 4px; } QPushButton:hover { background-color: #45a049; } QPlainTextEdit { background-color: #ffffff; border: 1px solid #d0d0d0; } QPlainTextEdit::selection { background-color: #a0c4ff; color: black; } QListWidget { background-color: #ffffff; border: 1px solid #d0d0d0; } QListWidget::item { background-color: #ffffff; color: black; } QListWidget::item:selected { background-color: #a0c4ff; color: black; } QListWidget::indicator { width: 15px; height: 15px; border-radius: 2px; } QListWidget::indicator:checked { background-color: #4CAF50; border: 1px solid #45a049; } QListWidget::indicator:unchecked { background-color: #ffffff; border: 1px solid #c0c0c0; } QTableWidget::indicator { width: 15px; height: 15px; border-radius: 2px; } QTableWidget::indicator:checked { background-color: #4CAF50; border: 1px solid #45a049; } QTableWidget::indicator:unchecked { background-color: #ffffff; border: 1px solid #c0c0c0; }
        """

# --- کلاس RestoreDialog ---
class RestoreDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("بازیابی فایل پشتیبان")
        self.setFixedSize(400, 200)
        self.setStyleSheet(self.get_stylesheet())
        main_layout = QVBoxLayout(self)
        file_groupbox = QGroupBox("انتخاب فایل پشتیبان")
        file_layout = QVBoxLayout(file_groupbox)
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("مسیر فایل پشتیبان (.cmra) را انتخاب کنید...")
        browse_button = QPushButton("انتخاب فایل")
        browse_button.clicked.connect(self.select_file)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        file_layout.addLayout(path_layout)
        main_layout.addWidget(file_groupbox)
        self.compressed_checkbox = QCheckBox("فایل فشرده")
        main_layout.addWidget(self.compressed_checkbox)
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("تأیید")
        self.cancel_button = QPushButton("لغو")
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        self.ok_button.clicked.connect(self.perform_restore)
        self.cancel_button.clicked.connect(self.reject)
        self.selected_file_path = ""

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل پشتیبان", os.path.expanduser("~"), "(*.cmra);;All Files (*)")
        if file_path:
            self.path_input.setText(file_path)
            self.selected_file_path = file_path

    def perform_restore(self):
        if not self.selected_file_path:
            QMessageBox.warning(self, "خطا", "لطفاً یک فایل پشتیبان را انتخاب کنید.")
            return
        is_compressed = self.compressed_checkbox.isChecked()
        if is_compressed:
            try:
                subprocess.run(['unrar', '-v'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                QMessageBox.critical(self, "خطا", "نرم‌افزار UnRAR در سیستم شما یافت نشد. لطفاً آن را نصب کرده و به PATH سیستم اضافه کنید.")
                return
            try:
                extract_path = os.path.join(os.path.dirname(self.selected_file_path), "restored_data")
                os.makedirs(extract_path, exist_ok=True)
                command = ['unrar', 'x', '-o+', self.selected_file_path, extract_path]
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                QMessageBox.information(self, "بازیابی موفق", f"فایل فشرده با موفقیت به مسیر زیر بازیابی شد:\n{extract_path}\n\nخروجی:\n{result.stdout}")
                self.accept()
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "خطا در بازیابی", f"خطا در اجرای دستور UnRAR:\n{e.stderr}")
            except Exception as e:
                QMessageBox.critical(self, "خطای نامشخص", f"یک خطای نامشخص رخ داد: {e}")
        else:
            QMessageBox.information(self, "پیام سیستم", f"بازیابی از فایل:\n{self.selected_file_path}\nدر حال انجام است.")
            self.accept()
            
    def get_stylesheet(self):
        return """
            QDialog { background-color: #f0f0f0; }
            QGroupBox { border: 1px solid #c0c0c0; border-radius: 5px; margin-top: 10px; font-weight: bold; background-color: #ffffff; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
            QLineEdit { border: 1px solid #d0d0d0; padding: 5px; }
            QPushButton { background-color: #4CAF50; color: white; border: 1px solid #4CAF50; padding: 8px 16px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """

# --- کلاس VersionDialog ---
class VersionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("لیست نسخه‌های پروژه")
        self.setGeometry(150, 150, 800, 600)
        self.setStyleSheet(self.get_stylesheet())
        main_layout = QVBoxLayout(self)
        self.signatures_by_row = {}
        self.version_table = QTableWidget()
        self.version_table.setColumnCount(6)
        self.version_table.setHorizontalHeaderLabels(["ردیف", "نام نسخه", "اختصار", "رنگ", "نام نماینده", "ماهیت نسخه"])
        self.version_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.version_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.AnyKeyPressed)
        self.version_table.setAlternatingRowColors(True)
        self.version_table.cellChanged.connect(self.update_abbreviation)
        self.version_table.itemSelectionChanged.connect(self.update_signature_display)
        header = self.version_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        main_layout.addWidget(self.version_table)
        self.populate_version_table()
        signature_groupbox = QGroupBox("تصویر امضای نماینده")
        signature_layout = QVBoxLayout(signature_groupbox)
        self.signature_title_label = QLabel("تصویر امضای نماینده")
        self.signature_title_label.setAlignment(Qt.AlignCenter)
        self.signature_title_label.setStyleSheet("font-weight: bold; color: #555555;")
        self.signature_label = QLabel()
        self.signature_label.setAlignment(Qt.AlignCenter)
        self.signature_label.setFixedSize(150, 150)
        self.signature_label.setStyleSheet("border: 1px dashed #c0c0c0; background-color: #f0f0f0;")
        upload_button = QPushButton("اضافه کردن امضا")
        upload_button.clicked.connect(self.upload_signature)
        signature_layout.addWidget(self.signature_title_label, alignment=Qt.AlignCenter)
        signature_layout.addWidget(self.signature_label, alignment=Qt.AlignCenter)
        signature_layout.addWidget(upload_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(signature_groupbox)
        button_layout = QHBoxLayout()
        self.add_row_button = QPushButton(QIcon("Images/Add-1.png"), "افزودن سطر")
        self.delete_row_button = QPushButton(QIcon("Images/Delete-1.png"), "حذف سطر")
        button_layout.addStretch()
        button_layout.addWidget(self.add_row_button)
        button_layout.addWidget(self.delete_row_button)
        main_layout.addLayout(button_layout)
        self.add_row_button.clicked.connect(self.add_new_row)
        self.delete_row_button.clicked.connect(self.delete_selected_row)

    def populate_version_table(self):
        data = [("پیمانکار", "پیمانکار"), ("مشاور", "مشاور"), ("کارفرما", "کارفرما")]
        self.version_table.setRowCount(len(data))
        for row_index, (name, nature) in enumerate(data):
            row_item = QTableWidgetItem(str(row_index + 1))
            row_item.setFlags(row_item.flags() & ~Qt.ItemIsEditable)
            row_item.setTextAlignment(Qt.AlignCenter)
            self.version_table.setItem(row_index, 0, row_item)
            name_item = QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignCenter)
            self.version_table.setItem(row_index, 1, name_item)
            abbreviation_item = QTableWidgetItem(name[0])
            abbreviation_item.setTextAlignment(Qt.AlignCenter)
            self.version_table.setItem(row_index, 2, abbreviation_item)
            color_combo = QComboBox()
            colors = {"آبی": "#007BFF", "آبی آسمانی": "#87CEEB", "آبی خاکستری": "#708090", "بنفش": "#800080", "خاکستری": "#808080", "زرد": "#FFFF00", "زیتونی": "#808000", "سبز": "#008000", "سبز کم رنگ": "#90EE90", "سرمه ای": "#000080", "صورتی": "#FFC0CB", "قرمز": "#FF0000", "قهوه ای": "#A52A2A", "مشکی": "#000000", "نارنجی": "#FFA500", "نقره ای": "#C0C0C0"}
            color_combo.addItems(colors.keys())
            self.version_table.setCellWidget(row_index, 3, color_combo)
            color_combo.currentIndexChanged.connect(self.change_row_color)
            default_color = QColor(colors.get(color_combo.currentText(), "#000000"))
            name_item.setForeground(default_color)
            rep_name_item = QTableWidgetItem("")
            rep_name_item.setTextAlignment(Qt.AlignCenter)
            self.version_table.setItem(row_index, 4, rep_name_item)
            nature_combo = QComboBox()
            nature_combo.addItems(["پیمانکار", "ناظر", "مشاور", "مدیر طرح", "کارفرما", "پیمان رسیدگی", "بهره بردار"])
            nature_combo.setCurrentText(nature)
            self.version_table.setCellWidget(row_index, 5, nature_combo)
        self.version_table.selectRow(0)

    def change_row_color(self, index):
        sender_combo = self.sender()
        if sender_combo:
            row = self.version_table.indexAt(sender_combo.pos()).row()
            color_name = sender_combo.currentText()
            colors = {"آبی": "#007BFF", "آبی آسمانی": "#87CEEB", "آبی خاکستری": "#708090", "بنفش": "#800080", "خاکستری": "#808080", "زرد": "#FFFF00", "زیتونی": "#808000", "سبز": "#008000", "سبز کم رنگ": "#90EE90", "سرمه ای": "#000080", "صورتی": "#FFC0CB", "قرمز": "#FF0000", "قهوه ای": "#A52A2A", "مشکی": "#000000", "نارنجی": "#FFA500", "نقره ای": "#C0C0C0"}
            q_color = QColor(colors.get(color_name, "#000000"))
            name_item = self.version_table.item(row, 1)
            if name_item:
                name_item.setForeground(q_color)
    
    def add_new_row(self):
        row_count = self.version_table.rowCount()
        self.version_table.insertRow(row_count)
        row_item = QTableWidgetItem(str(row_count + 1))
        row_item.setFlags(row_item.flags() & ~Qt.ItemIsEditable)
        row_item.setTextAlignment(Qt.AlignCenter)
        self.version_table.setItem(row_count, 0, row_item)
        name = "جدید"
        name_item = QTableWidgetItem(name)
        name_item.setTextAlignment(Qt.AlignCenter)
        self.version_table.setItem(row_count, 1, name_item)
        abbreviation_item = QTableWidgetItem(name[0])
        abbreviation_item.setTextAlignment(Qt.AlignCenter)
        self.version_table.setItem(row_count, 2, abbreviation_item)
        color_combo = QComboBox()
        colors = {"آبی": "#007BFF", "آبی آسمانی": "#87CEEB", "آبی خاکستری": "#708090", "بنفش": "#800080", "خاکستری": "#808080", "زرد": "#FFFF00", "زیتونی": "#808000", "سبز": "#008000", "سبز کم رنگ": "#90EE90", "سرمه ای": "#000080", "صورتی": "#FFC0CB", "قرمز": "#FF0000", "قهوه ای": "#A52A2A", "مشکی": "#000000", "نارنجی": "#FFA500", "نقره ای": "#C0C0C0"}
        color_combo.addItems(colors.keys())
        self.version_table.setCellWidget(row_count, 3, color_combo)
        default_color_name = "مشکی"
        color_combo.setCurrentText(default_color_name)
        q_color = QColor(colors.get(default_color_name, "#000000"))
        name_item.setForeground(q_color)
        color_combo.currentIndexChanged.connect(self.change_row_color)
        rep_name_item = QTableWidgetItem("")
        rep_name_item.setTextAlignment(Qt.AlignCenter)
        self.version_table.setItem(row_count, 4, rep_name_item)
        nature_combo = QComboBox()
        nature_combo.addItems(["پیمانکار", "ناظر", "مشاور", "مدیر طرح", "کارفرما", "پیمان رسیدگی", "بهره بردار"])
        self.version_table.setCellWidget(row_count, 5, nature_combo)
        self.version_table.selectRow(row_count)

    def delete_selected_row(self):
        selected_rows = self.version_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "خطا", "لطفاً یک سطر را برای حذف انتخاب کنید.")
            return
        selected_row_index = selected_rows[0].row()
        self.version_table.removeRow(selected_row_index)
        if selected_row_index in self.signatures_by_row:
            del self.signatures_by_row[selected_row_index]
        new_signatures = {}
        for old_index, signature in self.signatures_by_row.items():
            if old_index > selected_row_index:
                new_signatures[old_index - 1] = signature
            else:
                new_signatures[old_index] = signature
        self.signatures_by_row = new_signatures

    def update_abbreviation(self, row, column):
        if column == 1:
            item = self.version_table.item(row, 1)
            if item and item.text():
                first_char = item.text()[0]
                abbreviation_item = self.version_table.item(row, 2)
                if abbreviation_item:
                    abbreviation_item.setText(first_char)

    def update_signature_display(self):
        selected_items = self.version_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            name_item = self.version_table.item(row, 1)
            if name_item:
                name = name_item.text()
                self.signature_title_label.setText(f"تصویر امضای نماینده ({name})")
            else:
                self.signature_title_label.setText("تصویر امضای نماینده")
            if row in self.signatures_by_row:
                pixmap = self.signatures_by_row[row]
                self.signature_label.setPixmap(pixmap.scaled(self.signature_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.signature_label.clear()

    def upload_signature(self):
        selected_items = self.version_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "خطا", "لطفاً ابتدا یک سطر را انتخاب کنید.")
            return
        row = selected_items[0].row()
        file_path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل امضا", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation), "Images (*.png *.jpg *.jpeg *.svg);;All Files (*)")
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.signatures_by_row[row] = pixmap
                self.signature_label.setPixmap(pixmap.scaled(self.signature_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                QMessageBox.critical(self, "خطا", "فایل انتخاب شده معتبر نیست.")

    def get_stylesheet(self):
        return """
            QDialog { background-color: #f0f0f0; }
            QGroupBox { border: 1px solid #c0c0c0; border-radius: 5px; margin-top: 10px; font-weight: bold; background-color: #ffffff; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
            QTableWidget { border: 1px solid #d0d0d0; background-color: #ffffff; gridline-color: #c0c0c0; }
            QTableWidget::item:alternate { background-color: #f2f2f2; }
            QTableWidget::item:selected { background-color: #a0c4ff; color: black; }
            QHeaderView::section { background-color: #d8e0c9; padding: 5px; border: 1px solid #c0c0c0; font-weight: bold; }
            QPushButton { background-color: #4CAF50; color: white; border: 1px solid #4CAF50; padding: 8px 16px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
            QPlainTextEdit { background-color: #ffffff; border: 1px solid #d0d0d0; }
            QPlainTextEdit::selection { background-color: #a0c4ff; color: black; }
            QComboBox { border: 1px solid #d0d0d0; padding: 5px; text-align: center; }
            QComboBox::drop-down { border: none; }
        """

# --- کلاس CopyDialog ---
class CopyDialog(QDialog):
    def __init__(self, projects_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("کپی پروژه‌ها")
        self.setGeometry(200, 200, 950, 700)
        self.setStyleSheet(self.get_stylesheet())
        self.projects_data = projects_data

        main_grid_layout = QGridLayout()

        # --- ردیف بالا ---
        self.from_project_groupbox = QGroupBox("کپی از پروژه")
        from_project_layout = QVBoxLayout(self.from_project_groupbox)
        self.to_project_groupbox = QGroupBox("کپی به پروژه")
        to_project_layout = QVBoxLayout(self.to_project_groupbox)
        
        from_search_layout = QVBoxLayout()
        from_search_label = QLabel("جستجو")
        from_search_layout.addWidget(from_search_label)
        from_search_input_layout = QHBoxLayout()
        self.from_search_combo = QComboBox()
        self.from_search_combo.addItems(["ID پروژه", "نام پروژه", "نام سازنده یا پیمانکار", "شماره پیمان", "مبنا"])
        self.from_search_input = QLineEdit()
        self.from_search_input.setPlaceholderText("عبارت مورد نظر را تایپ و Enter بزنید...")
        from_search_input_layout.addWidget(self.from_search_combo)
        from_search_input_layout.addWidget(self.from_search_input)
        from_search_layout.addLayout(from_search_input_layout)
        from_project_layout.addLayout(from_search_layout)
        self.from_project_list = QListWidget()
        from_project_layout.addWidget(self.from_project_list)
        
        self.existing_project_radio = QRadioButton("پروژه موجود")
        to_project_layout.addWidget(self.existing_project_radio)
        to_search_layout = QVBoxLayout()
        to_search_label = QLabel("جستجو")
        to_search_layout.addWidget(to_search_label)
        to_search_input_layout = QHBoxLayout()
        self.to_search_combo = QComboBox()
        self.to_search_combo.addItems(["ID پروژه", "نام پروژه", "نام سازنده یا پیمانکار", "شماره پیمان", "مبنا"])
        self.to_search_input = QLineEdit()
        self.to_search_input.setPlaceholderText("عبارت مورد نظر را تایپ و Enter بزنید...")
        to_search_input_layout.addWidget(self.to_search_combo)
        to_search_input_layout.addWidget(self.to_search_input)
        to_search_layout.addLayout(to_search_input_layout)
        to_project_layout.addLayout(to_search_layout)
        self.to_project_list = QListWidget()
        to_project_layout.addWidget(self.to_project_list)

        # اصلاح چیدمان: "کپی از" در ستون 0 (راست) و "کپی به" در ستون 2 (چپ)
        main_grid_layout.addWidget(self.from_project_groupbox, 0, 0)
        
        arrow_label = QLabel()
        arrow_icon_path = os.path.join("Images", "left.png")
        if os.path.exists(arrow_icon_path):
            arrow_label.setPixmap(QPixmap(arrow_icon_path))
        arrow_label.setAlignment(Qt.AlignCenter)
        main_grid_layout.addWidget(arrow_label, 0, 1, 2, 1, Qt.AlignCenter)

        main_grid_layout.addWidget(self.to_project_groupbox, 0, 2)

        # --- ردیف پایین: گزینه‌های کپی ---
        bottom_right_container = QWidget()
        bottom_right_v_layout = QVBoxLayout(bottom_right_container)
        bottom_right_v_layout.setContentsMargins(0,0,0,0)
        
        from_options_groupbox = self.create_from_options_groupbox()
        bottom_right_v_layout.addWidget(from_options_groupbox)

        extra_options_h_layout = QHBoxLayout()
        sections_groupbox = self.create_sections_groupbox()
        booklets_groupbox = self.create_booklets_groupbox()
        extra_options_h_layout.addWidget(sections_groupbox)
        extra_options_h_layout.addWidget(booklets_groupbox)
        bottom_right_v_layout.addLayout(extra_options_h_layout)

        main_grid_layout.addWidget(bottom_right_container, 1, 0)
        
        to_options_groupbox = self.create_to_options_groupbox()
        main_grid_layout.addWidget(to_options_groupbox, 1, 2, Qt.AlignTop)

        # --- دکمه‌های نهایی ---
        button_layout = QHBoxLayout()
        confirm_button = QPushButton("تأیید")
        confirm_button.setAutoDefault(False)
        cancel_button = QPushButton("لغو")
        cancel_button.setAutoDefault(False)
        button_layout.addStretch()
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        final_layout = QVBoxLayout(self)
        final_layout.addLayout(main_grid_layout)
        final_layout.addLayout(button_layout)
        
        self.populate_project_lists()
        confirm_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        self.from_search_input.returnPressed.connect(lambda: self.find_and_select_item(self.from_project_list, self.from_search_combo, self.from_search_input))
        self.to_search_input.returnPressed.connect(lambda: self.find_and_select_item(self.to_project_list, self.to_search_combo, self.to_search_input))
        
        self.to_project_list.itemSelectionChanged.connect(self.highlight_to_groupbox)
        self.from_project_list.itemSelectionChanged.connect(self.highlight_from_groupbox)
        
        self.existing_project_radio.toggled.connect(self.toggle_copy_to_panel)
        self.from_all_revisions_checkbox.stateChanged.connect(self.toggle_revision_options)
        self.from_all_versions_checkbox.stateChanged.connect(self.toggle_version_options)

        self.toggle_copy_to_panel(False)
        self.from_all_revisions_checkbox.setChecked(True)
        self.from_all_versions_checkbox.setChecked(True)

    def create_from_options_groupbox(self):
        groupbox = QGroupBox("کپی از")
        layout = QVBoxLayout(groupbox)
        
        rev_layout = QHBoxLayout()
        self.from_all_revisions_checkbox = QCheckBox("همه صورت جلسه ها")
        rev_layout.addWidget(self.from_all_revisions_checkbox)
        rev_layout.addStretch()
        self.from_revision_combo = QComboBox()
        self.from_revision_combo.addItems([str(i) for i in range(5)])
        rev_layout.addWidget(self.from_revision_combo)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        ver_layout = QHBoxLayout()
        self.from_all_versions_checkbox = QCheckBox("همه نسخه ها")
        ver_layout.addWidget(self.from_all_versions_checkbox)
        ver_layout.addStretch()
        self.from_version_combo = QComboBox()
        self.from_version_combo.addItems(["پیمانکار", "مشاور", "کارفرما"])
        ver_layout.addWidget(self.from_version_combo)
        
        layout.addLayout(rev_layout)
        layout.addWidget(separator)
        layout.addLayout(ver_layout)
        return groupbox

    def create_to_options_groupbox(self):
        groupbox = QGroupBox("کپی به")
        layout = QVBoxLayout(groupbox)

        rev_layout = QHBoxLayout()
        rev_layout.addWidget(QLabel("صورت جلسه ها"))
        rev_layout.addStretch()
        self.to_revision_combo = QComboBox()
        self.to_revision_combo.addItems([str(i) for i in range(5)])
        rev_layout.addWidget(self.to_revision_combo)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        ver_layout = QHBoxLayout()
        ver_layout.addWidget(QLabel("نسخه ها"))
        ver_layout.addStretch()
        self.to_version_combo = QComboBox()
        self.to_version_combo.addItems(["پیمانکار", "مشاور", "کارفرما"])
        ver_layout.addWidget(self.to_version_combo)

        layout.addLayout(rev_layout)
        layout.addWidget(separator)
        layout.addLayout(ver_layout)
        return groupbox

    def create_sections_groupbox(self):
        groupbox = QGroupBox("بخش های")
        layout = QVBoxLayout(groupbox)
        sections = ["مشخصات پیمان", "دفترچه ها و فصول و ضرایب", "ریز متره و خلاصه متره", "برگه مالی"]
        for sec in sections:
            cb = QCheckBox(sec)
            layout.addWidget(cb)
        return groupbox

    def create_booklets_groupbox(self):
        groupbox = QGroupBox("دفترچه های")
        layout = QVBoxLayout(groupbox)
        for i in range(1, 4):
            cb = QCheckBox(f"دفترچه شماره {i}")
            layout.addWidget(cb)
        return groupbox
    
    def toggle_copy_to_panel(self, checked):
        self.to_search_combo.setEnabled(checked)
        self.to_search_input.setEnabled(checked)
        self.to_project_list.setEnabled(checked)
        
        self.to_project_groupbox.setProperty("locked", not checked)
        self.to_project_groupbox.style().unpolish(self.to_project_groupbox)
        self.to_project_groupbox.style().polish(self.to_project_groupbox)
        
    def toggle_revision_options(self, state):
        is_checked = (state == Qt.Checked)
        self.from_revision_combo.setDisabled(is_checked)
        self.to_revision_combo.setDisabled(is_checked)
        
    def toggle_version_options(self, state):
        is_checked = (state == Qt.Checked)
        self.from_version_combo.setDisabled(is_checked)
        self.to_version_combo.setDisabled(is_checked)

    def populate_project_lists(self):
        self.to_project_list.clear()
        self.from_project_list.clear()
        for project in self.projects_data:
            html_text = f"""
            <table width='100%' dir="rtl" style="border-collapse: collapse;">
                <tr>
                    <td width='15%' style='text-align: right; padding: 2px 5px; border-left: 1px solid #eeeeee;'><b>مبنا:</b> {project['basis']}</td>
                    <td width='20%' style='text-align: right; padding: 2px 5px; border-left: 1px solid #eeeeee;'><b>پیمان:</b> {project['contract_number']}</td>
                    <td width='25%' style='text-align: right; padding: 2px 5px; border-left: 1px solid #eeeeee;'><b>سازنده:</b> {project['builder']}</td>
                    <td width='30%' style='text-align: right; padding: 2px 5px; border-left: 1px solid #eeeeee;'><b>نام:</b> {project['name']}</td>
                    <td width='10%' style='text-align: right; padding: 2px 5px;'><b>ID:</b> {project['id']}</td>
                </tr>
            </table>
            """
            
            item_to = QListWidgetItem(self.to_project_list)
            label_to = QLabel(html_text)
            label_to.setStyleSheet("background-color: transparent;")
            item_to.setSizeHint(label_to.sizeHint())
            self.to_project_list.setItemWidget(item_to, label_to)

            item_from = QListWidgetItem(self.from_project_list)
            label_from = QLabel(html_text)
            label_from.setStyleSheet("background-color: transparent;")
            item_from.setSizeHint(label_from.sizeHint())
            self.from_project_list.setItemWidget(item_from, label_from)

    def find_and_select_item(self, list_widget, combo_box, line_edit):
        search_text = line_edit.text().strip().lower()
        if not search_text:
            return
        search_index = combo_box.currentIndex()
        key_map = {0: 'id', 1: 'name', 2: 'builder', 3: 'contract_number', 4: 'basis'}
        search_key = key_map.get(search_index)
        for i in range(list_widget.count()):
            project = self.projects_data[i]
            field_value = str(project.get(search_key, '')).lower()
            if search_text in field_value:
                item = list_widget.item(i)
                list_widget.scrollToItem(item, QAbstractItemView.PositionAtCenter)
                list_widget.setCurrentItem(item)
                return

    def highlight_to_groupbox(self):
        if self.to_project_groupbox.isEnabled():
            self.from_project_groupbox.setStyleSheet(self.get_stylesheet() + "QGroupBox { border: 2px solid transparent; }")
            self.to_project_groupbox.setStyleSheet(self.get_stylesheet() + "QGroupBox { border: 2px solid #a0c4ff; }")

    def highlight_from_groupbox(self):
        self.to_project_groupbox.setStyleSheet(self.get_stylesheet() + "QGroupBox { border: 2px solid transparent; }")
        self.from_project_groupbox.setStyleSheet(self.get_stylesheet() + "QGroupBox { border: 2px solid #a0c4ff; }")
                
    def get_stylesheet(self):
        return """
            QDialog { background-color: #f0f0f0; }
            QGroupBox { border: 2px solid transparent; border-radius: 8px; margin-top: 15px; font-weight: bold; background-color: #ffffff; }
            QGroupBox[locked="true"] { background-color: #e0e0e0; }
            QGroupBox[locked="true"]::title { color: #999999; }
            QListWidget:disabled { background-color: #e0e0e0; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; color: #004d99; }
            QLabel { font-weight: bold; color: #555555; }
            QLineEdit, QComboBox { border: 1px solid #d0d0d0; padding: 5px; }
            QListWidget { border: 1px solid #c0c0c0; background-color: #ffffff; }
            QListWidget::item:selected { background-color: #e0f7fa; }
            QPushButton { background-color: #4CAF50; color: white; border: 1px solid #4CAF50; padding: 8px 16px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
            QRadioButton { spacing: 5px; }
            QRadioButton::indicator { width: 15px; height: 15px; }
            QRadioButton::indicator::checked { background-color: #4CAF50; border-radius: 7px; border: 1px solid #45a049; }
            QRadioButton::indicator::unchecked { background-color: #ffffff; border-radius: 7px; border: 1px solid #c0c0c0; }
        """

# --- کلاس داشبورد ---
class Dashboard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sina Manager Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_stylesheet())

        menubar = self.menuBar()
        file_menu = menubar.addMenu("پرونده")
        edit_menu = menubar.addMenu("ویرایش")
        view_menu = menubar.addMenu("مشاهده")
        help_menu = menubar.addMenu("راهنما")
        
        toolbar = QToolBar("ابزار اصلی")
        self.addToolBar(toolbar)
        toolbar.setStyleSheet("QToolBar { background: #f0f0f0; border-bottom: 1px solid #c0c0c0; }")
        
        self.backup_action = QAction(QIcon("Images/Recovery.png"), "پشتیبان", self)
        self.restore_action = QAction(QIcon("Images/Restore.png"), "بازیابی", self)
        
        self.backup_action.triggered.connect(self.backup_data)
        self.restore_action.triggered.connect(self.restore_data)
        
        toolbar.addAction(self.backup_action)
        toolbar.addAction(self.restore_action)

        self.version_action = QAction(QIcon("Images/Version.png"), "نسخه", self)
        self.copy_action = QAction(QIcon("Images/Copy.png"), "کپی", self)
        self.remote_action = QAction(QIcon("Images/Remote.png"), "ریموت", self)
        self.print_action = QAction(QIcon("Images/Printer.png"), "چاپ", self)

        self.version_action.triggered.connect(self.show_version)
        self.copy_action.triggered.connect(self.show_copy_dialog)
        self.remote_action.triggered.connect(self.start_remote)
        self.print_action.triggered.connect(self.print_document)

        toolbar.addAction(self.version_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.remote_action)
        toolbar.addAction(self.print_action)

        self.addToolBarBreak()
        
        toolbar2 = QToolBar("ابزار عملیات")
        self.addToolBar(toolbar2)
        toolbar2.setStyleSheet("QToolBar { background: #f0f0f0; border-bottom: 1px solid #c0c0c0; }")
        
        self.new_action = QAction(QIcon("Images/Add.png"), "جدید", self)
        self.delete_action = QAction(QIcon("Images/Delete.png"), "حذف", self)
        
        self.new_action.triggered.connect(self.new_item)
        self.delete_action.triggered.connect(self.delete_item)

        toolbar2.addAction(self.new_action)
        toolbar2.addAction(self.delete_action)

        filter_toolbar = QToolBar("فیلتر")
        self.addToolBar(filter_toolbar)
        filter_toolbar.setStyleSheet("QToolBar { background: #f0f0f0; border-bottom: 1px solid #c0c0c0; }")

        filter_toolbar.addWidget(QLabel("جستجو بر اساس نام پروژه:"))
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("نام پروژه...")
        self.project_name_input.setMinimumWidth(200)
        filter_toolbar.addWidget(self.project_name_input)
        
        filter_toolbar.addWidget(QLabel("تاریخ:"))
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("تاریخ...")
        self.date_input.setMinimumWidth(120)
        filter_toolbar.addWidget(self.date_input)

        filter_button = QPushButton("فیلتر")
        filter_button.setStyleSheet("QPushButton { border: 1px solid #c0c0c0; padding: 5px 10px; }")
        filter_toolbar.addWidget(filter_button)

        filter_button.clicked.connect(self.apply_filter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "نام پروژه", "نام سازنده یا پیمانکار", "شماره پیمان", "مبنا", "ایجاد کننده", "تاریخ"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        self.table.doubleClicked.connect(self.on_table_double_clicked)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)

        main_layout.addWidget(self.table)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("QStatusBar { background-color: #d8e0c9; color: #555555; }")
        
        open_button = QPushButton("باز کردن پروژه")
        open_icon_path = os.path.join("Images", "Open folder.png")
        if os.path.exists(open_icon_path):
            open_button.setIcon(QIcon(open_icon_path))
            open_button.setIconSize(QSize(24, 24))
        open_button.clicked.connect(self.open_project)
        
        close_button = QPushButton("بستن برنامه")
        close_icon_path = os.path.join("Images", "Exit.png")
        if os.path.exists(close_icon_path):
            close_button.setIcon(QIcon(close_icon_path))
            close_button.setIconSize(QSize(24, 24))
        close_button.clicked.connect(QApplication.quit)
        
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(open_button)
        button_layout.addWidget(close_button)

        self.new_window_checkbox = QCheckBox("در پنجره جدید")
        full_tree_label = QLabel("درخت کامل پروژه ها")
        
        options_widget = QWidget()
        options_layout = QHBoxLayout(options_widget)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.addWidget(self.new_window_checkbox)
        options_layout.addWidget(QLabel("|"))
        options_layout.addWidget(full_tree_label)
        
        database_widget = QWidget()
        database_layout = QHBoxLayout(database_widget)
        database_layout.setContentsMargins(0, 0, 0, 0)
        database_layout.setSpacing(5)

        sql_icon_label = QLabel()
        sql_icon = QPixmap(os.path.join("Images", "Database.png")).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        sql_icon_label.setPixmap(sql_icon)
        
        sql_name_label = QLabel("sinadb.mdf")
        sql_name_label.setToolTip("نام دیتابیس متصل")

        database_layout.addWidget(sql_icon_label)
        database_layout.addWidget(sql_name_label)
        
        self.project_count_label = QLabel()
        self.version_label = QLabel("ورژن: 1.0")

        self.statusBar.addPermanentWidget(button_widget)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(options_widget)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(database_widget)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.project_count_label)
        self.statusBar.addPermanentWidget(QLabel("|"))
        self.statusBar.addPermanentWidget(self.version_label)
        
        self.original_data = [
            ["1", "پروژه A", "پیمانکار الف", "12345", "مبنای اول", "کاربر ۱", "1402/05/20"],
            ["2", "پروژه B", "پیمانکار ب", "23456", "مبنای دوم", "کاربر ۲", "1402/05/21"],
            ["3", "پروژه C", "پیمانکار ج", "34567", "مبنای سوم", "کاربر ۳", "1402/05/22"],
        ]
        
        self.populate_table(self.original_data)
    
    def on_table_double_clicked(self, index):
        self.open_project()

    def open_project(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "خطا", "لطفاً یک پروژه را انتخاب کنید.")
            return
        row_index = selected_rows[0].row()
        project_name = self.table.item(row_index, 1).text()
        if self.new_window_checkbox.isChecked():
            QMessageBox.information(self, "باز کردن پروژه", f"پروژه '{project_name}' در یک پنجره جدید باز می‌شود.")
        else:
            QMessageBox.information(self, "باز کردن پروژه", f"پروژه '{project_name}' در همین پنجره باز می‌شود.")
   
    def update_project_count_label(self):
        count = self.table.rowCount()
        self.project_count_label.setText(f"تعداد پروژه‌ها: {count}")
        
    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)
        self.update_project_count_label()

    def apply_filter(self):
        project_name_text = self.project_name_input.text().strip()
        date_text = self.date_input.text().strip()
        
        filtered_data = []
        for row_data in self.original_data:
            project_name = row_data[1]
            date = row_data[6]
            match_name = project_name_text.lower() in project_name.lower() or not project_name_text
            match_date = date_text in date or not date_text
            if match_name and match_date:
                filtered_data.append(row_data)
        self.populate_table(filtered_data)

    def show_copy_dialog(self):
        projects_data = []
        for row_data in self.original_data:
            projects_data.append({
                "id": row_data[0],
                "name": row_data[1],
                "builder": row_data[2],
                "contract_number": row_data[3],
                "basis": row_data[4]
            })
        dialog = CopyDialog(projects_data, self)
        dialog.exec()
    
    def backup_data(self):
        projects = []
        for row in range(self.table.rowCount()):
            project_id = self.table.item(row, 0).text()
            project_name = self.table.item(row, 1).text()
            projects.append((project_id, project_name))
        backup_dialog = BackupDialog(projects, self)
        if backup_dialog.exec() == QDialog.Accepted:
            pass

    def restore_data(self):
        restore_dialog = RestoreDialog(self)
        restore_dialog.exec()

    def show_version(self):
        version_dialog = VersionDialog(self)
        version_dialog.exec()

    def start_remote(self):
        QMessageBox.information(self, "ریموت", "ارتباط از راه دور در حال برقرار شدن است...")
        print("Remote button clicked!")

    def print_document(self):
        QMessageBox.information(self, "چاپ", "سند در حال آماده‌سازی برای چاپ است...")
        print("Print button clicked!")

    def new_item(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        current_date = QDateTime.currentDateTime().toString("yyyy/MM/dd")
        new_row_data = [
            str(row_count + 1), "پروژه جدید", "نام پیمانکار", "شماره پیمان", "مبنا", "نام ایجاد کننده", current_date
        ]
        for col_index, cell_data in enumerate(new_row_data):
            item = QTableWidgetItem(cell_data)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row_count, col_index, item)
        QMessageBox.information(self, "جدید", "یک ردیف جدید به جدول اضافه شد.")
        self.update_project_count_label()
        
    def delete_item(self):
        selected_rows = sorted(list(set(index.row() for index in self.table.selectedIndexes())))
        if not selected_rows:
            QMessageBox.warning(self, "حذف", "هیچ ردیفی برای حذف انتخاب نشده است.")
            return
        reply = QMessageBox.question(self, "تأیید حذف", "آیا مطمئن هستید که می‌خواهید ردیف‌های انتخاب شده را حذف کنید؟", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            for row in reversed(selected_rows):
                self.table.removeRow(row)
            QMessageBox.information(self, "حذف", f"{len(selected_rows)} ردیف با موفقیت حذف شد.")

    def get_stylesheet(self):
        return """
            QMainWindow { background-color: #f0f0f0; }
            QDockWidget { border: 1px solid #c0c0c0; background-color: #ffffff; }
            QDockWidget::title { text-align: center; background: #e0e0e0; padding: 5px; }
            QTableWidget { background-color: #ffffff; border: 1px solid #c0c0c0; gridline-color: #d0d0d0; }
            QTableWidget::item:alternate { background-color: #f2f2f2; }
            QTableWidget::item:selected { background-color: #a0c4ff; color: black; }
            QHeaderView::section { background-color: #d8e0c9; padding: 5px; border: 1px solid #c0c0c0; font-weight: bold; }
            QPushButton { background-color: #4CAF50; color: white; border: 1px solid #4CAF50; padding: 8px 16px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
            QFrame { background-color: #d8e0c9; }
            QCheckBox { spacing: 5px; }
            QCheckBox::indicator { width: 20px; height: 20px; }
            QLabel { font-weight: bold; color: #555555; }
            QStatusBar { background-color: #d8e0c9; color: #555555; }
            QStatusBar::item { border: none; }
        """

# --- تابع برای خواندن نام کاربری از قفل سخت‌افزاری (کد نمونه) ---
def get_username_from_hardware_lock():
    return "کامنرسا"

# --- کلاس اصلی صفحه ورود با اعتبارسنجی ---
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.dashboard_window = None

        self.ui.pushButtonConfirm.clicked.connect(self.show_dashboard)
        self.ui.pushButtonCancel.clicked.connect(self.close)
        
        try:
            self.username_input = self.ui.lineEdit 
            self.password_input = self.ui.lineEdit_2
            username = get_username_from_hardware_lock()
            self.username_input.setText(username)
            font = self.username_input.font()
            font.setBold(True)
            self.username_input.setFont(font)
        except AttributeError as e:
            print(f"Error: Could not find username or password input fields. Please check ui_sinamanager.py. Details: {e}")
            self.username_input = QLineEdit()
            self.password_input = QLineEdit()
        
        self.background_pixmap = QPixmap()
        self.background_item = None
        self.overlay_rect = None
        
        try:
            logo_path = os.path.join("Images", "logo.jpeg")
            if os.path.exists(logo_path):
                pixmap_logo = QPixmap(logo_path)
                self.ui.labelLogo.setPixmap(pixmap_logo)
                self.ui.labelLogo.setScaledContents(True)
                
            image_path = os.path.join("Images", "Gemini_Generated_Image_1.png")
            
            if os.path.exists(image_path):
                self.background_pixmap = QPixmap(image_path)
                
                self.scene = QGraphicsScene(self.ui.graphicsViewBackground)
                self.ui.graphicsViewBackground.setScene(self.scene)
                
                self.background_item = QGraphicsPixmapItem(self.background_pixmap)
                self.scene.addItem(self.background_item)

                self.overlay_rect = QGraphicsRectItem()
                self.overlay_rect.setBrush(QColor(0, 0, 0, 100)) 
                self.scene.addItem(self.overlay_rect)
            else:
                self.ui.graphicsViewBackground.setStyleSheet("background-color: #f0f0f0;")
                
        except Exception as e:
            print(f"Error loading background or logo. Details: {e}")
            self.ui.graphicsViewBackground.setStyleSheet("background-color: #f0f0f0;")

        style_sheet = """
            QGroupBox { background-color: transparent; border: 2px solid white; border-radius: 8px; font-size: 16px; color: white; }
            QLabel { color: white; font-weight: bold; }
            QLineEdit { background-color: transparent; border: 1px solid white; border-radius: 5px; padding: 5px; color: white; }
            QLineEdit::selection { color: black; background-color: white; }
            QPushButton { background-color: transparent; color: white; border: 1px solid white; border-radius: 5px; padding: 5px 10px; min-height: 25px; font-size: 14px; }
            QPushButton:hover { background-color: rgba(255, 255, 255, 50); border: 1px solid white; }
            QLabel#labelSoftwareName { color: orange; font-size: 36px; }
            QLabel#labelSoftwareDescription { color: #ffaa7f; font-size: 18px; }
            QLabel#labelCompanyInfo { color: orange; }
            QLabel#labelLocation { color: white; }
        """
        self.setStyleSheet(style_sheet)

        labels_with_shadow = ['labelSoftwareName', 'labelSoftwareDescription', 'labelCompanyInfo', 'labelLocation']
        for label_name in labels_with_shadow:
            if hasattr(self.ui, label_name):
                label = getattr(self.ui, label_name)
                shadow = QGraphicsDropShadowEffect(label)
                shadow.setBlurRadius(20)
                shadow.setColor(QColor(0, 0, 0, 200))
                shadow.setOffset(5, 5)
                label.setGraphicsEffect(shadow)

        self.ui.graphicsViewBackground.lower()
        if hasattr(self.ui, 'groupBox'):
            self.ui.groupBox.raise_()
        if hasattr(self.ui, 'labelLogo'):
            self.ui.labelLogo.raise_()
        if hasattr(self.ui, 'labelSoftwareName'):
            self.ui.labelSoftwareName.raise_()
        if hasattr(self.ui, 'labelSoftwareDescription'):
            self.ui.labelSoftwareDescription.raise_()
        if hasattr(self.ui, 'labelCompanyInfo'):
            self.ui.labelCompanyInfo.raise_()
        if hasattr(self.ui, 'labelLocation'):
            self.ui.labelLocation.raise_()
    
    def show_dashboard(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if username == "کامنرسا" and password == "31180":
            if self.dashboard_window is None:
                self.dashboard_window = Dashboard()
            
            self.hide()
            self.dashboard_window.show()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("خطای ورود")
            msg_box.setText("نام کاربری یا رمز عبور اشتباه است.")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet("""
                QMessageBox { background-color: #333333; color: white; font-size: 14px; }
                QLabel { color: white; }
                QPushButton { background-color: white; color: black; border: 1px solid black; border-radius: 4px; padding: 5px 15px; }
            """)
            msg_box.exec()
    
    def update_background_image(self):
        if self.background_pixmap.isNull() or not self.background_item:
            return
        view_size = self.ui.graphicsViewBackground.size()
        if view_size.isEmpty():
            return
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.ui.graphicsViewBackground.fitInView(self.background_item, Qt.KeepAspectRatioByExpanding)
        if self.overlay_rect:
            self.overlay_rect.setRect(self.scene.sceneRect())

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.update_background_image()

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        QTimer.singleShot(10, self.update_background_image)
        self.password_input.setFocus()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setLayoutDirection(Qt.RightToLeft)
    
    try:
        dialog = LoginDialog()
        dialog.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")