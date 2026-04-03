from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QGridLayout, QPushButton, QLabel, QSpinBox, 
                            QDoubleSpinBox, QComboBox, QLineEdit, QRadioButton, 
                            QButtonGroup, QTextEdit, QFrame, QSizePolicy,
                            QGroupBox, QApplication, QMenuBar, QMenu, QAction,
                            QDialog, QScrollArea, QTabWidget, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRegExp
from PyQt5.QtGui import QFont, QIcon, QPixmap, QKeySequence, QRegExpValidator, QIntValidator
import os
import requests
import webbrowser
import re
import sys
from requests.exceptions import ConnectTimeout, ConnectionError, Timeout, RequestException

from ui.calculator_widget import CalculatorWidget
from ui.fraud_module_widget import FraudModuleWidget
from ui.info_panel_widget import InfoPanelWidget
from ui.about_dialog import AboutDialog
from ui.help_dialog import HelpDialog
from ui.manual_dialog import ManualDialog
from ui.calculation_logic_dialog import CalculationLogicDialog
from ui.tools_dialog import OtherToolsDialog
from utils.calculator import PenaltyCalculator

# Güncelleme kontrolü için constants
CURRENT_VERSION = "1.3.3"
VERSION_URL = "https://cezamatik.blogspot.com/p/surum.html"
DOWNLOAD_PAGE = "https://cezamatik.blogspot.com/p/cezamatik-nasl-guncellenir.html"

class UpdateCheckThread(QThread):
    """Güncelleme kontrolü için ayrı thread"""
    updateAvailable = pyqtSignal(str)  # Yeni sürüm numarası
    noUpdateAvailable = pyqtSignal()
    errorOccurred = pyqtSignal(str)  # Hata mesajı
    
    def run(self):
        try:
            response = requests.get(VERSION_URL, timeout=15)
            if response.status_code == 200:
                # HTML içeriğinden sürüm numarasını çıkar
                html_content = response.text
                
                # Blogger sayfasının içeriğinden sürüm numarasını bul
                # <div class='post-body'> veya benzer yapıları ara
                version_pattern = r'(\d+\.\d+\.\d+)'
                matches = re.findall(version_pattern, html_content)
                
                if matches:
                    # En son bulunan sürüm numarasını al (genellikle içerik kısmında olan)
                    latest_version = matches[-1].strip()
                    
                    # Sürüm karşılaştırması
                    if self.compare_versions(latest_version, CURRENT_VERSION):
                        self.updateAvailable.emit(latest_version)
                    else:
                        self.noUpdateAvailable.emit()
                else:
                    self.errorOccurred.emit("⚠️ Sürüm bilgisi bulunamadı")
            else:
                self.errorOccurred.emit("⚠️ Sürüm bilgisi alınamadı")
        except (ConnectTimeout, Timeout) as e:
            # Zaman aşımı hataları için özel mesaj
            self.errorOccurred.emit("⏰ Zamanaşımına uğradı\n\nKurum ağı dışında mobil veya ev internetinde deneyiniz!")
        except ConnectionError as e:
            # Bağlantı hataları için özel mesaj
            if "timed out" in str(e).lower():
                self.errorOccurred.emit("⏰ Bağlantı zamanaşımına uğradı\n\nKurum ağı dışında mobil veya ev internetinde deneyiniz!")
            else:
                self.errorOccurred.emit("🌐 İnternet bağlantı hatası\n\nİnternet bağlantınızı kontrol ediniz!")
        except RequestException as e:
            # Diğer requests hataları
            if "timeout" in str(e).lower():
                self.errorOccurred.emit("⏰ İstek zamanaşımına uğradı\n\nKurum ağı dışında mobil veya ev internetinde deneyiniz!")
            else:
                self.errorOccurred.emit("🚫 Güncelleme kontrolü başarısız\n\nDaha sonra tekrar deneyiniz!")
        except Exception as e:
            # Genel hatalar için basit mesaj
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["timeout", "timed out", "connection"]):
                self.errorOccurred.emit("⏰ Bağlantı zamanaşımına uğradı\n\nKurum ağı dışında mobil veya ev internetinde deneyiniz!")
            else:
                self.errorOccurred.emit("🚫 Güncelleme kontrolü başarısız\n\nDaha sonra tekrar deneyiniz!")
    
    def compare_versions(self, version1, version2):
        """İki sürümü karşılaştır. version1 > version2 ise True döner"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Eksik kısımları 0 ile doldur
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            return v1_parts > v2_parts
        except:
            return False

class UpdateDialog(QDialog):
    """Güncelleme kontrolü dialog penceresi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Güncelleme Kontrolü")
        self.setMinimumSize(450, 280)  # Biraz daha yüksek yapıldı çok satırlı mesajlar için
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.update_thread = None
        self.latest_version = None
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Başlık
        title_label = QLabel("Güncelleme Kontrolü")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Mevcut sürüm bilgisi
        version_label = QLabel(f"Mevcut Sürüm: {CURRENT_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Durum etiketi
        self.status_label = QLabel("Güncelleme kontrolü için butona tıklayın")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(60)  # Çok satırlı mesajlar için yeterli alan
        layout.addWidget(self.status_label)
        
        # Yeni sürüm bilgisi (başlangıçta gizli)
        self.new_version_label = QLabel()
        self.new_version_label.setAlignment(Qt.AlignCenter)
        self.new_version_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        self.new_version_label.hide()
        layout.addWidget(self.new_version_label)
        
        # Buton layoutu
        button_layout = QHBoxLayout()
        
        # Güncelleme kontrol butonu
        self.check_button = QPushButton("Güncellemeleri Kontrol Et")
        self.check_button.setFixedHeight(35)
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.check_button.clicked.connect(self.check_for_updates)
        button_layout.addWidget(self.check_button)
        
        # Güncelle butonu (başlangıçta gizli)
        self.update_button = QPushButton("Güncelle")
        self.update_button.setFixedHeight(35)
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.update_button.clicked.connect(self.open_download_page)
        self.update_button.hide()
        button_layout.addWidget(self.update_button)
        
        # Kapat butonu
        close_button = QPushButton("Kapat")
        close_button.setFixedHeight(35)
        close_button.setFixedWidth(80)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
    def check_for_updates(self):
        """Güncelleme kontrolünü başlat"""
        self.check_button.setEnabled(False)
        self.update_button.hide()
        self.new_version_label.hide()
        self.status_label.setText("🔍 Güncelleme kontrol ediliyor...")
        
        # Thread oluştur ve başlat
        self.update_thread = UpdateCheckThread()
        self.update_thread.updateAvailable.connect(self.on_update_available)
        self.update_thread.noUpdateAvailable.connect(self.on_no_update)
        self.update_thread.errorOccurred.connect(self.on_error)
        self.update_thread.finished.connect(self.on_check_finished)
        self.update_thread.start()
        
    def on_update_available(self, latest_version):
        """Güncelleme mevcut olduğunda"""
        self.latest_version = latest_version
        self.status_label.setText("🔔 Yeni sürüm mevcut!")
        self.new_version_label.setText(f"Yeni Sürüm: {latest_version}")
        self.new_version_label.show()
        self.update_button.show()
        
    def on_no_update(self):
        """Güncelleme yoksa"""
        self.status_label.setText("✅ Uygulamanız güncel.")
        self.update_button.hide()
        self.new_version_label.hide()
        
    def on_error(self, error_message):
        """Hata durumunda"""
        self.status_label.setText(error_message)
        self.update_button.hide()
        self.new_version_label.hide()
        
    def on_check_finished(self):
        """Kontrol tamamlandığında"""
        self.check_button.setEnabled(True)
        
    def open_download_page(self):
        """Güncelleme sayfasını aç"""
        try:
            webbrowser.open(DOWNLOAD_PAGE)
            self.accept()  # Dialog'u kapat
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Güncelleme sayfası açılamadı: {str(e)}")

class UpdateHistoryDialog(QDialog):
    """Güncelleme geçmişi dialog penceresi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Güncelleme Geçmişi")
        self.setMinimumSize(600, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Başlık
        title_label = QLabel("Güncelleme Geçmişi")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Güncelleme geçmişi metni
        history_text = QTextEdit()
        history_text.setReadOnly(True)
        history_text.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        
        # Taslak güncelleme geçmişi metni
        history_content = """
<h3 style="color: #4b6eaf; margin-bottom: 10px;">📋 CezaMat'ik Güncelleme Geçmişi</h3>

<div style="margin-bottom: 20px;">
<h4 style="color: #2196F3; margin-bottom: 5px;">🔹 Sürüm 1.0.0 - 25 Mayıs 2025</h4>
<ul style="margin-left: 20px; margin-bottom: 10px;">
<li>İlk Beta sürümdür.</li>
<li>Kullanıcı testleri ve hesaplama hataları tespiti için geliştirilen sürümdür.</li>
</ul>
</div>

<div style="margin-bottom: 20px;">
<h4 style="color: #2196F3; margin-bottom: 5px;">🔹 Sürüm 1.3.0 - 1 Haziran 2025</h4>
<ul style="margin-left: 20px; margin-bottom: 10px;">
<li>Yeni hesaplama motoru entegrasyonu</li>
<li>Dolandırıcılık Modülü ondalık ve bindelik sisteme göre güncellendi.</li>
<li>Tam sayı artırımları ile ilgili hata giderildi. (Örn: 1 kat, 2 kat artırımlar)</li>
<li> 30-40 ay gibi yüksek ay hesaplama hataları giderildi. </li>
</ul>
</div>

<div style="margin-bottom: 20px;">
<h4 style="color: #2196F3; margin-bottom: 5px;">🔹 Sürüm 1.3.1 - 8 Haziran 2025</h4>
<ul style="margin-left: 20px; margin-bottom: 10px;">
<li>Yardım ve Güncellemeler sekmeleri eklendi.</li>
<li>Güncellemeler sekmesi ile uygulamanın güncelliğini anlık manuel kontrol edilebilmesi sağlandı.</li>
</ul>
</div>

<div style="margin-bottom: 20px;">
<h4 style="color: #2196F3; margin-bottom: 5px;">🔹 Sürüm 1.3.2 - 9 Haziran 2025</h4>
<ul style="margin-left: 20px; margin-bottom: 10px;">
<li>Sadece adli para cezası hesaplaması yapıldığında "Güncel Ceza" gösterimi düzenlendi.</li>
<li>Kurum internetinin yavaşlığı nedeniyle güncelleme kontrolü zamanaşımı 30 saniye olarak güncellendi.</li>
<li>Güncelleme geçmişi sekmesi eklendi</li>
</ul>
</div>

<div style="margin-bottom: 20px;">
<h4 style="color: #2196F3; margin-bottom: 5px;">🔹 Sürüm 1.3.3 - 4 Ocak 2026</h4>
<ul style="margin-left: 20px; margin-bottom: 10px;">
<li>Ceza Giriş Alanı'ndaki veri girişi QSpinBox'lar, QLineEdit'e dönüştürüldü.</li>
<li>QLineEdit dönüşümü ile artık girilen ceza miktarı silindiğinde hala eski ceza miktarının gözükmesi hatası giderildi.</li>
<li>Bu dönüşüm sayesinde "sıfırla" butonuna basmadan girilen ceza miktarı tamamen silinebilir hale geldi.</li>
</ul>
</div>

<hr style="margin: 20px 0; border: 1px solid #ddd;">

<p style="color: #666; font-size: 10px; text-align: center;">
<i>Bu güncelleme geçmişi sürekli olarak güncellenmektedir. Her yeni sürümde yapılan değişiklikler burada listelenecektir.</i>
</p>
"""
        
        history_text.setHtml(history_content)
        layout.addWidget(history_text)
        
        # Kapat butonu
        button_layout = QHBoxLayout()
        close_button = QPushButton("Kapat")
        close_button.setFixedHeight(35)
        close_button.setFixedWidth(100)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #aaa;
            }
        """)
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window icon kısmı buradaydı
        # Logo yükleme - exe ve development ikisinde çalışan
        if getattr(sys, 'frozen', False):
            # Exe olarak çalışıyorsa
            base_path = sys._MEIPASS
        else:
            # Normal Python çalıştırılıyorsa
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        icon_path = os.path.join(base_path, "assets", "logo.png")
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        
        self.setWindowTitle("Ceza Hesaplama Uygulaması - CezaMat'ik")
        self.setMinimumSize(900, 710)
        self.resize(900, 750)  # Set initial size larger than minimum to show more of the bottom section
        
        self.calculator = PenaltyCalculator()
        self.history = []
        
        # Store initial input values - Initialize with zeros instead of None
        self.initial_yil = 0
        self.initial_ay = 0
        self.initial_gun = 0
        self.initial_para = 0  # Initialize to 0 instead of None
        self.has_initial_values = False
        
        # Track selected ratio button
        self.selected_ratio = "1/2"
        
        self.setupMenuBar()
        self.setupUI()
        self.connectSignals()
        
    def setupMenuBar(self):
        # Create menu bar
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        # Create "Seçenekler" menu
        optionsMenu = QMenu("Seçenekler", self)
        self.menuBar.addMenu(optionsMenu)
        
        # Create "Güncellemeler" menu
        updatesMenu = QMenu("Güncellemeler", self)
        self.menuBar.addMenu(updatesMenu)
        
        # Create "Yardım" menu  
        helpMenu = QMenu("Yardım", self)
        self.menuBar.addMenu(helpMenu)
        
        # Create actions for "Seçenekler" menu
        self.aboutAction = QAction("Uygulama Hakkında", self)
        self.aboutAction.setShortcut(QKeySequence("F1"))
        
        self.manualAction = QAction("Kullanım Kılavuzu", self)
        self.manualAction.setShortcut(QKeySequence("F2"))
        
        self.calculationLogicAction = QAction("Hesaplama Mantığı", self)
        self.calculationLogicAction.setShortcut(QKeySequence("F4"))
        
        # Create actions for "Güncellemeler" menu
        self.updateCheckAction = QAction("Güncelleme Kontrolü", self)
        self.updateCheckAction.setShortcut(QKeySequence("F5"))
        
        self.updateHistoryAction = QAction("Güncelleme Geçmişi", self)
        self.updateHistoryAction.setShortcut(QKeySequence("F6"))
        
        # Create actions for "Yardım" menu
        self.helpAction = QAction("Yardım", self)
        self.helpAction.setShortcut(QKeySequence("F3"))
        
        # Add actions to "Seçenekler" menu
        optionsMenu.addAction(self.aboutAction)
        optionsMenu.addAction(self.manualAction)
        optionsMenu.addSeparator()
        optionsMenu.addAction(self.calculationLogicAction)
        
        # Add actions to "Güncellemeler" menu
        updatesMenu.addAction(self.updateCheckAction)
        updatesMenu.addAction(self.updateHistoryAction)
        
        # Add actions to "Yardım" menu
        helpMenu.addAction(self.helpAction)
        
        # Connect actions to slots
        self.aboutAction.triggered.connect(self.showAboutDialog)
        self.manualAction.triggered.connect(self.showManualDialog)
        self.calculationLogicAction.triggered.connect(self.showCalculationLogicDialog)
        self.updateCheckAction.triggered.connect(self.showUpdateDialog)
        self.updateHistoryAction.triggered.connect(self.showUpdateHistoryDialog)
        self.helpAction.triggered.connect(self.showHelpDialog)
    
    def showAboutDialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def showManualDialog(self):
        dialog = ManualDialog(self)
        dialog.exec_()
    
    def showHelpDialog(self):
        dialog = HelpDialog(self)
        dialog.exec_()
        
    def showCalculationLogicDialog(self):
        dialog = CalculationLogicDialog(self)
        dialog.exec_()
        
    def showUpdateDialog(self):
        """Güncelleme kontrolü dialog'unu göster"""
        dialog = UpdateDialog(self)
        dialog.exec_()
        
    def showUpdateHistoryDialog(self):
        """Güncelleme geçmişi dialog'unu göster"""
        dialog = UpdateHistoryDialog(self)
        dialog.exec_()

    def showOtherToolsDialog(self):
        dialog = OtherToolsDialog(self)
        dialog.exec_()
        
    def setupUI(self):
        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for the main layout
        
        # Content container
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel (Ceza calculation)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Input Area
        input_group = QGroupBox("Ceza Giriş Alanı")
        input_layout = QVBoxLayout(input_group)
        
        # Hapis Cezası
        hapis_layout = QHBoxLayout()
        hapis_label = QLabel("Hapis Cezası:")
        hapis_label.setStyleSheet("font-weight: bold;")
        hapis_layout.addWidget(hapis_label)
        
        yil_label = QLabel("Yıl:")
        # QLineEdit kullanarak SpinBox'ları değiştir
        self.yil_input = QLineEdit()
        self.yil_input.setPlaceholderText("0")
        self.yil_input.setFixedWidth(80)
        self.yil_input.setAlignment(Qt.AlignCenter)
        # Sadece 0-100 arası sayılara izin ver
        yil_validator = QIntValidator(0, 100)
        self.yil_input.setValidator(yil_validator)
        self.yil_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4b6eaf;
            }
        """)
        hapis_layout.addWidget(yil_label)
        hapis_layout.addWidget(self.yil_input)
        
        ay_label = QLabel("Ay:")
        self.ay_input = QLineEdit()
        self.ay_input.setPlaceholderText("0")
        self.ay_input.setFixedWidth(80)
        self.ay_input.setAlignment(Qt.AlignCenter)
        # Sadece 0-100 arası sayılara izin ver
        ay_validator = QIntValidator(0, 100)
        self.ay_input.setValidator(ay_validator)
        self.ay_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4b6eaf;
            }
        """)
        hapis_layout.addWidget(ay_label)
        hapis_layout.addWidget(self.ay_input)
        
        gun_label = QLabel("Gün:")
        self.gun_input = QLineEdit()
        self.gun_input.setPlaceholderText("0")
        self.gun_input.setFixedWidth(80)
        self.gun_input.setAlignment(Qt.AlignCenter)
        # Sadece 0-100 arası sayılara izin ver
        gun_validator = QIntValidator(0, 100)
        self.gun_input.setValidator(gun_validator)
        self.gun_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4b6eaf;
            }
        """)
        hapis_layout.addWidget(gun_label)
        hapis_layout.addWidget(self.gun_input)
        
        # Reset button with a proper icon
        self.reset_btn = QPushButton()
        self.reset_btn.setToolTip("Değerleri Sıfırla")
        self.reset_btn.setFixedSize(30, 30)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #c8c8c8;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # Set a reset icon using text characters that resemble a reset icon
        self.reset_btn.setText("↺")
        self.reset_btn.setFont(QFont("Arial", 14))
        
        hapis_layout.addWidget(self.reset_btn)
        
        hapis_layout.addStretch()
        input_layout.addLayout(hapis_layout)
        
        # Adli Para Cezası
        para_cezasi_layout = QHBoxLayout()
        para_label = QLabel("Adli Para Cezası:")
        para_label.setStyleSheet("font-weight: bold;")
        para_cezasi_layout.addWidget(para_label)
        
        self.para_input = QLineEdit()
        self.para_input.setPlaceholderText("0")
        self.para_input.setFixedWidth(80)
        self.para_input.setAlignment(Qt.AlignCenter)
        # Sadece 0-1000000 arası sayılara izin ver
        para_validator = QIntValidator(0, 1000000)
        self.para_input.setValidator(para_validator)
        self.para_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4b6eaf;
            }
        """)
        para_cezasi_layout.addWidget(self.para_input)
        
        gun_text = QLabel("Gün")
        para_cezasi_layout.addWidget(gun_text)
        para_cezasi_layout.addStretch()
        input_layout.addLayout(para_cezasi_layout)
        
        # Para cezası bilgilendirme 
        self.tl_info_label = QLabel("20 TL'den = 0 TL | 100 TL'den = 0 TL")
        input_layout.addWidget(self.tl_info_label)
        
        left_layout.addWidget(input_group)
        
        # Operation Area
        operation_group = QGroupBox("İşlem Alanı")
        operation_layout = QVBoxLayout(operation_group)
        operation_layout.setSpacing(10)  # Reduced spacing between elements
        operation_group.setMinimumHeight(200)  # Set minimum height for the operation area
        
        # Oran section with buttons in one row - CENTERED
        oran_container = QHBoxLayout()
        oran_container.setAlignment(Qt.AlignCenter)  # Center the entire container
        
        oran_buttons_layout = QHBoxLayout()
        oran_buttons_layout.setSpacing(5)  # Reduced spacing between buttons
        
        oran_label = QLabel("Oran:")
        oran_label.setStyleSheet("font-weight: bold;")
        oran_buttons_layout.addWidget(oran_label)
        
        # Updated larger button styling
        button_style_template = """
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 55px;
                max-width: 55px;
                height: 30px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
                border: 1px solid #aaa;
            }}
        """
        
        active_style = button_style_template.format(bg_color="#4b6eaf", text_color="white")
        inactive_style = button_style_template.format(bg_color="#f5f5f5", text_color="black")
        
        # Create ratio buttons
        self.ratio_buttons = {}
        self.ratio_button_group = QButtonGroup(self)
        self.ratio_button_group.setExclusive(True)
        
        ratio_values = ["1/2", "2/3", "1/4", "1/3", "1/6"]
        
        for ratio in ratio_values:
            btn = QPushButton(ratio)
            btn.setCheckable(True)
            btn.setProperty("ratio", ratio)
            if ratio == "1/2":  # Default selected
                btn.setChecked(True)
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(inactive_style)
            
            self.ratio_buttons[ratio] = btn
            self.ratio_button_group.addButton(btn)
            oran_buttons_layout.addWidget(btn)
        
        oran_container.addLayout(oran_buttons_layout)
        operation_layout.addLayout(oran_container)
        
        # "veya" label and custom ratio input in a more compact layout
        veya_layout = QHBoxLayout()
        veya_layout.setSpacing(5)  # Reduced spacing
        veya_label = QLabel("veya")
        veya_label.setAlignment(Qt.AlignCenter)
        veya_layout.addStretch(1)
        veya_layout.addWidget(veya_label)
        veya_layout.addStretch(1)
        operation_layout.addLayout(veya_layout)
        
        # Custom ratio input with reduced spacing
        ozel_oran_layout = QHBoxLayout()
        ozel_oran_layout.setSpacing(5)  # Reduced spacing
        self.ozel_oran_input = QLineEdit()
        self.ozel_oran_input.setPlaceholderText("Örn: 1/3 veya %25")
        self.ozel_oran_input.setFixedWidth(160)
        ozel_oran_layout.addStretch(1)
        ozel_oran_layout.addWidget(self.ozel_oran_input)
        ozel_oran_layout.addStretch(1)
        operation_layout.addLayout(ozel_oran_layout)
        
        # Reduced spacing before buttons
        operation_layout.addSpacing(10)  # Reduced from 20
        
        # Buttons for indirim/artırım
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)  # Add spacing between buttons
        
        self.indirim_btn = QPushButton("İndirim")
        self.indirim_btn.setFixedHeight(35)  # Reduce button height
        self.indirim_btn.setFixedWidth(120)  # Set fixed width
        self.indirim_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons_layout.addWidget(self.indirim_btn)
        
        self.artirim_btn = QPushButton("Artırım")
        self.artirim_btn.setFixedHeight(35)  # Reduce button height
        self.artirim_btn.setFixedWidth(120)  # Set fixed width
        self.artirim_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        buttons_layout.addWidget(self.artirim_btn)
        
        buttons_layout.setAlignment(Qt.AlignCenter)  # Center the buttons
        operation_layout.addLayout(buttons_layout)
        
        # Add stretch to push buttons up
        operation_layout.addStretch()
        
        left_layout.addWidget(operation_group)
        
        # Info Panel
        info_group = QGroupBox("Bilgi Paneli")
        info_layout = QVBoxLayout(info_group)
        
        self.girilen_ceza_label = QLabel("Girilen Ceza: ")
        self.girilen_ceza_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self.girilen_ceza_label)
        
        # History display
        self.info_panel = InfoPanelWidget()
        info_layout.addWidget(self.info_panel)
        
        # Buttons
        info_buttons_layout = QHBoxLayout()
        
        self.geri_al_btn = QPushButton("Geri Al")
        info_buttons_layout.addWidget(self.geri_al_btn)
        
        self.sonuc_kopyala_btn = QPushButton("Sonucu Kopyala")
        info_buttons_layout.addWidget(self.sonuc_kopyala_btn)
        
        self.sifirla_btn = QPushButton("Sıfırla")
        info_buttons_layout.addWidget(self.sifirla_btn)
        
        info_layout.addLayout(info_buttons_layout)
        left_layout.addWidget(info_group)
        
        # Right panel (Fraud module and calculator)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        # Fraud module
        self.fraud_module = FraudModuleWidget()
        right_layout.addWidget(self.fraud_module, 0, Qt.AlignTop)

        self.other_tools_btn = QPushButton("Diğer Hesaplama Araçları")
        self.other_tools_btn.setCursor(Qt.PointingHandCursor)
        self.other_tools_btn.setFixedHeight(38)
        self.other_tools_btn.setMinimumWidth(220)
        self.other_tools_btn.setStyleSheet("""
            QPushButton {
                background-color: #f4f6f9;
                color: #2f3a4a;
                border: 1px solid #cfd6e0;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #ebeff5;
                border: 1px solid #b8c2cf;
            }
            QPushButton:pressed {
                background-color: #e1e6ee;
            }
        """)
        right_layout.addStretch()
        right_layout.addWidget(self.other_tools_btn, 0, Qt.AlignHCenter)
        right_layout.addStretch()
        
        # Calculator
        self.calculator_widget = CalculatorWidget()
        right_layout.addWidget(self.calculator_widget, 0, Qt.AlignBottom)
        
        # Set the proportions for content
        content_layout.addWidget(left_panel, 3)
        content_layout.addWidget(right_panel, 2)
        
        # Add content to main layout
        main_layout.addWidget(content_widget)
        
        # Footer
        footer = QWidget()
        footer.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-top: 1px solid #e0e0e0;
                padding: 8px;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 5, 10, 5)
        
        copyright_label = QLabel("© 2025 İ.K | Haziran 2025")
        copyright_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
            }
        """)
        copyright_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(copyright_label)
        
        # Add footer to main layout
        main_layout.addWidget(footer)
        
        self.setCentralWidget(central_widget)
        
    def connectSignals(self):
        # Connect input change signals - QLineEdit için textChanged kullan
        self.yil_input.textChanged.connect(self.updateGirilenCeza)
        self.ay_input.textChanged.connect(self.updateGirilenCeza)
        self.gun_input.textChanged.connect(self.updateGirilenCeza)
        self.para_input.textChanged.connect(self.updateParaCezasi)
        
        # Connect button signals
        self.reset_btn.clicked.connect(self.resetInputs)
        self.indirim_btn.clicked.connect(lambda: self.applyOperation("indirim"))
        self.artirim_btn.clicked.connect(lambda: self.applyOperation("artirim"))
        self.geri_al_btn.clicked.connect(self.undoLastOperation)
        self.sonuc_kopyala_btn.clicked.connect(self.copyResult)
        self.sifirla_btn.clicked.connect(self.resetAll)
        self.other_tools_btn.clicked.connect(self.showOtherToolsDialog)
        
        # Connect ratio button signals
        self.ratio_button_group.buttonClicked.connect(self.onRatioButtonClicked)
        
        # Connect custom ratio input to clear button selection
        self.ozel_oran_input.textChanged.connect(self.onCustomRatioChanged)
        
        # Connect fraud module signals
        self.fraud_module.resultCalculated.connect(self.onFraudResultCalculated)
    
    def onRatioButtonClicked(self, button):
        # Update button styles
        active_style = """
            QPushButton {
                background-color: #4b6eaf;
                color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 55px;
                max-width: 55px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #3a5d9e;
                border: 1px solid #aaa;
            }
        """
        
        inactive_style = """
            QPushButton {
                background-color: #f5f5f5;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                min-width: 55px;
                max-width: 55px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #aaa;
            }
        """
        
        # Clear custom ratio input when a button is selected
        self.ozel_oran_input.clear()
        
        # Update selected ratio
        self.selected_ratio = button.property("ratio")
        
        # Update button styles
        for ratio, btn in self.ratio_buttons.items():
            if btn == button:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(inactive_style)
    
    def onCustomRatioChanged(self, text):
        # If custom ratio is entered, uncheck all ratio buttons
        if text:
            self.ratio_button_group.setExclusive(False)
            for btn in self.ratio_buttons.values():
                btn.setChecked(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f5f5f5;
                        color: black;
                        border: 1px solid #ccc;
                        border-radius: 6px;
                        padding: 6px 10px;
                        font-size: 14px;
                        min-width: 55px;
                        max-width: 55px;
                        height: 30px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                        border: 1px solid #aaa;
                    }
                """)
            self.ratio_button_group.setExclusive(True)
    
    def getInputValue(self, input_widget):
        """QLineEdit'ten güvenli değer al"""
        text = input_widget.text().strip()
        if text == "":
            return 0
        try:
            return int(text)
        except ValueError:
            return 0
        
    def updateGirilenCeza(self):
        if not self.has_initial_values:
            self.initial_yil = self.getInputValue(self.yil_input)
            self.initial_ay = self.getInputValue(self.ay_input)
            self.initial_gun = self.getInputValue(self.gun_input)
            
            text_parts = []
            if self.initial_yil > 0:
                text_parts.append(f"{self.initial_yil} Yıl")
            if self.initial_ay > 0:
                text_parts.append(f"{self.initial_ay} Ay")
            if self.initial_gun > 0:
                text_parts.append(f"{self.initial_gun} Gün")
            
            # Only add judicial fine if it's greater than 0
            if hasattr(self, 'initial_para') and self.initial_para and self.initial_para > 0:
                formatted_initial_para = f"{self.initial_para:,}".replace(",", ".")
                text_parts.append(f"ve {formatted_initial_para} Gün Adli Para Cezası")
                
            if not text_parts:
                text_parts.append("")
                
            self.girilen_ceza_label.setText(f"Girilen Ceza: {' '.join(text_parts)}")
            
            if not self.history:
                self.info_panel.setInitialPenalty(
                    self.initial_yil,
                    self.initial_ay,
                    self.initial_gun,
                    self.initial_para if hasattr(self, 'initial_para') and self.initial_para and self.initial_para > 0 else 0
                )
        
    def updateParaCezasi(self):
        para_value = self.getInputValue(self.para_input)
        tl_20 = para_value * 20
        tl_100 = para_value * 100
        
        # Format monetary values with dot as thousands separator
        formatted_tl_20 = f"{tl_20:,}".replace(",", ".")
        formatted_tl_100 = f"{tl_100:,}".replace(",", ".")
        
        self.tl_info_label.setText(f"20 TL'den = {formatted_tl_20} TL | 100 TL'den = {formatted_tl_100} TL")
        
        if not self.has_initial_values:
            self.initial_para = para_value
            self.updateGirilenCeza()
            
            if not self.history:
                self.info_panel.setInitialPenalty(
                    self.initial_yil,
                    self.initial_ay,
                    self.initial_gun,
                    para_value if para_value > 0 else 0
                )
        
    def resetInputs(self):
        self.yil_input.clear()
        self.ay_input.clear()
        self.gun_input.clear()
        self.para_input.clear()
        
    def getOranValue(self):
        if self.ozel_oran_input.text().strip():
            # Parse the custom ratio
            custom_ratio = self.ozel_oran_input.text().strip()
            
            if '/' in custom_ratio:
                try:
                    num, denom = custom_ratio.split('/')
                    return float(num) / float(denom)
                except (ValueError, ZeroDivisionError):
                    return 0.5  # Default to 1/2 if invalid
            elif '%' in custom_ratio:
                try:
                    percent = float(custom_ratio.replace('%', '').strip())
                    return percent / 100
                except ValueError:
                    return 0.5  # Default to 1/2 if invalid
            else:
                try:
                    return float(custom_ratio)
                except ValueError:
                    return 0.5  # Default to 1/2 if invalid
        else:
            # Use the selected ratio button
            if self.selected_ratio == "1/2":
                return 0.5
            elif self.selected_ratio == "2/3":
                return 2/3
            elif self.selected_ratio == "1/4":
                return 0.25
            elif self.selected_ratio == "1/3":
                return 1/3
            elif self.selected_ratio == "1/6":
                return 1/6
            else:
                return 0.5  # Default
    
    def applyOperation(self, operation_type):
        self.has_initial_values = True
        
        yil = self.getInputValue(self.yil_input)
        ay = self.getInputValue(self.ay_input)
        gun = self.getInputValue(self.gun_input)
        para_cezasi = self.getInputValue(self.para_input)
        oran = self.getOranValue()
        
        # Get current values or last result
        if self.history:
            last_result = self.history[-1]
            current_yil = last_result["result_years"]
            current_ay = last_result["result_months"]
            current_gun = last_result["result_days"]
            current_para = last_result["result_fine"]
        else:
            current_yil = yil
            current_ay = ay
            current_gun = gun
            current_para = para_cezasi if para_cezasi > 0 else 0  # Para cezası 0 ise hesaplamaya dahil etme
        
        # Calculate new values
        if operation_type == "indirim":
            operation_text = "indirim"
            is_reduction = True
        else:
            operation_text = "artırım"
            is_reduction = False
            
        # Use the calculator to compute the result
        result = self.calculator.calculate_penalty(
            current_yil, current_ay, current_gun, current_para,
            oran, is_reduction
        )
        
        # Add to history
        history_item = {
            "operation": operation_text,
            "ratio": oran,
            "ratio_text": self.selected_ratio if not self.ozel_oran_input.text() else self.ozel_oran_input.text(),
            "result_years": result["years"],
            "result_months": result["months"],
            "result_days": result["days"],
            "result_fine": result["fine"] if result["fine"] > 0 else 0  # Para cezası 0 ise kaydetme
        }
        
        self.history.append(history_item)
        self.info_panel.addHistoryItem(history_item, len(self.history))
        
        # Update input fields with the latest result
        self.yil_input.setText(str(int(result["years"])) if result["years"] > 0 else "")
        self.ay_input.setText(str(int(result["months"])) if result["months"] > 0 else "")
        self.gun_input.setText(str(int(result["days"])) if result["days"] > 0 else "")
        self.para_input.setText(str(int(result["fine"])) if result["fine"] > 0 else "")
        
    def undoLastOperation(self):
        if self.history:
            self.history.pop()
            self.info_panel.removeLastItem()
            
            # Update input fields with the previous result or reset to zero
            if self.history:
                last_result = self.history[-1]
                self.yil_input.setText(str(int(last_result["result_years"])) if last_result["result_years"] > 0 else "")
                self.ay_input.setText(str(int(last_result["result_months"])) if last_result["result_months"] > 0 else "")
                self.gun_input.setText(str(int(last_result["result_days"])) if last_result["result_days"] > 0 else "")
                self.para_input.setText(str(int(last_result["result_fine"])) if last_result["result_fine"] > 0 else "")
            else:
                self.has_initial_values = False
                self.resetInputs()
                
                # Reset initial values
                self.initial_yil = 0
                self.initial_ay = 0
                self.initial_gun = 0
                self.initial_para = 0
                self.updateGirilenCeza()
    
    def copyResult(self):
        if self.history:
            last_result = self.history[-1]
            
            years = last_result["result_years"]
            months = last_result["result_months"]
            days = last_result["result_days"]
            fine = last_result["result_fine"]
            
            # Format the result text
            text_parts = []
            if years > 0:
                text_parts.append(f"{int(years)} yıl")
            if months > 0:
                text_parts.append(f"{int(months)} ay")
            if days > 0:
                text_parts.append(f"{int(days)} gün")
                
            # Check if only judicial fine exists (no imprisonment)
            has_imprisonment = years > 0 or months > 0 or days > 0
            
            if fine > 0:
                formatted_fine = f"{int(fine):,}".replace(",", ".")
                if has_imprisonment:
                    # Both imprisonment and fine exist
                    penalty_text = " ".join(text_parts) if text_parts else "0 gün"
                    result_text = penalty_text + f" hapis ve {formatted_fine} gün adli para cezası"
                else:
                    # Only judicial fine exists
                    result_text = f"{formatted_fine} gün adli para cezası"
            else:
                # Only imprisonment exists
                penalty_text = " ".join(text_parts) if text_parts else "0 gün"
                result_text = penalty_text + " hapis cezası"
            
            # Copy to clipboard
            QApplication.clipboard().setText(result_text)
    
    def resetAll(self):
        self.has_initial_values = False
        self.initial_yil = 0
        self.initial_ay = 0
        self.initial_gun = 0
        self.initial_para = 0
        
        self.yil_input.clear()
        self.ay_input.clear()
        self.gun_input.clear()
        self.para_input.clear()
        
        self.history.clear()
        self.info_panel.clearHistory()
        self.updateGirilenCeza()
    
    def onFraudResultCalculated(self, days):
        if not self.has_initial_values:
            self.initial_para = days
            self.updateGirilenCeza()
        self.para_input.setText(str(days) if days > 0 else "")
