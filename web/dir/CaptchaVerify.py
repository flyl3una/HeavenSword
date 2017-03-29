#   # encoding:utf-8
# from PIL import Image, ImageDraw, ImageFont
# import random, StringIO
# import os
# from math import ceil
# import base64
#
# current_path = os.path.normpath(os.path.dirname(__file__))
#
#
# class Captcha(object):
#     # 定义一个验证码类，
#     def __init__(self, request):
#         self.django_request = request
#         self.session_key = request.session.session_key
#         self.words = []
#
#         # image size (pix)
#         self.img_width = 150
#         self.img_height = 30
#
#         # default type
#         self.type = 'number'
#
#     def _get_font_size(self):
#         """  将图片高度的80%作为字体大小
#         """
#         s1 = int(self.img_height * 0.8)
#         s2 = int(self.img_width / len(self.code))
#         return int(min((s1, s2)) + max((s1, s2)) * 0.05)
#
#     def _get_words(self):
#         """ The words list
#         """
#         # 扩充单词列表
#         if self.words:
#             return set(self.words)
#
#         file_path = os.path.join(current_path, 'words.list')
#         f = open(file_path, 'r')
#         return set([line.replace('\n', '') for line in f.readlines()])
#
#     def _set_answer(self, answer):
#         """  设置答案
#         """
#         self.django_request.session[self.session_key] = str(answer)
#
#     def _yield_code(self):
#         """  生成验证码数字,以及答案
#         """
#        # 数字公式验证码
#         def number():
#             m, n = 1, 50
#             x = random.randrange(m, n)
#             y = random.randrange(m, n)
#
#             r = random.randrange(0, 2)
#             if r == 0:
#                 code = "%s - %s = ?" % (x, y)
#                 z = x - y
#             else:
#                 code = "%s + %s = ?" % (x, y)
#                 z = x + y
#             self._set_answer(z)
#             return code
#
#         fun = eval(self.type.lower())
#         return fun()
#
#     def display(self):
#         """  把生成的验证码图片改成数据流返回
#         """
#
#         # 字体颜色
#         self.font_color = ['black', 'darkblue', 'darkred']
#
#         # 背景颜色，随机生成
#         self.background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
#
#         # 字体
#         self.font_path = os.path.join(current_path, 'timesbi.ttf')
#         # self.font_path = os.path.join(current_path,'Menlo.ttc')
#
#         # 生成的验证码只做一次验证，就会清空
#         self.django_request.session[self.session_key] = ''
#
#         #　使用 PIL创建画布
#         im = Image.new('RGB', (self.img_width, self.img_height), self.background)
#
#         # 生成验证码
#         self.code = self._yield_code()
#
#         # 设置字体大小
#         self.font_size = self._get_font_size()
#
#         # 实例化一个绘图
#         draw = ImageDraw.Draw(im)
#
#         # 在画布绘图,写验证码
#         if self.type == 'word':
#             c = int(8 / len(self.code) * 3) or 3
#         elif self.type == 'number':
#             c = 4
#
#         for i in range(random.randrange(c - 2, c)):
#             line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
#             xy = (
#                 random.randrange(0, int(self.img_width * 0.2)),
#                 random.randrange(0, self.img_height),
#                 random.randrange(3 * self.img_width / 4, self.img_width),
#                 random.randrange(0, self.img_height)
#             )
#             draw.line(xy, fill=line_color, width=int(self.font_size * 0.1))
#             # draw.arc(xy,fill=line_color,width=int(self.font_size*0.1))
#         # draw.arc(xy,0,1400,fill=line_color)
#         # code part
#         j = int(self.font_size * 0.3)
#         k = int(self.font_size * 0.5)
#         x = random.randrange(j, k)  # starts point
#         for i in self.code:
#             # 上下抖动量,字数越多,上下抖动越大
#             m = int(len(self.code))
#             y = random.randrange(1, 3)
#             if i in ('+', '=', '?'):
#                 # 对计算符号等特殊字符放大处理
#                 m = ceil(self.font_size * 0.8)
#             else:
#                 # 字体大小变化量,字数越少,字体大小变化越多
#                 m = random.randrange(0, int(45 / self.font_size) + int(self.font_size / 5))
#             self.font = ImageFont.truetype(self.font_path.replace('\\', '/'), self.font_size + int(ceil(m)))
#             draw.text((x, y), i, font=self.font, fill=random.choice(self.font_color))
#             x += self.font_size * 0.9
#         del x
#         del draw
#         # 序列化处理
#         buf = StringIO.StringIO()
#         im.save(buf, 'gif')
#         buf.closed
#         data = base64.encodestring(buf.getvalue())
#         return data
#
#     def validate(self, code):
#         """
#         检查用户输入和服务器上的密码是否一致
#         """
#         if not code:
#             return False
#         _code = self.django_request.session.get(self.session_key) or ''
#         self.django_request.session[self.session_key] = ''
#         return _code.lower() == str(code).lower()
#
#     def check(self, code):
#         """
#         检查用户输入和服务器上保存的密码是否一致
#         """
#         return self.validate(code)