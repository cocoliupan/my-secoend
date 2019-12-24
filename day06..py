n=int(input("请输入一个数："))
for i in range(1,n+1):
	blanks_count=n-i
	print(' '*blanks_count+'*'*(2*i-1))
for i in range(1,n+1):
	print(' '*(n-1)+'*')