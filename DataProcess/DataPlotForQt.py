from sys import path
import csv
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import math

class FigurePlot(FigureCanvas):
    def __init__(self,width = 500,height = 400,dpi = 100) -> None:
        self.fig = Figure(figsize=(width,height),dpi=dpi)

        super(FigurePlot,self).__init__(self.fig)

        self.axes = self.fig.add_subplot(1,1,1)
    
    def plotSin(self):
        t = np.arange(0,3,0.01)
        s = np.sin(2*np.pi*t)
        self.axes.plot(t,s)

    def plotData(self,path,num,fresh):
        if fresh:
            self.fig.clf()
        rows = math.ceil(math.sqrt(num))
        cols = rows
        i = 0
        for n in path:
            i += 1
            self.axes = self.fig.add_subplot(rows,cols,i)
            DataProcessor = DataProcess(n)
            DataProcessor.plotLines(self.axes)
        self.draw()


class DataProcess():
    def __init__(self,path):
        self.Totaldata = self.getDatas(path)

    def getDatas(self,path):
        TotalData = []
        with open(path, encoding='utf-8') as text:
            row = csv.reader(text, delimiter=',')

            data = {}
            for r in row:
                # print(r)
                if len(r) > 0:
                    if r[0].strip() == "SetupTitle":
                        # 此处为设置标题
                        if len(data.keys()) > 1:
                            TotalData.append(data)  # 将读取完的的数据集并入Total
                        data = {"Mode": r[1].strip()}  # 初始化数据集
                        '''
                        Id_Vd 下 Vd 为 第一扫描， Vg为第二扫描
                        Id_Vg 下 Vg 为 第一扫描， Vd为第二扫描
                        '''

                    elif r[0].strip() == "TestParameter" and r[1].strip() == "Name":
                        Namelist = []
                        for num in range(2, len(r)):
                            Namelist.append(r[num].strip())
                        data["namelist"] = Namelist
                    elif r[0].strip() == "TestParameter" and r[1].strip() == "Value":
                        for i in range(len(Namelist)):
                            # if r[i+2].strip().isdigit() or r[i+2].strip()[1:].isdigit():
                            try:
                                data[Namelist[i]] = float(r[i + 2])
                            except:
                                data[Namelist[i]] = r[i + 2].strip().replace("\t", "  ")

                    elif len(r) > 1 and r[1].strip() == "TestRecord.RecordTime":
                        data['TestTime'] = r[2]  # 测量时间（一般不需要这个数据）

                    elif r[0].strip() == "DataName":  # 初始化一下数据向量
                        variables = []
                        for name in r[1:]:
                            variables.append(name.strip())
                            data[name.strip()] = []

                    elif r[0].strip() == "DataValue":
                        for i in range(len(variables)):
                            '''填充数据'''
                            data[variables[i]].append(float(r[i + 1]))
                    elif r[0].strip() == "PrimitiveTest":
                        data = {}
            if "Mode" not in data:
                data = {}
            if len(data.keys()) > 1:
                TotalData.append(data)
        return TotalData

    def PlotOneDatas(self,axes,data, legend):
        """
        画一组数据,比方说Total里面的一个子集
        """
        if data == {} or "Mode" not in data.keys():
            return

        if "Id_Vd" in data["Mode"] or "Id-Vd" in data["Mode"]:
            '''
            Id_Vd 模式以Vd为横轴，Id为纵轴
            Vg为Legend
            '''
            # plt.xlabel("Voltage/V")
            # plt.ylabel("Current/A")
            axes.set_xlabel("Voltage/V")
            axes.set_ylabel("Current/A")
            vdlen = int((data['VdStop'] - data['VdStart']) / data['VdStep'] + 1)  # 单条线Vd的数据点数
            vglen = int((data['VbgStop'] - data['VbgStart']) / data['VbgStep'] + 1)  # Vg点数，也是曲线数
            vglist = [data['VbgStart'] + i * data['VbgStep'] for i in range(vglen)]
            for j in range(vglen):
                '''画vglen条线'''
                v = data["Vdrain"][j * vdlen: (j + 1) * vdlen]  # 横轴v
                i = data["Idrain"][j * vdlen:(j + 1) * vdlen]  # 纵轴i
                axes.plot(v, i)
                l = "Vg = " + str(vglist[j])  # 图例
                legend.append(l)
            probeInformation = "BackGate:" + data['BackGate'] + "   Source:" + data['Source'] + \
                               "\n   Drain:" + data['Drain'] + "\n   SideGate: " + data['SideGate'] + "  (Barely Used)"

        elif "Id-Vg" in data["Mode"] or "Id_Vg" in data["Mode"]:
            """
            Id_Vg 模式，以Vg为横轴，Id为纵轴
            Vd为Legend
            """
            axes.set_xlabel("Voltage/V")
            axes.set_ylabel("Current/A")
            if "TFT" in data["Mode"]:
                vglen = int((data['VgStop'] - data['VgStart']) / data['VgStep'] + 1)  # 单条线Vd的数据点数
                vdlen = int((data['VdStop'] - data['VdStart']) / data['VdStep'] + 1)  # Vg点数，也是曲线数
            elif "CNT" in data["Mode"]:
                vglen = int((data['VbgStop'] - data['VbgStart']) / data['VbgStep'] + 1)  # 单条线Vd的数据点数
                vdlen = int((data['VdStop'] - data['VdStart']) / data['VdStep'] + 1)  # Vg点数，也是曲线数
                data["Vgate"] = data["Vbackgate"]
                data["Gate"] = data["BackGate"]
            vdlist = [data['VdStart'] + i * data['VdStep'] for i in range(vglen)]
            for j in range(vdlen):
                """画vdlen条线"""
                v = data["Vgate"][j * vglen: (j + 1) * vglen]  # 横轴v
                i = data["Idrain"][j * vglen:(j + 1) * vglen]  # 纵轴i
                axes.plot(v, i)
                l = "Vd = " + str(vdlist[j])
                legend.append(l)
            probeInformation = "Gate:" + data['Gate'] + "   Source:" + data['Source'] + \
                               "\n   Drain:" + data['Drain']

        else:
            print("Not Found Match Mode")

        axes.legend(legend)

        axes.set_title("Mode:" + data["Mode"] + "\n" + probeInformation)

    def plotLines(self,axes):
        """
        画文件中的所有线
        : path of csv:
        : return None:
        """
        # TotalData = self.getDatas(path)
        # plt.figure()
        legend = []
        for data in self.Totaldata:
            # f = plt.subplot(2, 1, i)
            self.PlotOneDatas(axes,data, legend)
        # plt.show()


if __name__ == "__main__":
    path0 = r"D:\GH\DailyDataProcess\Data\0929\strain-1.csv"
    ploter = DataProcess(path0)
    ploter.plotLines()
