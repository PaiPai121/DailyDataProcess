import matplotlib.pyplot as plt
fig = plt.figure(1)
from matplotlib import font_manager
font = font_manager.FontProperties(fname = r"C:\Windows\Fonts\simsun.ttc")
strain = [i/100 for i in range(-5,6,1)]
bridgeOut = [125.078,100.04,75.017,50.005,25.001,0,-25.001,-50.005,-75.017,-100.04,-125.077]
bridgeOut = [i/1000 for i in bridgeOut]
INA126Out = [2.44,2.22,2.00,1.77,1.55,1.33,1.10,0.878,0.655,0.477,0.436]
ADInput = [1.126,0.900391,0.675208,0.450127,0.225113,133.5*1e-6,-0.224846,-0.44986,-0.647894,-0.873109,-0.896026]

plt.plot(strain,bridgeOut,label = u"电桥输出")

plt.plot(strain,INA126Out,label = u"放大器输出")

plt.plot(strain,ADInput,label = u"AD输入")
plt.legend(prop = font)
plt.xlabel("Strain")
plt.ylabel("Voltage/V")
plt.show()