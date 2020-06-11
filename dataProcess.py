import csv
import matplotlib.pyplot as plt
path = r"D:\可能有用\1\1231"

res = []
for lll in range(1,4):
    with open(path + '\\' + 'zyx1231-' + str(lll) + 'IdVd' +'.csv',encoding = 'utf-8') as text:
        row = csv.reader(text, delimiter = ',')
        nums = {}
        begin = False
        for r in row:
            if r[0].strip() == "TestParameter" and r[1].strip() == "Value":
                nums['Vgstart'] = float(r[6])
                nums['Vgstop'] = float(r[7])
                nums['Vgstep'] = float(r[8])
                nums['Vdstart'] = float(r[9])
                nums['Vdstop'] = float(r[10])
                nums['Vdstep'] = float(r[11])
            elif r[0].strip() == "DataName":
                nums['Vg'] = []
                nums['Vd'] = []
                nums['Id'] = []
                begin = True
            elif r[0].strip() == "DataValue":
                nums['Vd'].append(float(r[1]))
                nums['Vg'].append(float(r[2]))
                nums['Id'].append(float(r[4]))
            elif r[0].strip() == "PrimitiveTest":
                break
        res.append(nums)

#print (res)


numi = 1
vneed=4.5
for fig in res:
    a = plt.figure(1)
    vdlen =  -int((fig['Vdstop'] - fig['Vdstart'])/fig['Vdstep'] + 1)
    # for i in range(int((fig['Vgstop'] - fig['Vgstart'])/fig['Vgstep'] + 1)):
    #     plt.plot(fig['Vd'][i*vdlen:(i+1)*vdlen],fig['Id'][i*vdlen:(i+1)*vdlen],label = str(fig['Vg'][i*vdlen]))
    #     print("绘图")
    
    for vneed2 in range(45,46,5):
        vneed=vneed2/10
        Idx = vdlen* (vneed - fig['Vdstop'])/-(fig['Vdstop'] - fig['Vdstart'])
        Idnew = []
        for i in range(int((fig['Vgstop'] - fig['Vgstart'])/fig['Vgstep'] + 1)):
            Idnew.append(fig['Id'][i*vdlen+int(Idx)])
        Vglist = list(range(int((fig['Vgstop'] - fig['Vgstart'])/fig['Vgstep'] + 1)))
        plt.plot([-i*fig['Vgstep']+5 for i in Vglist],Idnew[-len(Vglist):],'o',label = "Vd = "+str(vneed))
    plt.title(str(numi))
    
    plt.legend()
    plt.xlabel('Vg')
    plt.ylabel('Id')
    plt.show()
    #plt.savefig(str(numi))
    numi += 1
    plt.close()

