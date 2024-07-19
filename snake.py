import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter  # Add this import statement

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        
        self.window_width = 800
        self.window_height = 600
        self.square_size = 20
        self.snake = [(20, 20)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.score = 0
        self.game_over = False
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Snake Game')
        self.setGeometry(100, 100, self.window_width, self.window_height)      
        
        self.score_label = QLabel(f'Score: {self.score}', self)
        self.score_label.setAlignment(Qt.AlignTop)
        self.score_label.setStyleSheet("font-size: 24px; color: red;")
        
        self.game_over_label = QLabel('Game Over', self)
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.setStyleSheet("font-size: 24px; color: red;")
        self.game_over_label.setVisible(False)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.game_over_label)
        self.setLayout(self.layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(100)
        
        self.show()
        
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.fillRect(self.rect(), Qt.black)
        self.draw_snake(qp)
        self.draw_food(qp)
        
    def draw_snake(self, painter):
        painter.setBrush(Qt.yellow)
        for segment in self.snake:
            painter.drawEllipse(segment[0], segment[1], self.square_size, self.square_size)
    
    def draw_food(self, painter):
        painter.setBrush(Qt.red)
        painter.drawRect(self.food[0], self.food[1], self.square_size, self.square_size)
    
    def move_snake(self):
        if not self.game_over:
            head = self.snake[0]
            if self.direction == 'Right':
                new_head = (head[0] + self.square_size, head[1])
            elif self.direction == 'Left':
                new_head = (head[0] - self.square_size, head[1])
            elif self.direction == 'Up':
                new_head = (head[0], head[1] - self.square_size)
            elif self.direction == 'Down':
                new_head = (head[0], head[1] + self.square_size)
            
            if new_head in self.snake or not (0 <= new_head[0] < self.window_width) or not (0 <= new_head[1] < self.window_height):
                self.game_over = True
                self.timer.stop()
                self.game_over_label.setVisible(True)
            else:
                self.snake.insert(0, new_head)
                if new_head == self.food:
                    self.score += 10
                    self.score_label.setText(f'Score: {self.score}')
                    self.food = self.create_food()
                else:
                    self.snake.pop()
                self.update()
    
    def create_food(self):
        while True:
            x = random.randint(0, (self.window_width - self.square_size) // self.square_size) * self.square_size
            y = random.randint(0, (self.window_height - self.square_size) // self.square_size) * self.square_size
            if (x, y) not in self.snake:
                return (x, y)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left and self.direction != 'Right':
            self.direction = 'Left'
        elif event.key() == Qt.Key_Right and self.direction != 'Left':
            self.direction = 'Right'
        elif event.key() == Qt.Key_Up and self.direction != 'Down':
            self.direction = 'Up'
        elif event.key() == Qt.Key_Down and self.direction != 'Up':
            self.direction = 'Down'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    sys.exit(app.exec_())
