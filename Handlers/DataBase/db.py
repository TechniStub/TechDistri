import mysql.connector as connector
import xml.etree.ElementTree as et

class DataBaseHandler():
    def __init__(self, parameterFileLocation):
        self.configParse = et.parse(parameterFileLocation)
        self.root = self.configParse.getroot()
        self.roots = {}

        it = -1
        for tree in self.root:
            it += 1
            self.roots[tree.tag] = self.root[it]

        self.config = {}

        for data in self.roots["database"]:
            self.__type = data.get("type")
            if(self.__type == "username"):
                self.config["user"] = data.text
            elif(self.__type == "password"):
                self.config["password"] = data.text
            elif(self.__type == "ip"):
                self.config["host"] = data.text

        self.config["database"] = "users"
        self.conn = connector.connect(**self.config)
        self.cursor = self.conn.cursor(buffered=True)

    def getQuery(self, query):
        self.cursor.execute(query)

        return self.cursor

    def getAvailableQueries(self):
        self.queries = {}

        for query in self.roots["queries"]:
            self.queries[query.attrib["name"]] = query.text

        return self.queries

    def getProducts(self):
        _ = self.getAvailableQueries()
        r = self.getQuery(self.queries["getProducts"])
        self.products = []
        index = -1
        for (Id, Row, Col, isPresent, Nom, NomC, Price, Stock, Min) in r:
            index += 1
            self.products.append({})
            self.products[index]["id"] = Id
            self.products[index]["row"] = Row
            self.products[index]["col"] = Col
            self.products[index]["isPresent"] = isPresent
            self.products[index]["nom"] = Nom
            self.products[index]["nomc"] = NomC
            self.products[index]["price"] = Price
            self.products[index]["stock"] = Stock
            self.products[index]["min"] = Min

        return self.products



if __name__ == "__main__":
    ist = DataBaseHandler("params.xml")
    result = ist.getQuery("SELECT * FROM users.Badges WHERE Data = '550785624180'")
    print(ist.getAvailableQueries())
    print(ist.getProducts())

    for (id, data) in result:
        print("{} {}".format(id, data))
