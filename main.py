import pygame
from buttons import Buttons
from constants import WHITE, RED, BACKGROUND,TEXT_COLOR, BUTTON_COLOR,\
                      BUTTON_PRESSED_COLOR, BACKGROUND_2, SCREEN_WIDTH, \
                      SCREEN_HEIGHT,FONT_SMALL, FONT_MEDIUM, FONT_LARGE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the display
pygame.display.set_caption("Add 3 or 5")  # Title
isMaximizing = None


def drawText(text, font, color, x, y):  # Funkcija ļauj vienkārši uz ekrāna izvadīt tekstu
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def drawBoard(number):  # Spēles lauka izveidošana
    screen.fill(BACKGROUND)
    screen.fill(BACKGROUND_2, rect=(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT))
    drawText("Add 3 or 5", FONT_LARGE, TEXT_COLOR, SCREEN_WIDTH // 2, 50)
    drawText("Current number: {}".format(number), FONT_MEDIUM, TEXT_COLOR, SCREEN_WIDTH // 2, 150)


def chooseStarter():
    global isMaximizing
    pygame.draw.rect(screen, BUTTON_COLOR, Buttons.player)  # player poga
    screen.blit(Buttons.player_text, Buttons.player.midleft)

    pygame.draw.rect(screen, BUTTON_COLOR, Buttons.computer)  # computer poga
    screen.blit(Buttons.computer_text, Buttons.computer.midleft)

    drawText("Who starts first?", FONT_LARGE, TEXT_COLOR, SCREEN_WIDTH // 2, 50)
    pygame.display.update()  # Spēles loga atsvaidzināšana

    starter = None  # inicializēts tukšs mainīgais
    while starter not in (1, 2):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Iespēja iziet no spēles spiežot "Q" uz tastatūras
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Ja tiek nospiesta kreisā peles poga, tad ....
                if Buttons.player.collidepoint(event.pos):  # Ja peles kursors atradās uz pogas brīdī, kad
                    pygame.draw.rect(screen, BUTTON_PRESSED_COLOR, Buttons.player)  # tika nospiesta kreisā peles poga
                    screen.blit(Buttons.player_text, Buttons.player.center)
                    pygame.display.update()
                    pygame.time.delay(500)
                    starter = 1  # Spēli sāk lietotājs
                    isMaximizing = True
                elif Buttons.computer.collidepoint(event.pos):
                    pygame.draw.rect(screen, BUTTON_PRESSED_COLOR, Buttons.computer)
                    screen.blit(Buttons.computer_text, Buttons.computer.midleft)
                    pygame.display.update()
                    pygame.time.delay(500)
                    isMaximizing = False
                    starter = 2  # Spēli sāk dators

    if starter == 1: return True
    else: return False


def getPlayerMove():  # Atkarībā no nospiestās pogas tiek iegūta lietotāja gājiena vērtība
    player_move = None
    while player_move not in (3, 5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Buttons.button_3.collidepoint(event.pos):
                    pygame.draw.rect(screen, BUTTON_PRESSED_COLOR, Buttons.button_3)
                    screen.blit(Buttons.button_3_text, Buttons.button_3.center)
                    pygame.display.update()
                    pygame.time.delay(500)
                    player_move = 3
                elif Buttons.button_4.collidepoint(event.pos):
                    pygame.draw.rect(screen, BUTTON_PRESSED_COLOR, Buttons.button_4)
                    screen.blit(Buttons.button_4_text, Buttons.button_4.center)
                    pygame.display.update()
                    pygame.time.delay(500)
                    player_move = 5

    return player_move


def alphaBeta(pos, depth, alpha, beta, isMaximizing):
    if depth == 0 or pos is None or pos == 43: return pos

    if isMaximizing:  # isMaximizing ir boolean tipa mainīgais, kurš norāda vai dators maksimizē vai minimizē
        maxEval = -float('inf')
        for i in (3, 5):    #Abas iespējamās kustības
            if pos + i <= 43:   #Pārbauda, vai spēle ir beigusies
                eval = alphaBeta(pos + i, depth - 1, alpha, beta, False)  # Funkcija rekursīvi izsauc sevi katrā datora
                maxEval = max(maxEval, eval)                             # gājienā
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = float('inf') #minimizē
        for i in (3, 5):
            if pos + i <= 43:
                eval = alphaBeta(pos + i, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval

def getComputerMove(number):
    global isMaximizing
    bestMove = None
    bestVal = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for i in (3, 5):
        if number + i <= 43:
            val = alphaBeta(number + i, 3, alpha, beta, isMaximizing)
            if val > bestVal:
                bestVal = val
                bestMove = i
            alpha = max(alpha, val)

    if bestMove is None:
        return 3
    else:
        return bestMove


def drawTurnText(playerTurn):  # Funkcija izvada uz ekrāna tekstu, kurš norāda šībrīža gājiena veicēju
    if playerTurn: turn_text = "Player's Turn"
    else: turn_text = "Computer's Turn"
    drawText(turn_text, FONT_MEDIUM, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)


def engine():  # Galvenais spēles cikls
    pygame.init()
    screen.fill(BACKGROUND)
    number = 3  # Spēles sākuma vērtība
    player_turn = chooseStarter()  # Tiek izsaukta funkcija, kas nosaka kurš spēles dalībnieks veiks pirmo gājienu
    game_over = False
    history = []  # Saraksts, kurā tiek glabāta gājienu vēsture
    drawText("Player starts" if player_turn else "Computer starts", FONT_LARGE, TEXT_COLOR, SCREEN_WIDTH // 2, 500)
    pygame.display.update()
    pygame.time.wait(1500)  # Ik pa laikam tiek pielietota time.wait() funkcija, lai spēle šķistu plūstošāka

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Iespēja lietotājam ar "Q" taustiņa palīdzību uzreiz iziet no spēles
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

        drawBoard(number)
        drawTurnText(player_turn)
        drawText("Player's turn" if player_turn else "Computer's turn", FONT_SMALL, TEXT_COLOR, SCREEN_WIDTH // 2, 200)

        pygame.draw.rect(screen, BUTTON_COLOR, Buttons.button_3)
        screen.blit(Buttons.button_3_text, Buttons.button_3.center)
        pygame.draw.rect(screen, BUTTON_COLOR, Buttons.button_4)
        screen.blit(Buttons.button_4_text, Buttons.button_4.center)

        drawText("History:", FONT_MEDIUM, TEXT_COLOR, 200, 150)  # Vēsture tiek izvadīta uz ekrāna
        for i, move in enumerate(history):
            drawText(move, FONT_SMALL, TEXT_COLOR, 200, 190 + 30 * i)
        pygame.display.update()

        if player_turn:
            player_move = getPlayerMove()
            number += player_move
            history.append(f"Player added {player_move}.")
            if number == 43:        # Ja ir spēlētāja gājiens, un tiek sasniegts cipars 43, tad spēle ir beigusies
                drawBoard(number)   # un lietotājs ir uzvarējis
                drawText("Player wins!", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.display.update()
                pygame.time.delay(1500)
                game_over = True
            elif number > 43:       # Ja ir spēlētāja gājiens, un tiek sasniegts cipars > 43, tad spēle ir beigusies
                drawBoard(number)   # un dators ir uzvarējis
                drawText("Computer wins!", FONT_LARGE, RED, SCREEN_WIDTH // 2, 350)
                pygame.display.update()
                pygame.time.delay(1500)
                game_over = True
        else:
            player_move = getComputerMove(number)
            pygame.time.delay(500)
            number += player_move
            history.append(f"Computer added {player_move}.")
            if number == 43:  # Tas pats, kas iepriekšējā if statement
                drawBoard(number)
                drawText("Computer wins!", FONT_LARGE, RED, SCREEN_WIDTH // 2, 350)
                pygame.display.update()
                pygame.time.delay(1500)
                game_over = True
            elif number > 43:
                drawBoard(number)
                drawText("Player wins!", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                pygame.display.update()
                pygame.time.delay(1500)
                game_over = True

        player_turn = not player_turn

    while True:
        drawText("History:", FONT_MEDIUM, TEXT_COLOR, 200, 150)  # Vēsture tiek izvadīta uz ekrāna
        for i, move in enumerate(history):
            drawText(move, FONT_SMALL, TEXT_COLOR, 200, 190 + 30 * i)

        pygame.draw.rect(screen, BUTTON_COLOR, Buttons.quit)  # quit poga
        screen.blit(Buttons.quit_text, Buttons.quit.midleft)

        pygame.draw.rect(screen, BUTTON_COLOR, Buttons.restart)  # restart poga
        screen.blit(Buttons.restart_text, Buttons.restart.midleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Buttons.restart.collidepoint(event.pos):
                    pygame.draw.rect(screen, BUTTON_PRESSED_COLOR, Buttons.restart)
                    screen.blit(Buttons.restart_text, Buttons.restart.midleft)  # ja nospiež pogu, tad poga uz brīdi
                    pygame.display.update()  # iedegas zaļa, un spēle sākas no sākuma
                    pygame.time.delay(500)
                    engine()  # spēles cikls sākas no sākuma
                elif Buttons.quit.collidepoint(event.pos):
                    pygame.draw.rect(screen, BUTTON_PRESSED_COLOR, Buttons.quit)  # ja nospiež pogu, tad poga uz brīdi
                    screen.blit(Buttons.quit_text, Buttons.quit.midleft)  # iedegas zaļa, un spēle tiek aizvērta
                    pygame.display.update()
                    pygame.time.delay(500)
                    screen.fill(BACKGROUND)
                    drawText("Thank You for playing!", FONT_LARGE, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

engine()
