import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Point, GraphicException, Color
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from math import sqrt


def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return None
    o = []
    m = dist / steps
    for i in xrange(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o


class DrawingBoard(FloatLayout):
    color = ListProperty([0, 0, 0])
    colors = ObjectProperty(None)
    board = ObjectProperty(None)
    point_size = NumericProperty(5)
    button_move = ObjectProperty(None)
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)

    def on_touch_down(self, touch):
        if super(DrawingBoard, self).on_touch_down(touch):
            return

        touch.grab(self)
        if self.button_move.state == 'down':
            touch.ud['move'] = touch.pos
        else:
            touch.ud['pos'] = touch.x - self.pos_x, touch.y - self.pos_y
            with self.board.canvas:
                Color(self.color[0], self.color[1], self.color[2], mode='rgb')
                touch.ud['points'] = Point(
                        points=(touch.x - self.pos_x, touch.y - self.pos_y),
                        source='particle.png',
                        pointsize=self.point_size)

        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return

        if touch.ud.get('move'):
            self.pos_x += touch.x - touch.ud['move'][0]
            self.pos_y += touch.y - touch.ud['move'][1]

            touch.ud['move'] = touch.pos

        else:
            oldx, oldy = touch.ud['points'].points[-2:]
            points = calculate_points(
                    oldx,
                    oldy,
                    touch.x - self.pos_x,
                    touch.y - self.pos_y,
                    steps=self.point_size)

            touch.ud['pos'] = touch.x - self.pos_x, touch.y - self.pos_y
            if points:
                try:
                    lp = touch.ud['points'].add_point
                    for idx in xrange(0, len(points), 2):
                        lp(points[idx], points[idx+1])
                except GraphicException:
                    pass

        self.canvas.ask_update()

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)


class DrawingBoardApp(App):
    title = 'Touchtracer'
    icon = 'icon.png'

    def build(self):
        return DrawingBoard()

    def on_pause(self):
        return True

if __name__ in ('__main__', '__android__'):
    DrawingBoardApp().run()
