import Pyro4

@Pyro4.expose
class Database(object):
    
    # Always have to call this
    def init(self, id, data):
        self.data = data
        self.id = id

        return self

    def getID(self):
        return self.id

    def list(self):
        print "> Listing data. . ."
        return self.data

    def get(self, index):
        print "> Returning data. . . {0}".format(self.data[index])

        item = self.data[index]

        return item

    def remove(self, item):
        print "> Removing data. . . {0}".format(item)

        self.data.remove(item)

        return True

    def add(self, item):
        print "> Inserting data. . . {0}".format(item)
        self.data.append(item)

        return True

def main():
    name = raw_input('Name of this database: ')
    id = raw_input('ID of the database: ')

    db = Database().init(id, list())

    Pyro4.Daemon().serveSimple({
            db : name
        },
        ns=True, verbose=True)

if __name__ == "__main__":
    main()
