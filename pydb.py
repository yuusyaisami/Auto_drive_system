import pygame
import pysave
import numpy as np
pygame.init()
class DataBase:
    def __init__(self):
        self.pysave = pysave.SaveText()
        self.font = self.Font()
        self.color = self.Color()
        self.view = self.View(self)
        self.driver = self.Driver()
    def save(self):
        path = "pydatabase_save.txt"
        self.pysave.add("use_fonttype", self.use_fonttype, path)
        self.pysave.add("inactive", self.color.inactive, path)
        self.pysave.add("active", self.color.active, path)
        self.pysave.add("on_mouse", self.color.on_mouse, path)
        self.pysave.add("alpha", self.color.alpha, path)
        self.pysave.add("background", self.color.background, path)
    def init(self):
        path = "pydatabase_save.txt"
        self.use_fonttype = self.pysave.search("use_fonttype", path)
        self.color.inactive = self.color.convert_str_to_colorcode(self.pysave.search("inactive", path))
        self.color.active = self.color.convert_str_to_colorcode(self.pysave.search("active", path))
        self.color.on_mouse = self.color.convert_str_to_colorcode(self.pysave.search("on_mouse", path))
        self.color.alpha = self.color.convert_str_to_colorcode(self.pysave.search("alpha",path))
        self.color.background = self.color.convert_str_to_colorcode(self.pysave.search("background", path))
    class View:
        def __init__(self, p) -> None:
            self.layer = []
            """layerにView関数を追加してください"""
            self.default_screen = self.Screen(1980, 1080)
            self.screen = pygame.display.set_mode((self.default_screen.w, self.default_screen.h), pygame.FULLSCREEN) 
            self.parent = p
        def draw(self):
            """draw関数はscreenに表示する、関数実行後layerをリセットする"""
            self.screen.fill((30, 30, 30))
            for layer_index in range(100):
                for i in range(len(self.layer)):
                    if layer_index == self.layer[i].layer:
                        if self.layer[i].name == "text" or self.layer[i].name == "blit":
                            pass
                            self.screen.blit(self.parent.font.fontrender_m_s.render(self.layer[i].text, True, self.parent.color.get(self.layer[i].color)), (self.layer[i].rect.x, self.layer[i].rect.y))
                        if self.layer[i].name == "square" or self.layer[i].name == "rect":
                            pygame.draw.rect(self.screen, self.parent.color.get(self.layer[i].color), self.layer[i].rect, self.layer[i].line_width)
                        if self.layer[i].name == "corner" or self.layer[i].name == "cornerbox" or self.layer[i].name == "CornerBox":
                            self.CornerBox(self.screen, self.layer[i].rect, self.parent.color.get(self.layer[i].color), self.layer[i].line_width)
            self.layer = []
            pygame.display.flip()
        def CornerBox(screen, rect, color, line_width, corner = 2):
            if line_width == 0:
                pygame.draw.rect(screen, color, pygame.Rect(rect.x, rect.y, rect.w, rect.h), line_width) # 横
            else:
                pygame.draw.line(screen, color, (rect.x + corner, rect.y), (rect.x + rect.w - corner, rect.y), line_width) # 上のライン
                pygame.draw.line(screen, color, (rect.x + rect.w, rect.y + corner), (rect.x + rect.w, rect.y + rect.h - corner), line_width) # 右のライン
                pygame.draw.line(screen, color, (rect.x + rect.w - corner, rect.y + rect.h), (rect.x + corner, rect.y + rect.h), line_width) # 下のライン
                pygame.draw.line(screen, color, (rect.x, rect.y + rect.h - corner), (rect.x, rect.y + corner), line_width) # 左のライン

                pygame.draw.line(screen, color, (rect.x, rect.y + corner), (rect.x + corner, rect.y), line_width) # 左上のライン
                pygame.draw.line(screen, color, (rect.x + rect.w - corner, rect.y), (rect.x + rect.w, rect.y + corner), line_width)
                pygame.draw.line(screen, color, (rect.x + rect.w, rect.y + rect.h - corner), (rect.x + rect.w - corner, rect.y + rect.h), line_width)
                pygame.draw.line(screen, color, (rect.x + corner, rect.y + rect.h), (rect.x, rect.y + rect.h - corner), line_width)
        class Screen:
            def __init__(self, screen_w, screen_h):
                self.w = screen_w
                self.h = screen_h
        class View:
            """layerに入れる"""
            def __init__(self, name, fontsize, color, rect, layer, text="", line_width=3):
                """color : str、テキストはnameがtextの時のみ"""
                self.name = name
                self.fontsize = fontsize
                self.text = text
                self.color = color
                self.rect = rect
                self.line_width = line_width
                self.layer = layer
    class Color:
        def __init__(self):
            self.inactive = pygame.Color('lightskyblue2')
            self.active = pygame.Color('dodgerblue2')
            self.track = pygame.Color("dodgerblue")
            self.on_mouse = pygame.Color('lightskyblue3')
            self.alpha = pygame.Color(50, 50, 50)
            self.background = pygame.Color(30,30,30)
            self.hold_active = pygame.Color('skyblue2')

            self.goal = pygame.Color('gold')
            self.start = pygame.Color('white')
        def get(self, name) -> pygame.Color:
            """名前で色を取得する"""
            if name == "inactive":
                return self.inactive
            elif name == "active":
                return self.active
            elif name == "on_mouse":
                return self.on_mouse
            elif name == "alpha":
                return self.alpha
            elif name == "background":
                return self.background
            elif name == "hold_active":
                return self.hold_active
            elif name == "goal":
                return self.goal
            elif name == "start":
                return self.start
            elif name == "track":
                return self.track
            else:
                return pygame.Color(name)
        def convert_str_to_colorcode(str) -> int:
            """開発者用"""
            str = str[1:len(str) - 1]
            str = str.replace(" ", "")
            value = 0
            R = G = B = A = ""
            for i in range(len(str)):
                if str[i] == ",":
                    value += 1
                else:
                    if value == 0:
                        R += str[i]
                    elif value == 1:
                        G += str[i]
                    elif value == 2:
                        B += str[i]
                    elif value == 3:
                        A += str[i]
            return int(R), int(G), int(B), int(A)
    class Font:
        def __init__(self):
            self.type = self.Type()
            self.size = self.Size()
            self.fontrender_m_vs = pygame.font.Font(self.type.m, self.size.vs)
            self.fontrender_m_s  = pygame.font.Font(self.type.m, self.size.s)
            self.fontrender_m_m  = pygame.font.Font(self.type.m, self.size.m)
            self.fontrender_m_l  = pygame.font.Font(self.type.m, self.size.l)
        def get(self, arg_type, arg_size) -> pygame.font.Font:
            """arg_type : vs, s, m, l;arg_size : s, m, l;"""
            size = 0
            type_ = "s"
            if arg_size == "vs":
                return self.fontrender_m_vs
            elif arg_size == "s":
                return self.fontrender_m_s
            elif arg_size == "m":
                return self.fontrender_m_m
            elif arg_size == "l":
                return self.fontrender_m_l
            elif type(arg_size) is int:
                size = arg_size
            else:
                print("フォントの指定方法に問題があります")
                return pygame.font.Font(self.type.m, size)
            #if arg_type == "s":
            #    type_ = self.type.s
            #elif arg_type == "m":
            #    type_ = self.type.m
            #elif arg_type == "l":
            #    type_ = self.type.l
            #else:
            #    print("フォントの指定方法に問題があります s m l で指定してください")
            return pygame.font.Font(type_, size)
        class Size:
            def __init__(self):
                self.vs = 8
                self.s = 16
                self.m = 32
                self.l = 46
        class Type:
            def __init__(self) -> None:
                self.s = "font/NotoSansJP-Light.ttf"
                self.m = "font/NotoSansJP-Regular.ttf"
                self.l = "font/NotoSansJP-Medium.ttf"
    class Driver:
        def __init__(self):
            self.img = None
            """ラズベリーパイのみ"""
            self.car = self.Player(1,2,0)
            self.goal = self.XandY(4, 3)
            self.rightclick = self.XandY(-1, -1)
            self.click = self.XandY(-1, -1)
            self.map_len = self.XandY(9, 9)
            self.nav = self.Navigator(self) 
            self.map_box_size = 20
            self.map_box_margin = 10
            self.map = []
            self.create_map()
            self.mapbox = []
            self.traffic = []
        def create_map(self):
            self.map = np.empty((0, self.map_len.x))
            rowsline = np.zeros(self.map_len.x)
            for i in range(self.map_len.x):
                rowsline[i] = np.array(99)
            self.map = np.vstack((self.map, rowsline))
            rowsline = np.zeros(self.map_len.x)
            for i in range(1,self.map_len.y - 1,1):
                for j in range(self.map_len.x):
                    if j == 0:
                        rowsline[j] = 99
                    elif j % 2 == 0 and i % 2 == 0:
                        rowsline[j] = 99
                    elif j == self.map_len.x - 1:
                        rowsline[j] = 99
                    else:
                        rowsline[j] = 0
                self.map = np.vstack((self.map, rowsline))
                rowsline = np.zeros(self.map_len.x)

            rowsline = []
            for i in range(self.map_len.x):
                rowsline.append(99)
            self.map = np.vstack((self.map, rowsline))
        def match_goal(self, arg_x, arg_y):
            return arg_x == self.goal.x and arg_y == self.goal.y
        def match_start(self, arg_x, arg_y):
            return arg_x == self.car.x and arg_y == self.car.y
        class Player:
            def __init__(self, x, y, d):
                self.x = x
                self.y = y
                self.direction = d
        class XandY:
            def __init__(self, x, y) -> None:
                self.x = x
                self.y = y
        class Navigator:
            def __init__(self, parent):
                self.driver = parent
            def Reset(self):
                for y in range(len(self.driver.map)):
                    for x in range(len(self.driver.map[0])):
                        if self.driver.map[y][x] == 99:
                            self.driver.map[y][x] = 99
                        elif self.driver.map[y][x] == 0:
                            self.driver.map[y][x] = 0
                        else:
                            self.driver.map[y][x] = 0
            #数値検索
            def Search(self, value):
                for i in range(len(self.driver.map)):
                    for j in range(len(self.driver.map[0])):
                        if self.driver.map[i][j] == value:
                            return j, i
                return -1, -1
            def DebugDriver1(self, obs_object_value, other_value):
                """前方がobs_object_valueだったら return -1"""
                if self.driver.car.direction == 0:
                    if self.driver.map[self.driver.car.y - 1][self.driver.car.x] == obs_object_value:
                        return -1
                elif self.driver.car.direction == 1:
                    if self.driver.map[self.driver.car.y][self.driver.car.x + 1] == obs_object_value:
                        return -1
                elif self.driver.car.direction == 2:
                    if self.driver.map[self.driver.car.y + 1][self.driver.car.x] == obs_object_value:
                        return -1
                elif self.driver.car.direction == 3:
                    if self.driver.map[self.driver.car.y][self.driver.car.x - 1] == obs_object_value:
                        return -1
                else:
                    return other_value
            # driverの向いてる先の座標
            def SearchDirection(self):
                if self.driver.car.direction == 0:
                    return self.driver.car.x ,self.driver.car.y - 1
                elif self.driver.car.direction == 1:
                    return self.driver.car.x + 1 ,self.driver.car.y
                elif self.driver.car.direction == 2:
                    return self.driver.car.x ,self.driver.car.y + 1
                elif self.driver.car.direction == 3:
                    return self.driver.car.x - 1 ,self.driver.car.y
                else:
                    return -1, -1
            #数値流し
            def MazeWaterValue(self):
                if self.DebugDriver1(99, 0) == -1:
                    print("前方が壁です")
                    return True
                nx, ny = self.SearchDirection()
                self.driver.map[ny][nx] = count = 2
                self.driver.map[self.driver.car.y][self.driver.car.x] = 99
                try:
                    while True:
                        for y in range(len(self.driver.map)):
                            for x in range(len(self.driver.map[0])):
                                if self.driver.map[y][x] == count:
                                    if self.driver.map[y - 1][x] == 0:
                                        self.driver.map[y - 1][x] = count + 1
                                        flag = True
                                    if self.driver.map[y][x + 1] == 0:
                                        self.driver.map[y][x + 1] = count + 1
                                        flag = True
                                    if self.driver.map[y + 1][x] == 0:
                                        self.driver.map[y + 1][x] = count + 1
                                        flag = True
                                    if self.driver.map[y][x - 1] == 0:
                                        self.driver.map[y][x - 1] = count + 1
                                        flag = True
                        count = count + 1
                        if flag == False:
                            break
                        else:
                            flag = False
                    self.driver.map[self.driver.car.y][self.driver.car.x] = 1
                    return False
                except:
                    print("error")
                    return True
            # 最短距離
            def MazeShortestRoute(self):
                gx = self.driver.goal.x
                gy = self.driver.goal.y

                nowvalue = 98
                self.driver.map[gy][gx] = 90
                flag = False
                while True:
                    go = -1
                    if self.driver.map[gy - 1][gx] < nowvalue and self.driver.map[gy - 1][gx] != 0 and self.driver.map[gy - 1][gx] != 1:
                        nowvalue = self.driver.map[gy - 1][gx]
                        go = 0
                        flag = True
                    if self.driver.map[gy][gx + 1] < nowvalue and self.driver.map[gy][gx + 1] != 0 and self.driver.map[gy][gx + 1] != 1 :
                        nowvalue = self.driver.map[gy][gx + 1]
                        go = 1
                        flag = True
                    if self.driver.map[gy + 1][gx] < nowvalue and self.driver.map[gy + 1][gx] != 0 and self.driver.map[gy + 1][gx] != 1:
                        nowvalue = self.driver.map[gy + 1][gx]
                        go = 2
                        flag = True
                    if self.driver.map[gy][gx - 1] < nowvalue and self.driver.map[gy][gx - 1] != 0 and self.driver.map[gy][gx - 1] != 1:
                        nowvalue = self.driver.map[gy][gx - 1]
                        go = 3
                        flag = True

                    if go == 0:
                        nowvalue = self.driver.map[gy - 1][gx]
                        self.driver.map[gy - 1][gx] = 90
                        gy = gy - 1
                    if go == 1:
                        nowvalue = self.driver.map[gy][gx + 1]
                        self.driver.map[gy][gx + 1] = 90
                        gx = gx + 1
                    if go == 2:
                        nowvalue = self.driver.map[gy + 1][gx]
                        self.driver.map[gy + 1][gx] = 90
                        gy = gy + 1
                    if go == 3:
                        nowvalue = self.driver.map[gy][gx - 1]
                        self.driver.map[gy][gx - 1] = 90
                        gx = gx - 1
                    if flag == False and nowvalue != 2:
                        error = 1
                        break
                    if nowvalue == 0:
                        error = 1
                        break
                    if nowvalue == 2:
                        break
                    flag = False
            def PrintArray(self, frame = 0):
                if frame == 1:
                    print("-----------------------------------------------")
                string = ""
                for y in range(len(self.driver.map)):
                    for x in range(len(self.driver.map[0])):
                        if self.driver.map[y][x] < 10:
                            string += " " + str(self.driver.map[y][x]) + ", "
                        elif self.driver.map[y][x] < 100:
                            string += str(self.driver.map[y][x]) + ", "
                    print(string)
                    string = ""
                if frame == 1:
                    print("-----------------------------------------------")
            def DriverDirection(self) -> int:
                """返り値は移動した後のx, y, next d, d"""
                next_direction = -2
                if self.driver.car.direction == 0:
                    if self.driver.map[self.driver.car.y - 1][self.driver.car.x - 1] == 90:
                        next_direction = -1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y - 1
                        self.driver.car.x = self.driver.car.x - 1
                        self.driver.car.direction = 3
                    elif self.driver.map[self.driver.car.y - 1][self.driver.car.x + 1] == 90:
                        next_direction = 1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y - 1
                        self.driver.car.x = self.driver.car.x + 1
                        self.driver.car.direction = 1
                    elif self.driver.map[self.driver.car.y - 2][self.driver.car.x] == 90:
                        next_direction = 0
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.map[self.driver.car.y - 1][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y - 2
                        self.driver.car.x = self.driver.car.x
                        self.driver.car.direction = 0
                elif self.driver.car.direction == 1:
                    if self.driver.map[self.driver.car.y - 1][self.driver.car.x + 1] == 90:
                        next_direction = -1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y - 1
                        self.driver.car.x = self.driver.car.x + 1
                        self.driver.car.direction = 0
                    elif self.driver.map[self.driver.car.y + 1][self.driver.car.x + 1] == 90:
                        next_direction = 1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y + 1
                        self.driver.car.x = self.driver.car.x + 1
                        self.driver.car.direction = 2
                    elif self.driver.map[self.driver.car.y    ][self.driver.car.x + 2] == 90:
                        next_direction = 0
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.map[self.driver.car.y][self.driver.car.x + 1] = 80
                        self.driver.car.y = self.driver.car.y
                        self.driver.car.x = self.driver.car.x + 2
                        self.driver.car.direction = 1
                elif self.driver.car.direction == 2:
                    if self.driver.map[self.driver.car.y + 1][self.driver.car.x + 1] == 90:
                        next_direction = -1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y + 1
                        self.driver.car.x = self.driver.car.x + 1
                        self.driver.car.direction = 1
                    elif self.driver.map[self.driver.car.y + 1][self.driver.car.x - 1] == 90:
                        next_direction = 1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y + 1
                        self.driver.car.x = self.driver.car.x - 1
                        self.driver.car.direction = 3
                    elif self.driver.map[self.driver.car.y + 2][self.driver.car.x] == 90:
                        next_direction = 0
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.map[self.driver.car.y + 1][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y + 2
                        self.driver.car.x = self.driver.car.x
                        self.driver.car.direction = 2
                elif self.driver.car.direction == 3:
                    if self.driver.map[self.driver.car.y + 1][self.driver.car.x - 1] == 90:
                        next_direction = -1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y + 1
                        self.driver.car.x = self.driver.car.x - 1
                        self.driver.car.direction = 2
                    elif self.driver.map[self.driver.car.y - 1][self.driver.car.x - 1] == 90:
                        next_direction = 1
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.car.y = self.driver.car.y - 1
                        self.driver.car.x = self.driver.car.x - 1
                        self.driver.car.direction = 0
                    elif self.driver.map[self.driver.car.y    ][self.driver.car.x - 2] == 90:
                        next_direction = 0
                        self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                        self.driver.map[self.driver.car.y][self.driver.car.x - 1] = 80
                        self.driver.car.y = self.driver.car.y
                        self.driver.car.x = self.driver.car.x - 2
                        self.driver.car.direction = 3
                self.driver.map[self.driver.car.y][self.driver.car.x] = 80
                if next_direction != -2:
                    return self.driver.car.x, self.driver.car.y, next_direction, self.driver.car.direction
                else:
                    return -1, -1, -1, -1
#if __name__ == '__main__':
#   db.driver.nav.Reset()
#   db.driver.nav.MazeWaterValue()
#   db.driver.nav.MazeShortestRoute()
#   db.driver.nav.PrintArray()
#   x, y, nd, d = db.driver.nav.DriverDirection()
#   print("x : " + str(x) + ", y : " + str(y) + ", nd : " + str(nd) + ", d : " + str(d))
#   x, y, nd, d = db.driver.nav.DriverDirection()
#   print("x : " + str(x) + ", y : " + str(y) + ", nd : " + str(nd) + ", d : " + str(d))
#   x, y, nd, d = db.driver.nav.DriverDirection()
#   print("x : " + str(x) + ", y : " + str(y) + ", nd : " + str(nd) + ", d : " + str(d))
#   x, y, nd, d = db.driver.nav.DriverDirection()
#   print("x : " + str(x) + ", y : " + str(y) + ", nd : " + str(nd) + ", d : " + str(d))
#   x, y, nd, d = db.driver.nav.DriverDirection()
#   print("x : " + str(x) + ", y : " + str(y) + ", nd : " + str(nd) + ", d : " + str(d))
#   x, y, nd, d = db.driver.nav.DriverDirection()
#   print("x : " + str(x) + ", y : " + str(y) + ", nd : " + str(nd) + ", d : " + str(d))