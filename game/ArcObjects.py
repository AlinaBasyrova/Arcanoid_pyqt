from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem

class Ball(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__(0, 0, 20, 20)
        self.setPos(270, 300)
        self.setBrush(Qt.white)
        self.x_speed = 5
        self.y_speed = -5

    def move(self):
        self.setPos(self.x() + self.x_speed, self.y() + self.y_speed)

class Paddle(QGraphicsRectItem):
    def __init__(self):
        super().__init__(0, 0, 150, 10)
        self.setPos(300, 650)
        self.setBrush(Qt.yellow)
        self.x_speed = 30        

    def move_left(self):
        if self.x() > 0:
            self.setPos(self.x() - self.x_speed, self.y())

    def move_right(self):
        if self.x() < 550:
            self.setPos(self.x() + self.x_speed, self.y())

class Block(QGraphicsRectItem):
    def __init__(self, x, y):
        super().__init__(0, 0, 50, 20)
        self.setPos(x, y)
        self.setBrush(Qt.green)

class Background(QGraphicsRectItem):
    def __init__(self):
        super().__init__(0, 0, 700, 700)
        self.setPos(0, 0)
        self.setBrush(Qt.darkBlue)