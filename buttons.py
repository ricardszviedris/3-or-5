import pygame

class Buttons:
    pygame.init()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    TEXT_COLOR = (240, 139, 61)

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 760

    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 50
    BUTTON_MARGIN = 20

    player = pygame.Rect(
        SCREEN_WIDTH // 2 - BUTTON_WIDTH - BUTTON_MARGIN // 2,
        SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
        BUTTON_WIDTH, BUTTON_HEIGHT
    )
    player_text = pygame.font.SysFont("Fixed Sys", 20).render("Player", True, TEXT_COLOR)
    player_ico = pygame.transform.scale(pygame.image.load('assets/user.png'),(50,35))

    computer = pygame.Rect(
        SCREEN_WIDTH // 2 + BUTTON_MARGIN // 2,
        SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )
    computer_text = pygame.font.SysFont("Fixed Sys", 20).render("Computer", True, TEXT_COLOR)

    button_3 = pygame.Rect(
        SCREEN_WIDTH // 2 - BUTTON_WIDTH - BUTTON_MARGIN // 2,
        SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
        BUTTON_WIDTH, BUTTON_HEIGHT
    )

    button_3_text = pygame.font.SysFont("Fixed Sys", 20).render("3", True, TEXT_COLOR)

    button_4 = pygame.Rect(
        SCREEN_WIDTH // 2 + BUTTON_MARGIN // 2,
        SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )
    button_4_text = pygame.font.SysFont("Fixed Sys", 20).render("5", True, TEXT_COLOR)

    quit = pygame.Rect(
        SCREEN_WIDTH // 2 - BUTTON_WIDTH - BUTTON_MARGIN // 2, # x koord
        (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2)+100, # y koord
        BUTTON_WIDTH, #platums
        BUTTON_HEIGHT #augstums
    )

    quit_text = pygame.font.SysFont("Fixed Sys", 20).render("Quit", True, TEXT_COLOR)

    restart = pygame.Rect(
        SCREEN_WIDTH // 2 + BUTTON_MARGIN // 2,
        (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2)+100,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
    )
    restart_text = pygame.font.SysFont("Fixed Sys", 20).render("Restart", True, TEXT_COLOR)


