from sys import setprofile, winver
from PIL.Image import FASTOCTREE
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QLineEdit, QApplication, QFileDialog, QMainWindow, QHBoxLayout, QMenu, QPushButton, QTextEdit, QVBoxLayout, QAction, QWidget, qApp, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtWidgets, QtCore
import sys

from numpy.lib.twodim_base import diag

import DataPlotForQt
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # 高分辨率屏幕支持



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.InitUI()
        self.show()

    def InitUI(self):
        """
        初始化UI
        """
        
        self.setGeometry(300,300,1600,800)  # x,y,w,h
        self.setWindowTitle("莱莎的奇妙炼金术")
        self.setWindowIcon(QIcon(r"Imgs\Ryza.ico"))        

        ### 状态栏
        self.statusBar().showMessage("Ready")

        """动作设置"""

        ### 退出程序动作
        exitAct = QAction(QIcon(r'Imgs\exit.jpg'), '退出(&E)', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('退出程序')
        exitAct.triggered.connect(qApp.quit)

        ### 打开文件动作
        openfileAct = QAction(QIcon(r"Imgs\open.jpg"),"打开",self)
        openfileAct.triggered.connect(self.openFile)
        openfileAct.setStatusTip('打开单个文件')

        ### 打开多个文件动作
        openfilesAct = QAction(QIcon(r"Imgs\opens.png"),"打开多个文件",self)
        openfilesAct.triggered.connect(self.openFile)
        openfilesAct.setStatusTip('打开多个文件')

        ### 关于动作
        aboutAct = QAction(QIcon(r"Imgs\abouticon.png"),"关于此程序",self)
        aboutAct.triggered.connect(self.aboutMyself)
        aboutAct.setStatusTip("作者的一点屁话")
        


        """ 菜单设置 """

        ### 打开菜单设置

        openMenu = QMenu("打开(&O)",self) 
        openMenu.addAction(openfileAct)
        openMenu.addAction(openfilesAct)


        menuBar = self.menuBar()
        menuBar.setStatusTip("打开主菜单")

        fileMenu = menuBar.addMenu("Main")  #  在菜单Bar上添加一个标签
        fileMenu.addMenu(openMenu)  #  带子菜单
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)  #  标签里面的下拉菜单

        ### 工具栏
        toolbar = self.addToolBar("ToolBar")
        toolbar.addAction(openfileAct)
        toolbar.addAction(exitAct)
        toolbar.addAction(aboutAct)



        """绘图设置"""

        self.figure = DataPlotForQt.FigurePlot()

        """布局设置"""

        ### CheckBox设置
        self.NewFigureCheck = QCheckBox("在新figure绘图",self)
        self.NewFigureCheck.stateChanged.connect(self.changeCheckBoxState)
        self.NewFigureCheck.setStatusTip("取消勾选可以重复绘图")
        self.NewFigureCheck.setChecked(True)
        self.NewFigure = True

        ### 文件地址输入框
        
        self.pathText = QLineEdit("键入文件地址",self)
        self.pathText.selectAll()
        self.pathText.setFocus()  # 激活光标

        ### 自定义坐标轴

        self.SetAxis = QPushButton("使用自定义坐标",self) # 确定按键
        self.SetAxis.clicked.connect(self.changeSetCoordinateState)
        self.xmin = QLineEdit("x最小值",self)
        self.xmax = QLineEdit("x最大值",self)
        self.ymin = QLineEdit("y最小值",self)
        self.ymax = QLineEdit("y最大值",self)

        hAxiBox = QHBoxLayout()
        hAxiBox.addStretch(1)
        hAxiBox.addWidget(self.SetAxis)
        hAxiBox.addWidget(self.xmin)
        hAxiBox.addWidget(self.xmax)
        hAxiBox.addWidget(self.ymin)
        hAxiBox.addWidget(self.ymax)
        hAxiBox.addStretch(1)


        ### 在MainWindow中要先创建一个QWidget
        wid = QWidget(self)
        self.setCentralWidget(wid)


        
        vbox = QVBoxLayout()
        vbox.addWidget(self.figure)
        vbox.addStretch(1)
        vbox.addLayout(hAxiBox)
        vbox.addWidget(self.NewFigureCheck)
        # vbox.addWidget(self.SetCoordinateCheck)
        vbox.addStretch(1)
        vbox.addWidget(self.pathText)
        vbox.addStretch(1)
        hbox =QVBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        wid.setLayout(hbox)

    def aboutMyself(self):
        msgBox = QMessageBox(QMessageBox.NoIcon,"关于！","啊哈，我还没想好在这里埋点什么骚话！")
        msgBox.setIconPixmap(QPixmap(r"Imgs\about.jpg"))
        msgBox.exec()

    def changeCheckBoxState(self):
        if self.NewFigureCheck.checkState() == Qt.Checked:
            self.NewFigure = True
        else:
            self.NewFigure = False

    def changeSetCoordinateState(self):
        try:
            xmin = float (self.xmin.text())
            xmax = float (self.xmax.text())
            self.figure.axes.set_xlim(xmin,xmax)
            xchanged = True
        except:
            xchanged = False
        try:
            ymin = float (self.ymin.text())
            ymax = float (self.ymax.text())
            self.figure.axes.set_ylim(ymin,ymax)
            ychanged = True
        except:
            ychanged = False
        if xchanged or ychanged:
            self.figure.draw()
        else:
            self.errorHandle("蠢货！连个最大最小值都输不对！！")


    def openFile(self):
        """
        打开文件
        """
        if self.sender() == None:
            sender = "打开"
        else:
            sender = self.sender().text()
        if sender == "打开":
            fname = QFileDialog.getOpenFileName(self,"打开文件","./",("逗号分隔符文件 (*.csv)"))
            if fname[0]:
                self.pathText.setText(fname[0])
                # plotter = DataPlotForQt.DataProcess(fname[0])
                # plotter.plotLines()
                # self.canvas.draw()
                self.figure.plotData([fname[0]],1,self.NewFigure)
        elif sender == "打开多个文件":
            fnames = QFileDialog.getOpenFileNames(self,"Open Files","./",("逗号分隔符文件 (*.csv)"))
            if fnames[0]:
                self.figure.axes.clear()
                paths = ""
                for fn in fnames[0]:
                    paths += fn
                    paths += ";\n"
                self.pathText.setText(paths)
                self.figure.plotData(fnames[0],len(fnames[0]),self.NewFigure)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """右击菜单栏"""
        cmenu = QMenu(self)
        openAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()
        if action == openAct:
            self.openFile()
        # if action == newAct:
            # self.newAct.event()
            

    def errorHandle(self,message = "喂!你搞错了!"):
        """
        弹出错误信息
        """
        QMessageBox.about(self,"错误信息",message)


    def closeEvent(self,event):
        """
        关闭事件处理函数
        """
        reply = QMessageBox.question(self,"小老弟你不对劲","不会有人真的想摸鱼吧",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_())
