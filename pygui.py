import pygame
import pydb

db = pydb.DataBase()
class Text:
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
        self.property = Property(rect, color, layer,  visible, fontsize, text, is_frame)
    def handle_event(self, event):
        pass
    def update(self):
        self.property.rects.update()
    def draw(self):
        db.view.layer.append(db.view.View("text", self.property.fontsize, self.property.color, self.property.rects.rect, self.property.layer, self.property.text))
        if self.property.is_frame:
            db.view.layer.append(db.view.View("rect", self.property.fontsize, self.property.color, self.property.rects.rect, self.property.layer, line_width=2))
class Button:
    def __init__(
            self,
            rect,
            color,
            layer,
            visible,
            fontsize,
            text,
            is_frame,
            ):
        self.property = Property(rect, color, layer, visible, fontsize, text, is_frame)
        self.click_timer = Timer()
        self.handle = Handle_event()
        self.old_click = False
        self.click = False
    def handle_event(self, event):
        if self.property.visible:
            if self.handle.click(event, self.property.rects.rect):
                self.click = True
                self.click_timer.reset()
                self.property.color = "active"
            if self.handle.on_mouse(event, self.property.rects.rect) and not self.click:
                self.property.color = "on_mouse"
            elif not self.click:
                self.property.color = "inactive"

    def update(self):
        self.property.rects.update()
        if self.property.visible:
            if self.click_timer.Do(10):
                self.click = False
                self.property.color = "inactive"
    def draw(self):
        if self.property.visible:
            db.view.layer.append(db.view.View("text", self.property.fontsize, self.property.color, pygame.Rect(self.property.rects.rect.x + 5, self.property.rects.rect.y, self.property.rects.rect.w, self.property.rects.rect.h), self.property.layer, self.property.text, 2))
            if self.property.is_frame:
                db.view.layer.append(db.view.View("rect", self.property.fontsize, self.property.color, self.property.rects.rect, self.property.layer, self.property.text, 2))
    def get(self, only_confirm = False):
        if self.click:
            if only_confirm == False:
                self.click = False
            return True
        return False
    def change_click_get(self):
        if self.old_click != self.click:
            self.old_click = self.click
            return True
        return False
    
class ButtonSwitch:
    def __init__(
            self,
            rect,
            color,
            layer,
            visible,
            fontsize,
            text,
            is_frame,
            ):
        self.property = Property(rect, color, layer, visible, fontsize, text, is_frame)
        self.handle = Handle_event()

        self.click = False
    def handle_event(self, event):
        if self.property.visible:
            if self.handle.click(event, self.property.rects.rect):
                self.click = not self.click
                if self.click:
                    self.property.color = "active"
                else:
                    self.property.color = "inactive"
            if self.handle.on_mouse(event, self.property.rects.rect) and not self.click:
                self.property.color = "on_mouse"
            elif not self.click:
                self.property.color = "inactive"
        elif not self.click:
            self.property.color = "inactive"

    def update(self):
        self.property.rects.update()
    def draw(self):
        if self.property.visible:
            db.view.layer.append(db.view.View("text", self.property.fontsize, self.property.color, pygame.Rect(self.property.rects.rect.x + 5, self.property.rects.rect.y, self.property.rects.rect.w, self.property.rects.rect.h), self.property.layer, self.property.text, 2))
            if self.property.is_frame:
                db.view.layer.append(db.view.View("rect", self.property.fontsize, self.property.color, self.property.rects.rect, self.property.layer, self.property.text, 2))
    def get(self, change_visible_False = False):
        return self.click
    def unclick(self):
        self.click = False
        self.property.color = "inactive"
class InputBox:
    def __init__(self, rect, color, layer, visible, fontsize, text, alpha_text = "", clear_text = False):
        self.property = Property(rect, color, layer, visible, fontsize, text)
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
        self.handle = Handle_event()
    def handle_event(self, event):
        if self.property.visible:
            if self.handle.click(event, self.property.rects.rect):
                self.click = not self.click
                if self.click:
                    self.property.color = "active"
                else:
                    self.property.color = "inactive"
            if self.handle.other_click(event, self.property.rects.rect):
                self.click = False
            if self.handle.Enter_key_down(event) and self.click:
                self.determined_text = self.text
                if self.clear_text:
                    self.text = ""
            if self.handle.BackSpace_key_down(event) and self.click:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    def update(self):
        self.property.rects.update()
        if self.property.visible:
            width = max(200, db.font.get("m", self.property.fontsize).render(self.text, True, db.color.get(self.property.color))).get_width() + 10
            self.property.rects.rect.w = width
    def draw(self):
        if self.property.visible:
            if self.text == "":
                db.view.layer.append(db.view.View("text", self.property.fontsize, "alpha", pygame.Rect(self.property.rects.rect.x + 5, self.property.rects.rect.y + 2, self.property.rects.rect.w,self.property.rects.rect.h), self.property.layer, self.alpha_text))
            else:
                db.view.layer.append(db.view.View("text", self.property.fontsize, self.property.color, pygame.Rect(self.property.rects.rect.x + 5, self.property.rects.rect.y + 2, self.property.rects.rect.w,self.property.rects.rect.h), self.property.layer, self.text))
            db.view.layer.append(db.view.View("rect", self.property.fontsize, self.property.color, self.property.rects.rect, self.property.layer, line_width=0))
class CombineBox:
    def __init__(self, rect, color, layer, visible, fontsize, text = "", elements = ["a", "b", "c"], is_frame = True, parent_visible = True):
        self.property = Property(rect, color, layer, visible, fontsize, text)
        """textはこのCombineBoxの親の名前"""
        self.parent_btn = ButtonSwitch(rect, color, layer, visible, fontsize, text, parent_visible)
        """コンボボックスの親"""
        self.handle = Handle_event()
        self.children_btn = []
        self.frame = rect
        self.parent_visible = parent_visible
        self.create_btn(elements)
    def create_btn(self, elements = []):
        self.max = 0
        """maxはelementsの文字のスクリーン上の長さの最大値を入れるもの"""
        for e in elements:
            if db.font.get("m", self.property.fontsize).render(e, True, db.color.get(self.property.color)).get_width() + 10 > self.max:
                self.max = db.font.get("m", self.property.fontsize).render(e, True, db.color.get(self.property.color)).get_width() + 10
        for i in range(len(elements)):
            self.children_btn.append(Button(pygame.Rect(self.property.rects.rect.x, self.property.rects.rect.y + (i * (self.property.rects.rect.h + 10)) + (self.property.rects.rect.h + 10), self.max, self.property.rects.rect.h), self.property.color, self.property.layer, self.property.visible, self.property.fontsize, elements[i], self.property.is_frame))
        self.frame = pygame.Rect(self.children_btn[0].property.rects.rect.x, self.children_btn[0].property.rects.rect.y, self.max, self.children_btn[len(self.children_btn) - 1].property.rects.rect.y + self.children_btn[len(self.children_btn) - 1].property.rects.rect.h - self.children_btn[0].property.rects.rect.y)    
        for children in self.children_btn:
            children.property.visible = False # 全ての子を非表示にする
        self.parent_btn.unclick() # チェックを外す
    def handle_event(self, event):
        if self.property.visible:
            for children in self.children_btn:
                children.handle_event(event)
            self.frame = pygame.Rect(self.children_btn[0].property.rects.rect.x, self.children_btn[0].property.rects.rect.y, self.max, self.children_btn[len(self.children_btn) - 1].property.rects.rect.y + self.children_btn[len(self.children_btn) - 1].property.rects.rect.h - self.children_btn[0].property.rects.rect.y)
            if self.handle.other_click(event, self.frame):
                for children in self.children_btn:
                    children.property.visible = False # 全ての子を非表示にする
                self.parent_btn.unclick() # チェックを外す
            if self.handle.click(event, self.frame):
                for children in self.children_btn:
                    children.property.visible = False # 全ての子を非表示にする
                self.parent_btn.unclick() # チェックを外す
        if self.property.visible or self.parent_visible:
            self.parent_btn.handle_event(event) 

    def update(self):
        if self.property.visible:
            self.property.rects.update()
            for children in self.children_btn:
                children.property.rects.add = self.property.rects.add
            for children in self.children_btn:
                children.update()
        if self.property.visible or self.parent_visible: 
            self.parent_btn.update()
            if self.parent_btn.get():
                for children in self.children_btn:
                    children.property.visible = self.parent_btn.click
        
    def draw(self):
        if self.property.visible:
            for children in self.children_btn:
                children.draw()
            if not self.property.is_frame and self.children_btn[0].property.visible:
                db.view.layer.append(db.view.View("rect", self.property.fontsize, self.property.color, self.frame, self.property.layer, line_width=2))
        if self.property.visible or self.parent_visible: self.parent_btn.draw()
    def get(self, only_children_name = True):
        """クリックされたchildrenの名前を出力する、クリック検知がされてない場合はFalseを返す 返り値 parent children または children"""
        for children in self.children_btn:
            if children.get():
                if only_children_name:
                    return self.property.text, children.property.text
                return self.property.text, children.property.text
        return False, False

class MenuBar:
    def __init__(self, rect, color, layer, visible, fontsize, text, elements = []):
        """rectは一個のCombineboxのサイズです"""
        self.property = Property(rect, color, layer, visible, fontsize, text)
        self.combine_boxs = []
        self.create_combinebox(elements)
    def create_combinebox(self, elements):
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
            self.combine_boxs.append(CombineBox(pygame.Rect(self.property.rects.rect.x + i * (self.property.rects.rect.w + 10), self.property.rects.rect.y, self.property.rects.rect.w, self.property.rects.rect.h),
                                                self.property.color, self.property.layer, self.property.visible, self.property.fontsize, parent[i], line, self.property.is_frame))
    def handle_event(self, event):
        for com in self.combine_boxs:
            com.handle_event(event)
        for com in self.combine_boxs:
            com.parent_visible = self.property.visible
    def update(self):
        self.property.rects.update()
        for com in self.combine_boxs:
            com.property.rects.add = self.property.rects.add
        for com in self.combine_boxs:
            com.update()
    def draw(self):
        for com in self.combine_boxs:
            com.draw()

    def get(self):
        """クリックされたコンボボックスの親の名前と子の名前を出力します、クリック検知がされなかった場合はFalseが返されます"""
        for com in self.combine_boxs:
            parent_name, child_name = com.get()
            if parent_name != False:
                return parent_name, child_name
        return False, False
class Property:
    def __init__(self, rect, color, layer, visible, fontsize, text = "", is_frame = False):
        """ここのis_frameは全体のことを指す"""
        self.rects = self.Rects(rect)
        self.color = color
        self.layer = layer
        self.visible = visible
        self.fontsize = fontsize
        self.text = text
        self.is_frame = is_frame
    class Rects:
        def __init__(self, rect):
            self.rect = rect
            """通常のrect"""
            self.default = pygame.Rect(rect.x, rect.y, rect.w, rect.h)
            self.add = pygame.Rect(0,0,0,0)
        def update(self):
            """addrect分をrectに代入"""
            self.rect.x = self.default.x + self.add.x
            self.rect.y = self.default.y + self.add.y
            self.rect.w = self.default.w + self.add.w
            self.rect.h = self.default.h + self.add.h
class Timer:
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
            if self.value % goal == 0:
                return True
            return False
class Handle_event:
    def __init__(self):
        pass
    def click(self, event, rect, button_type = "left") -> bool:
        """button_typeはleft、center、rightまたはleft||right"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                if button_type == "left":
                    if event.button == 1: return True
                if button_type == "center":
                    if event.button == 2: return True
                if button_type == "right":
                    if event.button == 3: return True
                if button_type == "left||right":
                    if event.button == 1: return True
                    if event.button == 3: return True
        return False
    def other_click(self, event, rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                return False
            else:
                return True
        return False
    def on_mouse(self, event, rect):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_x, mouse_y): return True
        else: return False
    def any_key_down(self, event):
        if event.type == pygame.KEYDOWN:
            return True
        return False
    def Enter_key_down(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
        return False
    def BackSpace_key_down(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return True
        return False
    
def main():
    clock = pygame.time.Clock()
    menu = MenuBar(pygame.Rect(20, 5, 128, 26), "inactive", 0, True, "s", "n",[["file", "a", "b", "cと思ったらG"], ["edit", "m", "s", "x"]])
    done = False
    while not done:
        for event in pygame.event.get():
            menu.handle_event(event)
        menu.update()
        p, c = menu.get()
        if p != False:
            print(p + ", " + c)
        menu.draw()
        db.view.draw()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()