from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


def vbox_layout():
    window = QWidget()
    window.setStyleSheet("background-color:blue;")

    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)

    return window


if __name__ == '__main__':
    app = QApplication([])
    win = vbox_layout()
    win.show()
    app.exec_()
