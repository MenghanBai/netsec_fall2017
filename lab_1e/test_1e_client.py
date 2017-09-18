from asyncio import *
import playground 
from playground.network.packet import PacketType 
from playground.network.packet.fieldtypes import STRING,BOOL,UINT32
from playground.network.common import StackingProtocol
from playground.network.common import StackingTransport
from playground.network.common import StackingProtocolFactory


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


class Protocol_client(Protocol):
	def __init__(self):
		self.status=0
		self.transport=None
		
	def connection_made(self, transport):
		self.transport=transport
		print ("client starts to work!")

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
		print("This is request!")
		if isinstance(packet, ConnectRequest):
			self.transport.write(packet.__serialize__())
		else:
			raise TypeError("it is not a logging in request!")

	# design a method to process ID and Password:
	def IandP(self,packet ):
		self.transport.write(packet.__serialize__())
	
	def connection_lost(self,exc):
		print("connection lost")

def  Test_client():

	
	loop=get_event_loop() # create the client object
	connection_client=playground.getConnector().create_playground_connection(lambda:Protocol_client(),"20174.1.1.1",8222)
	transportation, client_object=loop.run_until_complete(connection_client)

	RequestForConnect=ConnectRequest() #Realize the function in  connection_made:
	RequestForConnect.ConnectionRequest="Request for connecting!"
	client_object.Request(RequestForConnect)

	AnswerIDandPassword=LogInAnswer()  #return the ID and Password to the server:
	AnswerIDandPassword.ID=1
	AnswerIDandPassword.Password="BMH1012"
	client_object.IandP(AnswerIDandPassword)

	loop.run_forever()
	loop.close()

if __name__ == '__main__':
	Test_client()