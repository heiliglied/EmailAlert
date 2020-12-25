#-*- coding:utf-8 -*- 

import os, sys, signal, atexit, time, subprocess
#from functools import wraps

import syslog

class Decorator(object):
	def __init__(self, function):
		self.function  = function
		
	def __call__(self, *args, **kwargs):
		if(len(sys.argv) < 2):
			print('옵션을 지정하세요. start or stop or restart')
			sys.exit()
		else:
			result = self.function(*args, **kwargs)
			return result

class Daemon(object):
	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.pidfile = pidfile
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr

	def daemonize(self):
		self.fork()
		#double fork
		self.fork()
		
		sys.stdout.flush()
		sys.stderr.flush()

		self.attach_stream('stdin', mode='r')
		self.attach_stream('stdout', mode='a+')
		self.attach_stream('stderr', mode='a+')
		
		self.create_pidfile()

	def attach_stream(self, name, mode):
		stream = open(getattr(self, name), mode)
		os.dup2(stream.fileno(), getattr(sys, name).fileno())

	def get_pid(self):
		try:
			pf = open(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except(IOError, TypeError):
			pid = None
			
		return pid
		
	def create_pidfile(self):
		#atexit.register(self.delpid)
		pid = str(os.getpid())
		open(self.pidfile,'w+').write("%s\n" % pid)
		
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		pid = self.get_pid()
		if pid:
			print('PID파일이 존재함. 데몬이 실행중인지 확인')
			sys.exit(1)
		
		self.daemonize()
		self.run()

	def stop(self, silent=False):
		pid = self.get_pid()
		
		if not pid:
			if not silent:
				print('pid가 존재하지 않음. 실행중이 맞는지 확인.')
			return
			
		try:
			while True:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as error:
			err = str(error)
			if err.find('No such process') > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
				else:
					sys.stdout.write(str(err))
					sys.exit(1)

	def restart(self):
		self.stop(silent=True)
		self.start()
		
	def fork(self):
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError as e:
			sys.stderr.write("Fork failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
			
	def run(self):
		#override
		raise NotImplementedError
		
class DaemonRunner(Daemon):
	def run(self):
		while True:
			#로직 작성.
			#time을 이용한 정기 체크를 이용하고 있음.
			subprocess.call('python3 sendmail.py email', shell=True)
			time.sleep(600)

@Decorator	
def main():
	daemon = DaemonRunner('/tmp/daemon.pid')

	if sys.argv[1] == 'start':
		daemon.start()
	elif sys.argv[1] == 'stop':
		daemon.stop()
	elif sys.argv[1] == 'restart':
		daemon.restart()
	else:
		print('옵션 값이 잘못되었습니다')
		sys.exit()

if __name__ == "__main__":
	print('프로세스 호출')
	main()
