import pygame # Import pygame
import pygame.freetype # Used for fonts
import numpy as np # Numpy is a library used for arrays and the sort
import random # Random ofc
from pygame import * # Basically import all functions from pygame so that they can be called directly. (Eg pygame.Rect() can be called with just Rect(). Only used this as it a necessity for the rounded rectangles function)

pygame.init() # Initialising pygame

# ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ 

#  _____  _     ___________  ___   _       _   _  ___  ______ _____  ___  ______ _      _____ _____ 
# |  __ \| |   |  _  | ___ \/ _ \ | |     | | | |/ _ \ | ___ \_   _|/ _ \ | ___ \ |    |  ___/  ___|
# | |  \/| |   | | | | |_/ / /_\ \| |     | | | / /_\ \| |_/ / | | / /_\ \| |_/ / |    | |__ \ `--. 
# | | __ | |   | | | | ___ \  _  || |     | | | |  _  ||    /  | | |  _  || ___ \ |    |  __| `--. \
# | |_\ \| |___\ \_/ / |_/ / | | || |____ \ \_/ / | | || |\ \ _| |_| | | || |_/ / |____| |___/\__/ /
#  \____/\_____/\___/\____/\_| |_/\_____/  \___/\_| |_/\_| \_|\___/\_| |_/\____/\_____/\____/\____/ 
                                                                                                  
                                                                                                  
# Just some colours that i use
white = (190, 190, 190)
l_grey = (60, 60, 60)
d_grey = (50, 50, 50)
green = (6, 143, 13)
yellow = (255, 199, 31)
grey = (20, 20, 20)

# Bringing in the font for the text
font = pygame.freetype.Font('JetBrainsMono-Bold.ttf', 36)
key_font = pygame.freetype.Font('JetBrainsMono-Bold.ttf', 14)

window = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()

# Function to get rounded rectangles (No clue how it works, it just does)
# https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
def AAfilledRoundedRect(surface,rect,color,radius=0.3):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)

    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

# ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ 

#  _____  _____ _      _       _____  _       ___   _____ _____ 
# /  __ \|  ___| |    | |     /  __ \| |     / _ \ /  ___/  ___|
# | /  \/| |__ | |    | |     | /  \/| |    / /_\ \\ `--.\ `--. 
# | |    |  __|| |    | |     | |    | |    |  _  | `--. \`--. \
# | \__/\| |___| |____| |____ | \__/\| |____| | | |/\__/ /\__/ /
#  \____/\____/\_____/\_____/  \____/\_____/\_| |_/\____/\____/ 
                                                            
# Class for all the cells in the main wordle game. The little boxes that fill with colour
class Cell():
    
    def __init__(self, rectangle, font):
        self.rectangle = rectangle # The pygame rectangle for the cell
        self.letter = None # The letter that has been inputted into the cell
        self.complete = False # Does the cell have a letter?
        self.colour = green # The colour of the cell
        
    __str__ = lambda self: str(self.letter) # What is printed when i do print(cell) ... mostly for debugging
    
    # Drawing the cell on the screen
    def draw(self):
        
        if not self.complete: # If its not complete, draw a simple rectangle
            pygame.draw.rect(window, self.colour, self.rectangle, 2)
        elif self.complete and self.colour == grey: # If it not in the word, we only want border to changle colour, not the fill of the box
            pygame.draw.rect(window, d_grey, self.rectangle, 2)
        else:
            pygame.draw.rect(window, self.colour, self.rectangle) # Drawing the coloured boxes
            
        if self.letter: # If it has a letter
            if self.complete: # This is if it is a previous guess
                if self.colour == grey: # If it is a wrong letter, we want dark grey text
                    font.render_to(window, (self.rectangle.centerx-9, self.rectangle.centery-13), self.letter, d_grey)
                else: # If it is a right letter, colour should be pure white
                    font.render_to(window, (self.rectangle.centerx-9, self.rectangle.centery-13), self.letter, (255,255,255))
            else: # This means it is part of the ongoing guess so white colour
                font.render_to(window, (self.rectangle.centerx-9, self.rectangle.centery-13), self.letter, white)

# This is the class for the keyboard keys on the bottom of the wordle
class Key():
    
    def __init__ (self, rectangle, font, value):
        self.rectangle = rectangle # Pygame rectangle representing the key
        self.font = font # Font for letters shown on the key
        self.value = value # Letter, Delete or Enter values
        self.used = 0 # Has key been used in a letter before
        self.colour = green # Colour of the key
    
    # Drawing the key on the screen
    def draw(self):
        
        if not self.used: # If the key isnt used, we draw a white rect
            AAfilledRoundedRect(window, self.rectangle, white)
        else: # Else we draw a rect of the colour of the key
            AAfilledRoundedRect(window, self.rectangle, self.colour)
            
        self.font.render_to(window, (self.rectangle.x+7, self.rectangle.y+7), self.value, grey) # Printing the letter on the key
            
    __str__ = lambda self: str(self.rectangle.center)  # What is printed when i do print(key) ... mostly for debugging

# A 6x5 grid for the cells in wordle
word_grid=np.array([[0]*5]*6).astype(dtype=Cell)

# A grid for all the keys
keyboard=np.array([ [0]*10,
                    [0]*9,
                    [0]*9], dtype=Key)

# Essentially a map of the keys on the keyboard
keyboard_str=np.array([['q','w','e','r','t','y','u','i','o','p'],
                       ['a','s','d','f','g','h','j','k','l'],
                       ['enter', 'z','x','c','v','b','n','m','delete']], dtype=object)

# Iterate over all the keys
for i, row in enumerate(keyboard):
    l = len(row)
    for j, col in enumerate(row):
        
        # We want the delete and enter keys to be longer than the other, so we use a width_multiplier
        if (i == 2 and j == 0) or (i == 2 and j == 8):
            width_mul = 1.75
        else:
            width_mul = 1
        
        # Since the enter key has a longer len, it has to be moved to the left as it is in the beginning of the row and
        # should not overlap with the other keys so we implement a shift
        if (i == 2 and j == 0):
            rect_shift = -30
        else:
            rect_shift = 0
        
        # Creating all the keys and saving them in the keybaord. This includes:
        keyboard[i][j] = Key(pygame.Rect(300+45*(j-l/2)+rect_shift, 600+55*i, 40 * width_mul, 50), # Their rectangle
                             key_font, # Their font
                             keyboard_str[i][j]) # The value of the key which we take from the map we created earlier

# Iterate over all the cells in the wordle
for i, row in enumerate(word_grid):
    for j, box in enumerate(word_grid[0]):
        word_grid[i][j] = Cell(pygame.Rect(105+80*j, 60+80*i, 70, 70), font)

active_line = 0 # The current line we are on, i.e. the nth guess - 1 cause the first guess is on the 0th line
curr_word = '' # The current word that is being guessed

# ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ 

#  _    _  _________________ _      _____ 
# | |  | ||  _  | ___ \  _  \ |    |  ___|
# | |  | || | | | |_/ / | | | |    | |__  
# | |/\| || | | |    /| | | | |    |  __| 
# \  /\  /\ \_/ / |\ \| |/ /| |____| |___ 
#  \/  \/  \___/\_| \_|___/ \_____/\____/ 
                 
                 
target_word = random.choice([line.rstrip() for line in open('possible_words.txt')]) # Finding the target word
print("================================")
print(target_word) # This will print it in the terminal, for debugging purposes
print("================================")
                 
# The function that evaluates any given word 
def wordle(word):
    
    curr_count = {} # The count for all the letters eord
    res = '' # Result calculated
    for letter in word:
        curr_count[letter] = 0 # Setting the count to be 0
        
    for i, letter in enumerate(word):
        
        # Finding the coordinates of the key in the 2D array created and storing it in x, y
        for m, row in enumerate(keyboard_str):
            for n, char in enumerate(row):
                if char == letter:
                    x, y = m, n
        
        # WHenever we find a letter, we increase count by 1
        curr_count[letter] += 1
        
        print(curr_count[letter] < target_word.count(letter)) # Debugging stuff ... ignore
        
        if letter == target_word[i]: # If the letter is in the correct pos,
            word_grid[active_line][i].colour = green # Set the cell to green
            keyboard[x][y].colour = green # Set the key to green
            keyboard[x][y].used = 1 # Set the letter to used
            print("Set colour of letter {} to green".format(letter))
            res+='g' # Add g to result
        
        elif (letter in target_word) and (curr_count[letter] <= target_word.count(letter)): # Correct letter in wrong pos
            word_grid[active_line][i].colour = yellow # Set cell to yellow
            keyboard[x][y].colour = yellow # Set the key to yellow
            keyboard[x][y].used = 1 # Set the letter to used
            print("Set colour of letter {} to yellow".format(letter))
            res += 'y' # Add y to the result
        
        else: # Letter not in word
            word_grid[active_line][i].colour = grey # Set cell to grey
            keyboard[x][y].colour = l_grey # Set key to grey
            keyboard[x][y].used = 1 # Set letter to used
            print("Set colour of letter {} to grey".format(letter))
            res+='b' # Add b to result
            
        word_grid[active_line][i].complete = True # Set every cell in the row to complete, i.e. it has been used in the game
        print(curr_count)
        
        
    if res == 'ggggg': # If the game is won
        return True
                                        


# ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ 

#  _____   ___  ___  ___ _____   _     _____  ___________ 
# |  __ \ / _ \ |  \/  ||  ___| | |   |  _  ||  _  | ___ \
# | |  \// /_\ \| .  . || |__   | |   | | | || | | | |_/ /
# | | __ |  _  || |\/| ||  __|  | |   | | | || | | |  __/ 
# | |_\ \| | | || |  | || |___  | |___\ \_/ /\ \_/ / |    
#  \____/\_| |_/\_|  |_/\____/  \_____/\___/  \___/\_|    
                                                        
                                                        

running = True # Start the game loop
checking = True # Start the checking loop
won = False
while running:
    
    clock.tick(60) # Set speed to 60fps
    for event in pygame.event.get(): # Check all occuring events
        if event.type == pygame.QUIT: # If the cross button is pressed
            running = False # Quit the game as loop will be false
            
        if event.type == pygame.KEYDOWN and checking == True: # If a key is pressed and we are looking for input
            
            # Checking for backspace
            if pygame.key.name(event.key) == 'backspace':
                curr_word = curr_word[:-1] # Deleter the last letter from the current guess
                word_grid[active_line][len(curr_word)].letter = None # Remove the letter from the last cell
                print(curr_word)
            # Checking if the key pressed is a letter and length is less than 5
            elif pygame.key.name(event.key) in 'abcdefghijklmnopqrstuvwxyz' and len(curr_word) < 5:
                curr_word += pygame.key.name(event.key) # Add the letter to the current word
                word_grid[active_line][len(curr_word)-1].letter = pygame.key.name(event.key).upper() # Set the letter of the cell to that letter
                print(curr_word)
            # Checking if the key pressed is enter and the word is in a list of acceptable guesses
            elif pygame.key.name(event.key) == 'return' and curr_word in [line.rstrip() for line in open('allowed_guesses.txt')]:
                won = wordle(curr_word) # Check if the game has been won
                
                curr_word = '' # Reset the current word to nothing
                active_line += 1 # Increase active line by 1
                print(curr_word)
        
        # This is to check if input has been given by the mouse on the virtual keyboard
        if event.type == pygame.MOUSEBUTTONUP: # If the mouse button is release
            pos = pygame.mouse.get_pos() # Get mouse pos
            clicked_rect = [] # Check collisions and see which key it pressed
            for i, row in enumerate(keyboard):
                for j, key in enumerate(row):
                    if key.rectangle.collidepoint(pos):
                        clicked_rect.append(key)
            
            clicked_key = clicked_rect[0]
            
            # Essentially the same as the keyboard input
            if clicked_key.value == 'delete':
                curr_word = curr_word[:-1]
                word_grid[active_line][len(curr_word)].letter = None
                print(curr_word)
            # Checking if the key pressed is enter
            elif clicked_key.value == 'enter':
                if curr_word in [line.rstrip() for line in open('allowed_guesses.txt')]:
                    won = wordle(curr_word)
                    
                    curr_word = ''
                    active_line += 1
                    print(curr_word)
                
            else:
                curr_word += clicked_key.value
                word_grid[active_line][len(curr_word)-1].letter = clicked_key.value.upper()
                print(curr_word)
    
    window.fill(grey)
    
    # Going over all the cells
    for i in range(6):
        for j in range(5):
            
            # We set the active line to white in colour
            if(i==active_line):
                word_grid[i][j].colour = white
            elif(i>active_line): # We set everything after it to light grey. Everything before has been handled when it passed throug the wordle() function
                word_grid[i][j].colour = l_grey

            word_grid[i][j].draw() # Draw the cell
    
    # Going through the keybaord
    for i, row in enumerate(keyboard):
        for j, col in enumerate(row):
            keyboard[i][j].draw() # Draw the key
    
    pygame.display.flip() # Refresh the display
    if(won): # If the game is won
        pygame.time.delay(1750) # Wait 1.75 seconds to let them enjoy the win
        running = False # Quit the game
    
    
pygame.quit() # Quit pygame
exit() # Exit