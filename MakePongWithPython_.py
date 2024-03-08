# Import the pygame module to use its functions and classes for game development.
import pygame

# Initialize all imported pygame modules.
pygame.init()

# Set the width and height of the game window.
WIDTH, HEIGHT = 700, 400

# Create the game window with the specified width and height.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the game window.
pygame.display.set_caption("Pong")

# Set the game's frame rate.
FPS = 60

# Define color constants for easy reference.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set the paddle dimensions.
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

# Set the radius for the ball.
BALL_RADIUS = 7

# Create a font object for displaying scores.
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# Define the score needed to win the game.
WINNING_SCORE = 10

# Define the Paddle class to represent the player's paddles in the game.
class Paddle:
    COLOR = WHITE  # Set the paddle color.
    VEL = 8  # Set the paddle's velocity or speed of movement.
    
    def __init__(self, x, y, width, height):
        # Initialize a new paddle object with its position, dimensions, and original position.
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        # Draw the paddle on the window.
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        # Move the paddle up or down based on the boolean argument 'up'.
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset(self):
        # Reset the paddle to its original position.
        self.x = self.original_x
        self.y = self.original_y
        
# Define the Ball class to represent the game ball.
class Ball:
    MAX_VEL = 5  # Set the maximum velocity for the ball.
    COLOR = WHITE  # Set the ball's color.
    
    def __init__(self, x, y, radius):
        # Initialize a new ball object with its position, radius, and velocities.
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        
    def draw(self, win):
        # Draw the ball on the window.
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        # Move the ball by adding its velocities to its position.
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        # Reset the ball to its original position and reverse its horizontal velocity.
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

# Define a function to draw all game elements on the window.
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)  # Fill the game window with black.
    
    # Render the score texts for the left and right players.
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    
    # Position the score texts on the window.
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    # Draw each paddle in the paddles list.
    for paddle in paddles:
        paddle.draw(win)
        
    # Draw the center dividing line.
    for i in range(10, HEIGHT, HEIGHT//10):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    
    # Draw the ball.
    ball.draw(win)
    
    # Update the display.
    pygame.display.update()

# Define a function to handle ball collisions with walls and paddles.
def handle_collision(ball, left_paddle, right_paddle):
    # Invert the ball's vertical velocity if it hits the top or bottom of the window.
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1
        
    # Handle ball collisions with the left paddle.
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1  # Invert the ball's horizontal velocity.
                
                # Calculate the ball's new vertical velocity based on where it hit the paddle.
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        # Handle ball collisions with the right paddle similarly.
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

# Define a function to handle paddle movements based on keyboard input.
def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Move the left paddle up or down based on W and S key presses.
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
        
    # Move the right paddle up or down based on UP and DOWN arrow key presses.
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

# Define the main function to run the game loop.
def main():
    run = True
    clock = pygame.time.Clock()
    
    # Initialize paddles and the ball.
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # Initialize scores for both players.
    left_score = 0
    right_score = 0
    
    # Game loop.
    while run:
        clock.tick(FPS)  # Ensure the game runs at the specified FPS.
        
        # Draw game elements on the window.
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        # Check for game close event.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        # Handle paddle movements based on current key presses.
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        
        # Move the ball and handle collisions.
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Update scores and reset the ball if it goes past the left or right edge.
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Check for a winning score and display the winning message.
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
            
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)  # Pause for 5 seconds before resetting.
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()  # Quit the game when the loop ends.

# Call the main function to start the game.
main()
