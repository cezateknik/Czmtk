from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QStackedWidget,
    QButtonGroup,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.tool_sentence_days_widget import SentenceDaysToolWidget
from ui.tool_apc_orantilama_widget import APCProportionToolWidget
from ui.tool_age_calculation_widget import AgeCalculationToolWidget


class OtherToolsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Diğer Hesaplama Araçları")
        self.setMinimumSize(860, 560)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUI()

    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)

        title_label = QLabel("Diğer Hesaplama Araçları")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)

        subtitle_label = QLabel(
            "CezaMat'ik içindeki yardımcı hesaplama araçlarını tek pencerede toplar. "
            "Soldan aracı seçip sağ tarafta kullanabilirsiniz."
        )
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("color: #5d6778;")

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        self.tool_button_group = QButtonGroup(self)
        self.tool_button_group.setExclusive(True)

        nav_widget = QWidget()
        nav_widget.setFixedWidth(228)
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(12)

        nav_title = QLabel("Araçlar")
        nav_title.setAlignment(Qt.AlignCenter)
        nav_title.setStyleSheet("font-weight: 700; font-size: 15px; color: #24324a;")
        nav_layout.addWidget(nav_title)

        nav_hint = QLabel("Bir araç seçerek sağ tarafta kullanın.")
        nav_hint.setWordWrap(True)
        nav_hint.setStyleSheet("color: #6a7486; font-size: 11px;")
        nav_layout.addWidget(nav_hint)

        self.tool_stack = QStackedWidget()
        self.tool_stack.setStyleSheet(
            "QStackedWidget { background: white; border: 1px solid #d7dfea; border-radius: 10px; }"
        )

        tools = [
            ("Hapsi Güne Çevirme", SentenceDaysToolWidget()),
            ("Hapise göre APC Orantılama", APCProportionToolWidget()),
            ("Yaş Hesaplama", AgeCalculationToolWidget()),
        ]

        for index, (title, widget) in enumerate(tools):
            button = QPushButton(title)
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setMinimumHeight(66)
            button.setStyleSheet(self.toolButtonStyle())
            button.clicked.connect(lambda _, i=index: self.tool_stack.setCurrentIndex(i))
            self.tool_button_group.addButton(button, index)
            nav_layout.addWidget(button)
            self.tool_stack.addWidget(widget)

        nav_layout.addStretch()
        self.tool_button_group.button(0).setChecked(True)
        self.tool_stack.setCurrentIndex(0)

        content_layout.addWidget(nav_widget)
        content_layout.addWidget(self.tool_stack, 1)
        main_layout.addLayout(content_layout)

        button_row = QHBoxLayout()
        button_row.addStretch()
        reset_button = QPushButton("Sıfırla")
        reset_button.setFixedWidth(110)
        reset_button.clicked.connect(self.resetCurrentTool)
        reset_button.setStyleSheet(
            "QPushButton { background: #f0f2f7; border: 1px solid #c7d0df; "
            "border-radius: 6px; padding: 7px 14px; font-weight: 600; } "
            "QPushButton:hover { background: #e5eaf4; }"
        )
        button_row.addWidget(reset_button)
        close_button = QPushButton("Kapat")
        close_button.setFixedWidth(110)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet(
            "QPushButton { background: #f0f2f7; border: 1px solid #c7d0df; "
            "border-radius: 6px; padding: 7px 14px; font-weight: 600; } "
            "QPushButton:hover { background: #e5eaf4; }"
        )
        button_row.addWidget(close_button)
        main_layout.addLayout(button_row)

    def resetCurrentTool(self):
        current_widget = self.tool_stack.currentWidget()
        if current_widget and hasattr(current_widget, "resetTool"):
            current_widget.resetTool()

    def toolButtonStyle(self):
        return """
            QPushButton {
                background-color: #fbfcfe;
                color: #1f2d46;
                border: 1px solid #d5ddea;
                border-left: 3px solid #c6d2e6;
                border-radius: 14px;
                text-align: left;
                padding: 12px 16px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #f4f7fc;
                border: 1px solid #c4cfdf;
                border-left: 3px solid #9db2d7;
            }
            QPushButton:checked {
                background-color: #edf2fb;
                border: 1px solid #a8b8d6;
                border-left: 3px solid #5579ba;
                color: #15233f;
            }
        """
