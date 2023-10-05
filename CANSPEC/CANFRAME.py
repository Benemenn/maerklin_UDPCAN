from CANSPEC import CANIDENTIFIER

class CANFRAME:
    def __init__(self, data_bytes_list):
        self.CANMSGIdentifier = CANIDENTIFIER.CANIDENTIFIER(list(data_bytes_list)[:4])
        self.CANMSGDlc = list(data_bytes_list)[4:5]
        self.CANMSGData = list(data_bytes_list)[5:14]

    def printData(self):
        print("Data: ", end="")
        for databyte in self.CANMSGData:
            print(f"{hex(int(databyte, 16))} ", end="")
        print("\n")

    def explainIdentifier(self):
        self.CANMSGIdentifier.explainIdentifier()