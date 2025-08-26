# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sinamanager.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGraphicsView, QGroupBox,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.resize(400, 450)
        self.graphicsViewBackground = QGraphicsView(LoginDialog)
        self.graphicsViewBackground.setObjectName(u"graphicsViewBackground")
        self.graphicsViewBackground.setGeometry(QRect(-10, 0, 411, 451))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewBackground.sizePolicy().hasHeightForWidth())
        self.graphicsViewBackground.setSizePolicy(sizePolicy)
        self.graphicsViewBackground.setInteractive(False)
        self.groupBox = QGroupBox(LoginDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(100, 110, 201, 161))
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"    background-color: transparent; \n"
"    border: 2px solid white; \n"
"    border-radius: 8px;\n"
"    font-size: 16px;\n"
"}\n"
"QLabel {\n"
"    color: white; \n"
"    font-weight: bold;\n"
"}")
        self.lineEditUsername = QLabel(self.groupBox)
        self.lineEditUsername.setObjectName(u"lineEditUsername")
        self.lineEditUsername.setGeometry(QRect(132, 30, 51, 16))
        self.lineEditPassword = QLabel(self.groupBox)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setGeometry(QRect(130, 60, 44, 16))
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 26, 118, 52))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.pushButtonConfirm = QPushButton(self.groupBox)
        self.pushButtonConfirm.setObjectName(u"pushButtonConfirm")
        self.pushButtonConfirm.setGeometry(QRect(102, 110, 75, 25))
        self.pushButtonConfirm.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButtonConfirm.setAutoFillBackground(False)
        self.pushButtonCancel = QPushButton(self.groupBox)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setGeometry(QRect(21, 110, 75, 25))
        self.pushButtonCancel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButtonCancel.setAutoFillBackground(False)
        self.labelLogo = QLabel(LoginDialog)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setGeometry(QRect(150, 280, 91, 61))
        self.labelLogo.setPixmap(QPixmap(u":/logos/Images/logo.jpeg"))
        self.labelLogo.setScaledContents(True)
        self.labelCompanyInfo = QLabel(LoginDialog)
        self.labelCompanyInfo.setObjectName(u"labelCompanyInfo")
        self.labelCompanyInfo.setGeometry(QRect(140, 350, 111, 31))
        self.labelCompanyInfo.setStyleSheet(u"QGroupBox {\n"
"    background-color: transparent; \n"
"    border: 2px solid white; \n"
"    border-radius: 8px;\n"
"    font-size: 16px;\n"
"}\n"
"QLabel {\n"
"    color: white; \n"
"    font-weight: bold;\n"
"}")
        self.labelCompanyInfo.setMargin(0)
        self.labelCompanyInfo.setIndent(7)
        self.labelCompanyInfo.setOpenExternalLinks(False)
        self.labelSoftwareName = QLabel(LoginDialog)
        self.labelSoftwareName.setObjectName(u"labelSoftwareName")
        self.labelSoftwareName.setGeometry(QRect(150, 10, 111, 51))
        self.labelSoftwareName.setMinimumSize(QSize(9, 9))
        self.labelSoftwareName.setBaseSize(QSize(9, 9))
        font = QFont()
        font.setFamilies([u"B Nazanin"])
        font.setPointSize(36)
        font.setBold(True)
        self.labelSoftwareName.setFont(font)
        self.labelSoftwareName.setStyleSheet(u"color: orange;")
        self.labelSoftwareName.setScaledContents(True)
        self.labelSoftwareName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelSoftwareName.setMargin(0)
        self.labelSoftwareName.setIndent(7)
        self.labelSoftwareName.setOpenExternalLinks(False)
        self.labelSoftwareDescription = QLabel(LoginDialog)
        self.labelSoftwareDescription.setObjectName(u"labelSoftwareDescription")
        self.labelSoftwareDescription.setGeometry(QRect(50, 60, 291, 51))
        self.labelSoftwareDescription.setMinimumSize(QSize(9, 9))
        self.labelSoftwareDescription.setBaseSize(QSize(9, 9))
        font1 = QFont()
        font1.setFamilies([u"B Nazanin"])
        font1.setPointSize(18)
        font1.setBold(True)
        self.labelSoftwareDescription.setFont(font1)
        self.labelSoftwareDescription.setStyleSheet(u"color: #ffaa7f;")
        self.labelSoftwareDescription.setScaledContents(True)
        self.labelSoftwareDescription.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelSoftwareDescription.setMargin(0)
        self.labelSoftwareDescription.setIndent(7)
        self.labelSoftwareDescription.setOpenExternalLinks(False)
        self.labelLocation = QLabel(LoginDialog)
        self.labelLocation.setObjectName(u"labelLocation")
        self.labelLocation.setGeometry(QRect(20, 390, 371, 51))
        self.labelLocation.setMinimumSize(QSize(9, 9))
        self.labelLocation.setBaseSize(QSize(9, 9))
        font2 = QFont()
        font2.setFamilies([u"B Nazanin"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.labelLocation.setFont(font2)
        self.labelLocation.setStyleSheet(u"QGroupBox {\n"
"    background-color: transparent; \n"
"    border: 2px solid white; \n"
"    border-radius: 8px;\n"
"    font-size: 16px;\n"
"}\n"
"QLabel {\n"
"    color: white; \n"
"    font-weight: bold;\n"
"}")
        self.labelLocation.setScaledContents(True)
        self.labelLocation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelLocation.setWordWrap(True)
        self.labelLocation.setMargin(0)
        self.labelLocation.setIndent(7)
        self.labelLocation.setOpenExternalLinks(False)

        self.retranslateUi(LoginDialog)

        QMetaObject.connectSlotsByName(LoginDialog)
    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QCoreApplication.translate("LoginDialog", u"\u0648\u0631\u0648\u062f \u0628\u0647 \u0633\u0627\u0645\u0627\u0646\u0647", None))
        self.groupBox.setTitle(QCoreApplication.translate("LoginDialog", u"\u0641\u0631\u0645 \u0648\u0631\u0648\u062f", None))
        self.lineEditUsername.setText(QCoreApplication.translate("LoginDialog", u"\u0646\u0627\u0645 \u06a9\u0627\u0631\u0628\u0631\u06cc:", None))
        self.lineEditPassword.setText(QCoreApplication.translate("LoginDialog", u"\u0631\u0645\u0632 \u0639\u0628\u0648\u0631:", None))
        self.pushButtonConfirm.setText(QCoreApplication.translate("LoginDialog", u"\u062a\u0623\u06cc\u06cc\u062f", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("LoginDialog", u"\u0644\u063a\u0648", None))
        self.labelLogo.setText("")
        self.labelCompanyInfo.setText(QCoreApplication.translate("LoginDialog", u"www.comnersa.ir", None))
        self.labelSoftwareName.setText(QCoreApplication.translate("LoginDialog", u"\u0631\u0633\u0627", None))
        self.labelSoftwareDescription.setText(QCoreApplication.translate("LoginDialog", u"\u0646\u0631\u0645 \u0627\u0641\u0632\u0627\u0631 \u0635\u0648\u0631\u062a \u062c\u0644\u0633\u0647 \u0646\u0648\u06cc\u0633\u06cc", None))
        self.labelLocation.setText(QCoreApplication.translate("LoginDialog", u"\u0622\u062f\u0631\u0633: \u067e\u06cc\u0686 \u0634\u0645\u06cc\u0631\u0627\u0646 - \u0628\u0646 \u0628\u0633\u062a \u0631\u06cc\u062d\u0627\u0646\u06cc \u067e\u0644\u0627\u06a9 1 - \u0637\u0628\u0642\u0647 \u062f\u0648\u0645 \u0634\u0631\u0642\u06cc \u062a\u0644\u0641\u0646 \u062a\u0645\u0627\u0633: 09199524011", None))
    # retranslateUi

