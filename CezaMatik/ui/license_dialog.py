from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lisans")
        self.setMinimumSize(720, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel("Lisans ve Üçüncü Taraf Bileşenler")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        text = QTextBrowser()
        text.setReadOnly(True)
        text.setOpenExternalLinks(True)
        text.setStyleSheet("""
            QTextBrowser {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        text.setHtml("""
            <h3>Bu uygulamada kullanılan arayüz kütüphanesi</h3>
            <p>
              Bu uygulama <b>PyQt5 / Qt</b> kullanır.
              PyQt5, Riverbank Computing tarafından GPL veya ticari lisans modeliyle sunulan bir üçüncü taraf kütüphanedir.
            </p>

            <h3>Kısa lisans notu</h3>
            <p>
              Projede yer alan uygulama kodu kök dizindeki <b>LICENSE</b> dosyasında belirtilen lisans metni ile paylaşılır.
              Kullanılan <b>PyQt5 / Qt</b> bileşenlerine ilişkin üçüncü taraf notları ise <b>THIRD_PARTY.md</b> dosyasında ayrıca belirtilmiştir.
              Projenin dağıtımı değerlendirilirken hem proje lisansı hem de kullanılan PyQt5 / Qt bileşenlerine ilişkin lisans koşulları birlikte dikkate alınmalıdır.
            </p>

            <h3>PyQt5 / Qt için resmi bağlantılar</h3>
            <ul>
              <li><b>PyQt lisans bilgisi:</b> <a href="https://riverbankcomputing.com/commercial/">https://riverbankcomputing.com/commercial/</a></li>
              <li><b>PyQt5 PyPI paketi:</b> <a href="https://pypi.org/project/PyQt5/">https://pypi.org/project/PyQt5/</a></li>
              <li><b>Qt lisanslama:</b> <a href="https://doc.qt.io/qt-5/licensing.html">https://doc.qt.io/qt-5/licensing.html</a></li>
              <li><b>Qt belgeleri:</b> <a href="https://doc.qt.io/qt-5/">https://doc.qt.io/qt-5/</a></li>
            </ul>

            <h3>Kaynak ve Lisans Bağlantıları</h3>
            <ul>
              <li><b>Github kod linki:</b> <a href="https://github.com/cezateknik/Czmtk">https://github.com/cezateknik/Czmtk</a></li>
              <li><b>LICENSE</b>: Proje lisans metni</li>
              <li><b>THIRD_PARTY.md</b>: Üçüncü taraf bileşen ve lisans notları</li>
            </ul>

            <h3>Not</h3>
            <p>
              Bu ekran bilgilendirme amaçlıdır. Gerekli durumlarda resmi lisans metinleri ve ilgili sağlayıcıların resmi sayfaları esas alınmalıdır.
            </p>
        """)
        layout.addWidget(text)

        button_row = QHBoxLayout()
        button_row.addStretch()
        close_button = QPushButton("Kapat")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        button_row.addWidget(close_button)
        button_row.addStretch()
        layout.addLayout(button_row)
