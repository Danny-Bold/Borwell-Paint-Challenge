"""

Borwell 'Paint Calculator' Challenge, Danny Bold, 20/7/2022

I chose to code this project in Python, using Pygame, because that's what I'm most familiar with.

"""

import pygame

from widgets import Button, Textbox, Label
from vector import Vector as V


def validate(l, w, h):
    """

    Checks all measurements are valid. This means the user has entered a positive number.

    Inputs will be strings.

    """
    try:
        lf = float(l)
        wf = float(w)
        hf = float(h)

        # Once we get to this point with no error, we know the inputs were numbers.

        return lf > 0 and wf > 0 and hf > 0

    except ValueError:
        return False


def calcValues(l, w, h):
    """

    l, w: length and width. Any order.
    h: height. Must be the vertical measurement

    Returns a 3-tuple for the floor area, paint required to paint walls and volume of the room, in that order.

    Assumes the inputs given are valid.

    """

    floorArea = l * w
    wallSA = 2 * (l * h + w * h) + l * w
    volume = l * w * h

    return floorArea, wallSA, volume


def resultsScreen(screen, values):

    values = calcValues(*values)

    running = True

    title = Label('Borwell Paint Calculator', (50, 50), fontSize=70, col=(255, 255, 255))
    floorLabel = Label('Floor area: ' + str(values[0]), (50, 150), fontSize=60, col=(255, 255, 255))
    wallSALabel = Label('Paint required for walls: ' + str(values[1]), (50, 250), fontSize=60, col=(255, 255, 255))
    volumeLabel = Label('Room volume: ' + str(values[2]), (50, 350), fontSize=60, col=(255, 255, 255))
    backLabel = Label('Back', (820, 475), fontSize=60)

    labelList = [title, floorLabel, wallSALabel, volumeLabel, backLabel]

    backButton = Button(800, 450, 150, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # This is so the main function knows that the program has been quit

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.isPressed():
                    running = False

        screen.fill((0, 0, 0))

        backButton.draw(screen)

        for x in labelList:
            x.draw(screen)

        pygame.display.flip()


def main():
    screen = pygame.display.set_mode((1000, 600))  # Creating the screen - fixed dimensions for now

    # Control variables

    running = True
    quitFromResults = False
    errorMessageVisible = False

    # Widgets

    lengthTextbox = Textbox(50, 150, 300, 50, splashText='Please enter length')
    widthTextbox = Textbox(50, 250, 300, 50, splashText='Please enter width')
    heightTextbox = Textbox(50, 350, 300, 50, splashText='Please enter height')

    textBoxList = [lengthTextbox, widthTextbox, heightTextbox]

    enterButton = Button(800, 450, 150, 100)

    buttonList = [enterButton]

    errorMessage = Label('Invalid inputs', (50, 450), col=(255, 0, 0))

    title = Label('Borwell Paint Calculator', (50, 50), fontSize=70, col=(255, 255, 255))
    enterLabel = Label('Enter', (810, 475), fontSize=60)

    labelList = [title, enterLabel]

    """
    
    I'll include a graphic of a wireframe cuboid, with sides that colour depending on which textbox is selected.
    
    For this, we'll need a vector to specify the coordinates of the first corner, which I call O.
    
    I'll then specify vectors (a, b and c) to go from this corner, along the three directions of the cuboid.
    
    The corners of the cuboid are the O, O+a, O+b, O+c, O+a+b, O+a+c, O+b+c, O+a+b+c
    
    The lines going in the direction of length (a) have start and endpoints of:
    
    O -> O+a
    O+b -> O+a+b
    O+c -> O+a+c
    0+b+c -> O+a+b+c
    
    And similarly for the other directions.
    
    """

    O = V(450, 150)

    a = V(450, 0)
    b = V(50, 50)
    c = V(0, 200)

    vertices = [O, O + a, O + b, O + c, O + a + b, O + a + c, O + b + c, O + a + b + c]

    lengthLines = [(vertices[0].toTuple(), vertices[1].toTuple()),
                   (vertices[2].toTuple(), vertices[4].toTuple()),
                   (vertices[3].toTuple(), vertices[5].toTuple()),
                   (vertices[6].toTuple(), vertices[7].toTuple())]

    widthLines = [(vertices[0].toTuple(), vertices[2].toTuple()),
                  (vertices[1].toTuple(), vertices[4].toTuple()),
                  (vertices[3].toTuple(), vertices[6].toTuple()),
                  (vertices[5].toTuple(), vertices[7].toTuple())]

    heightLines = [(vertices[0].toTuple(), vertices[3].toTuple()),
                   (vertices[1].toTuple(), vertices[5].toTuple()),
                   (vertices[2].toTuple(), vertices[6].toTuple()),
                   (vertices[4].toTuple(), vertices[7].toTuple())]

    while running and not quitFromResults:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When the exit button is pressed
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for x in textBoxList:
                    x.isSelected = x.isPressed()

                if enterButton.isPressed():

                    l = lengthTextbox.text
                    w = widthTextbox.text
                    h = heightTextbox.text

                    valid = validate(l, w, h)  # Validate inputs

                    if valid:
                        quitFromResults = resultsScreen(screen, (float(l), float(w), float(h)))
                        errorMessageVisible = False  # Removing any error message after returning

                    else:
                        errorMessageVisible = True

            elif event.type == pygame.KEYDOWN:
                for x in textBoxList:
                    x.addChar(event)

        screen.fill((0, 0, 0))  # background

        # Rendering all objects on screen

        for x in buttonList:
            x.draw(screen)

        for x in labelList:
            x.draw(screen)

        for x in textBoxList:
            x.draw(screen)

        if errorMessageVisible:
            errorMessage.draw(screen)

        # Drawing the graphic

        for x in lengthLines:
            if lengthTextbox.isSelected:
                pygame.draw.aaline(screen, (255, 0, 0), x[0], x[1])

            else:
                pygame.draw.aaline(screen, (255, 255, 255), x[0], x[1])

        for x in widthLines:
            if widthTextbox.isSelected:
                pygame.draw.aaline(screen, (0, 255, 0), x[0], x[1])

            else:
                pygame.draw.aaline(screen, (255, 255, 255), x[0], x[1])

        for x in heightLines:
            if heightTextbox.isSelected:
                pygame.draw.aaline(screen, (0, 0, 255), x[0], x[1])

            else:
                pygame.draw.aaline(screen, (255, 255, 255), x[0], x[1])

        pygame.display.flip()  # Updates the screen


if __name__ == '__main__':
    main()
