import pygame

# Define some constants.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
FRAMES_PER_SECOND = 20

# Define hats positions
hat_positions = {(0, 0): 'Center',
                 (0, 1): 'North',
                 (0, -1): 'South',
                 (1, 0): 'East',
                 (-1, 0): 'West',
                 (1, 1): 'NorthEast',
                 (1, -1): 'SouthEast',
                 (-1, -1): 'SouthWest',
                 (-1, 1): 'NorthWest'}


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 200))
pygame.display.set_caption("AI fly")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates.
clock = pygame.time.Clock()
# Initialize the joysticks.
pygame.joystick.init()
# Get ready to print.
textPrint = TextPrint()

joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    print(f'Joystick: {joystick.get_name()}')
    joystick.init()

# -------- Main Program Loop -----------
while not done:

    for event in pygame.event.get():  # User did something.
        if event.type == pygame.QUIT:  # If user clicked close.
            done = True  # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f'Joystick button {event.button} pressed.')
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        elif event.type == pygame.JOYHATMOTION and hat_positions[event.value] != 'Center':
            print(f'Joystick hat {hat_positions[event.value]} presssed')

    screen.fill(WHITE)
    textPrint.reset()
    # Get count of joysticks.

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)

        textPrint.tprint(screen, "Joystick {}".format(i))
        textPrint.indent()

        for i in range(joystick.get_numaxes()):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # Limit frames per second.
    clock.tick(FRAMES_PER_SECOND)
pygame.quit()
