import pygame
import pydb
# Databaseのインスタンスを作成
db = pydb.DataBase()

# 多くのGUIItemに共通するClass
class Common:
    """Commonクラスはitemに付属する、基本的な変数を集めた構造体です"""
    def __init__(self, rect, color, layer, visible, fontsize, text = "", is_frame = False):
        self.rects = self.Rects(rect)
        self.color = color
        self.layer = layer
        self.visible = visible
        self.fontsize = fontsize
        self.text = text
        self.is_frame = is_frame
    class Rects:
        """RectsクラスはCommonクラスで扱うrectの汎用性を高めるために作成されます"""
        def __init__(self, rect):
            self.rect = rect
            """通常のrect、読み取り専用"""
            self.default = pygame.Rect(rect.x, rect.y, rect.w, rect.h)
            """最初に受け取った時の数値"""
            self.add = pygame.Rect(0,0,0,0)
            """rectの位置を動かすときに使います"""
        def update(self):
            """addrect分をrectに代入"""
            self.rect.x = self.default.x + self.add.x
            self.rect.y = self.default.y + self.add.y
            self.rect.w = self.default.w + self.add.w
            self.rect.h = self.default.h + self.add.h
class Timer:
    """Timerクラスは、itemにアニメーションなどゲームの時間処理時に使用されます"""
    def __init__(
            self,
            type = "onetime",
            count_increase = 1,
            count_first = 0,
            visible = True,
            ):
        self.visible = visible
        self.type = type
        self.count = self.Count(count_increase, count_first)
    def Do(self, goal_value):
        """Do関数は引数で渡した数値とDo関数内で追加されていくcount.valueが一致したときtrueを返します"""
        if self.visible:
            self.count.update()
            if self.count.Do(goal_value):
                if self.type == "onetime":
                    self.count.value = self.count.first
                    self.visible = False
                return True
        return False
    def reset(self, change_visible = True):
        self.count.value = self.count.first
        self.visible = change_visible
    class Count:
        def __init__(self, increase, first):
            self.increase = increase
            self.first = first
            self.value = first
        def update(self):
            self.value += self.increase
        def Do(self, goal):
            return self.value % goal == 0
# Handle_event関数内で使用されるであろう関数
class Handle:
    def click(self, event, rect, button_type = "left") -> bool:
        """button_typeはleft、center、rightまたはleft||right"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                if button_type == "left":
                    return event.button == 1
                if button_type == "center":
                    return event.button == 2
                if button_type == "right":
                    return event.button == 3
                if button_type == "left||right":
                    if event.button == 1: return True
                    if event.button == 3: return True
        return False
    def click_up(self, event, rect, button_type = "left"):
        if event.type == pygame.MOUSEBUTTONUP:
                if button_type == "left":
                    return event.button == 1
                if button_type == "center":
                    return event.button == 2
                if button_type == "right":
                    return event.button == 3
                if button_type == "left||right":
                    if event.button == 1: return True
                    if event.button == 3: return True
    def mouse_press(self):
        mouse_buttons = pygame.mouse.get_pressed()
        left_button, middle_button, right_button = mouse_buttons
        return left_button
    def other_click(self, event, rect):
        return event.type == pygame.MOUSEBUTTONDOWN and not rect.collidepoint(event.pos)
    def on_mouse(self, event, rect):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_x, mouse_y): return True
        else: return False
    def any_key_down(self, event):
        return event.type == pygame.KEYDOWN
    def Enter_key_down(self, event):
        return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
    def BackSpace_key_down(self, event):
        return event.key == pygame.K_BACKSPACE and event.type == pygame.KEYDOWN
handle = Handle()
class Square:
    def __init__(self,rect, color, layer, visible, fontsize, width):
        self.common = Common(rect, color, layer, visible, fontsize)
        self.width = width
        self.active = False
        self.posi_at_click_down = self.XandY(0,0)
        self.posi_mouse_move_differ = self.XandY(0,0)

        self.mouse_differ_x = 0
        self.value = 0
    def handle_event(self, event):
        if handle.click(event, self.common.rects.rect):
            self.active = True
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.posi_at_click_down.x = mouse_x
            self.posi_at_click_down.y = mouse_y
        if handle.click_up(event, self.common.rects.rect):
            self.active = False
        if handle.mouse_press():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.posi_mouse_move_differ.x =  mouse_x - self.posi_at_click_down.x
            self.posi_mouse_move_differ.y =  mouse_y - self.posi_at_click_down.y
    def update(self):
        if self.common.visible:
            if self.active:
                self.color = "active"
            else:
                self.color = "hold_active"
    def draw(self):
        self.common.rects.add.x = self.mouse_differ_x
        db.view.layer.append(db.view.View("rect", color=self.common.color, rect=self.common.rects.rect, layer=self.common.layer, line_width=self.width, fontsize="s", ))
    def check_active(self):
        return self.active
    class XandY:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    def set_add_rect(self, x):
        self.mouse_differ_x = x
class Text:
    """テキストを表示する"""
    def __init__(
            self,
            rect,
            color,
            layer,
            visible,
            fontsize,
            text,
            is_frame = False,
            ):
        self.common = Common(rect, color, layer,  visible, fontsize, text, is_frame)
    def handle_event(self, event):
        pass
    def update(self):
        self.common.rects.update()
    def draw(self):
        db.view.layer.append(db.view.View("text", self.common.fontsize, self.common.color, self.common.rects.rect, self.common.layer, self.common.text))
        if self.common.is_frame:
            db.view.layer.append(db.view.View("rect", self.common.fontsize, self.common.color, self.common.rects.rect, self.common.layer, line_width=2))

class Button:
    """ボタンを表示します"""
    def __init__(self, rect, color = "inactive", layer = 1, visible = True, fontsize = "s", text = "", is_frame = True):
        self.common = Common(rect, color, layer,  visible, fontsize, text, is_frame)
        self.__click_timer = Timer()
        self.click = False
        self.click_count = 0
    def handle_event(self, event):
        if self.common.visible:
            if handle.click(event, self.common.rects.rect):
                self.click = True
                self.__click_timer.reset()
                self.common.color = "active"
            if handle.on_mouse(event, self.common.rects.rect):
                self.common.color = "on_mouse"
            elif not self.click:
                self.common.color = "inactive"
    def update(self):
        self.common.rects.update()
        if self.__click_timer.Do(10):
            self.click = False
            self.common.color = "inactive"
    def draw(self):
        if self.common.visible:
            db.view.layer.append(db.view.View("text", self.common.fontsize, self.common.color, pygame.Rect(self.common.rects.rect.x + 5, self.common.rects.rect.y, self.common.rects.rect.w, self.common.rects.rect.h), self.common.layer, self.common.text, 2))
            if self.common.is_frame:
                db.view.layer.append(db.view.View("rect", self.common.fontsize, self.common.color, self.common.rects.rect, self.common.layer, self.common.text, 2))
    def clicked(self):
        if self.click:
            self.click = False
            self.click_count += 1
            return True
        return False
    def clicked_count(self):
        return self.click_count
class ButtonSwitch:
    def __init__(self, rect, color, layer, visible, fontsize, text, is_frame):
        self.common = Common(rect, color, layer, visible, fontsize, text, is_frame)
        self.click = False
    def handle_event(self, event):
        if self.common.visible:
            if handle.click(event, self.common.rects.rect):
                self.click = not self.click
                if self.click:
                    self.common.color = "active"
                else:
                    self.unclick()
            if handle.on_mouse(event, self.common.rects.rect) and not self.click:
                self.common.color = "on_mouse"

    def update(self):
        self.common.rects.update()
    def draw(self):
        if self.common.visible:
            db.view.layer.append(db.view.View("text", self.common.fontsize, self.common.color, pygame.Rect(self.common.rects.rect.x + 5, self.common.rects.rect.y, self.common.rects.rect.w, self.common.rects.rect.h), self.common.layer, self.common.text, 2))
            if self.common.is_frame:
                db.view.layer.append(db.view.View("rect", self.common.fontsize, self.common.color, self.common.rects.rect, self.common.layer, self.common.text, 2))
    def clicked(self, change_visible_False = False):
        if change_visible_False:
            self.click = False
        return self.click
    def unclick(self):
        self.click = False
        self.common.color = "inactive"
class InputBox:
    def __init__(self, rect, color, layer, visible, fontsize, text, alpha_text = "", clear_text = False):
        self.common = Common(rect, color, layer, visible, fontsize, text)
        """テキストは初期のテキストです"""
        self.alpha_text = alpha_text
        """ボックス内のテキストが空白だった場合表示する文字です"""
        self.click = False
        self.text = ""
        """ボックス内のテキストです"""
        self.determined_text = ""
        """エンターキーが入力されたときに収納されるテキストです"""
        self.clear_text = clear_text
        """エンターキーが入力されたときにテキスト内を空白にする設定"""
    def handle_event(self, event):
        if self.common.visible:
            if handle.click(event, self.common.rects.rect):
                self.click = not self.click
                if self.click:
                    self.common.color = "active"
                else:
                    self.common.color = "inactive"
            if handle.other_click(event, self.common.rects.rect):
                self.click = False
            if handle.Enter_key_down(event) and self.click:
                self.determined_text = self.text
                if self.clear_text:
                    self.text = ""
            if handle.BackSpace_key_down(event) and self.click:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    def update(self):
        self.common.rects.update()
        if self.common.visible:
            width = max(200, db.font.get("m", self.common.fontsize).render(self.text, True, db.color.get(self.common.color))).get_width() + 10
            self.common.rects.rect.w = width
    def draw(self):
        if self.common.visible:
            if self.text == "":
                db.view.layer.append(db.view.View("text", self.common.fontsize, "alpha", pygame.Rect(self.common.rects.rect.x + 5, self.common.rects.rect.y + 2, self.common.rects.rect.w,self.common.rects.rect.h), self.common.layer, self.alpha_text))
            else:
                db.view.layer.append(db.view.View("text", self.common.fontsize, self.common.color, pygame.Rect(self.common.rects.rect.x + 5, self.common.rects.rect.y + 2, self.common.rects.rect.w,self.common.rects.rect.h), self.common.layer, self.text))
            db.view.layer.append(db.view.View("rect", self.common.fontsize, self.common.color, self.common.rects.rect, self.common.layer, line_width=0))
class CombineBox:
    def __init__(self, rect, color, layer, visible, fontsize, text = "", elements = ["a", "b", "c"], parent_frame = True, child_frame = True, cant_edit = False):
        """textは親の名前 elementsはchildの名前"""
        self.common = Common(rect, color, layer, visible, fontsize, text)
        self.parent_btn = ButtonSwitch(rect, color, layer, visible, fontsize, text, is_frame=parent_frame)
        self.child_btn = []
        self.__frame = rect
        self.timer = Timer(visible=False)
        self.create_btn(elements, child_frame)
    def create_btn(self, elements = [], frame = False):
        self.__max = 0
        """__maxはelementsの文字のスクリーン上の長さの最大値を入れるもの"""
        # スクリーン上の最大横幅を求める
        for e in elements:
            if db.font.get("m", self.common.fontsize).render(e, True, db.color.get(self.common.color)).get_width() + 10 > self.__max:
                self.__max = db.font.get("m", self.common.fontsize).render(e, True, db.color.get(self.common.color)).get_width() + 10
        # ボタンの位置を求める
        for i in range(len(elements)):
            self.child_btn.append(Button(pygame.Rect(self.common.rects.rect.x, self.common.rects.rect.y + (i * (self.common.rects.rect.h + 10)) + (self.common.rects.rect.h + 10), self.__max, self.common.rects.rect.h), self.common.color, self.common.layer, self.common.visible, self.common.fontsize, elements[i], frame))
        self.__frame = pygame.Rect(self.child_btn[0].common.rects.rect.x, self.child_btn[0].common.rects.rect.y, self.__max, self.child_btn[len(self.child_btn) - 1].common.rects.rect.y + self.child_btn[len(self.child_btn) - 1].common.rects.rect.h - self.child_btn[0].common.rects.rect.y)    
        for child in self.child_btn:
            child.common.visible = False
    def handle_event(self, event):
        if self.common.visible:
            for child in self.child_btn:
                child.handle_event(event)
            self.frame = pygame.Rect(self.child_btn[0].common.rects.rect.x, self.child_btn[0].common.rects.rect.y, self.__max, self.child_btn[len(self.child_btn) - 1].common.rects.rect.y + self.child_btn[len(self.child_btn) - 1].common.rects.rect.h - self.child_btn[0].common.rects.rect.y)
        if handle.other_click(event, self.common.rects.rect):
            self.timer.reset()
        if self.common.visible:
            self.parent_btn.handle_event(event) 
    def update(self):
        if self.common.visible:
            self.common.rects.update()
            for child in self.child_btn:
                child.common.rects.add = self.common.rects.add
            for child in self.child_btn:
                child.update()
            if not self.parent_btn.clicked():
                for child in self.child_btn:
                    child.common.visible = False
                self.parent_btn.unclick()
            self.parent_btn.update()
            if self.parent_btn.clicked():
                if self.parent_btn.click:
                    db.driver.can_edit = False
                for child in self.child_btn:
                    child.common.visible = self.parent_btn.click
            if self.timer.Do(2):
                for child in self.child_btn:
                    child.common.visible = False
                self.parent_btn.unclick()
                db.driver.can_edit = True
                self.timer.reset(False)
    def draw(self):
        if self.common.visible:
            for children in self.child_btn:
                children.draw()
            if self.child_btn[0].common.visible:
                db.view.layer.append(db.view.View("rect", self.common.fontsize, "background", self.frame, self.common.layer - 1, line_width=0))
            if not self.common.is_frame and self.child_btn[0].common.visible:
                db.view.layer.append(db.view.View("rect", self.common.fontsize, self.common.color, self.frame, self.common.layer, line_width=2))
        if self.common.visible: self.parent_btn.draw()
    def get(self):
        """クリックされたchildの名前を出力する、クリック検知がされてない場合はFalseを返す 返り値 parent child または child"""
        for child in self.child_btn:
            if child.clicked():
                return self.common.text, child.common.text
        return False, False

class MenuBar:
    def __init__(self, rect, color, layer, visible, fontsize, text, elements = [], parent_frame = False, child_frame = False):
        self.common = Common(rect, color, layer, visible, fontsize, text, parent_frame)
        self.combine_boxs = []
        self.create_combinebox(elements, child_frame)

    def create_combinebox(self, elements, frame):
        parent = []
        child = []
        for combine_num in range(len(elements)):
            parent.append(elements[combine_num][0])
            line = []
            for i in range(1, len(elements[combine_num])):
                line.append(elements[combine_num][i])
            child.append(line)
        for i in range(len(parent)):
            line = []
            for j in range(len(child[i])):
                line.append(child[i][j])
            self.combine_boxs.append(CombineBox(pygame.Rect(self.common.rects.rect.x + i * (self.common.rects.rect.w + 10), self.common.rects.rect.y, self.common.rects.rect.w, self.common.rects.rect.h),
                                                self.common.color, self.common.layer, self.common.visible, self.common.fontsize, parent[i], line, parent_frame=self.common.is_frame, child_frame=frame))
    def handle_event(self, event):
        if self.common.visible:
            for com in self.combine_boxs:
                com.handle_event(event)
    def update(self):
        self.common.rects.update()
        for com in self.combine_boxs:
            com.common.rects.add = self.common.rects.add
        for com in self.combine_boxs:
            com.update()
    def draw(self):
        if self.common.visible:
            for com in self.combine_boxs:
                com.draw()
    def get(self):
        """クリックされたコンボボックスの親の名前と子の名前を出力します、クリック検知がされなかった場合はFalseが返されます"""
        for com in self.combine_boxs:
            parent_name, child_name = com.get()
            if parent_name != False:
                return parent_name, child_name
        return False, False
class SlideBar:
    def __init__(self, rect, color, layer, visible, fontsize, is_view_value = False, max_value = 100, min_value = 0, value = 0, small_change = 1, height = 10, handle_size = 20):
        self.common = Common(rect, color, layer, visible, fontsize, str(value), False)
        self.max_value = max_value
        self.min_value = min_value
        self.value = value
        self.__is_view_value = is_view_value
        self.small_change = small_change
        self.text = Text(rect=pygame.Rect(self.common.rects.rect.x + self.common.rects.rect.w + 12, self.common.rects.rect.y - 8, self.common.rects.rect.w, self.common.rects.rect.h), color=color, layer=layer, visible=True, fontsize=fontsize, text=str(value))
        self.bar = Square(rect=pygame.Rect(self.common.rects.rect.x + height / 2, self.common.rects.rect.y, self.common.rects.rect.w - height / 2, self.common.rects.rect.h), color=self.common.color, layer=1, visible=True, width=0, fontsize=fontsize)
        self.handle =  self.Square(rect=pygame.Rect(self.common.rects.rect.x - height / 2 , self.common.rects.rect.y - handle_size + (self.common.rects.rect.h * 1.5), handle_size, handle_size), color=self.common.color, layer=2, visible=True, width=0, fontsize=fontsize)
    def handle_event(self, event):
        if self.common.visible:
            self.handle.handle_event(event, self.bar.common.rects.rect.x)
            if self.handle.check_active():
                if (self.handle.posi_mouse_move_differ.x % self.max_value) % self.small_change == 0:
                    self.value = int(self.handle.posi_mouse_move_differ.x * ( self.max_value / self.bar.common.rects.rect.w))
                if self.value > self.max_value:
                    self.value = self.max_value
                if self.value < 0:
                    self.value = 0
                print(self.value)
    def update(self):
        self.handle.update(self.value, self.max_value, self.bar.common.rects.rect.w)
        self.bar.update()
        self.text.common.text = str(self.value)
    def draw(self):
        if self.common.visible:
            self.bar.draw()
            self.handle.draw()
            if self.__is_view_value:
                self.text.draw()
    def get_value(self) -> int:
        """現在の数値を取得する"""
        return self.value
    class Square:
        def __init__(self,rect, color, layer, visible, fontsize, width):
            self.common = Common(rect, color, layer, visible, fontsize)
            self.width = width
            self.active = False
            self.posi_at_click_down = self.XandY(0,0)
            self.posi_mouse_move_differ = self.XandY(0,0)

            self.mouse_differ_x = 0
            self.value = 0
        def handle_event(self, event, bar_x):
            if handle.click(event, self.common.rects.rect):
                self.active = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.posi_at_click_down.x = mouse_x
                self.posi_at_click_down.y = mouse_y
            if handle.click_up(event, self.common.rects.rect):
                self.active = False
            if handle.mouse_press() and self.active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.posi_mouse_move_differ.x =  mouse_x - bar_x
                self.posi_mouse_move_differ.y =  mouse_y - self.posi_at_click_down.y
        def update(self, value, max, width):
            if self.common.visible:
                if self.active:
                    self.common.color = "active"
                else:
                    self.common.color = "hold_active"
                add = (width / max) * value
                self.common.rects.add.x = int(add)
                self.common.rects.update()
        def draw(self):
            self.common.rects.add.x = self.mouse_differ_x
            db.view.layer.append(db.view.View("rect", color=self.common.color, rect=self.common.rects.rect, layer=self.common.layer, line_width=self.width, fontsize="s", ))
        def check_active(self):
            return self.active
        class XandY:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        def set_add_rect(self, x):
            self.mouse_differ_x = x









# AutoNavGuis
class Box:
    def __init__(self, rect, x, y, visible = True, layer=0):
        self.map = self.map_data(x, y)
        self.common = Common(rect, "inactive", layer, visible, "s")
        self.width = 0

    def handle_event(self, event):
        if self.common.visible:
            if handle.click(event, self.common.rects.rect, "left") and db.driver.can_edit:
                db.driver.click.x = self.map.x
                db.driver.click.y = self.map.y
            if handle.click(event, self.common.rects.rect, "right"):
                db.driver.rightclick.x = self.map.x
                db.driver.rightclick.y = self.map.y
            #elif handle.other_click(event, self.common.rects.rect) and self.check_select_me():
            #    db.driver.click.x = db.driver.click.y = -1
    def check_select_me(self):
        return db.driver.click.x == self.map.x and db.driver.click.y == self.map.y
    def check_selectbox(self):
        return not db.driver.click.x == -1
    def update(self):
        if self.common.visible:
            self.common.rects.update()
            self.width = 0
            if db.driver.match_goal(self.map.x, self.map.y):
                self.common.color = "goal"
            elif db.driver.match_start(self.map.x, self.map.y):
                self.common.color = "start"
            elif self.check_select_me():
                self.common.color = "active"
            elif db.driver.map[self.map.y][self.map.x] == 80:
                self.common.color = "track"
            elif db.driver.map[self.map.y][self.map.x] == 90:
                self.common.color = "hold_active"
            else:
                self.common.color = "inactive"
            if db.driver.map[self.map.y][self.map.x] == 99:
                self.width = 0
            else:
                self.width = 2
    def draw(self):
        db.view.layer.append(db.view.View("rect", color=self.common.color, fontsize="s", rect=self.common.rects.rect, layer=self.common.layer, line_width=self.width))
    class map_data:
        def __init__(self, x, y):
            self.x = x
            self.y = y
class BoxContainer:
    def __init__(self, rect, layer):
        map_list = []
        self.common = Common(rect, color="inactive", layer=layer, visible=True,fontsize="s")
        self.create_map()
        self.move_active = False
    def handle_event(self, event):
        for r in db.driver.mapbox:
            r.handle_event(event)
    def update(self):
        self.common.rects.update()
        for r in db.driver.mapbox:
            r.common.rects.add = self.common.rects.add
            r.update()
    def draw(self):
        for r in db.driver.mapbox:
            r.draw()
    def create_map(self):
        for r in range(len(db.driver.map)):
            for c in range(len(db.driver.map[r])):
                db.driver.mapbox.append(Box(pygame.Rect(c * db.driver.map_box_size + c * db.driver.map_box_margin + self.common.rects.rect.x, r * db.driver.map_box_size + r * db.driver.map_box_margin + self.common.rects.rect.y, db.driver.map_box_size, db.driver.map_box_size), c, r, self, self.common.layer))

# 自動走行のクラス
class DriverMap:
    def __init__(self):
        self.run = False
        self.direction = 0
        self.RunTime = Timer("cycle", visible=False)
    def handle_event(self, event):
        pass
    def update(self):
        #--------------------------------------------------自動走行処理--------------------------------------------------
        # 走行RUN
        if self.run:
            if self.RunTime.Do(60):
                db.driver.car.x, db.driver.car.y, self.direction, db.driver.car.direction = db.driver.nav.DriverDirection() # 次の移動先とその方向
                # 移動が終わったら実行する
                if self.direction == -1:
                    db.driver.nav.Reset()
                    db.driver.goal.x = db.driver.goal.y = -1
                    db.driver.can_edit = True
                    self.run = False # 処理終了
                    self.RunTime.reset(False)
    def Run(self):
        error = db.driver.nav.MazeWaterValue() # プライオリティーインデックスを振り分ける
        db.driver.can_edit = False
        if error:
            print("error 0")
            return 0
        db.driver.nav.MazeShortestRoute() # マップの最適ルートを検索する
        self.run = True
        self.RunTime.reset()
    def draw(self):
        pass
def main():
    clock = pygame.time.Clock()
    slidebar = SlideBar(pygame.Rect(20, 30, 200, 10), "inactive", 0, True, "s", True,max_value=100)
    menu = MenuBar(pygame.Rect(20, 5, 128, 26), "inactive", 50, True, "s", "n",[["file", "a", "b", "cと思ったらG"], ["edit", "m", "s", "x"]])
    
    done = False
    while not done:
        for event in pygame.event.get():
            menu.handle_event(event)
            slidebar.handle_event(event)
        menu.update()
        slidebar.update()
        menu.draw()
        db.view.draw()
        slidebar.draw()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()