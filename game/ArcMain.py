import json
import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
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
        end_window = EndGameWindow(text, self.score)
        game_stack.addWidget(end_window)
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

        score_button = QPushButton("Рекорды", self)
        score_button.setGeometry(300, 400, 120, 40)
        score_button.clicked.connect(self.score_window)

    def start_game(self):
        graphics_view = Game()
        game_stack.addWidget(graphics_view)
        game_stack.removeWidget(self)

    def score_window(self):
        score_window = ScoresWidget()
        game_stack.addWidget(score_window)
        game_stack.removeWidget(self)

class EndGameWindow(QMainWindow):
    def __init__(self, text, score):
        super(EndGameWindow, self).__init__()

        self.setStyleSheet("QLabel {font: 20pt Comic Sans MS; color: white} \
            QPushButton {font: 10pt Comic Sans MS; background-color: white} \
            QLineEdit {font: 10pt Comic Sans MS; color: white}")
        
        self.score = score

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

        self.player_name_input = QLineEdit("Aaa", self)
        self.player_name_input.setGeometry(300, 500, 120, 40)

        score_button = QPushButton("Add score", self)
        score_button.clicked.connect(self.score_window)
        score_button.setGeometry(300, 550, 120, 40)

    def restart_game(self):
        graphics_view = Game()
        game_stack.addWidget(graphics_view)
        game_stack.removeWidget(self)

    def on_start(self):
        start_window = StartWindow()
        game_stack.addWidget(start_window)
        game_stack.removeWidget(self)

    def score_window(self):
        score_window = ScoresWidget(self.player_name_input.text(), self.score)
        game_stack.addWidget(score_window)
        game_stack.removeWidget(self)

class ScoresWidget(QWidget):
    def __init__(self, name = '-', score = -1):
        super(ScoresWidget, self).__init__()

        self.setStyleSheet("QPushButton {font: 10pt Comic Sans MS; background-color: white} \
            QTableWidget {font: 10pt Comic Sans MS; background-color: black; color: white} \
            QHeaderView {font: 10pt Comic Sans MS; black; color: white} \
            QHeaderView::section {background-color:black}")

        self.high_scores_table = QTableWidget()
        self.high_scores_table.setColumnCount(2)
        self.high_scores_table.setHorizontalHeaderLabels(["Игрок", "Очки"])

        self.load_high_scores()

        if score != -1:
            self.add_score(name, score)

        self.add_score_button = QPushButton("На главную")
        self.add_score_button.clicked.connect(self.on_start)
        self.clear_score_button = QPushButton("Очистить")
        self.clear_score_button.clicked.connect(self.clear_score)

        layout = QVBoxLayout()
        layout.addWidget(self.high_scores_table)
        layout.addWidget(self.add_score_button)
        layout.addWidget(self.clear_score_button)
        self.setLayout(layout)

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as file:
                data = json.load(file)
                self.fill_high_scores(data)
        except FileNotFoundError:
            self.fill_high_scores([])

    def save_high_scores(self):
        data = []
        for row in range(self.high_scores_table.rowCount()):
            player = self.high_scores_table.item(row, 0).text()
            score = int(self.high_scores_table.item(row, 1).text())
            data.append({"Player": player, "Score": score})

        data.sort(key=lambda x: x["Score"], reverse = True)

        with open("high_scores.json", 'w') as file:
            json.dump(data, file)

    def fill_high_scores(self, data):
        for row, entry in enumerate(data):
            player = entry["Player"]
            score = entry["Score"]

            self.high_scores_table.insertRow(row)
            self.high_scores_table.setItem(row, 0, QTableWidgetItem(player))
            self.high_scores_table.setItem(row, 1, QTableWidgetItem(str(score)))

    def add_score(self, name, score):
        row_position = self.high_scores_table.rowCount()
        self.high_scores_table.insertRow(row_position)
        self.high_scores_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.high_scores_table.setItem(row_position, 1, QTableWidgetItem(str(score)))
        self.save_high_scores()

        self.update()

    def clear_score(self):
        with open("high_scores.json", 'w') as файл:
            json.dump({}, файл)
        self.high_scores_table.clear()

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