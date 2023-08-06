#=============#
#  PROPython  #
#=============#

#---------------#
# Version 1.0.7 #
#---------------#

# New version coming soon!
import random
import pygame
import os
import itertools
import time
import sys
import math
import json
from PROPython.Objects import *
from PROPython.Settings import *
from PROPython.Settings import _keys_
from PROPython.camera import *
from PROPython.network import Network
from PROPython.keys import *

class Terminal():
    def __init__(self):
        self.arguments = sys.argv[1:]

    def get_args(self):
        return self.arguments

class Language():
    en_ = True
    ru_ = False
    def en(self):
        self.en_ = True
        self.ru_ = False

    def ru(self):
        self.ru_ = True
        self.en_ = False

    def get_language(self):
        if self.en_:
            return "ENGLISH"
        elif self.ru_:
            return "RUSSIAN"
        else:
            self.en_ = True
            return "ENGLISH"

class Debug():
    def log(self, values, sep=None, end=None, file=None):
        if not sep == None:
            if not end == None:
                if not file == None:
                    print(values, sep=sep, end=end, file=file)
                else:
                    print(values, sep=sep, end=end)
            else:
                print(values, sep=sep)
        else:
            print(values)

    def cmd(self, msg):
        print(msg)

class Time():
    def delay(self, seconds):
        time.sleep(seconds)

class Base():
    def loading_animation(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)

    def writing_animation(self, text):
        for i in text:
            time.sleep(0.3)
            print(i, end='', flush=True)

    def __return__(self, object):
        return object

class Dict():
    def sort(self, dict):
        return sorted(dict.items(), key=lambda item: (item[1], item[0]))

class List():
    def enum(self, list):
        for index, value in enumerate(list):
            print("index: " + str(index), " value: " + str(value))

    def length(self, list):
        return len(list)

class Str():
    def has_number_or_letter(self, string):
        return string.isalnum()

    def has_number(self, string):
        return string.isnumeric()

    def has_letter(self, string):
        return string.isalpha()

    def computer_symbol(self, string):
        return ord(string)

    def upper(self, string):
        return string.upper()

    def lower(self, string):
        return string.lower()

class Directory():
    def is_exists(self, path):
        return os.path.exists(path)

    def create(self, path):
        os.mkdir(path)

    def delete(self, path):
        os.rmdir(path)

    def files_list(self, path):
        return os.listdir(path)

class Math():
    pi = math.pi
    euler_num = math.e

    def random(self, start, stop, step):
        return random.randrange(start, stop, step)

    def round(self, number):
        return math.trunc(number)

    def floor(self, number):
        return math.floor(number)

    def ceil(self, number):
        return math.ceil(number)

    def exponents(self, number):
        return math.exp(number)

    def square_root(self, number):
        return math.sqrt(number)

    def sum(self, values_list):
        res = 0

        for x in values_list:
            if type(x) == int or type(x) == float:
                res += x
            else:
                raise TypeError("Error! You have a string and you need int or float!")

        return res

    def difference(self, values_list):
        res = 0

        for x in values_list:
            if type(x) == int or type(x) == float:
                res = x - res
            else:
                raise TypeError("Error! You have a string and you need int or float!")

        return -res

    def composition(self, values_list):
        res = 1

        for x in values_list:
            if type(x) == int or type(x) == float:
                res = x * res
            else:
                raise TypeError("Error! You have a string and you need int or float!")

        return res

    def quotient(self, values_list):
        res = values_list[0]

        if values_list[0] == 0:
            raise ValueError("Error! Cannot be divided by zero!")

        for x in values_list:
            if x == values_list[0]:
                res = values_list[0]
            else:
                if type(x) == int or type(x) == float:
                    res = res / x
                else:
                    raise TypeError("Error! You have a string and you need int or float!")

        return res

    def binary(self, number):
        return bin(number)

    def degree(self, first, second):
        return pow(first, second)

class File():
    def __init__(self, path):
        self.path = path

    def write(self, object):
        self.file = open(self.path, "w")
        self.file.write(object)

    def add(self, object):
        self.file = open(self.path, "a")
        self.file.write(object)

    def read(self):
        self.file = open(self.path, "r")
        return self.file.read()

    def size(self):
        return os.path.getsize(self.path)

    def clear_lines(self):
        FILE = open(self.path, "w")
        FILE.truncate()
        FILE.close()

    def delete(self):
        os.remove(self.path)

    def rename(self, name):
        os.rename(self.path, name)

    def duplicate(self, value):
        FILE = open(str(value) + self.path, "w")
        FILE2 = open(self.path, "r")
        FILE.write(FILE2.read())
        FILE.close()
        FILE2.close()

    def close(self):
        self.file.close()

class PROGame:
    pygame.init()

    def __init__(self):
        self.run = True
        self.hasIF = False
        self.created_host = False
        self.created_network = False
        self.hasCheckCollision = False
        self.draw_particles = False
        self.hasFill = False
        self.hasPlayer = False
        self.hasBG = False
        self.drawTextbox = False
        self.run_p_sys = False
        self.check_key = False
        self.i = 0

    def Application(self, width, height, window_name):
        self.drawButton = True
        self.count = 0
        window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(window_name)
        window.fill((15, 150, 105))
        self.FillColor = (15, 150, 105)
        self.hasFill = True
        self.window = window
        self.windowX = width
        self.windowY = height

    def show(self, FPS, debug_mode):
        clock = pygame.time.Clock()

        self.run = True
        if self.run:
            clock.tick(FPS)

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.run = False

                if self.run_p_sys:
                    if self.draw_particles:
                        for i in range(20):
                            particles.append(ParticleSystem(self.p__x, self.p__y, self.p__speed, self.p__radius, self.p__color))

                def drawButton():
                    pos = pygame.mouse.get_pos()
                    if self.drawButton:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                for b in BUTTONS:
                                    if b.get_pos(b):
                                        b.Function(pygame.mouse.get_pos(), b.command)
                        else:
                            for b in BUTTONS:
                                if b.get_pos(b):
                                    if pos[0] > b.x and pos[0] < b.x + b.width:
                                        if pos[1] > b.y and pos[1] < b.y + b.height:
                                            b.draw(self.window, b.active_color, b.outline, b.font, b.size, b.text_color)
                                    else:
                                        b.draw(self.window, b.inactive_color, b.outline, b.font, b.size, b.text_color)

                def drawTextBox():
                    if self.hasIF:
                        for input_field in TEXT_BOXS:
                            if self.hasBG:
                                self.window.blit(self.BGimg, (0, 0))
                            else:
                                pygame.draw.rect(self.window, self.FillColor, (input_field.x, input_field.y , input_field.width + self.windowX, input_field.height + self.border_width))

                            input_field.update(event, self.window)

                drawTextBox()
                drawButton()

            if self.hasPlayer == True:
                if self.created_network:
                    self.p2 = self.n.send(self.p)
                    if debug_mode:
                        print(self.p)
                        print(self.p2)

                if self.hasBG:
                    self.window.blit(self.BGimg, (0, 0))
                else:
                    self.window.fill(self.FillColor)
                if self.created_network == True:
                    self.p.UpdatePlayer(self.window, self.windowX, self.windowY)
                    self.p2.UpdatePlayer(self.window, self.windowX, self.windowY)
                elif self.hasPlayer == True:
                    self.player.UpdatePlayer(self.window, self.windowX, self.windowY)

            if self.hasFill == True:
                self.window.fill(self.FillColor)

            if self.draw_particles:
                for particle in particles:
                    particle.draw(self.window)
                for particle in particles:
                    if particle.lifetime >= 21:
                        particle.lifetime = 0
                self.run_p_sys = False

            pygame.display.update()

    def draw_cube(self, color, pos_x, pos_y, width, height):
        pygame.draw.rect(self.window, color, (pos_x, pos_y, width, height))

    def draw_circle(self, color, pos_x, pos_y, width, height):
        pygame.draw.circle(self.window, color, (pos_x, pos_y), width, height)

    def draw_line(self, color, pos_x1, pos_y1, pos_x2, pos_y2, width):
        pygame.draw.line(self.window, color, [pos_x1, pos_y1], [pos_x2, pos_y2], width)

    def draw_polygon(self, color, pos_x1, pos_y1, pos_x2, pos_y2, pos_x3, pos_y3, pos_x4, pos_y4):
        pygame.draw.polygon(self.window, color, [[pos_x1, pos_y1], [pos_x2, pos_y2], [pos_x3, pos_y3], [pos_x4, pos_y4]])

    def create_text(self, text, font, size, color, pos_x, pos_y, smoothing):
        font = pygame.font.Font(font, size)
        Text = font.render(text, smoothing, color)
        self.window.blit(Text, [pos_x, pos_y])

    def play_sound(self, path):
        sound = pygame.mixer.Sound(path)
        sound.play()

    def fill(self, color):
        self.FillColor = color
        self.window.fill(color)
        self.hasFill = True

    def background(self, path):
        self.window.blit(pygame.image.load(path), (0, 0))
        self.hasBG = True
        self.BGimg = pygame.image.load(path)

    def create_image(self, path, pos_x, pos_y):
        self.window.blit(pygame.image.load(path), (pos_x, pos_y))
        return pygame.image.load(path).get_rect()

    def icon(self, path):
        pygame.display.set_icon(pygame.image.load(path))

    def create_button(self, active_color, inactive_color, width, height, x, y, text, size, font, text_color, outline=None, command=None):
        button = UI.Button(active_color, inactive_color, outline, font, size, text_color, x, y, width, height, text, command)
        BUTTONS.append(button)
        button.draw(self.window, inactive_color, outline, font, size, text_color)

    def clear(self):
        self.drawButton = False
        self.hasIF = False

    def create_player(self, x, y, speed, image, control_type = 1):
        self.p = Player(x, y, speed, image, control_type)
        self.hasPlayer = True
        self.player = self.p
        return self.p.get_rect()

    def create_text_box(self, width, height, x, y, active_color, inactive_color, border_width, text_color, font, size, max_chars):
        input_field = UI.Input_Field(width, height, x, y, active_color, inactive_color, border_width, text_color, font, size, max_chars)
        TEXT_BOXS.append(input_field)
        self.hasIF = True
        self.border_width = border_width

    def get_TextBoxs_text(self):
        for input_field in TEXT_BOXS:
            return input_field.GetInputFieldText(input_field)

    def create_network(self):
        self.n = Network()
        self.p = self.n.getP()
        self.created_network = True
        self.hasPlayer = True

    def particle_system(self, x, y, speed, radius, color):
        self.p__y = y
        self.p__x = x
        self.p__color = color
        self.p__speed = speed
        self.p__radius = radius
        self.draw_particles = True

    def run_particle_system(self):
        self.run_p_sys = True