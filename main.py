import pygui
import pygame
db = pygui.db
print("起動オプション")
is_traffic = False
print("traffic : " + str(is_traffic))
if input("y/n -> ") == "y":
    is_traffic = True
do_system = True
class Box:
    def __init__(self, rect, color, layer, visible, fontsize, map_x, map_y):
        self.property = pygui.Property(rect, color, layer, visible, fontsize)
        self.handle = pygui.Handle_event()
        self.x = map_x
        self.y = map_y
        self.width = 0
    def handle_event(self, event):
        if self.property.visible:
            if self.handle.click(event, self.property.rects.rect):
                db.driver.click.x = self.x
                db.driver.click.y = self.y
            if self.handle.other_click(event, self.property.rects.rect):
                if db.driver.click.x == self.x and db.driver.click.y == self.y:
                    db.driver.click.x = db.driver.click.y = -1
    def update(self):
        if self.property.visible:
            if db.driver.map[self.y][self.x] == 99:
                self.width = 0
            elif db.driver.goal.x == self.x and db.driver.goal.y == self.y:
                self.property.color ="goal"
                self.width = 2
            elif db.driver.car.x == self.x and db.driver.car.y == self.y:
                self.property.color = "start"
                self.width = 2
            else :
                self.property.color = "inactive"
                self.width = 2
    def draw(self):
        if self.property.visible:
            db.view.layer.append(db.view.View("rect", self.property.fontsize, self.property.color, self.property.rects.rect, self.property.layer, "", self.width))
class Boxes:
    def __init__(self, rect, color, layer, visible, fontsize):
        self.property = pygui.Property(rect, color, layer, visible, fontsize)
    def create_boxes(self):
        db.driver.mapbox = []
        for i in range(db.driver.map_len):
            line = []
            for j in range(db.driver.map_len):
                line.append(Box(pygame.Rect(self.property.rects.rect.x + j * self.p)))
    def handle_event(self, event):
        

class MainScene:
    def __init__(self) -> None:
        self.menu = pygui.MenuBar(pygame.Rect(20, 2, 100, 24), "inactive", 0, True, "s", "any", [["ファイル", "新規作成", "保存", "設定"], ["編集", "壁", "道", "ゴール", "スタート"]])
    def handle_event(self, event):
        self.menu.handle_event(event)
    def update(self):
        self.menu.update()
    def draw(self):
        self.menu.draw()
main_scene = MainScene()

lists = [main_scene]
while do_system:
    for event in pygame.event.get():
        for l in lists:
            l.handle_event(event)
    for l in lists:
        l.update()
    for l in lists:
        l.draw()
    db.view.draw()