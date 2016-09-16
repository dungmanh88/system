#!/usr/bin/python2

from PIL import Image, ImageDraw, ImageFont

class My_image:
  def open(self, path):
    self.img = Image.open(path)
    return True
  def __init__(self):
    self.font = None
    self.img = None
  def setFont(self, font_path, size):
    self.font = ImageFont.truetype(font_path, size)
    return True
  def draw(self, position, text, color, font):
    ImageDraw.Draw(self.img).text(position, text, fill=color, font=font)
    self.img.show()
    self.img.save(text + '_test' + '.jpg')
    return True


if __name__ == '__main__':
  test = My_image()
  test.open("logical_openstack.png")
  test.setFont('ahronbd.ttf',80)
  test.draw((5,5),'Hello\nPillow',(255,0,0),test.font) 


