d={}
while True:
	k=input("请输入单词:")
	if  not k:
		break
	v=input("请输入解释:")
	d[k]=v
while True:
	k=input("请输入要查询的单词:")
	if k in d:
		print("解释:",d[k])
	else:
		print("不存在解释")