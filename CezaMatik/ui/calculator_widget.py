from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, 
                            QLineEdit, QLabel, QGroupBox, QApplication, QHBoxLayout,
                            QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent
import re

class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setupUI()
        self.connectSignals()
        
        # Calculator state
        self.reset_next = False
        self.current_operation = None
        self.stored_number = 0
        self.last_button_was_operation = False
        
    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        calculator_group = QGroupBox("Hesap Makinesi")
        calculator_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        calculator_layout = QVBoxLayout(calculator_group)
        
        # Display container
        display_container = QVBoxLayout()
        
        # Operation display
        display_row = QHBoxLayout()
        
        self.operation_display = QLabel("")
        self.operation_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.operation_display.setFont(QFont("Arial", 14))
        self.operation_display.setStyleSheet("""
            QLabel {
                color: #4B89DC;
                font-weight: bold;
                padding: 5px;
                min-width: 30px;
            }
        """)
        
        # Number display
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(39)
        self.display.setFont(QFont("Arial", 14))
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        
        display_row.addWidget(self.operation_display, 1)
        display_row.addWidget(self.display, 4)
        display_container.addLayout(display_row)
        
        calculator_layout.addLayout(display_container)
        
        # Buttons grid
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(2)
        
        # Button style
        button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                min-height: 39px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
        
        operation_style = """
            QPushButton {
                background-color: #4B89DC;
                color: white;
                border: 1px solid #3a70b9;
                border-radius: 4px;
                font-size: 14px;
                min-height: 39px;
            }
            QPushButton:hover {
                background-color: #3a70b9;
            }
        """
        
        clear_style = """
            QPushButton {
                background-color: #F05454;
                color: white;
                border: 1px solid #d43f3f;
                border-radius: 4px;
                font-size: 14px;
                min-height: 39px;
            }
            QPushButton:hover {
                background-color: #d43f3f;
            }
        """
        
        # Clear button
        self.clear_btn = QPushButton("C")
        self.clear_btn.setStyleSheet(clear_style)
        buttons_layout.addWidget(self.clear_btn, 0, 0)
        
        # Special operations
        self.backspace_btn = QPushButton("⌫")
        self.backspace_btn.setStyleSheet(button_style)
        buttons_layout.addWidget(self.backspace_btn, 0, 1)
        
        self.open_parenthesis_btn = QPushButton("(")
        self.open_parenthesis_btn.setStyleSheet(button_style)
        buttons_layout.addWidget(self.open_parenthesis_btn, 0, 2)
        
        self.close_parenthesis_btn = QPushButton(")")
        self.close_parenthesis_btn.setStyleSheet(button_style)
        buttons_layout.addWidget(self.close_parenthesis_btn, 0, 3)
        
        # Numbers
        self.number_buttons = {}
        button_positions = [
            (7, 1, 0), (8, 1, 1), (9, 1, 2),
            (4, 2, 0), (5, 2, 1), (6, 2, 2),
            (1, 3, 0), (2, 3, 1), (3, 3, 2),
            (0, 4, 0)
        ]
        
        for number, row, col in button_positions:
            self.number_buttons[number] = QPushButton(str(number))
            self.number_buttons[number].setStyleSheet(button_style)
            buttons_layout.addWidget(self.number_buttons[number], row, col)
        
        # Decimal point
        self.decimal_btn = QPushButton(",")
        self.decimal_btn.setStyleSheet(button_style)
        buttons_layout.addWidget(self.decimal_btn, 4, 1)
        
        # Operations
        self.equals_btn = QPushButton("=")
        self.equals_btn.setStyleSheet(operation_style)
        buttons_layout.addWidget(self.equals_btn, 4, 2)
        
        self.add_btn = QPushButton("+")
        self.add_btn.setStyleSheet(operation_style)
        buttons_layout.addWidget(self.add_btn, 4, 3)
        
        self.subtract_btn = QPushButton("-")
        self.subtract_btn.setStyleSheet(operation_style)
        buttons_layout.addWidget(self.subtract_btn, 3, 3)
        
        self.multiply_btn = QPushButton("×")
        self.multiply_btn.setStyleSheet(operation_style)
        buttons_layout.addWidget(self.multiply_btn, 2, 3)
        
        self.divide_btn = QPushButton("/")
        self.divide_btn.setStyleSheet(operation_style)
        buttons_layout.addWidget(self.divide_btn, 1, 3)
        
        calculator_layout.addLayout(buttons_layout)
        main_layout.addWidget(calculator_group)
        
        # Enable focus to capture keyboard events
        self.setFocusPolicy(Qt.StrongFocus)
        
    def connectSignals(self):
        # Connect number buttons
        for number, button in self.number_buttons.items():
            button.clicked.connect(lambda _, n=number: self.numberPressed(n))
        
        # Connect operation buttons
        self.add_btn.clicked.connect(lambda: self.operationPressed('+'))
        self.subtract_btn.clicked.connect(lambda: self.operationPressed('-'))
        self.multiply_btn.clicked.connect(lambda: self.operationPressed('*'))
        self.divide_btn.clicked.connect(lambda: self.operationPressed('/'))
        self.equals_btn.clicked.connect(self.equalsPressed)
        
        # Connect other buttons
        self.clear_btn.clicked.connect(self.clearDisplay)
        self.decimal_btn.clicked.connect(self.decimalPressed)
        self.backspace_btn.clicked.connect(self.backspacePressed)
        self.open_parenthesis_btn.clicked.connect(lambda: self.appendToDisplay('('))
        self.close_parenthesis_btn.clicked.connect(lambda: self.appendToDisplay(')'))
        
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key >= Qt.Key_0 and key <= Qt.Key_9:
            self.numberPressed(int(event.text()))
        elif key == Qt.Key_Plus:
            self.operationPressed('+')
        elif key == Qt.Key_Minus:
            self.operationPressed('-')
        elif key == Qt.Key_Asterisk:
            self.operationPressed('*')
        elif key == Qt.Key_Slash:
            self.operationPressed('/')
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.equalsPressed()
        elif key == Qt.Key_Period or key == Qt.Key_Comma:
            self.decimalPressed()
        elif key == Qt.Key_Backspace:
            self.backspacePressed()
        elif key == Qt.Key_ParenLeft:
            self.appendToDisplay('(')
        elif key == Qt.Key_ParenRight:
            self.appendToDisplay(')')
        elif key == Qt.Key_Escape:
            self.clearDisplay()
    
    def format_number(self, value):
        """Format number with Turkish-style thousands/decimal separators."""
        if isinstance(value, float) and value.is_integer():
            value = int(value)

        if isinstance(value, int):
            return f"{value:,}".replace(",", ".")

        formatted = f"{value:,.2f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    def format_number_token(self, token):
        """Format a single numeric token for calculator display."""
        if not token:
            return token

        if "," in token:
            integer_part, decimal_part = token.split(",", 1)
        else:
            integer_part, decimal_part = token, None

        integer_digits = integer_part.replace(".", "")
        if integer_digits:
            formatted_integer = f"{int(integer_digits):,}".replace(",", ".")
        else:
            formatted_integer = "0" if decimal_part is not None else ""

        if decimal_part is not None:
            return f"{formatted_integer},{decimal_part}"
        return formatted_integer

    def format_expression(self, text):
        """Apply Turkish number formatting to all numeric parts of an expression."""
        return re.sub(r"\d[\d\.,]*", lambda match: self.format_number_token(match.group(0)), text)

    def parse_number(self, text):
        """Parse both raw calculator input and formatted display values."""
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", text):
            return float(text.replace(".", ""))
        if "," in text:
            return float(text.replace(".", "").replace(",", "."))
        return float(text)

    def normalize_expression(self, text):
        """Convert display-formatted expression into Python-evaluable form."""
        def repl(match):
            token = match.group(0)
            return token.replace(".", "").replace(",", ".")

        return re.sub(r"\d[\d\.,]*", repl, text)

    def get_current_number_token(self, text):
        token = ""
        for char in reversed(text):
            if char.isdigit() or char in ".,":  # current numeric token
                token = char + token
            else:
                break
        return token
    
    def updateOperationDisplay(self, operation=None):
        if operation is None:
            self.operation_display.setText("")
        elif operation == '+':
            self.operation_display.setText("+")
        elif operation == '-':
            self.operation_display.setText("-")
        elif operation == '*':
            self.operation_display.setText("×")
        elif operation == '/':
            self.operation_display.setText("÷")
            
    def numberPressed(self, number):
        if self.reset_next:
            self.display.setText("0")
            self.reset_next = False
            
        current_text = self.display.text()
        if current_text == "0":
            new_text = str(number)
        else:
            new_text = current_text + str(number)

        self.display.setText(self.format_expression(new_text))
        
        self.last_button_was_operation = False
    
    def operationPressed(self, operation):
        try:
            # If last button was an operation, just update the operation
            if self.last_button_was_operation:
                self.current_operation = operation
                self.updateOperationDisplay(operation)
                return
                
            current_text = self.display.text()
            
            # If we already have a pending operation, calculate it first
            if self.current_operation and not self.reset_next:
                self.calculateCurrentOperation()
            else:
                # Otherwise just store the current number
                self.stored_number = eval(self.normalize_expression(current_text))
                
            self.reset_next = True
            self.current_operation = operation
            
            # Update operation display
            self.updateOperationDisplay(operation)
            self.last_button_was_operation = True
        except Exception:
            self.display.setText("Error")
            self.reset_next = True
    
    def calculateCurrentOperation(self):
        try:
            current_text = self.display.text()
            current_number = eval(self.normalize_expression(current_text))
            
            if self.current_operation == '+':
                result = self.stored_number + current_number
            elif self.current_operation == '-':
                result = self.stored_number - current_number
            elif self.current_operation == '*':
                result = self.stored_number * current_number
            elif self.current_operation == '/':
                if current_number != 0:
                    result = self.stored_number / current_number
                else:
                    self.display.setText("Error")
                    return
            else:
                # No operation, just use the current number
                result = current_number
                
            # Format result
            if result == int(result):
                result = int(result)
                
            # Use the new formatting method
            self.display.setText(self.format_number(result))
            self.stored_number = result
            return result
        except Exception:
            self.display.setText("Error")
            return None
    
    def equalsPressed(self):
        try:
            current_text = self.display.text()
            
            # If there's no explicit operation but expression is provided, evaluate it
            if '(' in current_text or ')' in current_text or '+' in current_text or '-' in current_text or '*' in current_text or '/' in current_text:
                result = eval(self.normalize_expression(current_text))
                # Use the new formatting method
                self.display.setText(self.format_number(result))
            elif self.current_operation:
                self.calculateCurrentOperation()
                self.current_operation = None
                
                # Clear operation display
                self.updateOperationDisplay()
        except Exception:
            self.display.setText("Error")
            
        self.reset_next = True
        self.last_button_was_operation = False
    
    def clearDisplay(self):
        self.display.setText("0")
        self.current_operation = None
        self.stored_number = 0
        self.reset_next = False
        self.last_button_was_operation = False
        
        # Clear operation display
        self.updateOperationDisplay()
    
    def decimalPressed(self):
        if self.reset_next:
            self.display.setText("0")
            self.reset_next = False
            
        current_text = self.display.text()
        current_token = self.get_current_number_token(current_text)

        if "," in current_token:
            return

        if current_text == "0":
            new_text = "0,"
        elif current_text[-1] in "+-*/(":
            new_text = current_text + "0,"
        else:
            new_text = current_text + ","

        self.display.setText(self.format_expression(new_text))
        
        self.last_button_was_operation = False
    
    def backspacePressed(self):
        current_text = self.display.text()
        if len(current_text) > 1:
            self.display.setText(self.format_expression(current_text[:-1]))
        else:
            self.display.setText("0")
        
        self.last_button_was_operation = False
    
    def appendToDisplay(self, text):
        if self.reset_next:
            self.display.setText("")
            self.reset_next = False
            
        current_text = self.display.text()
        if current_text == "0" and text != ',':
            self.display.setText(text)
        else:
            self.display.setText(current_text + text)
        
        self.last_button_was_operation = False
