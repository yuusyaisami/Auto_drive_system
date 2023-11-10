import pygame
import pygui
import pydb
# import raspberry
# raspberryパイモジュールはraspberryパイを使用するときのみ呼び出してください
db = pygui.db
print("起動オプション")
is_traffic = False
print("traffic : " + str(is_traffic))
if input("y/n ->") == "y" :
    is_traffic = True
do_system = True
class MainScene:
    def __init__(self):
        self.menu = pygui.MenuBar(pygame.Rect(20, 5, 128, 26), "inactive", 3, True, "s", "n",[["ファイル", "新規作成", "保存", "設定"], ["編集", "壁", "道", "ゴール", "スタート", "信号設置"], ["実行", "Run", "変数表示", "パラメーター表示"]])
        self.boxs = pygui.BoxContainer(pygame.Rect(50, 100, 32, 32), 0)
        self.debug_text = pygui.Text(pygame.Rect(20, 600, 128,32),"inactive", 0, True, "s", "")
        self.debug_text1 = pygui.Text(pygame.Rect(20, 630, 128,32),"inactive", 0, True, "s", "")
        self.driver_item = pygui.DriverMap()
        self.items = [self.menu, self.boxs, self.debug_text,self.debug_text1, self.driver_item]
    def handle_event(self, event):
        for i in self.items:
            i.handle_event(event)


    def update(self):
        for i in self.items:
            i.update()
        self.debug_text.common.text = "x : "  + str(pygui.db.driver.click.x)
        self.debug_text1.common.text = "y : "  + str(pygui.db.driver.click.y)
        parent, child = self.menu.get()
        if parent == "実行" and child == "Run":
            self.driver_item.Run()
        if parent == "編集" and child == "壁" and db.driver.click.x != -1:
            db.driver.map[db.driver.click.y][db.driver.click.x] = 99
        if parent == "編集" and child == "道" and db.driver.click.x != -1:
            db.driver.map[db.driver.click.y][db.driver.click.x] = 0
        if parent == "編集" and child == "ゴール" and db.driver.click.x != -1:
            db.driver.goal.x = db.driver.click.x
            db.driver.goal.y = db.driver.click.y
        if parent == "編集" and child == "スタート" and db.driver.click.x != -1:
            db.driver.car.x = db.driver.click.x
            db.driver.car.y = db.driver.click.y
            
        
    def draw(self):
        for i in self.items:
            i.draw()
main_scene = MainScene()
container = [main_scene]
while do_system:
    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            for c in container:
                c.handle_event(event)
        for c in container:
            c.update()
        for c in container:
            c.draw()
        pygui.db.view.draw()
        clock.tick(60)