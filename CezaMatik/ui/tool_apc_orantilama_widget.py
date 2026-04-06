from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QApplication,
)
from PyQt5.QtCore import Qt

from ui.tool_input_widgets import NumericInput


class APCProportionToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(14)

        self.intro_label = QLabel(
            "Kanundaki hapis aralığı ile adli para cezası gün aralığı arasında "
            "doğrusal orantı kurar."
        )
        self.intro_label.setWordWrap(True)
        self.intro_label.setStyleSheet("color: #111111; font-weight: 500; line-height: 1.4; padding: 2px 2px 0 2px;")

        layout.addWidget(self.createRangeGroup())
        layout.addWidget(self.createAPCGroup())
        layout.addWidget(self.createGivenSentenceGroup())

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #c62828; font-weight: 600;")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        self.result_frame = QFrame()
        self.result_frame.setStyleSheet(
            "QFrame { background-color: #f8fbff; border: 1px solid #d7e2f2; "
            "border-radius: 10px; }"
        )
        result_layout = QVBoxLayout(self.result_frame)
        result_layout.setContentsMargins(12, 12, 12, 12)
        result_layout.setSpacing(8)
        self.proportional_result_label = self.createResultLabel("Orantılı Sonuç: 0,00 gün")
        self.rounded_result_label = self.createResultLabel("Yuvarlanmış Sonuç: 0 gün")
        result_layout.addWidget(self.createResultRow(self.proportional_result_label))
        result_layout.addWidget(self.createResultRow(self.rounded_result_label))
        layout.addWidget(self.result_frame)
        layout.addWidget(self.intro_label)
        layout.addStretch()

    def createRangeGroup(self):
        group = QGroupBox("Kanundaki Hapis Aralığı")
        group.setStyleSheet(self.groupStyle())
        layout = QGridLayout(group)
        layout.setContentsMargins(12, 18, 12, 10)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)

        self.alt_year_input = NumericInput()
        self.alt_month_input = NumericInput()
        self.alt_day_input = NumericInput()
        self.ust_year_input = NumericInput()
        self.ust_month_input = NumericInput()
        self.ust_day_input = NumericInput()
        for input_widget in (
            self.alt_year_input,
            self.alt_month_input,
            self.alt_day_input,
            self.ust_year_input,
            self.ust_month_input,
            self.ust_day_input,
        ):
            input_widget.setMinimumWidth(48)
            input_widget.setMaximumWidth(58)

        self.addDurationRow(
            layout, 0, "Alt Sınır:", self.alt_year_input, self.alt_month_input, self.alt_day_input
        )
        self.addDurationRow(
            layout, 1, "Üst Sınır:", self.ust_year_input, self.ust_month_input, self.ust_day_input
        )
        return group

    def createAPCGroup(self):
        group = QGroupBox("Adli Para Cezası Aralığı")
        group.setStyleSheet(self.groupStyle())
        layout = QGridLayout(group)
        layout.setContentsMargins(12, 18, 12, 10)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)

        self.apc_alt_input = NumericInput(maximum=1000000)
        self.apc_ust_input = NumericInput(maximum=1000000)
        self.apc_alt_input.setMinimumWidth(74)
        self.apc_alt_input.setMaximumWidth(86)
        self.apc_ust_input.setMinimumWidth(74)
        self.apc_ust_input.setMaximumWidth(86)

        alt_label = QLabel("APC Alt (gün):")
        ust_label = QLabel("APC Üst (gün):")
        alt_label.setStyleSheet(self.fieldLabelStyle())
        ust_label.setStyleSheet(self.fieldLabelStyle())

        layout.addWidget(alt_label, 0, 0)
        layout.addWidget(self.apc_alt_input, 0, 1)
        layout.addWidget(ust_label, 1, 0)
        layout.addWidget(self.apc_ust_input, 1, 1)
        layout.setColumnMinimumWidth(0, 120)
        layout.setColumnStretch(2, 1)
        return group

    def createGivenSentenceGroup(self):
        group = QGroupBox("Verilen Hapis Cezası")
        group.setStyleSheet(self.groupStyle())
        layout = QGridLayout(group)
        layout.setContentsMargins(12, 18, 12, 10)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)

        self.given_year_input = NumericInput()
        self.given_month_input = NumericInput()
        self.given_day_input = NumericInput()
        for input_widget in (self.given_year_input, self.given_month_input, self.given_day_input):
            input_widget.setMinimumWidth(48)
            input_widget.setMaximumWidth(58)
        self.addDurationRow(
            layout, 0, "Süre:", self.given_year_input, self.given_month_input, self.given_day_input
        )
        self.calculate_btn = QPushButton("Hesapla")
        self.calculate_btn.setFixedWidth(120)
        self.calculate_btn.clicked.connect(self.calculateProportion)
        self.calculate_btn.setStyleSheet(self.primaryButtonStyle())
        layout.addWidget(self.calculate_btn, 0, 7, alignment=Qt.AlignLeft)
        layout.setColumnMinimumWidth(7, 12)
        layout.setColumnStretch(8, 1)
        return group

    def addDurationRow(self, layout, row, label_text, year_input, month_input, day_input):
        title_label = QLabel(label_text)
        title_label.setStyleSheet(self.fieldLabelStyle())
        year_suffix = QLabel("Yıl:")
        month_suffix = QLabel("Ay:")
        day_suffix = QLabel("Gün:")

        for suffix in (year_suffix, month_suffix, day_suffix):
            suffix.setStyleSheet(self.fieldLabelStyle())

        layout.addWidget(title_label, row, 0)
        layout.addWidget(year_suffix, row, 1)
        layout.addWidget(year_input, row, 2)
        layout.addWidget(month_suffix, row, 3)
        layout.addWidget(month_input, row, 4)
        layout.addWidget(day_suffix, row, 5)
        layout.addWidget(day_input, row, 6)
        layout.setColumnMinimumWidth(0, 86)
        layout.setColumnStretch(7, 1)

    def createResultLabel(self, text):
        label = QLabel(text)
        label.setMinimumHeight(34)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        label.setStyleSheet(
            "QLabel { background-color: #eef4ff; border: 1px solid #cad8f0; "
            "border-radius: 7px; padding: 0 10px; font-weight: bold; color: #22324d; }"
        )
        return label

    def createResultRow(self, label):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(6)
        layout.addWidget(label, 1)
        layout.addWidget(self.createCopyButton(label))
        return row

    def createCopyButton(self, label):
        button = QPushButton("Kopyala")
        button.setFixedWidth(78)
        button.setFixedHeight(30)
        button.setStyleSheet(self.secondaryButtonStyle())
        button.clicked.connect(lambda: self.copyLabelText(label))
        return button

    def groupStyle(self):
        return """
            QGroupBox {
                background-color: #fbfcfe;
                border: 1px solid #d8e0ec;
                border-radius: 10px;
                margin-top: 12px;
                font-weight: bold;
                color: #20314d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                color: #20314d;
                background-color: #fbfcfe;
            }
        """

    def fieldLabelStyle(self):
        return "color: #20314d; font-weight: 600;"

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

    def secondaryButtonStyle(self):
        return """
            QPushButton {
                background-color: #f3f6fc;
                color: #23324d;
                border: 1px solid #cfd9ea;
                border-radius: 6px;
                padding: 6px 10px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e8eef9;
                border: 1px solid #becce5;
            }
            QPushButton:pressed {
                background-color: #dbe5f5;
                border: 1px solid #aebdd9;
                padding-top: 7px;
                padding-left: 11px;
            }
        """

    def copyLabelText(self, label):
        QApplication.clipboard().setText(label.text())

    def sentenceToDays(self, years, months, days):
        return years * 365 + months * 30 + days

    def formatInteger(self, value):
        return f"{int(value):,}".replace(",", ".")

    def formatDecimal(self, value):
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def calculateProportion(self):
        self.error_label.clear()

        alt_hapis_gun = self.sentenceToDays(
            self.alt_year_input.value(),
            self.alt_month_input.value(),
            self.alt_day_input.value(),
        )
        ust_hapis_gun = self.sentenceToDays(
            self.ust_year_input.value(),
            self.ust_month_input.value(),
            self.ust_day_input.value(),
        )
        verilen_hapis_gun = self.sentenceToDays(
            self.given_year_input.value(),
            self.given_month_input.value(),
            self.given_day_input.value(),
        )
        apc_alt = self.apc_alt_input.value()
        apc_ust = self.apc_ust_input.value()

        if ust_hapis_gun <= alt_hapis_gun:
            self.error_label.setText("Hapis üst sınırı, alt sınırdan büyük olmalıdır.")
            return

        if apc_ust < apc_alt:
            self.error_label.setText("APC üst sınırı, alt sınırdan küçük olamaz.")
            return

        orantili_apc = apc_alt + (
            (verilen_hapis_gun - alt_hapis_gun) / (ust_hapis_gun - alt_hapis_gun)
        ) * (apc_ust - apc_alt)
        yuvarlanmis_apc = round(orantili_apc)

        self.proportional_result_label.setText(
            f"Orantılı Sonuç: {self.formatDecimal(orantili_apc)} gün"
        )
        self.rounded_result_label.setText(
            f"Yuvarlanmış Sonuç: {self.formatInteger(yuvarlanmis_apc)} gün"
        )

    def resetTool(self):
        for input_widget in (
            self.alt_year_input,
            self.alt_month_input,
            self.alt_day_input,
            self.ust_year_input,
            self.ust_month_input,
            self.ust_day_input,
            self.apc_alt_input,
            self.apc_ust_input,
            self.given_year_input,
            self.given_month_input,
            self.given_day_input,
        ):
            input_widget.clear()
        self.error_label.clear()
        self.proportional_result_label.setText("Orantılı Sonuç: 0,00 gün")
        self.rounded_result_label.setText("Yuvarlanmış Sonuç: 0 gün")
