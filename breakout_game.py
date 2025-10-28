from turtle import Screen, Turtle
import time

# Setup screen
screen = Screen()
screen.title("Breakout Game by Jiya")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Paddle
paddle = Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -200)
ball.dx = 4
ball.dy = 4

# Bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]

y_start = 250
for color in colors:
    for x in range(-350, 400, 70):
        brick = Turtle()
        brick.shape("square")
        brick.color(color)
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.penup()
        brick.goto(x, y_start)
        bricks.append(brick)
    y_start -= 30

# Score
score = 0
score_display = Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-360, 260)
score_display.write(f"Score: {score}", align="left", font=("Courier", 16, "normal"))

# Paddle movement
def paddle_right():
    x = paddle.xcor()
    if x < 340:
        paddle.setx(x + 40)

def paddle_left():
    x = paddle.xcor()
    if x > -340:
        paddle.setx(x - 40)

screen.listen()
screen.onkeypress(paddle_right, "Right")
screen.onkeypress(paddle_left, "Left")

# Game loop
game_on = True
while game_on:
    time.sleep(0.02)
    screen.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Wall collision
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.dx *= -1

    if ball.ycor() > 280:
        ball.dy *= -1

    # Paddle collision
    if (ball.ycor() < -230 and paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
        ball.dy *= -1

    # Missed ball
    if ball.ycor() < -280:
        score_display.goto(0, 0)
        score_display.write("GAME OVER", align="center", font=("Courier", 24, "bold"))
        game_on = False

    # Brick collision
    for brick in bricks:
        if brick.isvisible() and (ball.distance(brick) < 35):
            ball.dy *= -1
            brick.hideturtle()
            bricks.remove(brick)
            score += 10
            score_display.clear()
            score_display.goto(-360, 260)
            score_display.write(f"Score: {score}", align="left", font=("Courier", 16, "normal"))

    # Win condition
    if len(bricks) == 0:
        score_display.goto(0, 0)
        score_display.write("YOU WIN!", align="center", font=("Courier", 24, "bold"))
        game_on = False

screen.mainloop()
