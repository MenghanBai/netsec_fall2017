from playground.network.packet import PacketType 
from playground.network.packet.fieldtypes import STRING,BOOL,UINT32


class ConnectRequest(PacketType):
	DEFINITION_IDENTIFIER="Request for connecting "
	DEFINITION_VERSION="1.0"

	FIELDS=[]


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


def basicUnitTest():
	packet1=ConnectRequest()
	packetBytes=packet1.__serialize__()
	packet1_1=PacketType.Deserialize(packetBytes)
	if packet1==packet1_1:	
		print("packet1: These two packets are the same!")
	else:
		print("Different packets")


	packet2=LogInRequest()
	packet2.LogInOperation="Please enter your ID and Password"
	packetBytes=packet2.__serialize__()
	packet2_1=PacketType.Deserialize(packetBytes)
	if packet2==packet2_1:
		print("packet2: These two packets are the same!")
	else:
		print("Different packets")


	packet3=LogInAnswer()
	packet3.ID=1
	packet3.Password="MB1012"
	packetBytes=packet3.__serialize__()
	packet3_1=PacketType.Deserialize(packetBytes)
	if packet3==packet3_1:	
		print("packet3: These two packets are the same!")
	else:
		print("Different packets")

	packet4=VerifyAnswer()
	packet4.result=True
	packetBytes=packet4.__serialize__()
	packet4_1=PacketType.Deserialize(packetBytes)
	if  packet4==packet4_1:
		print("packet4: These two packets are the same!")
	else:
		print("Different packets")

def basicUnitTest2():
	packet3=LogInAnswer()
	try:
		packet3.ID=-1
	except:
		print("Invalid value!")
	


if  __name__=="__main__":
	basicUnitTest()
	basicUnitTest2()



