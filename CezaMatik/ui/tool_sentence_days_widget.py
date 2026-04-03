from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QGridLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QButtonGroup,
    QRadioButton,
    QSizePolicy,
)
from PyQt5.QtCore import Qt

from ui.tool_input_widgets import NumericInput


class SentenceDaysToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        intro_label = QLabel(
            "Hapis sürelerini sabit hukuk mantığına göre dönüştürür. "
            "1 yıl = 365 gün, 1 ay = 30 gün olarak esas alınır."
        )
        intro_label.setWordWrap(True)
        intro_label.setStyleSheet("color: #b86a15; font-weight: 600; line-height: 1.4; padding: 0 2px 4px 2px;")
        layout.addWidget(intro_label)

        tabs = QTabWidget()
        tabs.setStyleSheet(self.tabStyle())
        tabs.addTab(self.createSentenceToDaysTab(), "Hapsi Güne Çevir")
        tabs.addTab(self.createDaysToSentenceTab(), "Günü Yıl/Ay/Gün Yap")
        layout.addWidget(tabs)

    def createSentenceToDaysTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(6, 8, 6, 6)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        sentence_group = self.createSentenceGroup()
        fine_group = self.createFineGroup()
        fine_group.setMaximumWidth(280)
        top_row.addWidget(sentence_group, 1)
        top_row.addWidget(fine_group, 0)
        layout.addLayout(top_row)

        button_row = QHBoxLayout()
        calculate_btn = QPushButton("Hesapla")
        calculate_btn.setFixedWidth(130)
        calculate_btn.clicked.connect(self.calculateSentenceDays)
        calculate_btn.setStyleSheet(self.primaryButtonStyle())
        button_row.addStretch()
        button_row.addWidget(calculate_btn)
        button_row.addStretch()
        layout.addLayout(button_row)

        self.sentence_to_days_result = self.createResultLabel("Toplam: 0 gün")
        self.fine_amount_result = self.createResultLabel("Adli Para Cezası Tutarı: 0 TL")
        layout.addWidget(self.sentence_to_days_result)
        layout.addWidget(self.fine_amount_result)
        layout.addStretch()
        return tab

    def createSentenceGroup(self):
        group = QGroupBox("Hapis Süresi")
        group.setStyleSheet(self.groupStyle())
        layout = QGridLayout(group)
        layout.setContentsMargins(12, 18, 12, 10)
        layout.setHorizontalSpacing(4)
        layout.setVerticalSpacing(4)

        self.sentence_year_input = NumericInput()
        self.sentence_month_input = NumericInput()
        self.sentence_day_input = NumericInput()
        for input_widget in (self.sentence_year_input, self.sentence_month_input, self.sentence_day_input):
            input_widget.setMinimumWidth(58)
            input_widget.setMaximumWidth(72)

        sure_label = QLabel("Süre:")
        sure_label.setStyleSheet(self.fieldLabelStyle())
        year_label = QLabel("Yıl:")
        year_label.setStyleSheet(self.fieldLabelStyle())
        month_label = QLabel("Ay:")
        month_label.setStyleSheet(self.fieldLabelStyle())
        day_label = QLabel("Gün:")
        day_label.setStyleSheet(self.fieldLabelStyle())

        layout.addWidget(sure_label, 0, 0)
        layout.addWidget(year_label, 0, 1)
        layout.addWidget(self.sentence_year_input, 0, 2)
        layout.addWidget(month_label, 0, 3)
        layout.addWidget(self.sentence_month_input, 0, 4)
        layout.addWidget(day_label, 0, 5)
        layout.addWidget(self.sentence_day_input, 0, 6)

        layout.setColumnStretch(7, 1)
        return group

    def createFineGroup(self):
        group = QGroupBox("Günlük Miktar")
        group.setStyleSheet(self.groupStyle())
        layout = QVBoxLayout(group)
        layout.setContentsMargins(12, 18, 12, 10)
        layout.setSpacing(6)

        self.fine_button_group = QButtonGroup(self)
        self.fine_button_group.setExclusive(True)
        preset_row = QHBoxLayout()
        preset_row.setSpacing(4)

        self.fine_radio_20 = QRadioButton("20 TL")
        self.fine_radio_100 = QRadioButton("100 TL")
        self.fine_radio_500 = QRadioButton("500 TL")
        self.fine_radio_20.setChecked(True)

        for idx, button in enumerate((self.fine_radio_20, self.fine_radio_100, self.fine_radio_500)):
            button.setStyleSheet("color: #20314d; font-weight: 600;")
            self.fine_button_group.addButton(button, idx)
            preset_row.addWidget(button)
        layout.addLayout(preset_row)

        custom_row = QHBoxLayout()
        custom_row.setSpacing(6)
        custom_label = QLabel("Özel Tutar")
        custom_label.setStyleSheet(self.fieldLabelStyle())
        self.custom_fine_input = NumericInput(maximum=1000000)
        self.custom_fine_input.setPlaceholderText("Örn: 250")
        self.custom_fine_input.setMinimumWidth(82)
        self.custom_fine_input.setMaximumWidth(96)
        self.custom_fine_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.custom_fine_input.textChanged.connect(self.handleCustomFineChanged)
        custom_row.addWidget(custom_label)
        custom_row.addWidget(self.custom_fine_input)
        custom_row.addWidget(self.suffixLabel("TL"))
        custom_row.addStretch()
        layout.addLayout(custom_row)
        return group

    def createDaysToSentenceTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(6, 8, 6, 6)
        layout.setSpacing(6)

        group = QGroupBox("Toplam Gün")
        group.setStyleSheet(self.groupStyle())
        group_layout = QGridLayout(group)
        group_layout.setContentsMargins(12, 18, 12, 10)
        group_layout.setHorizontalSpacing(6)
        group_layout.setVerticalSpacing(6)

        self.total_days_input = NumericInput(maximum=1000000)
        self.total_days_input.setMinimumWidth(72)
        self.total_days_input.setMaximumWidth(90)
        label = QLabel("Gün:")
        label.setStyleSheet(self.fieldLabelStyle())
        convert_btn = QPushButton("Dönüştür")
        convert_btn.setFixedWidth(120)
        convert_btn.clicked.connect(self.convertDaysToSentence)
        convert_btn.setStyleSheet(self.primaryButtonStyle())
        result_title = QLabel("Sonuç:")
        result_title.setStyleSheet(self.fieldLabelStyle())
        self.days_to_sentence_result = self.createInlineResultLabel("0 gün")

        group_layout.addWidget(label, 0, 0)
        group_layout.addWidget(self.total_days_input, 0, 1)
        group_layout.addWidget(convert_btn, 0, 2)
        group_layout.addWidget(result_title, 0, 3)
        group_layout.addWidget(self.days_to_sentence_result, 0, 4)
        group_layout.setColumnStretch(5, 1)
        layout.addWidget(group)
        layout.addStretch()
        return tab

    def handleCustomFineChanged(self, text):
        if text.strip():
            self.fine_button_group.setExclusive(False)
            for button in self.fine_button_group.buttons():
                button.setChecked(False)
            self.fine_button_group.setExclusive(True)
        elif not any(button.isChecked() for button in self.fine_button_group.buttons()):
            self.fine_radio_20.setChecked(True)

    def getSelectedFineAmount(self):
        custom_value = self.custom_fine_input.value()
        if custom_value > 0:
            return custom_value
        if self.fine_radio_100.isChecked():
            return 100
        if self.fine_radio_500.isChecked():
            return 500
        return 20

    def suffixLabel(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: #445067; font-weight: 600;")
        return label

    def createResultLabel(self, text):
        label = QLabel(text)
        label.setMinimumHeight(34)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        label.setStyleSheet(
            "QLabel { background-color: #eef4ff; border: 1px solid #cad8f0; "
            "border-radius: 7px; padding: 0 8px; font-weight: bold; color: #22324d; }"
        )
        return label

    def createInlineResultLabel(self, text):
        label = QLabel(text)
        label.setMinimumHeight(30)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        label.setStyleSheet(
            "QLabel { background-color: #eef4ff; border: 1px solid #cad8f0; "
            "border-radius: 7px; padding: 0 10px; font-weight: bold; color: #22324d; }"
        )
        return label

    def groupStyle(self):
        return """
            QGroupBox {
                background-color: #fbfcfe;
                border: 1px solid #d8e0ec;
                border-radius: 9px;
                margin-top: 10px;
                font-weight: bold;
                color: #20314d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px;
                color: #20314d;
                background-color: #fbfcfe;
            }
        """

    def tabStyle(self):
        return """
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: #f3f6fc;
                border: 1px solid #d6deeb;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 14px;
                min-width: 165px;
                margin-right: 4px;
                color: #31415f;
                font-weight: 600;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border: 1px solid #c7d3e7;
                border-bottom: none;
                color: #22324d;
            }
        """

    def fieldLabelStyle(self):
        return "color: #20314d; font-weight: 600; padding-right: 2px;"

    def primaryButtonStyle(self):
        return """
            QPushButton {
                background-color: #3F51B5;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34449b;
            }
            QPushButton:pressed {
                background-color: #2b3a87;
            }
        """

    def formatInteger(self, value):
        return f"{int(value):,}".replace(",", ".")

    def formatSentence(self, years, months, days):
        parts = []
        if years:
            parts.append(f"{years} yıl")
        if months:
            parts.append(f"{months} ay")
        if days:
            parts.append(f"{days} gün")
        return " ".join(parts) if parts else "0 gün"

    def calculateSentenceDays(self):
        total_days = (
            self.sentence_year_input.value() * 365
            + self.sentence_month_input.value() * 30
            + self.sentence_day_input.value()
        )
        fine_amount = self.getSelectedFineAmount()
        total_tl = total_days * fine_amount

        self.sentence_to_days_result.setText(f"Toplam: {self.formatInteger(total_days)} gün")
        self.fine_amount_result.setText(
            f"Adli Para Cezası Tutarı: {self.formatInteger(total_tl)} TL ({self.formatInteger(fine_amount)} TL x {self.formatInteger(total_days)} gün)"
        )

    def convertDaysToSentence(self):
        total_days = self.total_days_input.value()
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30
        self.days_to_sentence_result.setText(self.formatSentence(years, months, days))
