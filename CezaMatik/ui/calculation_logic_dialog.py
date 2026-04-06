from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget
from PyQt5.QtCore import Qt

class CalculationLogicDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hesaplama Mantığı")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Add explanation text
        explanation = """
<h2>CezaMat'ik Hesaplama Mantığı</h2>

<h3>1. Temel Hesaplama Prensipleri</h3>
<p>Uygulama, ceza hesaplamalarını aşağıdaki temel prensiplere göre yapar:</p>
<ul>
    <li>1 yıl = 365 gün (12 ay × 30 gün)</li>
    <li>1 ay = 30 gün</li>
</ul>
<p>1 yıl 365 gündür. Ancak yıldan gelen 12 aylık sonuç tekrar yıla çevrildiği için hesaplama mantığında 360 gün kabul edilir. (12 ay = 360 gün)</p>

<h3>2. Hesaplama Adımları</h3>
<p>Ceza hesaplaması şu adımları takip eder:</p>
<ol>
    <li>Girilen ceza süresi (yıl, ay, gün) toplam gün sayısına çevrilir</li>
    <li>Yıl hesabı ayrı, ay ve gün hesabı birlikte olmaz üzere ayrı hesaplanır.</li>
    <li>Seçilen oran bu toplam güne uygulanır</li>
    <li>Ay ve günden gelen sonuç tekrar ay ve gün olarak düzenlenir(Ay yıla çevrilmez.)</li>
    <li>Yıldan gelen sonuç yıl, ay ve gün olarak düzenlenir</li>
</ol>

<h3>3. İndirim ve Artırım İşlemleri</h3>
<p><b>İndirim işlemi için:</b></p>
<ul>
    <li>Hesaplanan miktar ana cezadan çıkarılır ve nihai sonuç bulunur.</li>

    <li>Adli para cezasında minimum değer 1 gündür</li>
</ul>

<p><b>Artırım işlemi için:</b></p>
<ul>
    <li>Hesaplanan miktar ana cezaya eklenir ve nihai sonuç bulunur.</li>

    <li>Ay ve gün değerleri gerektiğinde üst birime aktarılır (30 gün = 1 ay)</li>
</ul>

<h3>4. Yuvarlama İşlemi ve Özel Durumlar</h3>
<ul>
  <li>Küsuratlı günler, tüm sonuçlar toplandıktan sonra artırımlar ve indirimler uygulanarak tek seferde yuvarlanır.</li>
  <li>Örneğin; 2,3 gün ve 3,7 gün ayrı ayrı 3 ve 4 olarak yuvarlanmaz. Bunun yerine önce toplanır: 2,3 + 3,7 = 6,0 ve sonuç doğrudan 6 gün olarak esas alınır.</li>
  <li>Benzer şekilde, 2,3 + 3,8 = 6,1 olduğunda sonuç 7 gün olarak yuvarlanır. Böylece iki kez lehe işlem yapılması önlenmiş olur.<em> (Hukuki yoruma göre sonuç değişebilir.)</em></li>
  <li>Para cezasına ilişkin hesaplamalar, hapis cezasından bağımsız olarak yapılır.</li>
    <li>Oranlar kesir (örn: 1/2) veya yüzde (örn: %25) olarak girilebilir</li>
</ul>


<h3>5. Dolandırıcılık Adli Para Cezası Hesaplama</h3>
<p>Adli para cezası günlük miktarı iki farklı değer üzerinden hesaplanır:</p>
<ul>
    <li>20 TL üzerinden hesaplama</li>
    <li>100 TL üzerinden hesaplama</li>
    <li>20 TL üzerinden hesaplama durumunda "0" atma yöntemi uygulanır.</li>
    <li>100 TL üzerinden hesaplama durumunda "50" sayısına bölme yöntemi uygulanır.</li>
    <li>Miktarlar bölünmeden 10 veya 50 sayısına bölünecek şekilde yukarıya yuvarlanır. </li>
    <li>Menfaatin iki katından az olamayacağından küsuratlar yukarı yuvarlanır.</li>
        <li> 20 ve 100 TL dışındaki miktarda hesaplama manuel yapılmalıdır. Program desteklemez. </li>
</ul>
"""
        
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setTextFormat(Qt.RichText)
        content_layout.addWidget(explanation_label)
        
        # Set the content widget to the scroll area
        scroll.setWidget(content)
        layout.addWidget(scroll)