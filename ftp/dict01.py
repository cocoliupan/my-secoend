nos=[1001,1002,1003,1004]
name=['tom','jerry','spike','tyke']
d={nos[i]:name[i] for i in range(min(len(nos),len(name)))}
print(d)