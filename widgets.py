"""

File for the base widget classes that form the UI system.

Originally used in my A level chess project, imported for this challenge.

"""


import sys
from abc import abstractmethod, ABCMeta

import pygame


pygame.font.init()


class __Widget(metaclass=ABCMeta):
    def __init__(self, x, y, l, w):
        """

        :type x: int
        :type y: int
        :type l: int
        :type w: int

        """
        self.startX = x
        self.startY = y
        self.endX = x + l
        self.endY = y + w
        self.length = l
        self.width = w

    @abstractmethod
    def draw(self, screen):
        pass

    def isPressed(self):
        """

        A method to determine whether a widget is being pressed.

        Returns bool.

        """
        mousePressed = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()
        return ((self.startX < mousePos[0] < self.endX) and
                (self.startY < mousePos[1] < self.endY) and
                (mousePressed == 1))


class Button(__Widget):
    def __init__(self, x, y, l, w):
        super().__init__(x, y, l, w)

    def draw(self, screen):
        """

        A method to control displaying a Button object on screen.

        Returns None.

        """
        pygame.draw.rect(screen, (255, 255, 255), (self.startX, self.startY, self.length, self.width))


class Textbox(__Widget):
    """

    USAGE:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for x in textBoxList:
                    x.isSelected = x.isPressed()

            elif event.type == pygame.KEYDOWN:
                for x in textBoxList:
                    x.addChar(event)

    """

    def __init__(self, x, y, l, w, splashText='', font='Copperplate Gothic Bold', fontSize=30):
        super().__init__(x, y, l, w)
        self.isSelected = False
        self.text = ''
        self.splashText = splashText

        self.font = pygame.font.SysFont(font, fontSize)

    def addChar(self, keyDownEvent):
        """

        A method to add a character to a textbox, given a key down event.

        Returns None.

        """
        mods = pygame.key.get_mods()

        if self.isSelected:
            if keyDownEvent.key != pygame.K_BACKSPACE:
                if keyDownEvent.key in range(48, 126):

                    if mods & pygame.KMOD_LSHIFT:
                        self.text += chr(keyDownEvent.key).upper()

                    else:
                        self.text += chr(keyDownEvent.key)

                if keyDownEvent.key == pygame.K_SPACE:
                    self.text += ' '

            else:
                self.text = self.text[:-1]

    def draw(self, screen):
        """

        A method to control displaying a TextBox object on screen.

        Returns None.

        """
        pygame.draw.rect(screen, (255, 255, 255), (self.startX, self.startY, self.length, self.width))

        if self.text != '':
            textRender = self.font.render(self.text, True, (0, 0, 0))
            screen.blit(textRender, (self.startX + 5, self.startY + 10))

        elif self.text == '' and self.isSelected:
            pass

        else:
            textRender = self.font.render(self.splashText, True, (200, 200, 200))
            screen.blit(textRender, (self.startX + 5, self.startY + 15))


class SecureTextbox(Textbox):
    """

    Like a textbox, but displays *'s instead of the characters in self.text.

    Useful for password boxes.

    """
    def __init__(self, x, y, l, w, splashText='', font='Copperplate Gothic Bold', fontSize=30):
        super().__init__(x, y, l, w, splashText=splashText, font=font, fontSize=fontSize)

    def draw(self, screen):
        """

        A method to control displaying a SecureTextBox object on screen.

        Returns None.

        """

        pygame.draw.rect(screen, (255, 255, 255), (self.startX, self.startY, self.length, self.width))

        if self.text != '':
            textRender = self.font.render('*' * len(self.text), True, (0, 0, 0))
            screen.blit(textRender, (self.startX + 5, self.startY + 10))

        elif self.text == '' and self.isSelected:
            pass

        else:
            textRender = self.font.render(self.splashText, True, (200, 200, 200))
            screen.blit(textRender, (self.startX + 5, self.startY + 10))


class Label:
    def __init__(self, text, pos, font='Copperplate Gothic Bold', fontSize=30, col=(0, 0, 0)):
        self.text = pygame.font.SysFont(font, fontSize).render(text, True, col)
        self.pos = pos

    def draw(self, screen):
        """

        A method to control displaying a Label object on screen.

        Returns None.

        """
        screen.blit(self.text, self.pos)


class Image:
    def __init__(self, img, pos):
        """

        :type img: pygame.Surface
        :type pos: tuple

        """
        self.img = img
        self.pos = pos

    def draw(self, screen):
        """

        A method to control displaying an Image object on screen.

        Returns None.

        """
        screen.blit(self.img, self.pos)


if __name__ == '__main__':

    test = pygame.display.set_mode((600, 600))
    tb = SecureTextbox(50, 100, 500, 100, splashText='testing', fontSize=80)

    end = False

    while True:
        for testEvent in pygame.event.get():
            if testEvent.type == pygame.QUIT:
                end = True

            elif testEvent.type == pygame.MOUSEBUTTONDOWN:
                tb.isSelected = tb.isPressed()

            elif testEvent.type == pygame.KEYDOWN:
                tb.addChar(testEvent)

                if testEvent.key == pygame.K_RETURN:
                    print(tb.text)

        if end:
            break

        test.fill((0, 0, 0))

        tb.draw(test)

        pygame.display.flip()
