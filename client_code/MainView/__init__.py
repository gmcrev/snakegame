from ._anvil_designer import MainViewTemplate
from anvil import *
from anvil.js.window import document
import random

class MainView(MainViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Any code you write here will run before the form opens.
        #self.canvas_1.width = 500
        #self.canvas_1.height = 500

        self.block_size = 25
        self.rows = 20
        self.cols = 20
        #self.board = None
        self.context = None
        self.snake_x = self.block_size * 5
        self.snake_y = self.block_size * 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.snake_body = []
        self.food_x = None
        self.food_y = None
        self.game_over = False
        self.score = 0

        self.label_score.text = f"Your score is: {self.score}"

    def canvas_1_show(self, **event_args):
        #self.canvas_1.width = self.rows * self.block_size
        #self.canvas_1.height = self.cols * self.block_size
        #self.context = self.canvas_1
        #print(anvil.js.window.document)
        self.place_food()
        document.addEventListener("keyup", self.change_direction)

    def timer_forever_tick(self, **event_args):
        self.update()

    def update(self):
        if self.game_over:
            return

        c = self.canvas_1
        #board
        c.fill_style = "darkblue"
        c.fill_rect(0, 0, c.get_width(), c.get_height())

        #food
        c.fill_style = "red"
        c.fill_rect(self.food_x, self.food_y, self.block_size, self.block_size)

        #check if snake eats food
        if self.snake_x == self.food_x and self.snake_y == self.food_y:
            self.snake_body.append([self.food_x, self.food_y])
            self.score += 1
            self.label_score.text = f"Your score is: {self.score}"
            self.place_food()
            print("food eaten")
        
        for i, elem in reversed(list(enumerate(self.snake_body))):
            self.snake_body[i] = self.snake_body[i-1]
            
        if len(self.snake_body):
            #current pos of snake head
            self.snake_body[0] = [self.snake_x, self.snake_y]
            
        #snake
        c.fill_style = "lime"
        self.snake_x += self.velocity_x * self.block_size
        self.snake_y += self.velocity_y * self.block_size
        c.fill_rect(self.snake_x, self.snake_y, self.block_size, self.block_size)

        #make snake body follow the snake head
        for i, elem in enumerate(self.snake_body):
            print(i, elem)
            c.fill_rect(self.snake_body[i][0], self.snake_body[i][1], self.block_size, self.block_size)

        #check if snake head touches the edges
        if self.snake_x < 0 or self.snake_x > self.cols*self.block_size or self.snake_y < 0 or self.snake_y > self.rows*self.block_size:
            self.game_over = True
            alert("game over! refresh page to try again")

        #check if snake head touches the snake body
        for i, elem in enumerate(self.snake_body):
            if self.snake_x == self.snake_body[i][0] and self.snake_y == self.snake_body[i][1]:
                self.game_over = True
                alert("game over! refresh page to try again")

    #helper methods

    def place_food(self):
        self.food_x = random.randint(0, self.cols - 1) * self.block_size
        self.food_y = random.randint(0, self.rows - 1) * self.block_size
        print(self.food_x, self.food_y)
    
    def change_direction(self, e, **event_args):
        #print(e) #KeyboardEvent proxyobject

        if e.code == "ArrowUp" and self.velocity_y != 1:
            self.velocity_x = 0
            self.velocity_y = -1
            print("up pressed")
        elif e.code == "ArrowDown" and self.velocity_y != -1:
            self.velocity_x = 0
            self.velocity_y = 1
            print("down pressed")
        elif e.code == "ArrowLeft" and self.velocity_x != 1:
            self.velocity_x = -1
            self.velocity_y = 0
            print("left pressed")
        elif e.code == "ArrowRight" and self.velocity_x != -1:
            self.velocity_x = 1
            self.velocity_y = 0
            print("right pressed")