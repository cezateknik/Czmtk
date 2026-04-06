from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class ManualDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanım Kılavuzu")
        self.setMinimumSize(700, 500)
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
        title_label = QLabel("Ceza Hesaplama Uygulaması - Kullanım Kılavuzu")
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)
        
        # Manual content
        sections = [
            ("1. Giriş", """
<p>Ceza Hesaplama Uygulaması, hâkim, savcı, avukat ve diğer hukukçuların ceza hesaplamalarını hızlı ve doğru şekilde yapabilmelerini sağlayan kapsamlı bir araçtır. 
Bu kılavuz, uygulamanın tüm özelliklerini ve kullanım adımlarını detaylı olarak açıklamaktadır.</p>
            """),
            
            ("2. Ana Özellikler", """
<ul>
<li>Hapis cezası hesaplama (yıl, ay, gün)</li>
<li>Adli para cezası hesaplama</li>
<li>Standart ve özel oranlarla indirim/artırım yapabilme</li>
<li>Dolandırıcılık suçları için özel hesaplama modülü</li>
<li>İşlem geçmişi takibi</li>
<li>Hesap makinesi</li>
</ul>
            """),
            
            ("3. Ana Hesaplama Modülü Kullanımı", """
<h4>3.1. Ceza Girişi</h4>
<ul>
<li>Hapis Cezası: Yıl, ay ve gün olarak giriş yapın</li>
<li>Adli Para Cezası: Gün sayısı olarak girin</li>
<li>Değerleri sıfırlamak için '↺' butonunu kullanın</li>
<li>Para cezası otomatik olarak 20 TL ve 100 TL bazında hesaplanır</li>
</ul>

<h4>3.2. Oran Seçimi</h4>
<ul>
<li>Standart oranlar: 1/2, 2/3, 1/4, 1/6</li>
<li>Özel oran girişi: "1/3" veya "%25" formatında</li>
<li>Her seferinde sadece bir oran seçilebilir</li>
</ul>

<h4>3.3. İndirim/Artırım İşlemleri</h4>
<ol>
<li>Ceza değerlerini girin</li>
<li>Oranı seçin</li>
<li>"İndirim" veya "Artırım" butonuna tıklayın</li>
<li>Sonuç otomatik hesaplanır ve bilgi paneline eklenir</li>
</ol>

<h4>3.4. Sonuç İşlemleri</h4>
<ul>
<li>Sonucu Kopyala: Hesaplanan cezayı panoya kopyalar</li>
<li>Geri Al: Son işlemi iptal eder</li>
<li>Sıfırla: Tüm hesaplamaları sıfırlar</li>
</ul>
            """),
            
            ("4. Dolandırıcılık Modülü", """
<h4>4.1. Hesaplama Yöntemi</h4>
<ul>
<li>01.06.2024 Öncesi: Tutar en yakın 10 TL'ye yuvarlanır ve 10'a bölünür</li>
<li>01.06.2024 Sonrası: Tutar en yakın 50 TL'ye yuvarlanır ve 50'ye bölünür</li>
<li>Minimum ceza 5 gündür</li>
</ul>

<h4>4.2. Kullanım Adımları</h4>
<ol>
<li>Dolandırıcılık suçuna konu olan tutarı TL cinsinden girin</li>
<li>Tarih seçimini yapın (01.06.2024 öncesi/sonrası)</li>
<li>"Hesapla" butonuna tıklayın</li>
<li>Sonucu kopyalayabilir veya ana hesaplamaya aktarabilirsiniz</li>
</ol>

<h4>4.3. Kullanım Alanı</h4>
<ol>
<li>TCK m.158/1 (e), (f), (j), (k) ve (l) bentlerinde kullanılabilir.</li>
</ol>                         
            """),
            
            ("5. Hesap Makinesi", """
<h4>5.1. Özellikler</h4>
<ul>
<li>Temel matematiksel işlemler</li>
<li>Parantez kullanımı</li>
<li>Ondalık sayı hesaplamaları</li>
<li>Klavye desteği</li>
</ul>

<h4>5.2. Klavye Kısayolları</h4>
<ul>
<li>0-9: Rakamlar</li>
<li>+ - * /: İşlemler</li>
<li>Enter: Hesapla</li>
<li>Backspace: Son karakteri sil</li>
<li>Esc: Temizle</li>
<li>. veya ,: Ondalık ayırıcı</li>
</ul>
            """),
            
            ("6. İpuçları ve Öneriler", """
<ol>
<li>Karmaşık hesaplamalarda adım adım ilerleyin</li>
<li>Her önemli aşamada sonucu kontrol edin</li>
<li>İşlem geçmişini düzenli takip edin</li>
<li>Şüphe durumunda hesaplamayı tekrarlayın</li>
<li>Özel oranları dikkatli girin ve kontrol edin</li>
</ol>
            """),
            
            ("7. Sık Karşılaşılan Sorunlar", """
<h4>7.1. Hesaplama Hataları</h4>
<ul>
<li>Girilen değerlerin doğruluğunu kontrol edin</li>
<li>Oranın doğru formatta olduğundan emin olun</li>
<li>Ondalık sayılarda nokta (.) kullanın</li>
</ul>

<h4>7.2. Sistem Sorunları</h4>
<ul>
<li>Yeniden kurulum deneyin.</li>
<li>Programın güncel sürümü var mı kontrol edin.</li>
</ul>
            """),
            
            ("8. Teknik Gereksinimler", """
<ul>
<li>Windows işletim sistemi</li>
</ul>
            """),
            
            ("9. Yasal Uyarı", """
<p>Bu uygulama sadece yardımcı bir araçtır. Tüm hesaplamaların son kontrolü kullanıcının 
sorumluluğundadır. Yasal süreçlerde bu uygulamanın sonuçlarını kullanmadan önce manuel 
doğrulama yapılması önerilir.</p>
            """)
        ]
        
        # Add sections with headers and content
        for title, content in sections:
            # Section header
            header = QLabel(title)
            header_font = QFont()
            header_font.setPointSize(12)  # Reduced from 14 to 12
            header_font.setBold(True)
            header.setFont(header_font)
            content_layout.addWidget(header)
            
            # Section content
            content_label = QLabel(content)
            content_label.setWordWrap(True)
            content_label.setTextFormat(Qt.RichText)
            content_label.setStyleSheet("margin-left: 20px; margin-bottom: 15px;")
            content_layout.addWidget(content_label)
        
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