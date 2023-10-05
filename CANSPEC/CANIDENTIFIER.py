import binascii
from CANSPEC import ENUMS

class CANIDENTIFIER:
    def __init__(self, identifier_list):
        self.identifier_list = identifier_list
        self.msgPrio1   = ""
        self.msgPrio2   = ""
        self.msgCmd     = ""
        self.msgResp    = ""
        self.msgHash    = ""
        self.debug = False

    def explainIdentifier(self):

        completeIdentifierHEX = self.identifier_list[0] + self.identifier_list[1] + self.identifier_list[2] + self.identifier_list[3]
        # print(f'Complete CAN IDENTIFIER in HEX: {completeIdentifierHEX}')

        completeIdentifierBINARY = format(int(completeIdentifierHEX, 16), '032b')
        print(f"Complete CAN IDENTIFIER in BINARY: {completeIdentifierBINARY}")

        self.msgPrio1 = completeIdentifierBINARY[3:5]
        self.msgPrio2 = completeIdentifierBINARY[5:7]
        self.msgCmd = completeIdentifierBINARY[7:15]
        self.msgResp = completeIdentifierBINARY[15:16]
        self.msgHash = completeIdentifierBINARY[16:22] + completeIdentifierBINARY[25:]

        # print(f"In BINARY: Prio1: {msgPrio1}, Prio2: {msgPrio2}, Cmd: {msgCmd}, Resp: {msgResp}, Hash: {msgHash}")
        print(
            f"In HEX: Prio1: {hex(int(self.msgPrio1, 2))}, Prio2: {hex(int(self.msgPrio2, 2))}, Cmd: {hex(int(self.msgCmd, 2))}, Resp: {hex(int(self.msgResp, 2))}, Hash: {hex(int(self.msgHash, 2))}")

        if self.debug:
            for hex_string in self.identifier_list:
                binary_string = bin(int.from_bytes(binascii.unhexlify(hex_string), byteorder='big'))

                print(f'Hexadecimal: {hex_string}, Binary: {binary_string}')

    def returnMessageType(self):
        return (ENUMS.MSGTYPE.REQUEST if (int(self.msgResp, 2) == 0) else ENUMS.MSGTYPE.RESPONSE)

    def returnCommand(self, debug = False):
        cmd = self.msgCmd
        cmdStr = ""

        if cmd is ENUMS.COMMAND.SYSTEM_BEFEHL:
            cmdStr = "System Command"
        elif cmd is ENUMS.COMMAND.LOK_DIR:
            cmdStr = "Locomotive Direction"
        elif cmd is ENUMS.COMMAND.LOK_FCT:
            cmdStr = "Locomotive Function"
        elif cmd is ENUMS.COMMAND.LOK_VELOCITY:
            cmdStr = "Locomotive Speed/Velocity"
        elif cmd is ENUMS.COMMAND.LOK_DISCOVERY:
            cmdStr = "Locomotive Discovery"
        elif cmd is ENUMS.COMMAND.CTRL_ACCESSORY:
            cmdStr = "Control Accessory"
        else:
            cmdStr = "not implemented in code"

        if debug: print(cmdStr)
        return cmd