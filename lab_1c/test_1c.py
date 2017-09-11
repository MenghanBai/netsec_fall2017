from asyncio import *
from playground.network.packet import PacketType 
from playground.network.packet.fieldtypes import STRING,BOOL,UINT32
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol

#Define Package
class ConnectRequest(PacketType):
	DEFINITION_IDENTIFIER="Request for connecting "
	DEFINITION_VERSION="1.0"

	FIELDS=[("ConnectionRequest", STRING)]


class LogInRequest(PacketType):
	DEFINITION_IDENTIFIER="Operation of Logging in "
	DEFINITION_VERSION="1.0"

	FIELDS=[("LogInOperation",STRING)]


class LogInAnswer(PacketType):
	DEFINITION_IDENTIFIER="Enter ID and Password"
	DEFINITION_VERSION="1.0"

	FIELDS=[("ID",UINT32),("Password",STRING)]



class VerifyAnswer(PacketType):
	DEFINITION_IDENTIFIER="Verify the ID and Password"
	DEFINITION_VERSION="1.0"

	FIELDS=[("result",BOOL)]

#Design Server Protocol:
class Protocol_server(Protocol):
	def __init__(self):
		self.transport=None

	def  Connection_made(self, transport):
		print("Connected to the client")
		self.transport=transport
		self._deserializer=PacketType.Deserializer() # instantiate the Deserializer 

	def  IDandPassword(self,ID, Password):
		if ID==1 and  Password=="BMH1012":
			print("Verified Answer packet sent!")
			return True
		else:
			return False

	def  data_received(self, data):
		self._deserializer.update(data)
		for  pkt in self._deserializer.nextPackets():
			if  isinstance(pkt,ConnectRequest):
				print("Connect Request packet received!")
				print("Login request packet sent!")
				LogIn=LogInRequest()
				LogIn.LogInOperation="Please enter your ID and Password: "
				packetBytes1=LogIn.__serialize__()
				self.transport.write(packetBytes1)
			if isinstance(pkt,LogInAnswer):
				print("LogIn Answer packet received!")
				TorF = self.IDandPassword(pkt.ID, pkt.Password)
				if TorF:
					print("log in successfully!")
					verify = VerifyAnswer()
					verify.result = True
					packetBytes2 = verify.__serialize__()
					self.transport.write(packetBytes2)
				else:
					print("Failure!")

	def connection_lost(self,exc):
		print("connection lost")


#Design Client Protocol:
class Protocol_client(Protocol):
	def __init__(self):
		self.status=0
		self.transport=None
		
	def Connection_made(self, transport):
		self.transport=transport

	def data_received(self, data):
		deserializer = PacketType.Deserializer()
		deserializer.update(data)
		for  pkt in deserializer.nextPackets():
			if isinstance(pkt,LogInRequest) :
				if self.status==0:
					self.status+=1
					break
				else:
					raise TypeError("Error of  Server")
			elif isinstance(pkt, VerifyAnswer):
				if self.status==1:
					self.status+=1
					break
				else:
					raise TypeError("Error of  Server")
			else:
				raise TypeError("no Result")

	#design a communication start:
	def Request(self, packet):
		if isinstance(packet, ConnectRequest):
			self.transport.write(packet.__serialize__())
		else:
			raise TypeError("it is not a logging in request!")
	# design a method to process ID and Password:
	def IandP(self,packet ):
		self.transport.write(packet.__serialize__())
	
	def connection_lost(self,exc):
		print("connection lost")


#Protocol Test:
def  ProtocolTest():
	set_event_loop(TestLoopEx())
	client=Protocol_client()
	server=Protocol_server()
	transportToServer=MockTransportToProtocol(server)
	transportToClient=MockTransportToProtocol(client)
	server.Connection_made(transportToClient)
	client.Connection_made(transportToServer)

#Realize the function in  connection_made:
	RequestForConnect=ConnectRequest()
	RequestForConnect.ConnectionRequest="Request for connecting!"
	client.Request(RequestForConnect)
#return the ID and Password to the server:
	AnswerIDandPassword=LogInAnswer()
	AnswerIDandPassword.ID=1
	AnswerIDandPassword.Password="BMH1012"
	client.IandP(AnswerIDandPassword)
	

if __name__ == '__main__':
	ProtocolTest()