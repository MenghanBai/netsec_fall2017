from asyncio import *
import playground
from playground.network.packet import PacketType 
from playground.network.packet.fieldtypes import STRING,BOOL,UINT32

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

	def  connection_made(self, transport):
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

def  Test_server():
	loop=get_event_loop()
	loop.set_debug(enabled=True)
	#connection_server=loop.create_server(lambda: Protocol_server(),host="127.0.0.1",port=8888)
	connection_server=playground.getConnector().create_playground_server(lambda:Protocol_server(),8222)
	
	server=loop.run_until_complete(connection_server)
	loop.run_forever()
	loop.close()


if __name__ == '__main__':
	Test_server()



