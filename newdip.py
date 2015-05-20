#导入模块
import Tkinter as tk
import tkFileDialog
import ImageTk
import Image, ImageDraw, ImageChops, ImageFilter
from tkMessageBox import showinfo
from math import log

#------------------dip类-------------------------
class dip(object):


    def __init__(self, root):

        #self.filename = tkFileDialog.askopenfilename(initialdir =\
         #                                 'C:\Users\Administrator\Desktop\pywin\DIP by python')
        #self.im = Image.open(self.filename)
        self.root = root
        

    def myopen(self):
        try:
            self.filename = tkFileDialog.askopenfilename(initialdir =\
                                          'C:\Users\Administrator\Desktop\pywin\DIP by python')
            self.im = Image.open(self.filename)
            tkImage = ImageTk.PhotoImage(self.im)
            label = tk.Label(framLeft, image = tkImage)
            label.image = tkImage
            label.pack()
        except (IOError,KeyboardInterrupt):
            print '打开失败！请重新检查文件的格式及路径。'

        


    def saveas(self):
        self.savename = tkFileDialog.asksaveasfilename(initialdir = 'C:\Users\Administrator\Desktop\pywin\DIP by python')
        self.propic.save(self.savename)


    def out(self):
        exit()

#---------------------------------------------------

    def showImage(self, title):
        new = tk.Toplevel(self.root, width = 600, height = 500)
        new.title(title)
        tkImage = ImageTk.PhotoImage(self.propic)
        label = tk.Label(new, image = tkImage)
        label.image = tkImage
        label.pack()
        
#---------------------------------------------------

    def point(self):
    
        self.propic = self.im.point(lambda i: 1.2 * i + 10)
        self.showImage('点运算-线性')


    def logp(self):
        
        pixs = self.im.load()
        w, h = self.im.size
        self.propic = Image.new('RGB', (w, h), \
                        (255, 255,255))
        draw = ImageDraw.Draw(self.propic)
        for i in range(w):
            for j in range(h):
                t = pixs[i,j]
                t = tuple(map(lambda i :int(35*log(i + 1)), t))
                #print type(t)
                draw.point([i, j], t)
        
        #new.show()
        
        
        self.showImage('对数运算')
        
    
        #self.propic = Image.eval(lambda i:log(i), self.im)
    

    def offset(self):
        self.propic = self.im.offset(100, 100)
        self.showImage('平移')
        

    def rotate(self):
        self.propic = self.im.rotate(45)
        self.showImage('旋转')

    def reSize(self):
        w, h = self.im.size
        
        self.propic = self.im.resize((w/2, h/2))
        self.showImage('缩放')


    def zhiFang(self):
        
        pixs = self.im.load()
        w, h = self.im.size
        zhiFang = [0] * 256

        for i in range(w):
            for j in range(h):
                p = pixs[i, j]
                p = p[0]
                #print type(p)
                zhiFang[p] += 1
                #print zhiFang

        self.propic = Image.new('RGB', (256, 256), \
                        (255, 255,255))
        #new.show()
        draw = ImageDraw.Draw(self.propic)
        s = max(zhiFang)
        for i in range(256):
            zhiFang[i] = zhiFang[i] * 200 / s
            source = (i, 255)
            target = (i, 255 - zhiFang[i])
            draw.line([source, target], (50, 50, 50))
        self.showImage('直方图')

    def junZhi(self):
        self.propic = self.im.filter(ImageFilter.SMOOTH)
        self.showImage('均值滤波')


    def zhongZhi(self):
        self.propic = self.im.filter(ImageFilter.MedianFilter(3))
        self.showImage('中值滤波')
        
    def ruiHua(self):
        self.propic = self.im.filter(ImageFilter.SHARPEN_LPLS)
        self.showImage('锐化')

    def weiCaiSe(self):
        from random import randint
        
        pixs = self.im.load()
        w, h = self.im.size
        layer = [0] * 256
        for i in range(256):
            layer[i] = (randint(0,255), randint(0,255), randint(0,255))
        
        for i in range(w):
            for j in range(h):
                t = pixs[i,j]
                t = t[0]
                #print t, type(t)
                pixs[i, j] = layer[t]
        self.propic = self.im
        self.showImage('伪彩色')
#--------------------------------------------------------------

    def cut(self):
        pass
    

    def copy(self):
        pass


    def paste(self):
        pass

#---------------------------------------------------------------

    def explain(self):

        showinfo('说明','数字图像处理（bmp格式图片），请选择图片和处理的功能')


    def athor(self):
        showinfo('作者', '''秦绍阳
（昆明理工大学 理学院 电子信息科学与技术121班）
（学号：201211106102）
                            日期：2015/4/29--''')


#---------------------------------------------------

#根窗口
root = tk.Tk()
root.title('DIP by 秦绍阳')
root.geometry('1000x600')



#类实例化
dip = dip(root)



#布局
framLeft = tk.Frame(width = 500,height = 580, bg ='white')
framRight = tk.Frame(width = 490, height = 580, bg = 'white')
framLeft.grid(row = 0, column =0)
framRight.grid(row=0, column = 1)
framLeft.grid_propagate(1)
framRight.grid_propagate(0)
    


#菜单
m = tk.Menu(root)
fmenu = tk.Menu(m)
fmenu.add_command(label = '打开', command= dip.myopen)
fmenu.add_command(label = '另存为', command= dip.saveas)
fmenu.add_command(label = '退出', command= dip.out)
        
emenu = tk.Menu(m)
emenu.add_command(label = '复制', command = dip.copy)
emenu.add_command(label = '粘贴', command = dip.paste)
emenu.add_command(label = '剪切', command = dip.cut)
    
aboutmenu = tk.Menu(m)
aboutmenu.add_command(label = '说明', command = dip.explain)
aboutmenu.add_command(label = '作者', command = dip.athor)
    
m.add_cascade(label = '文件', menu = fmenu)
m.add_cascade(label = '编辑', menu = emenu)
m.add_cascade(label = '关于', menu = aboutmenu)
root['menu'] = m



#按钮功能
tk.Button(framRight, text = '点运算-线性', command = dip.point,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 0,column = 0)
tk.Button(framRight, text = '点运算-对数', command = dip.logp,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 0,column = 1)
tk.Button(framRight, text = '平移', command = dip.offset,\
          bg='blue', fg='white', height = 3, width = 10).grid(row = 1,column = 0)
tk.Button(framRight, text = '旋转', command = dip.rotate,\
          bg='blue', fg='white', height = 3, width = 10).grid(row = 1,column = 1)
tk.Button(framRight, text = '缩放', command = dip.reSize,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 1,column = 2)
tk.Button(framRight, text = '直方图', command = dip.reSize,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 2,column = 0)
tk.Button(framRight, text = '均值滤波', command = dip.junZhi,\
          bg='yellow', fg='black', height = 3, width = 10).grid(row = 3,column = 0)
tk.Button(framRight, text = '中值滤波', command = dip.zhongZhi,\
          bg='yellow', fg='black', height = 3, width = 10).grid(row = 3,column = 1)
tk.Button(framRight, text = '锐化', command = dip.ruiHua,\
          bg='yellow', fg='black', height = 3, width = 10).grid(row = 3,column = 2)
tk.Button(framRight, text = '伪彩色', command = dip.weiCaiSe,\
          bg='green', fg='black', height = 3, width = 10).grid(row = 4,column = 0)


root.mainloop()
       
