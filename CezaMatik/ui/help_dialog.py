from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yardım")
        self.setMinimumSize(600, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.setupUI()
        
    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Yardım ve Destek")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)
        
        # Help content
        help_text = """
<h3>Sık Sorulan Sorular</h3>

<p><b>S: İndirim veya artırım oranını nasıl girerim?</b></p>
<p>C: Standart oranlar için butonları kullanabilirsiniz (1/2, 2/3, 1/4, 1/6). 
Özel bir oran girmek istiyorsanız, "Örn: 1/3 veya %25" yazılı alana 
değeri yazabilirsiniz.</p>

<p><b>S: Dolandırıcılık hesaplama modülünü nasıl kullanabilirim?</b></p>
<p>C: Sağ paneldeki "Dolandırıcılık Suçu Hesaplama" modülüne dolandırıcılık 
miktarını TL cinsinden girin ve dönem seçimini yaparak "Hesapla" butonuna basın.</p>

<p><b>S: Hesaplanan dolandırıcılık cezasını ana hesaplamaya nasıl aktarırım?</b></p>
<p>C: Dolandırıcılık modülünde hesaplamayı yaptıktan sonra "Adli Para Cezasına Aktar" 
butonuna tıklayarak hesaplanan gün sayısını ana hesaplama alanına doğrudan aktarabilirsiniz.</p>

<h3>İletişim</h3>
<p>Daha fazla istek, öneri ve hesap hataları için:</p>
<p>Email: adliyeishak@gmail.com</p>

<p>Web: <a href="https://cezamatik.blogspot.com" target="_blank">
cezamatik.blogspot.com
</a></p>
"""

        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setTextFormat(Qt.RichText)
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setOpenExternalLinks(True)
        content_layout.addWidget(help_label)
        
        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Kapat")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
