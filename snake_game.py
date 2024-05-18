# Classic arcade-style Snake game by Kostasco

import turtle
import time
import random 

delay = 0.1 # this is in seconds

# Score
score = 0
high_score = 0

# Set up the screen
screen = turtle.Screen()
screen.title("Snake Game by @Kostas Ko")
screen.bgcolor("gray")
screen.setup(width=600, height=600)
screen.tracer(0) # turns off the screen updates

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("black")
border_pen.penup()
border_pen.setposition(-293, 290)  # Bottom-left corner of the game area
border_pen.pendown()
border_pen.pensize(3)

for _ in range(4):
    border_pen.forward(580)  
    border_pen.right(90)

border_pen.hideturtle()

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.setpos(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()

# Function to move food to a random position within the grid
def move_food():
    x = random.randint(-13, 13) * 20  
    y = random.randint(-13, 13) * 20 
    food.setpos(x, y)

move_food()

segments = []

# Scoring title
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.setpos(0, 250)
pen.write("Score: 0 High Score: 0", align="center", font=("Times", 20, "normal"))

# Functions for snake movement
def go_up():
    if head.direction != "doscreen":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "doscreen"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "doscreen":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
screen.listen()
screen.onkeypress(go_up, "w")       # "W" key
screen.onkeypress(go_up, "Up")      # Up arrow key
screen.onkeypress(go_down, "s")     # "S" key
screen.onkeypress(go_down, "Down")  # Down arrow key
screen.onkeypress(go_left, "a")     # "A" key
screen.onkeypress(go_left, "Left")  # Left arrow key
screen.onkeypress(go_right, "d")    # "D" key
screen.onkeypress(go_right, "Right") # Right arrow key

# Update the score
def update_score():
    pen.clear()
    pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Times", 20, "normal"))

# Function to close the window
def close_window():
    screen.bye()

# Function to toggle pause
paused = False
pause_count = 0

def toggle_pause():
    global paused, pause_count
    pause_count += 1
    if pause_count % 2 == 1:
        paused = True
        print("Game paused. Press Space to resume.")
    else:
        paused = False
        print("Game resumed.")

# Keyboard bindings
screen.onkeypress(toggle_pause, "space")
screen.onkeypress(close_window, "Escape")

running = True

# Main game loop
while running:
    screen.update()
    if not paused:
        # Check for a collision with the border
        if head.xcor() > 270 or head.xcor() < -270 or head.ycor() > 270 or head.ycor() < -270:
            time.sleep(1)
            head.setpos(0, 0)
            head.direction = "stop"

            # Hide the segments
            for segment in segments:
                segment.setpos(1000, 1000)

            # Clear the segments list
            segments.clear()
            
            score = 0
            delay = 0.1

            update_score()

        # Check for a collision with the food
        if head.distance(food) < 20:
            move_food()  

            # Add a segment
            new_segment = head.clone()
            new_segment.color("white")  
            segments.append(new_segment)

            # Shorten the delay
            delay -= 0.005

            # Increase the score
            score += 10

            if score > high_score:
                high_score = score
            
            update_score()

        # Move the end segments first in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].setpos(x, y)

        # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].setpos(x, y)

        move()

        # Check for head collision with the body segments
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.setpos(0 ,0)
                head.direction = "stop"

                # Hide the segments
                for segment in segments:
                    segment.setpos(1000, 1000)

                # Clear the segments list
                segments.clear()

                # Reset 
                score = 0
                delay = 0.1
                
                # Update the score display
                update_score()

        time.sleep(delay)
    else:
        running = False
