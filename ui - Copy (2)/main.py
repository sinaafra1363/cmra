import sys
import os
from PySide6.QtWidgets import (QApplication, QDialog, QGraphicsScene, QGraphicsPixmapItem, 
                               QGraphicsView, QGraphicsRectItem, QGraphicsDropShadowEffect, 
                               QGroupBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTableWidget, QTableWidgetItem, QHeaderView, QDockWidget,
                               QListWidget, QPushButton, QTextEdit, QLabel, QLineEdit,
                               QMessageBox, QToolBar, QMenu, QMenuBar, QFrame)
from PySide6.QtGui import QPixmap, QResizeEvent, QColor, QAction, QIcon
from PySide6.QtCore import Qt, QRectF, QSize

# تلاش برای وارد کردن کلاس طراحی UI
try:
    from ui_sinamanager import Ui_LoginDialog
except ImportError as e:
    print(f"Error: Could not import Ui_LoginDialog. Please ensure ui_sinamanager.py is in the correct path and generated correctly. Details: {e}")
    sys.exit(1)

# --- کلاس داشبورد اصلاح شده بر اساس طرح بصری شما ---
class Dashboard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sina Manager Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_stylesheet())

        # --- ایجاد نوار منو ---
        menubar = self.menuBar()
        file_menu = menubar.addMenu("پرونده")
        edit_menu = menubar.addMenu("ویرایش")
        view_menu = menubar.addMenu("مشاهده")
        help_menu = menubar.addMenu("راهنما")
        
        # --- ایجاد نوار ابزار و اضافه کردن دکمه‌ها ---
        toolbar = QToolBar("ابزار")
        self.addToolBar(toolbar)
        toolbar.setStyleSheet("QToolBar { background: #f0f0f0; border-bottom: 1px solid #c0c0c0; }")
        
        # --- اضافه کردن گزینه‌های پشتیبان و بازیابی ---
        self.backup_action = QAction(QIcon("ui/Images/backup_icon.png"), "پشتیبان", self)
        self.restore_action = QAction(QIcon("ui/Images/restore_icon.png"), "بازیابی", self)
        
        self.backup_action.triggered.connect(self.backup_data)
        self.restore_action.triggered.connect(self.restore_data)
        
        toolbar.addAction(self.backup_action)
        toolbar.addAction(self.restore_action)

        # --- اضافه کردن گزینه‌های جدید: نسخه، کپی، ریموت و چاپ ---
        self.version_action = QAction(QIcon("ui/Images/version_icon.png"), "نسخه", self)
        self.copy_action = QAction(QIcon("ui/Images/copy_icon.png"), "کپی", self)
        self.remote_action = QAction(QIcon("ui/Images/remote_icon.png"), "ریموت", self)
        self.print_action = QAction(QIcon("ui/Images/print_icon.png"), "چاپ", self)

        self.version_action.triggered.connect(self.show_version)
        self.copy_action.triggered.connect(self.copy_content)
        self.remote_action.triggered.connect(self.start_remote)
        self.print_action.triggered.connect(self.print_document)

        toolbar.addAction(self.version_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.remote_action)
        toolbar.addAction(self.print_action)

        # --- ایجاد ویجت مرکزی ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- ستون سمت راست: منو و فیلترها ---
        left_dock = QDockWidget("منو", self)
        left_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        left_dock_widget = QWidget()
        left_layout = QVBoxLayout(left_dock_widget)
        
        main_menu_list = QListWidget()
        main_menu_list.addItem("وضعیت و صورت وضعیت")
        main_menu_list.setStyleSheet("QListWidget { background-color: #e0e0e0; border: none; }")
        left_layout.addWidget(main_menu_list)

        filter_groupbox = QGroupBox("فیلتر صورت وضعیت")
        filter_groupbox.setStyleSheet("QGroupBox { font-weight: bold; }")
        filter_layout = QVBoxLayout(filter_groupbox)

        self.project_name_input = QLineEdit()
        self.date_input = QLineEdit()
        self.apply_filter_button = QPushButton("اعمال فیلتر")

        filter_layout.addWidget(QLabel("نام پروژه"))
        filter_layout.addWidget(self.project_name_input)
        filter_layout.addWidget(QLabel("تاریخ"))
        filter_layout.addWidget(self.date_input)
        filter_layout.addWidget(self.apply_filter_button)
        left_layout.addWidget(filter_groupbox)
        
        left_dock.setWidget(left_dock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, left_dock)

        self.apply_filter_button.clicked.connect(self.apply_filter)

        # --- ستون میانی: جدول داده‌ها ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ردیف", "نام", "توضیحات", "تاریخ"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.populate_table()
        
        main_layout.addWidget(self.table)

        # --- ستون سمت چپ: جزئیات / لاگ ---
        right_dock = QDockWidget("جزئیات", self)
        right_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        right_dock_widget = QWidget()
        right_layout = QVBoxLayout(right_dock_widget)
        right_layout.addWidget(QLabel("جزئیات ردیف انتخاب شده:"))
        right_layout.addWidget(QTextEdit())
        right_dock.setWidget(right_dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, right_dock)

    def populate_table(self, data=None):
        if data is None:
            data = [
                ["1", "ردیف 1", "توضیحات مربوط به داده", "1402/05/20"],
                ["2", "ردیف 2", "توضیحات مربوط به داده", "1402/05/21"],
                ["3", "ردیف 3", "توضیحات مربوط به داده", "1402/05/22"],
                ["4", "ردیف 4", "توضیحات مربوط به داده", "1402/05/23"],
                ["5", "ردیف 5", "توضیحات مربوط به داده", "1402/05/24"],
                ["6", "ردیف 6", "توضیحات مربوط به داده", "1402/05/25"],
                ["7", "ردیف 7", "توضیحات مربوط به داده", "1402/05/26"],
                ["8", "ردیف 8", "توضیحات مربوط به داده", "1402/05/27"],
                ["9", "ردیف 9", "توضیحات مربوط به داده", "1402/05/28"],
                ["10", "ردیف 10", "توضیحات مربوط به داده", "1402/05/29"],
            ]
        
        self.table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

    def apply_filter(self):
        project_name = self.project_name_input.text()
        date = self.date_input.text()
        
        print(f"Filter button clicked! Project Name: '{project_name}', Date: '{date}'")
        
    def backup_data(self):
        """
        این تابع برای انجام عملیات پشتیبان‌گیری از داده‌ها استفاده می‌شود.
        """
        QMessageBox.information(self, "پشتیبان‌گیری", "عملیات پشتیبان‌گیری در حال انجام است...")
        print("Backup button clicked!")

    def restore_data(self):
        """
        این تابع برای انجام عملیات بازیابی داده‌ها استفاده می‌شود.
        """
        QMessageBox.information(self, "بازیابی", "عملیات بازیابی در حال انجام است...")
        print("Restore button clicked!")

    # --- توابع جدید برای مدیریت دکمه‌ها ---
    def show_version(self):
        QMessageBox.information(self, "نسخه", "نسخه نرم‌افزار: 1.0")
        print("Version button clicked!")

    def copy_content(self):
        QMessageBox.information(self, "کپی", "محتوای انتخاب شده کپی شد.")
        print("Copy button clicked!")

    def start_remote(self):
        QMessageBox.information(self, "ریموت", "ارتباط از راه دور در حال برقرار شدن است...")
        print("Remote button clicked!")

    def print_document(self):
        QMessageBox.information(self, "چاپ", "سند در حال آماده‌سازی برای چاپ است...")
        print("Print button clicked!")

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QDockWidget {
                border: 1px solid #c0c0c0;
                background-color: #ffffff;
            }
            QDockWidget::title {
                text-align: center;
                background: #e0e0e0;
                padding: 5px;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #c0c0c0;
                gridline-color: #d0d0d0;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 1px solid #4CAF50;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

# --- تابع برای خواندن نام کاربری از قفل سخت‌افزاری (کد نمونه) ---
def get_username_from_hardware_lock():
    """
    این تابع باید با کد مربوط به قفل سخت‌افزاری شما جایگزین شود.
    در حال حاضر، یک نام کاربری ثابت را برمی‌گرداند.
    """
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

        except AttributeError as e:
            print(f"Error: Could not find username or password input fields. Please check ui_sinamanager.py. Details: {e}")
            self.username_input = QLineEdit()
            self.password_input = QLineEdit()
        
        self.background_pixmap = QPixmap()
        self.background_item = None
        self.overlay_rect = None
        
        try:
            logo_path = os.path.join("ui", "Images", "logo.jpeg")
            if os.path.exists(logo_path):
                pixmap_logo = QPixmap(logo_path)
                self.ui.labelLogo.setPixmap(pixmap_logo)
                self.ui.labelLogo.setScaledContents(True)
                
            image_path = os.path.join("ui", "Images", "Gemini_Generated_Image_1.png")
            
            if os.path.exists(image_path):
                self.background_pixmap = QPixmap(image_path)
                
                self.scene = QGraphicsScene(self.ui.graphicsViewBackground)
                self.ui.graphicsViewBackground.setScene(self.scene)
                self.background_item = QGraphicsPixmapItem(self.background_pixmap)
                self.scene.addItem(self.background_item)

                self.overlay_rect = QGraphicsRectItem()
                self.overlay_rect.setBrush(QColor(0, 0, 0, 100)) 
                self.scene.addItem(self.overlay_rect)

                self.adjust_background_size()
            else:
                self.ui.graphicsViewBackground.setStyleSheet("background-color: #f0f0f0;")
                
        except Exception as e:
            print(f"Error loading background or logo. Details: {e}")
            self.ui.graphicsViewBackground.setStyleSheet("background-color: #f0f0f0;")

        style_sheet = """
            QGroupBox {
                background-color: transparent; 
                border: 2px solid white; 
                border-radius: 8px;
                font-size: 16px;
                color: white; 
            }
            QLabel {
                color: white; 
                font-weight: bold;
            }
            QLineEdit {
                background-color: transparent; 
                border: 1px solid white; 
                border-radius: 5px;
                padding: 5px;
                color: white; 
            }
            QPushButton {
                background-color: transparent; 
                color: white; 
                border: 1px solid white; 
                border-radius: 5px;
                padding: 5px 10px; 
                min-height: 25px; 
                font-size: 14px; 
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50); 
                border: 1px solid white; 
            }
            QLabel#labelSoftwareName {
                color: orange;
                font-size: 36px;
            }
            QLabel#labelSoftwareDescription {
                color: #ffaa7f;
                font-size: 18px;
            }
            QLabel#labelCompanyInfo {
                color: orange;
            }
            QLabel#labelLocation {
                color: white;
            }
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
        
        print(f"Username entered: '{username}'")
        print(f"Password entered: '{password}'")
        
        if username == "کامنرسا" and password == "31180":
            if self.dashboard_window is None:
                self.dashboard_window = Dashboard()
            
            self.hide()
            self.dashboard_window.show()
        else:
            QMessageBox.warning(self, "خطای ورود", "نام کاربری یا رمز عبور اشتباه است.")

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.adjust_background_size()

    def adjust_background_size(self):
        if self.background_pixmap.isNull() or not self.background_item:
            return

        view_size = self.ui.graphicsViewBackground.size()
        if view_size.isEmpty():
            return

        scaled_pixmap = self.background_pixmap.scaled(
            view_size, 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.background_item.setPixmap(scaled_pixmap)
        
        x = (view_size.width() - scaled_pixmap.width()) / 2
        y = (view_size.height() - scaled_pixmap.height()) / 2

        self.background_item.setPos(x, y)
        self.scene.setSceneRect(0, 0, view_size.width(), view_size.height())

        if self.overlay_rect:
            self.overlay_rect.setRect(0, 0, view_size.width(), view_size.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # --- تغییر مهم در اینجا ---
    # تنظیم جهت‌دهی سراسری برنامه به راست به چپ
    app.setLayoutDirection(Qt.RightToLeft)
    
    # اجرای برنامه در یک بلوک try...except برای اشکال‌یابی بهتر
    try:
        dialog = LoginDialog()
        dialog.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")