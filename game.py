import turtle
import random
import time

# Game setup
win = turtle.Screen()
win.title("Space Invaders")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Game variables
score = 0
game_over = False
alien_speed = 0.5
alien_direction = 1
move_down = False

# Player
player = turtle.Turtle()
player.speed(0)
player.shape("square")
player.color("cyan")
player.shapesize(stretch_wid=1, stretch_len=2)
player.penup()
player.goto(0, -250)

# Bullet
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.5, stretch_len=0.2)
bullet.penup()
bullet.hideturtle()
bullet.goto(0, -400)
bullet_state = "ready"

# Aliens
aliens = []
alien_rows = 3
alien_cols = 8
alien_start_x = -280
alien_start_y = 200

for row in range(alien_rows):
    for col in range(alien_cols):
        alien = turtle.Turtle()
        alien.speed(0)
        alien.shape("square")
        alien.color("lime")
        alien.shapesize(stretch_wid=1, stretch_len=1.5)
        alien.penup()
        alien.goto(alien_start_x + col * 70, alien_start_y - row * 50)
        aliens.append(alien)

# Barriers
barriers = []
barrier_positions = [-250, -100, 50, 200]

for pos in barrier_positions:
    for i in range(5):
        for j in range(3):
            barrier = turtle.Turtle()
            barrier.speed(0)
            barrier.shape("square")
            barrier.color("green")
            barrier.shapesize(stretch_wid=0.8, stretch_len=0.8)
            barrier.penup()
            barrier.goto(pos + i * 15, -150 + j * 15)
            barriers.append(barrier)

# Score display
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-380, 260)
score_pen.write(f"Score: {score}", align="left", font=("Courier", 16, "normal"))

# Game over display
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("red")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# Movement functions
def move_left():
    x = player.xcor()
    if x > -360:
        player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 360:
        player.setx(x + 20)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 20
        bullet.goto(x, y)
        bullet.showturtle()

def is_collision(t1, t2):
    distance = ((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)**0.5
    return distance < 20

# Keyboard bindings
win.listen()
win.onkey(move_left, "Left")
win.onkey(move_right, "Right")
win.onkey(fire_bullet, "space")

# Main game loop
last_alien_move = time.time()

while True:
    win.update()
    
    if game_over:
        time.sleep(0.1)
        continue
    
    # Move bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        bullet.sety(y + 5)
        
        # Check if bullet goes off screen
        if bullet.ycor() > 280:
            bullet.hideturtle()
            bullet_state = "ready"
    
    # Move aliens
    current_time = time.time()
    if current_time - last_alien_move > 0.5:
        last_alien_move = current_time
        move_down = False
        
        # Check if any alien hits the edge
        for alien in aliens:
            if alien.xcor() > 360 or alien.xcor() < -360:
                move_down = True
                alien_direction *= -1
                break
        
        # Move all aliens
        for alien in aliens:
            if move_down:
                alien.sety(alien.ycor() - 20)
            else:
                alien.setx(alien.xcor() + alien_speed * 30 * alien_direction)
            
            # Check if alien reaches player
            if alien.ycor() < -230:
                game_over = True
                game_over_pen.write("GAME OVER!", align="center", font=("Courier", 36, "bold"))
                break
            
            # Check collision with player
            if is_collision(alien, player):
                game_over = True
                game_over_pen.write("GAME OVER!", align="center", font=("Courier", 36, "bold"))
                break
    
    # Check bullet collision with aliens
    for alien in aliens[:]:
        if bullet_state == "fire" and is_collision(bullet, alien):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)
            alien.goto(1000, 1000)
            aliens.remove(alien)
            score += 10
            score_pen.clear()
            score_pen.write(f"Score: {score}", align="left", font=("Courier", 16, "normal"))
    
    # Check bullet collision with barriers
    for barrier in barriers[:]:
        if bullet_state == "fire" and is_collision(bullet, barrier):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)
            barrier.hideturtle()
            barriers.remove(barrier)
    
    # Check if all aliens are destroyed
    if len(aliens) == 0:
        game_over_pen.color("cyan")
        game_over_pen.write("YOU WIN!", align="center", font=("Courier", 36, "bold"))
        game_over = True
    
    time.sleep(0.02)

win.mainloop()