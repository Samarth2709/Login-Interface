import pandas as pd
import pygame
import time
import sys

pygame.init()


def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


class Excel:
    def __init__(self):
        self.login_df = pd.read_excel('Login.xlsx')
        self.usernames = []
        self.passwords = []

    def init_col(self):
        self.usernames = list(self.login_df['Username'])
        self.passwords = list(self.login_df['Password'])

    def add_login(self, username, password):
        add_login = [username, password]
        length = len(self.login_df.index)
        self.login_df.loc[length] = add_login
        #print(self.login_df)

class PygameWindow:
    def __init__(self, caption):
        self.game_size = (1000, 500)
        self.game_caption = caption
        self.display = pygame.display.set_mode(self.game_size, pygame.RESIZABLE)
        pygame.display.set_caption(self.game_caption)
        self.display_button_a = 0
        self.outcome_display_dic = {}

    def fill_back(self, color=(0, 0, 0)):
        self.display.fill(color)

    def text_objects(self, text, font, color=(0, 0, 0)):
        self.textSurface = font.render(text, True, color)
        return self.textSurface, self.textSurface.get_rect()

    def text(self, text, size, x, y, color=(0, 0, 0)):
        self.smallText = pygame.font.Font("freesansbold.ttf", size)
        self.textSurf, self.textRect = text_objects(text, self.smallText, color)
        self.textRect.center = (x, y)
        self.display.blit(self.textSurf, self.textRect)

    def outcome_display(self, key, text, cond = True):
        self.outcome_display_dic[key] = [cond, text]
        #self.text(text, 20, 300, 500, c.blue)
    def clear_outcome(self):
        for key in self.outcome_display_dic:
            self.outcome_display_dic[key][0] = False

    def print_outcome(self):
        for i in range(len(self.outcome_display_dic)):
            if list(self.outcome_display_dic.values())[i][0]:
                self.text(list(self.outcome_display_dic.values())[i][1], 20, self.game_size[0]/2, 300, c.light_black)


class Button():
    def __init__(self, text, coord, size, color, color_text, border_radius=0, txt_size=25, alt_color=(0, 0, 0),
                 alt_txt_color=(0, 0, 0), transparent=False):
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.text = text
        self.rect = pygame.Rect(coord[0], coord[1], size[0], size[1])
        self.color = color
        self.text_color = color_text
        self.border_radius = border_radius
        self.text_size = txt_size
        self.alt_color = alt_color
        self.alt_text_color = alt_txt_color
        self.transparent = transparent
        self.end_login = False
        self.active_mouse = False

        self.register = False

    def display_button(self):
        if self.active_mouse:
            # ACTION WHEN MOUSE IS ON
            if self.transparent:
                pygame.draw.rect(wind.display, self.alt_color, self.rect, border_radius=self.border_radius, width=2)
            elif not self.transparent:
                pygame.draw.rect(wind.display, self.alt_color, self.rect, border_radius=self.border_radius)

            wind.text(self.text, self.text_size, self.rect.x + (self.rect.w / 2), self.rect.y + (self.rect.h / 2),
                      self.alt_text_color)

        else:
            # ACTION WHEN MOUSE IS NOT ON BUTTON
            if self.transparent:
                pygame.draw.rect(wind.display, self.color, (self.rect.x, self.rect.y, self.rect.w, self.rect.h),
                                 border_radius=self.border_radius, width=2)
            elif not self.transparent:
                pygame.draw.rect(wind.display, self.color, (self.rect.x, self.rect.y, self.rect.w, self.rect.h),
                                 border_radius=self.border_radius)

            wind.text(self.text, self.text_size, self.rect.x + (self.rect.w / 2), self.rect.y + (self.rect.h / 2),
                      self.text_color)

    def check_active_mouse(self, event, action, *args, **kwargs):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.active_mouse = True
            else:
                self.active_mouse = False
        if event.type == pygame.MOUSEBUTTONDOWN and self.active_mouse:
            action(*args, **kwargs)
            #ACTION

    def button_action_1(self):
        correct_login = False
        wind.clear_outcome()
        for i in range(len(excel.usernames)):
            if main.username_box.user_text == excel.usernames[i] and main.password_box.user_text == excel.passwords[i]:
                correct_login  = True
            else:
                correct_login = False
        if correct_login:
            wind.outcome_display('login action true', 'Correct', cond=True)
            print("CORRECT")
            self.user = main.username_box.user_text
            self.end_login = True
            # quit()
            # sys.exit()
        else:

            wind.outcome_display('login action false', 'Incorrect', cond=True)
            print('INCORRECT')



    def button_action_2(self):
        wind.clear_outcome()
        if main.username_box.user_text != '' and main.password_box.user_text != '':
            if not main.username_box.user_text in excel.usernames:
                excel.add_login(main.username_box.user_text, main.password_box.user_text)
                wind.outcome_display('register action avail', 'The login has been registered', cond=True)
            else:
                wind.outcome_display('register_action', 'The entered username is not available', cond = True)
                print('The Username: \'', main.username_box.user_text, "\' is not available ")
        excel.init_col()




class TextBox:
    def __init__(self, x, y, w, h, back_text='', centered_left=True, password = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = c.black
        self.text = back_text
        self.active_text = False
        self.user_text = ''
        self.centered_left = centered_left
        self.once = True
        self.end_text = False
        self.password = password
        if self.password:
            self.astric = ''

    def text_box(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active_text = True
            else:
                self.active_text = False
        pygame.key.set_repeat(500, 50)
        if self.active_text:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.end_text = True
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
            if event.type == pygame.TEXTINPUT:
                pygame.key.set_repeat(0)
                self.user_text += event.text

    def display(self):
        font = pygame.font.Font("freesansbold.ttf", self.rect.h - 5)
        self.textSurface_back = font.render(self.text, True, c.black)
        self.textSurface = font.render(self.user_text, True, c.black)
        width_back = self.textSurface_back.get_width()
        width = self.textSurface.get_width()
        self.rect.w = max(self.rect.w, width_back + 10)
        pygame.draw.rect(wind.display, self.color, self.rect, width=2, border_radius=2)
        if self.centered_left:
            if self.user_text == '':
                wind.text(self.text, self.rect.h - 5, self.rect.x + width_back / 2 + 5,
                          self.rect.y + +(self.rect.h / 2) + 1, c.gray)
            else:
                if not self.password:
                    wind.text(self.user_text, self.rect.h - 5, self.rect.x + width / 2 + 5,
                              self.rect.y + (self.rect.h / 2) + 1, self.color)
                elif self.password:
                    numb_astric = len(self.user_text)
                    self.astric = str('*'*numb_astric)
                    font = pygame.font.Font("freesansbold.ttf", self.rect.h - 5)
                    self.textSurface_a = font.render(self.astric, True, c.black)
                    self.rect.w = max(100, self.textSurface_a.get_width() + 10)
                    wind.text(self.astric, self.rect.h-5, self.rect.x + self.textSurface_a.get_width() / 2 + 5,
                              self.rect.y + (self.rect.h / 2) + 1, self.color)


            if self.active_text: #BLINCKER
                if time.time() % 1 >= 0.5:
                    if not self.password:
                        width = self.textSurface.get_width()
                        rect = (self.rect.x + width + 5, self.rect.y + 2, 2, self.rect.h - 2)
                        pygame.draw.rect(wind.display, c.light_black, rect)
                    if self.password:
                        if self.astric == '' or self.astric == ' ':
                            width = 0
                        else:
                            width = self.textSurface_a.get_width()
                        rect = (self.rect.x + width + 5, self.rect.y + 2, 2, self.rect.h - 2)

                        print(width)
                        pygame.draw.rect(wind.display, c.light_black, rect)


    def update(self):
        # Resize the box if the text is too long.
        if not self.password:
            font = pygame.font.Font("freesansbold.ttf", self.rect.h - 5)
            self.textSurface = font.render(self.user_text, True, c.black)
            width = max(100, self.textSurface.get_width() + 10)
            self.rect.w = width
        elif self.password:
            font = pygame.font.Font("freesansbold.ttf", self.rect.h - 5)
            self.textSurface_a = font.render(self.astric, True, c.black)
            width = max(100, self.textSurface_a.get_width() + 10)
            self.rect.w = width


class Color:
    def __init__(self):
        self.black = (0, 0, 0)
        self.light_black = (50, 50, 50)
        self.white = (255, 255, 255)
        self.light_white = (200, 200, 200)
        self.red = (255, 0, 0)
        self.light_red = (255, 60, 60)
        self.green = (0, 255, 0)
        self.light_green = (110, 255, 110)
        self.blue = (0, 0, 255)
        self.light_blue = (0, 115, 255)
        self.gray = (150, 150, 150)


wind = PygameWindow("Login")
c = Color()
excel = Excel()
excel.init_col()

def main():
    clock = pygame.time.Clock()
    main.username_box = TextBox(300, 150, 200, 30, back_text='Username')
    main.password_box = TextBox(300, 200, 200, 30, back_text='Password', password=True)
    login_button = Button('Login', (300, 250), (75, 30), c.blue, c.black, border_radius=5, alt_color=c.light_blue, transparent=False, txt_size=15)
    register_button = Button('Register', (400, 250), (75, 30), c.blue, c.black, border_radius=5, alt_color=c.light_blue, transparent=True, txt_size=15)
    end = False
    while not end:
        for event in pygame.event.get():  # ANY EVENTS THAT HAPPEN WITHIN WINDOW
            print(event)
            # EVENT TYPES ARE ANY MAJOR EVENT (QUIT, ACTIVEEVENT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP,
            # MOUSEBUTTONDOWN, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN, VIDEORESIZE,
            # VIDEOEXPOSE, USEREVENT)
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print('w')
            main.username_box.text_box(event)
            main.password_box.text_box(event)
            login_button.check_active_mouse(event, login_button.button_action_1)
            register_button.check_active_mouse(event, register_button.button_action_2)
        main.username_box.update()
        main.password_box.update()
        wind.fill_back(c.white)
        # DISPLAY OTHER OBJECTS HERE
        login_button.display_button()
        register_button.display_button()
        wind.print_outcome()

        # for i in range(len(wind.outcome_display_dic)):
        #     if list(wind.outcome_display_dic.values())[i][0]:
        #         wind.text(list(wind.outcome_display_dic.values())[i][1], 20, wind.game_size[0]/2, 300, c.blue)
        # wind.display_button('Login', (300, 250), (75, 30), c.blue, c.black, border_radius=5, alt_color=c.light_blue,
        #                     transparent=False, txt_size=15)
        # wind.display_button('Register', (400, 250), (75, 30), c.blue, c.black, border_radius=5, alt_color=c.light_blue,
        #                     transparent=True, txt_size=15)
        main.username_box.display()
        main.password_box.display()
        pygame.display.update()
        if login_button.end_login:
            time.sleep(1.5)
            exit()
        clock.tick(144)  # REFRESH RATE


if __name__ == '__main__':
    main()
    #excel.add_login('apple', 'car')
pygame.quit()
