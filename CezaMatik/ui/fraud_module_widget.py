from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                            QPushButton, QRadioButton, QButtonGroup, QGroupBox, QApplication,
                            QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator

class FraudModuleWidget(QWidget):
    # Signal to notify when the result is calculated
    resultCalculated = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.setupUI()
        self.connectSignals()
        
    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        fraud_group = QGroupBox("Dolandırıcılık Adli Para Cezası Hesaplama")
        fraud_layout = QVBoxLayout(fraud_group)
        fraud_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        fraud_layout.setContentsMargins(10, 12, 10, 10)
        fraud_layout.setSpacing(4)
        
        # Amount input
        amount_layout = QHBoxLayout()
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setSpacing(10)
        amount_label = QLabel("Tutarı Girin (TL)")
        amount_label.setFixedWidth(92)
        amount_layout.addWidget(amount_label)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Menfaat tutarı giriniz.")
        self.amount_input.setAlignment(Qt.AlignRight)
        self.amount_input.setFixedHeight(28)
        amount_layout.addWidget(self.amount_input)
        
        fraud_layout.addLayout(amount_layout)

        # Date selection
        date_layout = QHBoxLayout()
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(10)
        date_label = QLabel("Suç Tarihi:")
        date_label.setFixedWidth(92)
        date_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        date_layout.addWidget(date_label)
        
        date_options_layout = QVBoxLayout()
        date_options_layout.setContentsMargins(0, 0, 0, 0)
        date_options_layout.setSpacing(2)
        
        self.before_radio = QRadioButton("01.06.2024 Öncesi")
        self.before_radio.setChecked(True)
        date_options_layout.addWidget(self.before_radio)
        
        self.after_radio = QRadioButton("01.06.2024 ve Sonrası")
        date_options_layout.addWidget(self.after_radio)
        
        date_layout.addLayout(date_options_layout)
        date_layout.addStretch()
        fraud_layout.addLayout(date_layout)
        
        # Radio button group
        self.date_group = QButtonGroup()
        self.date_group.addButton(self.before_radio, 1)
        self.date_group.addButton(self.after_radio, 2)
        
        # Info label
        self.info_label = QLabel("Hesaplama 20 TL baz alınarak yapılacaktır.")
        self.info_label.setStyleSheet("color: #3F51B5; font-style: italic; font-size: 12px;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setContentsMargins(0, 4, 0, 3)
        fraud_layout.addWidget(self.info_label)
        
        # Calculate button
        self.calculate_btn = QPushButton("Hesapla")
        self.calculate_btn.setFixedHeight(30)
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                border-radius: 4px;
                padding: 6px 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #303F9F;
            }
        """)
        fraud_layout.addWidget(self.calculate_btn)
        
        # Results
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(3)
        self.rounded_amount_label = QLabel("Yuvarlanan Tutar: 0 TL")
        self.rounded_amount_label.setContentsMargins(0, 2, 0, 1)
        results_layout.addWidget(self.rounded_amount_label)
        
        self.result_label = QLabel("Adli Para Cezası: 0 Gün")
        self.result_label.setStyleSheet("font-weight: bold;")
        self.result_label.setContentsMargins(0, 0, 0, 2)
        results_layout.addWidget(self.result_label)
        fraud_layout.addLayout(results_layout)
        
        # Copy and transfer buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(4)
        
        self.copy_btn = QPushButton("Sonucu Kopyala")
        self.copy_btn.setFixedHeight(28)
        self.copy_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttons_layout.addWidget(self.copy_btn, 1)
        
        self.transfer_btn = QPushButton("Ana Hesaplamaya Aktar")
        self.transfer_btn.setFixedHeight(28)
        self.transfer_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.transfer_btn.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                border-radius: 3px;
                padding: 4px 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #303F9F;
            }
        """)
        buttons_layout.addWidget(self.transfer_btn, 1)
        
        fraud_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(fraud_group, 0, Qt.AlignTop)
        
    def connectSignals(self):
        self.before_radio.toggled.connect(self.updateInfoLabel)
        self.calculate_btn.clicked.connect(self.calculateFraudPenalty)
        self.copy_btn.clicked.connect(self.copyResult)
        self.transfer_btn.clicked.connect(self.transferResult)
        self.amount_input.textChanged.connect(self.formatCurrency)
        
    def updateInfoLabel(self):
        if self.before_radio.isChecked():
            self.info_label.setText("Hesaplama 20 TL baz alınarak yapılacaktır.")
        else:
            self.info_label.setText("Hesaplama 100 TL baz alınarak yapılacaktır.")
    
    def formatCurrency(self, text):
        if not text:
            return
            
        # Disconnect to prevent recursive calls
        self.amount_input.textChanged.disconnect(self.formatCurrency)
        
        # Store cursor position and text length before changes
        cursor_pos = self.amount_input.cursorPosition()
        old_length = len(text)
        
        # Clean the text - keep only digits, comma and dot
        clean_text = ''.join(c for c in text if c.isdigit() or c in '.,')
        
        # Handle the decimal part (using comma as decimal separator)
        parts = clean_text.split(',')
        
        # Integer part (remove any dots as they were thousand separators)
        integer_part = parts[0].replace('.', '')
        
        # Format the integer part with thousand separators (dots)
        formatted_integer = ''
        for i, char in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                formatted_integer = '.' + formatted_integer
            formatted_integer = char + formatted_integer
        
        # Combine with decimal part if it exists
        formatted_text = formatted_integer
        if len(parts) > 1:
            # Only keep the first decimal part if multiple commas were entered
            decimal_part = parts[1]
            formatted_text = f"{formatted_integer},{decimal_part}"
        
        # Calculate the new cursor position
        # Count dots before cursor in the new formatted text
        if cursor_pos <= len(parts[0]):
            # Cursor is in the integer part
            # Count original digits before cursor
            digits_before_cursor = len(parts[0].replace('.', '')[:cursor_pos])
            
            # Count dots in the formatted number before the cursor position
            dots_count = 0
            for i in range(len(formatted_integer)):
                if formatted_integer[i] == '.' and i < digits_before_cursor + dots_count:
                    dots_count += 1
            
            new_cursor_pos = digits_before_cursor + dots_count
        else:
            # Cursor is in or after the decimal part
            new_cursor_pos = len(formatted_text) - (old_length - cursor_pos)
            if len(parts) > 1 and new_cursor_pos > len(formatted_text):
                new_cursor_pos = len(formatted_text)
        
        # Update the text and cursor position
        self.amount_input.setText(formatted_text)
        self.amount_input.setCursorPosition(max(0, min(new_cursor_pos, len(formatted_text))))
        
        # Reconnect the signal
        self.amount_input.textChanged.connect(self.formatCurrency)
    
    def calculateFraudPenalty(self):
        try:
            # Get amount and properly process it for calculation
            amount_text = self.amount_input.text()
            
            # Handle empty input
            if not amount_text:
                self.result_label.setText("Geçersiz tutar girişi!")
                return
                
            # Remove thousand separators and convert decimal separator for calculation
            amount_text = amount_text.replace('.', '').replace(',', '.')
            amount = float(amount_text)
            
            # Calculate based on date selection
            if self.before_radio.isChecked():
                # Before 01.06.2024: Round up to nearest 10, divide by 10
                rounded_amount = 10 * ((amount + 9) // 10)
                days = int(rounded_amount / 10)
            else:
                # After 01.06.2024: Round up to nearest 50, divide by 50
                rounded_amount = 50 * ((amount + 49) // 50)
                days = int(rounded_amount / 50)
            
            # Ensure minimum 5 days for fraud penalty
            days = max(5, days)
            
            # Format the rounded amount with thousand separators for display
            formatted_rounded_amount = f"{rounded_amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            self.rounded_amount_label.setText(f"Yuvarlanan Tutar: {formatted_rounded_amount} TL")
            self.result_label.setText(f"Adli Para Cezası: {days} Gün")
            
            # Store the days for later use
            self.calculated_days = days
            
        except ValueError:
            self.result_label.setText("Geçersiz tutar girişi!")
    
    def copyResult(self):
        if hasattr(self, 'calculated_days'):
            result_text = f"{self.calculated_days} gün adli para cezası"
            clipboard = QApplication.clipboard()
            clipboard.setText(result_text)
    
    def transferResult(self):
        if hasattr(self, 'calculated_days'):
            self.resultCalculated.emit(self.calculated_days)

    def resetModule(self):
        self.amount_input.clear()
        self.before_radio.setChecked(True)
        self.rounded_amount_label.setText("Yuvarlanan Tutar: 0 TL")
        self.result_label.setText("Adli Para Cezası: 0 Gün")
        self.updateInfoLabel()
        if hasattr(self, 'calculated_days'):
            del self.calculated_days
