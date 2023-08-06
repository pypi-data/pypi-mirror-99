import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from alioss import OSSession
import random
import time
import os
import markdown
from markdown import extensions
from markdown.treeprocessors import Treeprocessor

class zwymarkdown:
    
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    __version__ = "0.0.1"
    
    """
        未来会加上数学公式的功能  
        添加引言等功能 [√]
        添加vip 
    """
    
    def __init__(self):
        self.markdown = ""
        self.markdownExtension = ["markdown.extensions.fenced_code","markdown.extensions.toc",'markdown.extensions.tables']
        self.extensions = self.markdownExtension
        self.handleDataframeMD = lambda x: "\n".join([i[5:] for i in x.split("\n")])
        self.p1 = "zwy"
        self.p2 = "qwerty123"
        self.session = OSSession(self.p1,self.p2)
        self.cloudreferencebasepath = "https://tianchioss.oss-cn-beijing.aliyuncs.com/"
        self.localpath="./images"
        self.cloudbasepath="imagesbed/"
        self.title = "test"
        self.css = r"./css/index.css"
        self.markdownparse = ""
        self.htmlhelp()
        self.imagestyle = '?x-oss-process=style/cloudsheet'
        self.templine = ""
        self.quoting = False
    
    def vip(self):
        pass
    
    def hn(self,string,n):
        """
        构建n主题
        """
        self.add("#"*n + " "+string)
        return self

    def parsemarkdown(self,string):
        return markdown.markdown(string,extensions=self.extensions)
    
    def nextquoteblock(self):
        """
        告诉markdown 下一个内容是quote内容
        """
        self.quoting = True
        return self
    
    def divstart(self,classnames="",idnames=""):
        div = "<div"
        classnames = " class='{}'".format(classnames) if classnames else classnames
        idnames = " id='{}'".format(idnames) if idnames else idnames
        div = div + classnames + idnames + ">"
        self.markdownparse += div
        return self
    
    def divend(self):
        self.markdownparse += "</div>"
        return self
    
    def centerstart(self):
        self.divstart(classnames="divcenter")
        return self
    
    def imagewithurl(self,url="",title=""):
        """
        url 插入图片
        """
        if not url:
            url = self.cloudimagepath
        self.add("![{}]({})".format(title,url + self.imagestyle))
        return self

    def image(self,image,imageTitle="",uploadToCloud=False,):
        """
        思路： 图片保存本地后上传到云端或者云端的链接插入进去 
        1. 保存图片到本地 , self.imagepath
        2. 上传图片到云端 
        3. 获得云端的图片链接
        4. 插入到self.markdown
        """
        if type(image) == str:
            if image.startswith("http"):
                self.imagewithurl(url=image,title=imageTitle)
            if os.path.isfile(image):
                self.imagelocalpath = image
                self.local2cloud()
                self.imagewithurl(title=imageTitle)
        if type(image) == matplotlib.figure.Figure:
            self.pltimage(image,imageTitle)
            self.local2cloud()
            self.imagewithurl(title=imageTitle)
        return self
            
    def local2cloud(self):
        cloudimagepath = self.cloudbasepath + self.imagelocalpath.split("/")[-1]
        self.session.upload_local_files(self.imagelocalpath,cloudimagepath)
        self.cloudimagepath = self.cloudreferencebasepath + cloudimagepath
    
    def pathifnotexist(self,path):
        if not os.path.isdir(path):
            os.mkdir(path)
        return self
    
    @classmethod
    def randomfilename(cls,n=7):
        return "".join(random.choices(cls.base_str,k=n))
    
    def randomfilename(self,n=7):
        return "".join(random.choices(self.base_str,k=n))
    
    def imageCustom(self,func):
        """
        用户自己定制,func是一个函数，最后会运行这个函数，这个函数得到本地图片路径，不保证添加time信息，不确定是否会覆盖已有的图片
        注意这里面的func没有参数 ，用户可以通过闭包的方式自己实现 不确保是否会出现os错误 
        """
        try:
            self.imagelocalpath = func()
            self.local2cloud()
            self.imagewithurl()
        except:
            ValueError("func is not suitable for this custom image")
      
    def pltimage(self,plt,imageTitle=""):
        """
        plt得到图片直接保存到本地 
        """
        if not imageTitle:
            imageTitle = self.randomfilename()
        imageTitle += str(time.time()) + ".jpg"
        self.pathifnotexist(self.localpath)
        print(self.localpath,imageTitle)
        plt.savefig(self.localpath+"/"+imageTitle)
        self.imagelocalpath = self.localpath+ "/" + imageTitle
        return self
    
    def add(self,string="",wrap=True):
        if self.quoting:
            string = "\n".join(["> "+i for i in string.split("\n")])
            self.quoting = False
        self.markdownparse += self.parsemarkdown(string)
        self.markdown += string
        if wrap:
            self.markdown += "\n"
            self.markdownparse += "\n"
        return self
    
    def add2(self,string=""):
        """
        这里的add2特指添加一行的内容，所以后续要结束这一行
        """
        self.templine += string
        return self
    
    def add2end(self,string=""):
        """
        结束add2所添加的一行   
        """
        self.templine += string
        self.add(self.templine)
        return self
    
    def strong(self,string=""):
        if string:
            self.add2("*"+string+"*")
        return self
    
    def table(self,table,names=None):
        """
        这里的table分为好多种 
        1. dataframe 
        2. multidata
        3. dictdata
        """
        if type(table) == pd.core.frame.DataFrame:
            self.dataFrameTable(table)
        if type(table) == dict:
            self.dictdataTable(table)
        if type(table) == list:
            self.multidataTable(table,names=names)
        return self
    
    def loadimage(self):
        pass
    
    def parseimage(self):
        pass
    
    def imagenamehandle(self):
        pass
        
    def dictdataTable(self,table):
        assert type(table) == dict
        data = pd.DataFrame(table)
        self.dataFrameTable(data)
        return self
    
    def line(self):
        self.add("----------------------")
        return self
    
    def multidataTable(self,table,names):
        if not names:
            names = range(len(table))
        data = pd.DataFrame(table,columns=names)
        self.dataFrameTable(data)
        return self
    
    def dataFrameTable(self,table):
        assert type(table) == pd.core.frame.DataFrame
        tablemarkdown = table.to_markdown()
        tablemarkdown = tablemarkdown if not self.handleDataframeMD else self.handleDataframeMD(tablemarkdown)
        tablemarkdown = tablemarkdown.replace(":","-")
        tablemarkdownhtml = markdown.markdown(tablemarkdown,extensions=self.extensions)
        self.markdown += tablemarkdown + "\n"
        self.markdownparse += tablemarkdownhtml + "\n"
        return self
    
    def TOC(self):
        """
        这一般是最后一步才做的 
        """
        self.markdown = "[TOC]\n"+self.markdown
        self.markdownparse = self.parsemarkdown("[TOC]") + "\n" + self.markdownparse
        return self
    
    def mathRegx(self,mathregx):
        pss
    
    def toHtml(self,path=".",save=False,whole=False):
        if save:
            self.preview(save)
            return self
        if whole:
            self.review(False)
            self.body = self.tempbody
            return self
        
        self.body = markdown.markdown(self.markdown,extensions=self.extensions)
        return self
    
    def preview(self,save=True):
        """
        预览
        """
        self.tempbody = self.markdownparse
        self.temphtml = self.htmlhead.format(self.title) + self.htmlbody.format(self.tempbody) + self.htmltail
        if save:
            with open("./temphtml.html",'w',encoding='utf8') as f:
                f.write(self.temphtml)
            with open("./index.css",'w',encoding='utf8') as f:
                f.write(open(self.css,'r',encoding='utf8').read())
        # 是否开启端口进行访问再说  通过callback去做 
        return self
        
    def htmlhelp(self):
        self.htmlhead = """
        <html lang = "zh-cn">
        <head>
            <title>{}</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <link rel="stylesheet" href="index.css" type="text/css">
        </head>
        """
        self.htmlbody = """
        <body id="app">{}</body>
        """
        self.htmltail = """
        </html>
        """
        return self
    
    def toPdf(self):
        pass
    
    def toDocs(self):
        pass
    
    def code(self,codecontent):
        if "markdown.extensions.fenced_code" not in self.markdownExtension:
            self.markdownExtension.append("markdown.extensions.fenced_code")
        self.add(codecontent)
        
    def addExtension(self,instance):
        self.markdownExtension.append(instance)
    
    def h1(self,string):
        self.hn(string,1)
        return self
    
    def h2(self,string):
        self.hn(string,2)
        return self
    
    def h3(self,string):
        self.hn(string,3)
        return self
        
    def h4(self,string):
        self.hn(string,4)
        return self
    
    def h5(self,string):
        self.hn(string,5)
        return self
    
    def h6(self,string):
        self.hn(string,6)
        return self