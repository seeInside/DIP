﻿#导入模块

import Tkinter as tk
import tkFileDialog
import ImageTk
import Image, ImageDraw, ImageChops, ImageFilter
from tkMessageBox import showinfo
from math import log
import cv


#------------------dip类-------------------------
class dip(object):


    def __init__(self, root):

        #self.filename = tkFileDialog.askopenfilename(initialdir =\
         #                                 'C:\Users\Administrator\Desktop\pywin\DIP by python')
        #self.im = Image.open(self.filename)
        self.root = root
    
        

    def myopen(self):
        def show():
            tkImage = ImageTk.PhotoImage(self.im)
            label = tk.Label(framLeft, image = tkImage)
            label.image = tkImage
            label.grid(row = 0, column = 0)
        try:
            try:
                w, h = self.im.size
                self.im = Image.new('RGB', (w, h), \
                        (255, 255,255))
                show()
            except (AttributeError):
                pass
            self.filename = tkFileDialog.askopenfilename(initialdir =\
                                          'C:\Users\Administrator\Desktop\pywin\DIP by python')
            self.im = Image.open(self.filename)
            show()
            
            
        except (IOError,KeyboardInterrupt):
            print '打开失败！请重新检查文件的格式及路径。'
        
        self.fourier()

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
                s = tuple(map(lambda i :int(35*(log(i + 1))), t))
                #print type(t)
                draw.point([i, j], s)
        
        #new.show()
        
        
        self.showImage('对数运算')
        
    
        #self.propic = Image.eval(lambda i:log(i), self.im)

    def twoTrans(self):
        
        pixs = self.im.load()
        w, h = self.im.size
        self.propic = Image.new('RGB', (w, h), \
                        (255, 255,255))
        draw = ImageDraw.Draw(self.propic)
        
        for i in range(w):
            for j in range(h):
                t = pixs[i,j]
                if t[0] <= 127:
                    s = (0,0,0)
                else:
                    s = (255, 255, 255)
                #print type(t)
                draw.point([i, j], s)
        self.showImage('二值化')
                
        
    

    def offset(self):

        x = int(getOffsetx.get())
        y = int(getOffsety.get())
        self.propic = self.im.offset(x, y)
        self.showImage('平移')
        

    def rotate(self):
        r = float(getRotate.get())
        self.propic = self.im.rotate(r)
        self.showImage('旋转')

    def reSize(self):
        w, h = self.im.size
        size = float(getSize.get())
        self.propic = self.im.resize((int(w*size), int(h*size)))

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

    def zftjh(self):                #直方图均衡化
        w, h = self.im.size
        pixs = self.im.load()
        
        a = [0] * 256

        self.propic = Image.new('RGB', (w, h), \
                        (255, 255,255))
        #new.show()
        draw = ImageDraw.Draw(self.propic)

        for i in range(h):
            for j in range(w):
                p = pixs[i, j]
                p = p[0]
                igray = p
                a[igray] +=  1          #累计灰度级像素总数
        for i in range(1, 256):
            a[i] = a[i] + a[i - 1]      
            #print a[i]
        m = max(a)
        for k in range(256):
            a[k] = a[k]* 200/m
            #print a[k]                 #直方图均衡
        for i in range(h):
            for j in range(w):
                p = pixs[i,j]
                p = p[0]
                pix = a[p]              
                p = (pix, pix, pix)
                #print pix
                draw.point([i,j], p)
        self.showImage('直方图均值化')

        

    def junZhi(self):
        self.propic = self.im.filter(ImageFilter.SMOOTH)
        self.showImage('均值滤波')


    def zhongZhi(self):
        self.propic = self.im.filter(ImageFilter.MedianFilter(3))
        self.showImage('中值滤波')
        
    def ruihua_lpls(self):
        self.propic = self.im.filter(ImageFilter.SHARPEN_LPLS)
        self.showImage('锐化_拉普拉斯')
    def ruihua_sobel(self):
        self.propic = self.im.filter(ImageFilter.SHARPEN_SOBEL)
        self.showImage('锐化_Sobel')
    def ruihua_prewitt(self):

        w, h = self.im.size
        pixs = self.im.load()
        self.propic = Image.new('RGB', (w, h), \
                        (255, 255,255))
        #new.show()
        draw = ImageDraw.Draw(self.propic)
        for i in range(w-1):
            for j in range(h-1):
                pix1 = pixs[i,j]
                pix1 = pix1[0]
                
                pix2 = pixs[i,j+1]
                pix2 = pix2[0]
                
                pix3 = pixs[i+1,j]
                pix3 = pix3[0]
                
                pix4 = pixs[i+1,j+1]
                pix4 = pix4[0]

                pix = abs(pix4 - pix1) + abs(pix3 - pix2)
                p = (pix, pix, pix)

                draw.point([i, j], p)
        self.showImage('锐化_梯度')
    def ruihua_zonghe(self):
        self.propic = self.im.filter(ImageFilter.SHARPEN_ZONGHE)
        self.showImage('锐化_综合')
        
                

    def weiCaiSe(self):
        
        from random import randint

        pixs = self.im.load()
        w, h = self.im.size
        self.propic = Image.new('RGB', (w, h), \
                        (255, 255,255))
        #new.show()
        draw = ImageDraw.Draw(self.propic)
        layer = [0] * 256
        for i in range(256):
            layer[i] = (randint(0,255), randint(0,255), randint(0,255))
        
        for i in range(w):
            for j in range(h):
                t = pixs[i,j]
                t = t[0]
                
                draw.point([i, j], layer[t])
                #pixs[i, j] = layer[t]
        
        self.showImage('伪彩色')
        
    def fourier(self):              #傅里叶变换（低通、高通）
        
        def FFT(image,flag = 0):

            '''将输入的图像进行中心变换 ，然后进行DFT'''
            w = image.width
            h = image.height
            iTmp = cv.CreateImage((w,h),cv.IPL_DEPTH_32F,1)
            cv.Convert(image,iTmp)
            iMat = cv.CreateMat(h,w,cv.CV_32FC2)
            mFFT = cv.CreateMat(h,w,cv.CV_32FC2)
            for i in range(h):
                for j in range(w):
                    if flag == 0:
                        num = -1 if (i+j)%2 == 1 else 1
                    else:
                        num = 1
                    iMat[i,j] = (iTmp[i,j]*num,0)
            cv.DFT(iMat,mFFT,cv.CV_DXT_FORWARD)
            return mFFT
        
        def IFFT(mat):
            '''进行IFFT'''
            mIFFt = cv.CreateMat(mat.rows,mat.cols,cv.CV_32FC2)
            cv.DFT(mat,mIFFt,cv.CV_DXT_INVERSE)
            return mIFFt

        def Restore(mat):
            '''将IFFT的实部乘以(-1)^(x+y)'''
            w = mat.cols
            h = mat.rows
            size = (w,h)
            iRestore = cv.CreateImage(size,cv.IPL_DEPTH_8U,1)
            for i in range(h):
                for j in range(w):
                    num = -1 if (i+j)%2 == 1 else 1
                    iRestore[i,j] = mat[i,j][0]*num/(w*h)
            return iRestore

        def FImage(mat):
            '''将DFT后的实部虚部相加 得到频谱图'''
            w = mat.cols
            h = mat.rows
            size = (w,h)
            # iReal = cv.CreateImage(size,cv.IPL_DEPTH_8U,1)
            # iIma = cv.CreateImage(size,cv.IPL_DEPTH_8U,1)
            iAdd = cv.CreateImage(size,cv.IPL_DEPTH_8U,1)
            for i in range(h):
                for j in range(w):
                    # iReal[i,j] = mat[i,j][0]/h
                    # iIma[i,j] = mat[i,j][1]/h
                    iAdd[i,j] = mat[i,j][1]/h + mat[i,j][0]/h
            return iAdd

    
        def Filter(mat,flag = 0,num = 10):
            mFilter = cv.CreateMat(mat.rows,mat.cols,cv.CV_32FC2)
            for i in range(mat.rows):
                for j in range(mat.cols):
                    if flag == 0:
                        mFilter[i,j] = (0,0)
                    else:
                        mFilter[i,j] = mat[i,j]
            for i in range(mat.rows/2-num,mat.rows/2+num):
                for j in range(mat.cols/2-num,mat.cols/2+num):
                    if flag == 0:
                        mFilter[i,j] = mat[i,j]
                    else:
                        mFilter[i,j] = (0,0)
            return mFilter

        image = cv.LoadImage(self.filename,0)    

        mFFT = FFT(image)
        mIFFt = IFFT(mFFT)
        
        
        self.iAfter = FImage(mFFT)
        mLP = Filter(mFFT)
        mIFFt1=IFFT(mLP)
        self.iLP = FImage(mLP)
        self.iRestore = Restore(mIFFt1)
        
        
        
        mHP = Filter(mFFT,1)
        mIFFt2 = IFFT(mHP)
        self.iHP = FImage(mHP)
        self.iRestore2 = Restore(mIFFt2)
    def iAfter(self):
        cv.ShowImage('Origin',self.iAfter)
        #cv.WaitKey(0)
        
    def iLP(self):
        cv.ShowImage('iLP',self.iLP)
        cv.ShowImage('LP_Picture',self.iRestore)
        #cv.WaitKey(0)
    def iHP(self):
        cv.ShowImage('iHP',self.iHP)
        cv.ShowImage('HP_Picture',self.iRestore2)
        #cv.WaitKey(0)
        
        
            
        
        
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
                            日期：2015/4/29--2015/6/15''')

#--------------------------------------------------------------


#---------------------------------------------------

#根窗口
root = tk.Tk()
root.title('DIP by 秦绍阳')
root.geometry('1000x600')



#类实例化
dip = dip(root)



#布局
framLeft = tk.Frame(width = 500,height = 580, bg ='white')
framRight = tk.Frame(width = 490, height = 580, bg = 'gray')
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
tk.Button(framRight, text = '二值化', command = dip.twoTrans,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 0,column = 2)

tk.Button(framRight, text = '平移', command = dip.offset,\
          bg='blue', fg='white', height = 3, width = 10).grid(row = 1,column = 0)
label = tk.Label(framRight, text='请输入平移坐标(x, y):').grid(row = 1, column = 1, sticky = tk.W)
getOffsetx = tk.Entry(framRight)
getOffsetx.grid(row = 1, column = 2, sticky = tk.E)
getOffsety = tk.Entry(framRight)
getOffsety.grid(row = 1, column = 3, sticky = tk.E)


tk.Button(framRight, text = '旋转', command = dip.rotate,\
          bg='blue', fg='white', height = 3, width = 10).grid(row = 2,column = 0)

label = tk.Label(framRight, text='请输入旋转角度(逆时针):').grid(row = 2, column = 1, sticky = tk.W)

getRotate = tk.Entry(framRight)
getRotate.grid(row = 2, column = 2, sticky = tk.E)

tk.Button(framRight, text = '缩放', command = dip.reSize,\
          bg='blue', fg='white', height = 3, width = 10).grid(row = 4,column = 0)

label = tk.Label(framRight, text='请输入缩放倍数:').grid(row = 4, column = 1, sticky = tk.W)
getSize = tk.Entry(framRight)
getSize.grid(row = 4, column = 2, sticky = tk.E)


tk.Button(framRight, text = '直方图', command = dip.zhiFang,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 5,column = 0)
tk.Button(framRight, text = '直方图均衡化', command = dip.zftjh,\
          bg='black', fg='white', height = 3, width = 10).grid(row = 5,column = 1)
tk.Button(framRight, text = '均值滤波', command = dip.junZhi,\
          bg='yellow', fg='black', height = 3, width = 10).grid(row = 6,column = 0)
tk.Button(framRight, text = '中值滤波', command = dip.zhongZhi,\
          bg='yellow', fg='black', height = 3, width = 10).grid(row = 6,column = 1)


tk.Button(framRight, text = '锐化_梯度', command = dip.ruihua_prewitt,\
          bg='red', fg='black', height = 3, width = 10).grid(row = 7,column = 0)
tk.Button(framRight, text = '锐化_sobel', command = dip.ruihua_sobel,\
          bg='red', fg='black', height = 3, width = 10).grid(row = 7,column = 1)
tk.Button(framRight, text = '锐化_拉普拉斯', command = dip.ruihua_lpls,\
          bg='red', fg='black', height = 3, width = 10).grid(row = 7,column = 2)
tk.Button(framRight, text = '锐化_综合', command = dip.ruihua_zonghe,\
          bg='red', fg='black', height = 3, width = 10).grid(row = 7,column = 3)

tk.Button(framRight, text = '伪彩色', command = dip.weiCaiSe,\
          bg='green', fg='black', height = 3, width = 10).grid(row = 8,column = 0)

tk.Button(framRight, text = '频谱', command = dip.iAfter,\
          bg='brown', fg='black', height = 3, width = 10).grid(row = 9,column = 0)
tk.Button(framRight, text = '低通滤波', command = dip.iLP,\
          bg='brown', fg='black', height = 3, width = 10).grid(row = 9,column = 1)
tk.Button(framRight, text = '高通滤波', command = dip.iHP,\
          bg='brown', fg='black', height = 3, width = 10).grid(row = 9,column = 2)




root.mainloop()
       
