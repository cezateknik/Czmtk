from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Uygulama Hakkında")
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
        title_label = QLabel("CezaMat'İK")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)
        
        # Application description
        description_text = """
<p>📄 <b>Uygulama Hakkında</b></p>

<p>CezaMat'ik, İshak KOCATEPE tarafından yapay zeka desteğiyle Python ve PyQt5 / Qt tabanlı olarak geliştirilmiş bir masaüstü uygulamasıdır. 
Bu yazılım, ceza süresi ve adli para cezası hesaplamalarında kullanıcıya yardımcı olmak amacıyla hazırlanmıştır. 
Uygulama; oranlı indirim ve artırımları, hukuki yuvarlama kurallarını, adli para cezası hesaplarını ve 
dolandırıcılık gibi özel ceza tiplerini kapsamlı şekilde ele alır. Ayrıca yerleşik bir hesap makinesi de içerir.</p>

<p>🔒 <b>Lisans ve Kullanım Koşulları:</b></p>
<ul>
<li>Bu yazılım tamamen ücretsizdir.</li>
<li>Herhangi bir şekilde ticari amaçla satılamaz, ücret karşılığı dağıtılamaz.</li>
<li>Eğitim, kişisel kullanım ve hukuk alanında yardımcı araç olarak kullanılmak üzere geliştirilmiştir.</li>
<li>Uygulamanın meslektaşlar dahilinde ticari olmayan biçimde paylaşılması serbesttir, ancak güvenlik nedeniyle resmi web sitesi dışında bir yere yüklemek ve dağıtmak yasaktır.(Virüs yerleştirme vb. riskler)</li>
</ul>
<p><b>Github kod linki:</b> https://github.com/cezateknik/Czmtk</p>

<p>⚠️ <b>Yasal Uyarı:</b> Bu uygulama, yalnızca destekleyici bir araç olarak kullanılmalıdır. 
Kesin ve bağlayıcı sonuçlar garanti edilmez. Uygulama manuel hesaplamayı doğrulamak amacıyla tasarlanmıştır. Asli hesaplayıcı olarak kullanılamaz. Kullanıcı çıkan hesaplamaların doğruluğunu mutlaka kontrol etmelidir. Hesaplama hatalarından doğacak tüm sorumluluk kullanıcıya aittir.</p>




"""
        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        description_label.setTextFormat(Qt.RichText)
        description_label.setAlignment(Qt.AlignLeft)
        description_label.setOpenExternalLinks(True)
        content_layout.addWidget(description_label)
        
        # Version info
        version_label = QLabel("Sürüm: 1.3.4")
        version_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(version_label)
   
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
