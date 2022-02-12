import pygame
import random
import tkinter as tk
from tkinter import messagebox
from win32api import GetSystemMetrics

root = tk.Tk()
root.withdraw()

pygame.init()


class Grid:
    boxes = []
    ships = []

    def __init__(self, screen):
        self.screen = screen
        self.boxes.clear()
        self.ships.clear()
        size = (self.screen.get_width() - self.screen.get_height()) / 10
        column = int(self.screen.get_width() / 2.5)
        for x in range(0, column, int(size)):
            row = 10
            for y in range(0, self.screen.get_height(), int(size)):
                if row > 0:
                    rect = pygame.Rect(x + (self.screen.get_width() / 4), y + (self.screen.get_height() / 10),
                                       size, size)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)
                    self.boxes.append(rect)
                    row = row - 1
        pygame.display.flip()
        self.ships.append(random.choice(self.boxes))


class Game:
    lives = 10

    def __init__(self):
        pygame.display.set_caption("Naval War", "Powered by @Nyrok10 on Twitter.")
        self.screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.RESIZABLE)
        background = pygame.image.load('assets/background.png')
        self.screen.blit(background, (0, 0))
        self.start = True
        Grid(self.screen)
        pygame.display.flip()

    def launch(self):
        messagebox.showinfo("Naval War",
                            "The goal is to find the ships hidden, you have {} lives\nGood luck !".format(self.lives))
        while self.start and self.lives > 0:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    for rectangle in Grid.boxes:
                        if rectangle.collidepoint(event.pos):
                            if rectangle.colliderect(Grid.ships[0]):
                                won = pygame.image.load("assets/won.png").convert_alpha()
                                won = pygame.transform.scale(won, (rectangle.width, rectangle.height))
                                self.screen.blit(won, (rectangle.topleft, rectangle.bottomright))
                                pygame.display.flip()
                                messagebox.showinfo("Naval War", "Won in {} lives".format(self.lives))
                                self.lives = 0
                            elif Grid.ships[0].contains(rectangle.left, Grid.ships[0].top, rectangle.width,
                                                        rectangle.height) \
                                    or Grid.ships[0].contains(Grid.ships[0].left, rectangle.top, rectangle.width,
                                                              rectangle.height):
                                seeing = pygame.image.load("assets/seeing.png").convert_alpha()
                                seeing = pygame.transform.scale(seeing, (rectangle.width, rectangle.height))
                                self.screen.blit(seeing, (rectangle.topleft, rectangle.bottomright))
                                pygame.display.flip()
                                Grid.boxes.remove(rectangle)
                                self.lives = self.lives - 1
                                messagebox.showinfo("Naval War", "Seeing, {} lives left.".format(self.lives))
                            else:
                                lost = pygame.image.load("assets/lost.png").convert_alpha()
                                lost = pygame.transform.scale(lost, (rectangle.width, rectangle.height))
                                self.screen.blit(lost, (rectangle.topleft, rectangle.bottomright))
                                pygame.display.flip()
                                Grid.boxes.remove(rectangle)
                                self.lives = self.lives - 1
                                messagebox.showinfo("Naval War", "Lost, {} lives left.".format(self.lives))
                elif event.type == pygame.QUIT:
                    self.start = False
                    pygame.quit()

        if self.lives == 0 and self.start:
            Game().launch() if messagebox.askyesno("Naval War", "Do you want to play again ?") else pygame.quit()


if __name__ == "__main__":
    Game().launch()
