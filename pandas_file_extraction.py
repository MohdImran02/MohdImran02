import os
import pandas as pd

time_value_dict = {}
signal_names = []
#VDSO_02_TimeStamp.dump
for roots, directory, files in os.walk(os.getcwd()):
    for component in files:
        if 'TimeStamp' in component:
            signal = str(component).split('_TimeStamp')[0]
            signal_names.append(signal)
            with open(os.path.join(roots, component), 'r') as f:
                x = f.readlines()
                if 'VDSO_02' in component:
                    l = len(x)
                    #l = max(length, 600)
                time_value_dict[signal]=[]
                for i in range(0, l):
                    x[i] = int(x[i])
                print('len x = ', l)
                time_value_dict[signal].append(x)
        if 'Value' in component:
            with open(os.path.join(roots, component), 'r') as fr:
                y = fr.readlines()
                for i in range(0, l): #same length for all timestamp & value data
                    y[i] = int(y[i])
                print('len y = ', l)
                time_value_dict[signal].append(y)
#print('signals: ', signal_names)
#print('\n')
#print('dixt', time_value_dict[])

#TimeStamp = time_value_dict[keys][0]
#Values    = time_value_dict[keys][1]

with pd.ExcelWriter('KPI_outputFile.xlsx') as writer:
    for val in time_value_dict:
        sheet_name = val
        df = pd.DataFrame({"TimeStamp": time_value_dict[val][0],
                         "BZ": time_value_dict[val][1],
                         "Cycle_Time": "",
                         "BZ_Deviation": "",
                         "Cycle_Deviation": ""
                          })
        for i in df.index:
            if(i==0):
                df["Cycle_Time"][i] = 'NIL'
                df["BZ_Deviation"][i] = 'NIL'
                df["Cycle_Deviation"][i] = 'NIL'
            elif (i>0):
                df["Cycle_Time"][i] = '=(B'+str(i+2)+'-B'+str(i+1)+')/1000'
                df["BZ_Deviation"][i] = '=C'+str(i+2)+'-C'+str(i+1)
                df["Cycle_Deviation"][i] = '=D'+str(i+2)+'-D'+str(i+1)

        df.to_excel(write, sheet_name = val)