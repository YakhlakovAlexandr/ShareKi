import tkinter as tk
import random


class ColorLinesGame:
    def __init__(self, root, rows, cols, cell_size, min_line_length=7):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.selected_ball = None
        self.min_line_length = min_line_length  # Минимальная длина линии для уничтожения
        self.lines_destroyed = False  # Флаг для отслеживания уничтожения линий
        self.lines_destroyed_before_move = False  # Флаг для отслеживания уничтожения линий перед ходом
        self.score = 0  # Счетчик очков
        self.score_label = tk.Label(root, text="Очки: 0")  # Метка счетчика очков
        self.score_label.pack()
        self.moves = 0  # Счетчик ходов
        self.moves_label = tk.Label(root, text="Ходы: 0")  # Метка счетчика ходов
        self.moves_label.pack()
        self.total_balls = 0  # Счетчик шаров
        self.total_balls_label = tk.Label(root, text=f"Шары: 0/{rows * cols}")  # Метка счетчика шаров
        self.total_balls_label.pack()
        self.initialize_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        self.moves = 0  # Счетчик ходов
        self.score = 0  # Счетчик очков
        self.total_balls = 0  # Счетчик шаров
        self.update_score_label()  # Обновляем метку счетчика очков
        self.update_moves_label()  # Обновляем метку счетчика ходов
        self.update_total_balls_label()  # Обновляем метку счетчика шаров

    def update_moves_label(self):
        self.moves_label.config(text=f"Ходы: {self.moves}")

    def update_score_label(self):
        self.score_label.config(text=f"Очки: {self.score}")

    def update_total_balls_label(self):
        self.total_balls_label.config(text=f"Шары: {self.total_balls}/{self.rows * self.cols}")

    def initialize_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

    def create_ball(self, row, col, color):
        if self.grid[row][col]:
            return  # Если на клетке уже есть шар, не создавать новый
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        ball_radius = self.cell_size // 2 - 5
        ball = Ball(self.canvas, self, row, col, x, y, ball_radius, color)
        self.grid[row][col] = ball

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected_ball is None:
            ball = self.grid[row][col]
            if ball:
                ball.select()
                self.selected_ball = ball
        else:
            target_row, target_col = row, col
            if self.is_valid_move(self.selected_ball, target_row, target_col):
                self.selected_ball.move_to(target_row, target_col)
                self.selected_ball.deselect()
                self.selected_ball = None
                self.lines_destroyed_before_move = self.lines_destroyed
                self.remove_matching_lines()
                # Обновляем счетчик ходов после каждого хода
                self.moves += 1
                self.update_moves_label()
                # После уничтожения линий проверяем, были ли они уничтожены перед ходом и добавляем шары
                if not self.lines_destroyed_before_move:
                    self.add_new_balls(3)

    def is_valid_move(self, ball, target_row, target_col):
        if not self.is_within_grid(target_row, target_col):
            return False

        if self.grid[target_row][target_col]:
            return False

        return self.has_clear_path(ball.row, ball.col, target_row, target_col)

    def is_within_grid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def has_clear_path(self, start_row, start_col, target_row, target_col):
        return True

    def add_new_balls(self, count):
        for _ in range(count):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                if not self.grid[row][col]:
                    color = random.choice(["red", "green", "blue", "yellow"])
                    self.create_ball(row, col, color)
                    self.total_balls += 1  # Обновляем счетчик шаров
                    self.update_total_balls_label()  # Обновляем метку счетчика шаров
                    break


    def remove_matching_lines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]:
                    color = self.grid[row][col].color
                    if self.check_line(row, col, 1, 0, color) or \
                       self.check_line(row, col, 0, 1, color) or \
                       self.check_line(row, col, 1, 1, color) or \
                       self.check_line(row, col, 1, -1, color):
                        self.remove_line(row, col, 1, 0, color)
                        self.remove_line(row, col, 0, 1, color)
                        self.remove_line(row, col, 1, 1, color)
                        self.remove_line(row, col, 1, -1, color)
                        self.lines_destroyed = True  # Установим флаг, если линии уничтожены
                    else:
                        self.lines_destroyed = False  # Сбрасываем флаг, если линии не уничтожены


    def check_line(self, row, col, dr, dc, color):
        count = 0
        while self.is_within_grid(row, col) and self.grid[row][col] and self.grid[row][col].color == color:
            count += 1
            row += dr
            col += dc
        return count >= self.min_line_length

    def remove_line(self, row, col, dr, dc, color):
        removed_balls = []
        while self.is_within_grid(row, col) and self.grid[row][col] and self.grid[row][col].color == color:
            removed_balls.append((row, col))
            row += dr
            col += dc

        if len(removed_balls) >= self.min_line_length and all(self.grid[row][col] for row, col in removed_balls):
            for row, col in removed_balls:
                self.canvas.delete(self.grid[row][col].id)
                self.total_balls -= 1  # Обновляем счетчик шаров при уничтожении
                self.update_total_balls_label()  # Обновляем метку счетчика шаров
                self.score += 1  # Обновляем счетчик очков при уничтожении шара
                self.update_score_label()  # Обновляем метку счетчика очков
class Ball:
    def __init__(self, canvas, game, row, col, x, y, radius, color):
        self.canvas = canvas
        self.game = game
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.id = canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline="black"
        )

    def select(self):
        self.canvas.itemconfig(self.id, outline="white", width=2)

    def deselect(self):
        self.canvas.itemconfig(self.id, outline="black", width=1)

    def move_to(self, row, col):
        if not self.game.is_within_grid(row, col):
            return

        target_x = col * self.game.cell_size + self.game.cell_size // 2
        target_y = row * self.game.cell_size + self.game.cell_size // 2
        self.canvas.move(self.id, target_x - self.x, target_y - self.y)
        self.x = target_x
        self.y = target_y
        self.game.grid[self.row][self.col] = None
        self.game.grid[row][col] = self
        self.row = row
        self.col = col


def main():
    rows, cols = 7, 7
    cell_size = 50
    root = tk.Tk()
    root.title("Color Lines")

    game = ColorLinesGame(root, rows, cols, cell_size)

    for _ in range(3):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        color = random.choice(["red", "green", "blue", "yellow"])
        game.create_ball(row, col, color)

    root.mainloop()


if __name__ == "__main__":
    main()