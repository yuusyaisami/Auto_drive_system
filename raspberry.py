import pygame as pg
import pygui
import numpy as np
import pygame.mouse as ms
import socket
import pydb
import time
import random
from picarx import Picarx
from time import sleep
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import keyboard
class socketclass:
    def __init__(self):
        IPADDR = "10.0.16.70"
        PORT = 5555
        # ソケット作成
        self.sock = socket.socket(socket.AF_INET)
        # サーバーへ接続
        self.sock.connect((IPADDR, PORT))
sockets = socketclass()
pg.init()
db = pygui.db
kernel_5 = np.ones((5,5),np.uint8)
px = Picarx()
px.set_grayscale_reference(1400)
color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,85],'blue':[92,110],'purple':[115,165],'red_2':[165,180]}
gamma067LUT  = np.array([pow(x/255.0 , 2.2) * 255 for x in range(256)], dtype='uint8')

class Car:
    # ルール
    # initialは開始するとき、Trueにして、処理を停止させるときはinitialでない同じ名前の変数をFalseにしてください
    def __init__(self, angle, speed):
        self.angle = angle
        self.speed = speed
        self.black_reflectance = 50
        self.initial_Determined = False # Carの処理を開始するときはこの変数をTrueにする
        self.Determined = False # Carの処理を停止するときはこの変数をFalseにする
        
        self.turned_direction = 0

        self.linetrace = True # ライントレースをするか
        self.backtime = 0
        self.car_direction = 0 # ライントレーサーのTuning処理時に使用する
        
        self.Tuning_start_time = 2
        self.Tuning_start_count = 0
        
        self.do_Tuning = True # コースアウト時チューニング処理を挟むか
        self.Tuning = False 
        self.TuningCount = 0
        
        self.curve = False 
        self.initial_curve = False
        self.curve_count = 0 # ハンドリング時の微調整

        self.aftertreatment = False # コーナー後のちょっとした前進
        self.aftercount = 0
        
        self.back = False
        self.backcount = 0
        
        px.set_camera_servo2_angle(-50)
        px.set_camera_servo1_angle(10)

        # parameter変数
        self.back_count = 25
        self.first_camera_y = 108
        self.curve_angle = 20
        self.camera_angle = -50
        self.red_range = 4

        #text変数
        self.first_catch_color = "0"
        self.state = "とどまる"
    def color_detect(self, img,color_name):
        red_x = []
        red_y = []
        color_dict["red"] = [0, self.red_range]
        # 青色域は照明条件によって異なり、フレキシブルに調整できる。 H：彩度、S：彩度 v：明度
        resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # 計算量を減らすため、画像のサイズを(160,120)に縮小している。
        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # BGRからHSVへの変換
        color_type = color_name

        mask = cv2.inRange(hsv,np.array([min(color_dict[color_type]), 60, 60]), np.array([max(color_dict[color_type]), 255, 255]) ) # inRange()：下/上の間を白、それ以外を黒にする
        if color_type == 'red':
                mask_2 = cv2.inRange(hsv, (color_dict['red_2'][0],0,0), (color_dict['red_2'][1],255,255)) 
                mask = cv2.bitwise_or(mask, mask_2)

        morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5,iterations=1) #画像に対してオープン操作を行う

        # morphologyEx_imgで輪郭を検索し、面積の小さいものから大きいものまで輪郭を並べる。
        _tuple = cv2.findContours(morphologyEx_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)      
        # opencv3.x および openc4.x と互換性がある。
        if len(_tuple) == 3:
            _, contours, hierarchy = _tuple
        else:
            contours, hierarchy = _tuple

        color_area_num = len(contours) # 輪郭の数を数える

        if color_area_num > 0: 
            for i in contours:    # すべての輪郭を縦断する
                x,y,w,h = cv2.boundingRect(i)      # 輪郭を左上隅の座標と認識オブジェクトの幅と高さに分解する。

                # 画像に矩形を描く（画像、左上隅座標、右下隅座標、色、線幅）
                if w >= 8 and h >= 8: # 画像は元のサイズの4分の1に縮小されるため、元の画像に長方形を描いてターゲットを囲もうとすると、x、y、w、hを4倍しなければならない。
                    x = x * 4
                    y = y * 4 
                    w = w * 4
                    h = h * 4
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  # 長方形の枠を描く
                    cv2.putText(img,color_type,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)# キャラクターの説明を追加
                    red_x.append(x + ( w / 2 ))
                    red_y.append(y + ( h / 2 ))

        #      画像  色の数      色のx  色のy
        return img, len(red_x), red_x, red_y

    def update(self, direction, img):
        # イニシャライズ処理
        if self.initial_Determined:
            self.initial_Determined = False
            self.aftertreatment = False
            self.Determined = True
            self.backcount = 0
            # 前進のみの場合 赤テープの部分でコースアウト判定になるので、ライントレースはチューニング処理を入れないことにする
            if direction == 0:
                self.do_Tuning = False
                print("前進")
            print("イニシャライズメイン処理")
            self.state = "linetrace + detect color"
            self.turned_direction = 0
            
        # main処理
        if self.Determined:
            px.set_camera_servo2_angle(self.camera_angle)
            img,redflag,x,y =  self.color_detect(img,'red_2')
            cv2.imshow("color detect camera", img)
            self.LineTrace()
            self.LineTuning()
            # 前進でない場合
            if direction != 0:
                self.After()
            # 前進の時は後処理の前進時間を伸ばす
            else:
                self.After(10)
            self.Curve(direction)
            self.Back()
            for count in range(redflag):
                if y[count] > 160 and not self.curve and not self.aftertreatment and direction != 0 and not self.back:
                    self.back = True
                    self.backtime = y[count]
                    self.first_catch_color = str(y[count]) + ", back"
                if y[count] > self.first_camera_y and not self.curve and not self.aftertreatment:
                    self.first_catch_color = str(y[count]) + ", curve"
                    #前進以外は曲がる処理を必要とする
                    if direction != 0:
                        self.initial_curve = True
                    else:
                        print("detect red")
                        self.aftertreatment = True
        else:
            #処理命令が下されていない場合、数値を初期値にリセットする
            self.linetrace = True # ライントレースをするか

            self.car_direction = 0 # ライントレーサーのTuning処理時に使用する
            self.do_Tuning = True # コースアウト時チューニング処理を挟むか
            self.Tuning = False 
            self.TuningCount = 0

            self.curve = False 
            self.initial_curve = False
            self.curve_count = 0 # ハンドリング時の微調整

            self.aftertreatment = False # コーナー後のちょっとした前進
            self.aftercount = 0

    def Back(self):
        if self.back:
            px.set_dir_servo_angle(0)
            print("back")
            self.backcount += self.back_count
            self.linetrace = False
            px.backward(self.speed)
            if self.backcount > self.backtime / 3:
                self.backcount = 0
                self.back = False
                self.initial_curve = True
                
    def LineTrace(self):
        # ライントレース
        if self.linetrace:
            reflectance = px.get_grayscale_data()
            print(reflectance)
            if reflectance[0] < self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(0)
                self.car_direction = self.Tuning_start_count = 0
            elif reflectance[0] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(-self.angle)
                self.car_direction = -1
                self.Tuning_start_count = 1
            elif reflectance[2] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(self.angle)
                self.car_direction = self.Tuning_start_count = 1
            elif reflectance[0] > self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] > self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(0)
                self.car_direction = 0
            elif not self.Tuning:
                print("tunig")
                if self.do_Tuning:
                    self.Tuning_start_count += 1
                    if self.Tuning_start_count > self.Tuning_start_time:
                        #ラインから外れた tuning処理
                        self.Tuning = True
                        self.linetrace = False
                        self.Tuning_start_count = 0
                        print("Tuning start")
    def LineTuning(self):
        if self.Tuning:
            self.state = "linetuning..."
            on_line = False
            px.forward(self.speed)
            if self.car_direction == -1:
                px.set_dir_servo_angle(-self.angle - 16)
            if self.car_direction == 1:
                px.set_dir_servo_angle(self.angle + 16)
            reflectance = px.get_grayscale_data()
            if reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance:
                self.TuningCount += 1
                on_line = True
            # ラインに復帰する
            if self.TuningCount > 1 or on_line:
                if self.car_direction == -1:
                    px.set_dir_servo_angle(self.angle - 5)
                elif self.car_direction == 1:
                    px.set_dir_servo_angle(-self.angle + 5)
                else:
                    if self.turned_direction == -1:
                        px.set_dir_servo_angle(self.angle - 5)
                    elif self.turned_direction == 1:
                        px.set_dir_servo_angle(-self.angle + 5)
                # 初期値に戻す
                self.state = "linetrace(return) + detect color"
                print("Tuning Stop")
                self.Tuning = False
                self.linetrace = True
                self.TuningCount = 0
        
        
    def Curve(self, direction):
        #コーナーカーブ 初回
        if self.initial_curve and not self.Tuning:
            self.state = "curve"
            if  direction == -1:
                px.forward(self.speed)
                px.set_dir_servo_angle(-self.angle - self.curve_angle)
                self.car_direction = -1
            if direction == 1:
                px.forward(self.speed)
                px.set_dir_servo_angle(self.angle + self.curve_angle)
                self.car_direction = 1
            self.curve = True
            self.initial_curve = not self.initial_curve
            self.do_Tuning = False
            self.linetrace = False
            self.curve_count = 0
            print("Curve start")
            self.turned_direction = direction
        # コーナー処理
        if self.curve:
            reflectance = px.get_grayscale_data()
            self.curve_count += 1
            # ラインに乗ったかつ、初回時から50countした
            if (reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance) and self.curve_count > 8:
                self.curve = False
                self.aftertreatment = True
                self.linetrace = True
                self.do_Tuning = True
                self.aftercount = 0
                self.state = "After"
                print("Curve stop")
            elif self.curve_count > 1000: # 明らかにオーバーしている
                #進行方向を反転させる
                if  direction == 1:
                    px.set_dir_servo_angle(-self.angle - self.curve_angle)
                if direction == -1:
                    px.set_dir_servo_angle(self.angle + self.curve_angle)
                self.state = "over curve"
    def After(self, n = 5):
        if self.aftertreatment:
            self.aftercount += 1
            if self.aftercount > n:
                if not self.Tuning:
                    self.Determined = False
                    px.stop()
                    self.aftercount = 0
                    print("After stop")
                    self.state = "stop"
                else:
                    self.aftercount = 4
# 信号のクラス
class Traffic:
    def __init__(self, rect, w,h, greentime, redtime, direction, map_x, map_y, count = 0):
        self.rect = rect
        self.dx = rect.x
        self.dy = rect.y
        self.dw = w
        self.dh = h
        self.greentime = greentime
        self.redtime = redtime
        self.color = pg.Color('green')
        self.statue = 0
        self.traffic_direction = direction
        self.count = count
        self.map_x = map_x
        self.map_y = map_y
        self.visible = True
    def update(self):
        if self.visible:
            self.count = self.count + 1
            if self.count == self.greentime + self.redtime: # 緑
                self.statue = 0
                self.count = 0 # リセット
                self.color = pg.Color('green')
            elif self.count == self.greentime: # 赤
                self.statue = 1
                self.color = pg.Color('red')
    def draw(self, screen):
        if self.visible:
            # 信号の設置向きによって、座標を変える
            if self.traffic_direction == 0:
                self.rect.y = self.dy - (self.rect.h / 2)
                self.rect.x = self.dx + ((self.dw / 2) - self.rect.w / 2)
            elif self.traffic_direction == 1:
                self.rect.x = self.dx + self.dw - (self.rect.w / 2)
                self.rect.y = self.dy + ((self.dh / 2) - self.rect.h / 2)
            elif self.traffic_direction == 2:
                self.rect.y = self.dy - (self.rect.h / 2) + self.dh
                self.rect.x = self.dx + ((self.dw / 2) - self.rect.w / 2)
            elif self.traffic_direction == 3:
                self.rect.y = self.dy + ((self.dh / 2) - self.rect.h / 2)
                self.rect.x = self.dx - (self.rect.w / 2)
        pg.draw.rect(screen, self.color, self.rect, 0)
    def send(self, sock, command, x, y, direction, stute):
        x = str(x)
        y = str(y)
        direction = str(direction)
        stute = str(stute)
        sock.send(("type:" + command + ",x:" + str(x) + ",y:" + str(y) + ",direction:" + str(direction) + ",stute:" + str(stute)).encode("utf-8"))

## 自動走行のクラス
#class Car:
#    def __init__(self, x, y):
#        self.back_count = 0
#        self.first_camera_y = 0
#        self.curve_angle = 0
#        self.camera_angle = 0
#        self.red_range = 0
#        self.curve_count = 0
#        self.first_catch_color = 19
#        self.Determined = True
#        self.initial_Determined = True
#    def update(self, d, img):
#        pass
class DriverMap:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (528,480)
        self.camera.framerate = 24
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.run = False
        self.car = Car(10,10)
        self.direction = 0
        self.sliders_visible = True
        self.backtime_slider = pygui.SlideBar(pg.Rect(800, 200, 150, 10), "inactive", 1, True, "s", True, 100, 1, 25,title="backtime")
        self.first_camera_slider = pygui.SlideBar(pg.Rect(800, 250, 150, 10), "inactive", 1, True, "s", True, 200, 1, 25,title="first camera")
        self.curve_angle = pygui.SlideBar(pg.Rect(800, 300, 150, 10), "inactive", 1, True, "s", True, 60, 1, 20, title="curve angle")
        self.camera_angle = pygui.SlideBar(pg.Rect(800, 350, 150, 10), "inactive", 1, True, "s", True, 60, 1, 50, title="camera angle") # 本来は-がつく
        self.red_range = pygui.SlideBar(pg.Rect(800, 400, 150, 10), "inactive", 1, True, "s", True, 30, 1, 4, title="red range")
        self.curve_count = pygui.Text(pg.Rect(650, 450, 150, 10), "inactive", 1, True, "s", "curve_count")
        self.first_catch_color_text = pygui.Text(pg.Rect(650, 500, 150, 10), "inactive", 1, True, "s", "first camera")
        self.state_text = pygui.Text(pg.Rect(10, db.view.screen.get_height() - 20, 150, 10), "inactive", 1, True, "vs", "stop")
        self.save_btn = pygui.Button(pg.Rect(840, 450, 52, 32), "inactive", 2, text="save")
        self.load_btn = pygui.Button(pg.Rect(910, 450, 52, 32), "inactive", 2, text="load")
        self.slider = [
            self.backtime_slider, self.first_camera_slider, 
            self.curve_angle, self.camera_angle, 
            self.red_range, self.curve_count, 
            self.first_catch_color_text, 
            self.save_btn, self.load_btn,
            self.state_text,
            ]
    def handle_event(self, event):
        self.slider.handle_event(event)
    def update(self):
        if self.sliders_visible:
            for s in self.slider:
                s.update()
            if self.backtime_slider.get_change_value():
                self.car.back_count = self.backtime_slider.value
            if self.first_camera_slider.get_change_value():
                self.car.first_camera_y = self.first_camera_slider.value
            if self.curve_angle.get_change_value():
                self.car.curve_angle = self.curve_angle.value
            if self.camera_angle.get_change_value():
                self.car.camera_angle = -1 * self.camera_angle.value
            if self.red_range.get_change_value():
                self.car.red_range = self.red_range.value
            self.curve_count.common.text = "curve count " + str(self.car.curve_count)
            self.first_catch_color_text.common.text = "found color posi " + str(self.car.first_catch_color)

            if self.save_btn.clicked():
                self.save()
            if self.load_btn.clicked():
                self.load()
        #--------------------------------------------------自動走行処理--------------------------------------------------
        # 走行RUN
        if self.run:
            if not self.car.Determined:
                if db.driver.traffic.traffic_state(db.driver.car.x, db.driver.car.y, db.driver.car.direction) == "green":
                    db.driver.car.x, db.driver.car.y, self.direction, db.driver.car.direction = db.driver.nav.DriverDirection() # 次の移動先とその方向
                    # 移動が終わったら実行する
                    if self.direction == -2:
                        db.driver.nav.Reset()
                        db.driver.goal.x = db.driver.goal.y = -1
                        db.driver.can_edit = True
                        self.run = False # 処理終了
                    else:
                        self.car.initial_Determined = True
                else:
                    pass
            self.car.update(self.direction,db.driver.img.array)
    def Run(self):
        error = db.driver.nav.MazeWaterValue() # プライオリティーインデックスを振り分ける
        if error:
            return 0
        db.driver.nav.MazeShortestRoute() # マップの最適ルートを検索する
        self.run = True
    def draw(self):
        if self.sliders_visible:
            for s in self.slider:
                s.draw()
    def save(self):
        path = "pydatabase_save.txt"
        db.pysave.add("backtime", self.backtime_slider.value, path)
        db.pysave.add("first camera", self.first_camera_slider.value, path)
        db.pysave.add("curve angle", self.curve_angle.value, path)
        db.pysave.add("camera angle", self.camera_angle.value, path)
        db.pysave.add("red range", self.red_range.value, path)
    def load(self):
        path = "pydatabase_save.txt"
        backtime = db.pysave.search("backtime", path)
        self.car.back_count = int(backtime)
        self.backtime_slider.set_value(int(backtime))

        first_camera = db.pysave.search("first camera", path)
        self.car.first_camera_y = int(first_camera)
        self.first_camera_slider.set_value(int(first_camera))

        curve_angle = db.pysave.search("curve angle", path)
        self.car.curve_angle = int(curve_angle)
        self.curve_angle.set_value(int(curve_angle))

        camera_angle = db.pysave.search("camera angle", path)
        self.car.camera_angle = int(camera_angle)
        self.camera_angle.set_value(int(camera_angle))

        red_range = db.pysave.search("red range", path)
        self.car.red_range = int(red_range)
        self.red_range.set_value(int(red_range))
