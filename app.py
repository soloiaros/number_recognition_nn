# Импорт всех необходимых модулей
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PIL import Image
from recognize import predict_number


# Инициализвция класса главного окна программы
class NumberRecognition(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загрузка пользовательского интерфейса
        uic.loadUi('ui/ui_file.ui', self)
        # Заголовок окна программы
        self.setWindowTitle('Number Recognition')
        # Загрузка пустого холста из файлов программы
        self.pixmap = QPixmap('data/plain_img.png')
        self.imageLabel.setPixmap(self.pixmap)
        # Реакции программы на нажатия кнопок интерфейса
        self.recoButton.clicked.connect(self.save_image)
        self.clearButton.clicked.connect(self.clear_canvas)

    def mouseMoveEvent(self, event):
        # Проверка условия, что курсор находится на холсте
        if 10 < event.x() < 266 and 10 < event.y() < 266:
            # Задание объекта для рисования
            painter = QPainter(self.pixmap)
            # Определение кисти
            painter.setBrush(Qt.black)
            # На каждое движение мыши с любой ее зажатой кнопкой рисуется круг
            painter.drawEllipse(event.x() - 15, event.y() - 15,
                                15, 15)

            self.imageLabel.setPixmap(self.pixmap)
            self.update()

    def save_image(self):
        # Изменение разрешения изображения
        image = Image.fromqpixmap(self.pixmap)
        image = image.resize((28, 28))
        # Сохранение получившегося изображения в файлы программы
        image.save('data/image.png')
        self.recognize_image()

    def recognize_image(self):
        # Вызов нейросетевой функции для определения цифры
        predicted_n = predict_number()
        # Отображение полученного числа в окне программы
        self.lcdNumber.display(predicted_n)

    def clear_canvas(self):
        # Очистка холста при нажатии на соответствующую кнопку
        self.pixmap = QPixmap('data/plain_img.png')
        self.imageLabel.setPixmap(self.pixmap)


# Отлавливание ошибок и исключений прграммы
def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# Запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NumberRecognition()
    sys.excepthook = exception_hook
    ex.show()
    sys.exit(app.exec_())
