import xml.etree.ElementTree as et
import paypalrestsdk

class PayPalHandler():
    def __init__(self, parameterFileLocation):
        self.configParse = et.parse(parameterFileLocation)
        self.root = self.configParse.getroot()
        self.roots = {}

        it = -1
        for tree in self.root:
            it += 1
            self.roots[tree.tag] = self.root[it]

        self.config = {}

        for data in self.roots["paypal"]:
            self.__type = data.get("type")
            if(self.__type == "mode"):
                self.config["mode"] = data.text
            elif(self.__type == "clientid"):
                self.config["client_id"] = data.text
            elif(self.__type == "clientsecret"):
                self.config["client_secret"] = data.text

        paypalrestsdk.configure(self.config)

if __name__ == "__main__":
    ist = DataBaseHandler("config.xml")
