from socket import *
import sys
import time

#基本文件操作功能
class FtpClient(object):
	def __init__(self,sockfd):
		self.sockfd = sockfd

	def do_list(self):
		self.sockfd.send(b'L')#发送请求
		#等待回复
		data = self.sockfd.recv(1024).decode()
		if data =='ok':
			data = self.sockfd.recv(4096).decode()
			files = data.split('#')#用#号切割文件
			for file in files:
				print(file)
			print("文件展示完毕\n")
		else:
			#由服务器发送失败的原因
			print(data)
	def do_get(self,filename):
		self.sockfd.send(('G ' +filename).encode())#发送请求类型
		data = self.sockfd.recv(1024).decode()#接收服务端的回复看是否允许下载
		#文件传输
		if data == 'ok':
			fd = open(filename,'wb')
			while True:
				data = self.sockfd.recv(1024)#接收后再写入一个文件中
				if data == b'##':#发##表示发完了
					break
				fd.write(data)#写入
			fd.close()
			print("%s 下载完毕\n"%filename)

		else:
			print(data)

	#自己写的功能类的代码段
	def do_put(self,filename):
		try:
			f = open(filename,'rb')
		except:
			print("没有找到文件")
			return

		self.sockfd.send(('P ' + filename).encode())
		data = self.sockfd.recv(1024).decode()
		if data == 'ok':
			while True:
				data = f.read(1024)
				if not data:
					time.sleep(0.1)
					self.sockfd.send(b'##')
					break
				self.sockfd.send(data)
			f.close()
			print("%s 上传文件完成"%filename)
		else:
			print(data)


	def do_quit(self):
		self.sockfd.send(b'Q')
#网络连接
def main():
	if len(sys.argv) < 3:
		print("argv is erro")
		return
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST,PORT)#文件服务器地址

	sockfd = socket()

	try:
		sockfd.connect(ADDR) #连接不成功，捕获异常
	except:
		print("连接不成功")
		return
	ftp = FtpClient(sockfd)#功能类对象
	while True:
		
		print("========命令选项=========")
		print("********list************")
		print("********get file********")
		print("********put file********")
		print("********quit************")
		print("========================")

		cmd = input("请输入命>>>")
		if cmd.strip() == 'list':
			ftp.do_list()
		elif cmd[:3] == 'get':
			filename = cmd.split(' ')[-1]
			ftp.do_get(filename)

		#以下是自己写的文件上传的代码段
		elif cmd[:3] =='put':
			filename = cmd.split(' ')[-1]
			ftp.do_put(filename)

		elif cmd.strip() =='quit':
			ftp.do_quit()
			sockfd.close()
			sys.exit("谢谢使用")
		else:
			print("请输入正确命令！！！！")
			continue

if __name__ == "__main__":
	main()