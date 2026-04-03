import calendar
from datetime import date

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QDate

from ui.tool_input_widgets import NoWheelDateEdit


class AgeCalculationToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        intro_label = QLabel(
            "Takvimsel yaş hesabını yıl, ay ve gün olarak yapar. "
            "Suç tarihindeki yaş, şimdiki yaş ve duruşma türünü birlikte üretir."
        )
        intro_label.setWordWrap(True)
        intro_label.setStyleSheet("color: #b86a15; font-weight: 600; line-height: 1.4; padding: 0 2px 4px 2px;")
        layout.addWidget(intro_label)

        input_group = QGroupBox("Tarih Bilgileri")
        input_group.setStyleSheet(self.groupStyle())
        input_layout = QGridLayout(input_group)
        input_layout.setContentsMargins(12, 18, 12, 10)
        input_layout.setHorizontalSpacing(8)
        input_layout.setVerticalSpacing(6)

        today = QDate.currentDate()
        self.birth_date_input = self.createDateEdit(today.addYears(-18))
        self.crime_date_input = self.createDateEdit(today)
        self.current_date_input = self.createDateEdit(today)

        self.addFieldRow(input_layout, 0, "Doğum Tarihi:", self.birth_date_input)
        self.addFieldRow(input_layout, 1, "Suç Tarihi:", self.crime_date_input)
        self.addFieldRow(input_layout, 2, "Şimdiki Tarih:", self.current_date_input)
        calculate_btn = QPushButton("Hesapla")
        calculate_btn.setFixedWidth(140)
        calculate_btn.clicked.connect(self.calculateAges)
        calculate_btn.setStyleSheet(self.primaryButtonStyle())
        input_layout.addWidget(calculate_btn, 3, 1, alignment=Qt.AlignLeft)
        layout.addWidget(input_group)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #c62828; font-weight: 600;")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        self.crime_age_label = self.createResultLabel("Suç Tarihindeki Yaşı: 0 yıl, 0 ay, 0 gün")
        self.current_age_label = self.createResultLabel("Şimdiki Yaşı: 0 yıl, 0 ay, 0 gün")
        self.hearing_type_label = self.createResultLabel("Duruşma Türü: DURUŞMA KAPALI")
        layout.addWidget(self.crime_age_label)
        layout.addWidget(self.current_age_label)
        layout.addWidget(self.hearing_type_label)
        layout.addStretch()

    def addFieldRow(self, layout, row, label_text, widget):
        label = QLabel(label_text)
        label.setStyleSheet(self.fieldLabelStyle())
        layout.addWidget(label, row, 0)
        layout.addWidget(widget, row, 1)
        layout.setColumnStretch(2, 1)

    def createDateEdit(self, qdate):
        widget = NoWheelDateEdit()
        widget.setCalendarPopup(True)
        widget.setDisplayFormat("dd.MM.yyyy")
        widget.setDate(qdate)
        widget.setStyleSheet(
            "QDateEdit { background: white; border: 1px solid #c9d4e3; "
            "border-radius: 6px; padding: 4px 8px; }"
            "QDateEdit:focus { border: 1px solid #6f89bf; background: #fbfdff; }"
        )
        return widget

    def createResultLabel(self, text):
        label = QLabel(text)
        label.setMinimumHeight(34)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        label.setStyleSheet(
            "QLabel { background-color: #eef4ff; border: 1px solid #cad8f0; "
            "border-radius: 7px; padding: 0 8px; font-weight: bold; color: #22324d; }"
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

    def toDate(self, qdate):
        return date(qdate.year(), qdate.month(), qdate.day())

    def addYears(self, base_date, years):
        try:
            return base_date.replace(year=base_date.year + years)
        except ValueError:
            return base_date.replace(month=2, day=28, year=base_date.year + years)

    def calculateDetailedAge(self, birth_date, target_date):
        if target_date < birth_date:
            raise ValueError("Hedef tarih, doğum tarihinden önce olamaz.")

        years = target_date.year - birth_date.year
        months = target_date.month - birth_date.month
        days = target_date.day - birth_date.day

        if days < 0:
            previous_month = target_date.month - 1 or 12
            previous_month_year = target_date.year if target_date.month > 1 else target_date.year - 1
            days_in_previous_month = calendar.monthrange(previous_month_year, previous_month)[1]
            days += days_in_previous_month
            months -= 1

        if months < 0:
            months += 12
            years -= 1

        return years, months, days

    def formatAge(self, years, months, days):
        return f"{years} yıl, {months} ay, {days} gün"

    def determineHearingType(self, birth_date, current_date):
        return "DURUŞMA AÇIK" if current_date >= self.addYears(birth_date, 18) else "DURUŞMA KAPALI"

    def calculateAges(self):
        self.error_label.clear()

        birth_date = self.toDate(self.birth_date_input.date())
        crime_date = self.toDate(self.crime_date_input.date())
        current_date = self.toDate(self.current_date_input.date())

        if crime_date < birth_date:
            self.error_label.setText("Suç tarihi, doğum tarihinden önce olamaz.")
            return

        if current_date < birth_date:
            self.error_label.setText("Şimdiki tarih, doğum tarihinden önce olamaz.")
            return

        crime_age = self.calculateDetailedAge(birth_date, crime_date)
        current_age = self.calculateDetailedAge(birth_date, current_date)
        hearing_type = self.determineHearingType(birth_date, current_date)

        self.crime_age_label.setText(f"Suç Tarihindeki Yaşı: {self.formatAge(*crime_age)}")
        self.current_age_label.setText(f"Şimdiki Yaşı: {self.formatAge(*current_age)}")
        self.hearing_type_label.setText(f"Duruşma Türü: {hearing_type}")
