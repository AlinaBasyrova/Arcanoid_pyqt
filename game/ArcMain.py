import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsView, QLabel, QMainWindow, QPushButton, QGraphicsScene
from PyQt5.QtCore import Qt, QTimer
import ArcObjects

class Game(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 700, 700)
        self.scene.setBackgroundBrush(Qt.black)
        self.setStyleSheet("QLabel {font: 10pt Comic Sans MS; color: white}")

        self.score = 0

        self.score_label = QLabel("Score: {}".format(self.score), self)
        self.score_label.setStyleSheet("color: white;")
        self.score_label.setGeometry(10, 10, 200, 30)
        self.score_label.setAlignment(Qt.AlignCenter)

        self.bg = ArcObjects.Background()
        self.ball = ArcObjects.Ball()
        self.paddle = ArcObjects.Paddle()
        self.blocks = []

        self.scene.addItem(self.bg)
        self.scene.addItem(self.ball)
        self.scene.addItem(self.paddle)

        for row in range(5):
            for col in range(14):
                block = ArcObjects.Block(col * 50, 50 + row * 30)
                self.scene.addItem(block)
                self.blocks.append(block)

        self.view = QGraphicsView(self.scene)
        self.setScene(self.scene)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.paddle.move_left()
        elif event.key() == Qt.Key_Right:
            self.paddle.move_right()

    def update(self):
        self.ball.move()

        if self.ball.collidesWithItem(self.paddle):
            self.ball.y_speed = -self.ball.y_speed

        for block in self.blocks:
            if self.ball.collidesWithItem(block):
                self.increase_score(10)
                self.scene.removeItem(block)
                self.blocks.remove(block)
                self.ball.y_speed = -self.ball.y_speed

        if self.ball.y() < 0:
            self.ball.y_speed = -self.ball.y_speed
        if self.ball.x() < 0 or self.ball.x() > 680:
            self.ball.x_speed = -self.ball.x_speed

        if self.ball.y() > self.scene.height():
            self.game_over("Ты проиграл :(")
        if not self.blocks:
            self.game_over("Ты победил! :)")

    def increase_score(self, points):
        self.score += points
        self.score_label.setText("Score: {}".format(self.score))

    def game_over(self, text):
        self.timer.stop()
        print("Игра окончена.")
        lose_window = LoseWindow(text, self.score)
        game_stack.addWidget(lose_window)
        game_stack.removeWidget(self)

class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()

        self.setStyleSheet("QLabel {font: 20pt Comic Sans MS; color: white} \
                   QPushButton {font: 10pt Comic Sans MS; background-color: white}")

        welcome_label = QLabel("Добро пожаловать!", self)
        welcome_label.setGeometry(0, 250, 710, 40)
        welcome_label.setAlignment(Qt.AlignCenter)

        start_button = QPushButton("Начать игру", self)
        start_button.setGeometry(300, 350, 120, 40)
        start_button.clicked.connect(self.start_game)

    def start_game(self):
        graphics_view = Game()
        game_stack.addWidget(graphics_view)
        game_stack.removeWidget(self)

class LoseWindow(QMainWindow):
    def __init__(self, text, score):
        super(LoseWindow, self).__init__()

        self.setStyleSheet("QLabel {font: 20pt Comic Sans MS; color: white} \
                   QPushButton {font: 10pt Comic Sans MS; background-color: white}")

        label = QLabel(text, self)
        label.setGeometry(0, 200, 710, 40)
        label.setAlignment(Qt.AlignCenter)

        self.score_label = QLabel("Score: {}".format(score), self)
        self.score_label.setGeometry(0, 260, 710, 40)
        self.score_label.setAlignment(Qt.AlignCenter)

        restart_button = QPushButton("Ещё раз!", self)
        restart_button.clicked.connect(self.restart_game)
        restart_button.setGeometry(300, 350, 120, 40)

        restart_button = QPushButton("На главную", self)
        restart_button.clicked.connect(self.on_start)
        restart_button.setGeometry(300, 400, 120, 40)

    def restart_game(self):
        graphics_view = Game()
        game_stack.addWidget(graphics_view)
        game_stack.removeWidget(self)

    def on_start(self):
        start_window = StartWindow()
        game_stack.addWidget(start_window)
        game_stack.removeWidget(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartWindow()

    game_stack = QStackedWidget()
    game_stack.setWindowTitle("Арканоид")
    game_stack.setStyleSheet("background-color: black;")
    game_stack.setFixedHeight(710)
    game_stack.setFixedWidth(710)

    game_stack.addWidget(start_window)

    game_stack.show()
    sys.exit(app.exec_())