import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
import subprocess
import 111  # 导入变量interval

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My First PyQt Application")
        self.resize(400, 300)  # 设置窗口大小

        label = QLabel("Hello World!", self)
        label.move(50, 50)

        button = QPushButton("Click me!", self)
        button.move(50, 100)
        button.clicked.connect(self.button_clicked)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(50, 150)

        self.result_label = QLabel(self)
        self.result_label.move(50, 200)

    def button_clicked(self):
        # 运行xyz.py脚本
        subprocess.Popen(['python', '111.py'])

        text = self.line_edit.text()
        if text == "1":
            self.result_label.setText("a")
        elif text == "2":
            self.result_label.setText("b")

        subprocess.Popen(['python', '111.py', self.interval_edit.text()])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
