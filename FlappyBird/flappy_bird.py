import pygame
import random
import time

pygame.init()
font = pygame.font.Font('SHOWG.TTF', 48)

# Window settings
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('bird_mid.png')
pygame.display.set_icon(icon)

# Images
bird_images = [
    pygame.image.load('bird_down.png'),
    pygame.image.load('bird_mid.png'),
    pygame.image.load('bird_up.png'),
]
skyline_image = pygame.image.load('background.png')
ground_image = pygame.image.load('ground.png')
top_pipe_image = pygame.image.load('pipe_top.png')
bottom_pipe_image = pygame.image.load('pipe_bottom.png')
game_over_image = pygame.image.load('game_over.png')
start_image = pygame.image.load('start.png')

# Background and ground movement variables
bgX = 0
bgX_change = 0.5
groundX = 0
groundX_change = 2

# Bird and pipe variables
bird_frame = 0
frame_count = 0
birdY = 275
bird_velocity = 0
gravity = 0.5

pipe_width = bottom_pipe_image.get_width()
pipe_positions = [600, 800, 1000]
pipe_heights = [random.randint(250, 375) for _ in pipe_positions]
passed_pipes = [False, False, False]
gap = 150
score = 0

# Game state variables
run = True
game_over = False
game_started = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                game_started = True

            if game_started and not game_over:
                if event.key == pygame.K_SPACE:
                    bird_velocity = -8

            if game_over and event.key == pygame.K_r:
                # Restart game state
                birdY = 275
                bird_velocity = 0
                pipe_positions = [600, 800, 1000]
                pipe_heights = [random.randint(250, 375) for _ in pipe_positions]
                frame_count = 0
                bird_frame = 0
                game_over = False
                game_started = False
                score = 0
                passed_pipes = [False, False, False]

    if not game_started:
        # Start screen
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, (0, 525))
        x = (win_width - start_image.get_width()) // 2
        y = (win_height - start_image.get_height()) // 2
        window.blit(start_image, (x, y))

    elif not game_over:
        # Apply gravity to bird
        bird_velocity += gravity
        birdY += bird_velocity

        # Move background and ground
        bgX -= bgX_change
        if bgX <= -win_width:
            bgX = 0

        groundX -= groundX_change
        if groundX <= -win_width:
            groundX = 0

        # Move pipes
        for i in range(len(pipe_positions)):
            pipe_positions[i] -= groundX_change
            if pipe_positions[i] <= -pipe_width:
                pipe_positions[i] = win_width + random.randint(100, 250)
                pipe_heights[i] = random.randint(250, 375)
                passed_pipes[i] = False

        # Update score when bird passes a pipe
        for i in range(len(pipe_positions)):
            if pipe_positions[i] + pipe_width < 260 and not passed_pipes[i]:
                score += 1
                passed_pipes[i] = True

        # Drawing background, pipes, ground
        window.fill((0, 0, 0))
        window.blit(skyline_image, (bgX, 0))
        window.blit(skyline_image, (bgX + win_width, 0))

        for i in range(len(pipe_positions)):
            window.blit(bottom_pipe_image, (pipe_positions[i], pipe_heights[i]))
            top_y = pipe_heights[i] - gap - top_pipe_image.get_height()
            window.blit(top_pipe_image, (pipe_positions[i], top_y))

        window.blit(ground_image, (groundX, 525))
        window.blit(ground_image, (groundX + win_width, 525))

        # Bird animation
        frame_count += 1
        if frame_count % 5 == 0:
            bird_frame = (bird_frame + 1) % 3

        window.blit(bird_images[bird_frame], (260, birdY))

        # Collision detection
        bird_rect = bird_images[bird_frame].get_rect(topleft=(260, birdY)).inflate(-10, -10)
        for i in range(len(pipe_positions)):
            bottom_pipe_rect = bottom_pipe_image.get_rect(topleft=(pipe_positions[i], pipe_heights[i]))
            top_pipe_rect = top_pipe_image.get_rect(
                topleft=(pipe_positions[i], pipe_heights[i] - gap - top_pipe_image.get_height()))

            if bird_rect.colliderect(bottom_pipe_rect) or bird_rect.colliderect(top_pipe_rect):
                game_over = True
                time.sleep(0.5)
                break

        if birdY > 525 - bird_images[bird_frame].get_height() or birdY < 0:
            game_over = True
            time.sleep(0.5)

        # Draw score at the very end (on top of everything)
        score_text = font.render(str(score), True, (255, 255, 255))
        window.blit(score_text, (win_width // 2, 50))

    else:
        # Game over screen
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, (0, 525))
        x = (win_width - game_over_image.get_width()) // 2
        y = (win_height - game_over_image.get_height()) // 2
        window.blit(game_over_image, (x, y))

    pygame.display.update()
