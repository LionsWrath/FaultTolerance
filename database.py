import Pyro4

@Pyro4.expose
class Database(object):
    
    # Always have to call this
    def init(self, id, data):
        self.data = data
        self.id = id

        return self
    
    def ping(self):
        print "> Returning ping. . ."
        return True

    def getID(self):
        print "> Returning ID. . ."
        return self.id

    def list(self):
        print "> Listing data. . ."
        return self.data

    def get(self, index):

        try:
            item = self.data[index]
            print "> Returning data. . . {0}".format(item)
        except:
            print "> Error: Item not found!"
            return False

        return item

    def remove(self, item):
        print "> Removing data. . . {0}".format(item)
    
        try:
            self.data.remove(item)
        except:
            print "> Error: Item not found!"
            return False

        return True

    def add(self, item):
        print "> Inserting data. . . {0}".format(item)
        self.data.append(item)

        return True

    def propagate(self, databases, item):
        self.add(item)

        while True:
            if not databases:
                print "> Propagation ended!"
                break
            else:
                next = databases[0]
                try:
                    databases.remove(next)
                    print "> Propagating from {0} to {1}".format(
                            self.id,
                            next.getID())

                    next.propagate(databases, item)
                    break
                except:
                    print "> Error propagating from {0}".format(
                                self.id)

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
