#!/usr/bin/python3

# imports
import socket, time, sys
import threading

def main():
	socket.setdefaulttimeout(3)
	host, port = 'localhost', 13370

	for arg in sys.argv:
		if arg.startswith("-h="):
			host = arg[3:]
		elif arg.startswith("-p="):
			try: port = int(arg[3:])
			except ValueError:
				print("Invalid port: " + arg[3:])
				return
	
	client = Client(host, port)
	client.start()

	while not client.stopped:
		try: time.sleep(1)
		except KeyboardInterrupt:
			print("Received keyboard interrupt, use '/stop' to shut down.")
			break

# client class
class Client:
	def __init__(self, host, port):
		self.stopped = False
		print("Connecting to server...")
		self.addr = (host, port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(60)
		try: self.sock.connect(self.addr)
		except socket.timeout:
			print("Connection timed out. Shutting down...")
			self.sock.close()
			sys.exit(1)
		except ConnectionRefusedError:
			print("Server not reachable. Shutting down...")
			self.sock.close()
			sys.exit(1)
			
		self.console_thread = ConsoleThread(self)
		self.listen_thread = ListenThread(self)

	def start(self):
		self.console_thread.start()
		self.listen_thread.start()
	
	def stop(self):
		print("Shutting down client...")
		self.console_thread.end()
		self.listen_thread.end()
		self.listen_thread.join()
		self.sock.close()
		self.stopped = True

	def send(self, message):
		self.sock.sendall(bytes(message, "UTF-8"))

	def __del__(self):
		self.sock.close()

# thread for listening
class ListenThread(threading.Thread):
	def __init__(self, client):
		self.shouldStop = False
		self.parentClient = client
		threading.Thread.__init__(self, name="ListenThread")

	def run(self):
		while not self.shouldStop:
			try: data = self.parentClient.sock.recv(1024)
			except socket.timeout: continue
			if not data:
				print("Connection closed.")
				break
			else:
				print("[Incoming] " + str(data, "UTF-8"))
		print("ListenThread shut down.")
	
	def end(self):
		self.shouldStop = True

# console thread
class ConsoleThread(threading.Thread):
	def __init__(self, client):
		self.shouldStop = False
		self.parentClient = client
		threading.Thread.__init__(self, name="ConsoleThread")
	
	def run(self):
		while not self.shouldStop:
			message = sys.stdin.readline()
			message = message.strip()
			if message.lower() == "/stop":
				self.parentClient.stop()
				break
			else:
				self.parentClient.send(message)
		print("ConsoleThread shut down.")
	
	def end(self):
		self.shouldStop = True

# entrypoint
if __name__ == "__main__":
	main()

