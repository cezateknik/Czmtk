from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer

class InfoPanelWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)  # Reduced spacing between elements
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setFixedHeight(280)  # Reduced height to minimize empty space
        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 4px;
            }
        """)
        
        self.layout.addWidget(self.info_text)
        
        self.history_items = []
        self.initial_penalty = None
    
    def setInitialPenalty(self, years, months, days, fine):
        self.initial_penalty = {
            "years": years,
            "months": months,
            "days": days,
            "fine": fine
        }
        
        self._updateDisplay()
    
    def addHistoryItem(self, item, index):
        self.history_items.append(item)
        self._updateDisplay()
    
    def removeLastItem(self):
        if self.history_items:
            self.history_items.pop()
            self._updateDisplay()
    
    def clearHistory(self):
        self.history_items.clear()
        self.initial_penalty = None
        self._updateDisplay()

    def _formatFineDays(self, fine):
        return f"{int(fine):,}".replace(",", ".")
    
    def _formatPenalty(self, years, months, days, fine):
        text_parts = []
        if years > 0:
            text_parts.append(f"{int(years)} yıl")  # Convert to integer
        if months > 0:
            text_parts.append(f"{int(months)} ay")  # Convert to integer
        if days > 0:
            text_parts.append(f"{int(days)} gün")  # Convert to integer
            
        # Check if only judicial fine exists (no imprisonment)
        has_imprisonment = years > 0 or months > 0 or days > 0
        
        if fine > 0:
            if has_imprisonment:
                # Both imprisonment and fine exist
                penalty_text = " ".join(text_parts) if text_parts else "0 gün"
                return f"{penalty_text} hapis ve {self._formatFineDays(fine)} gün adli para cezası"
            else:
                # Only judicial fine exists
                return f"{self._formatFineDays(fine)} gün adli para cezası"
        else:
            # Only imprisonment exists
            penalty_text = " ".join(text_parts) if text_parts else "0 gün"
            return f"{penalty_text} hapis cezası"
    
    def _updateDisplay(self):
        html = ""
        
        # Add history items
        for i, item in enumerate(self.history_items):
            ratio_text = item["ratio_text"]
            operation = item["operation"]
            
            result_text = self._formatPenalty(
                item["result_years"],
                item["result_months"],
                item["result_days"],
                item["result_fine"]
            )
            
            html += f"<p><b>{i+1}.</b> {ratio_text} {operation} uygulandığında, sonuç ceza: {result_text}</p>"
        
        # Add current penalty if available
        if self.history_items:
            last_item = self.history_items[-1]
            current_text = self._formatPenalty(
                last_item["result_years"],
                last_item["result_months"],
                last_item["result_days"],
                last_item["result_fine"]
            )
            html += f"<p><b>Güncel Ceza:</b> {current_text}</p>"

            # Add extra space after the "Güncel Ceza:" section for better scrolling
            html += "<p>&nbsp;</p>"
            html += "<p>&nbsp;</p>"
            html += "<p>&nbsp;</p>"             
        
        self.info_text.setHtml(html)
        QTimer.singleShot(0, self._scrollToBottom)

    def _scrollToBottom(self):
        scrollbar = self.info_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
