import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server(object):

    name = ''
    accessed = []

    def init(self, name):
        self.name = name

    def accessDatabase(self, db):
        if db in self.accessed:
            print "\t> Server({0}) already accessed".format(
                    db.getID())
            return

        self.accessed.append(db)

        print "\t> Server ({0}) accessed database ({1})".format(
                self.name, db.getID())

    def disconnectDatabase(self, db):
        print "\t> Server ({0}) disconnecting from database ({1})".format(
                self.name, 
                db.getID())

        self.accessed.remove(db)

    def listDatabases(self):
        print "\t\t> Databases List:"
        for idx, val in enumerate(self.accessed):
            print "\t\t\t{0} : Database ({1})".format(
                    idx, 
                    val.getID())

    def retrieveAll(self, idx):
        data = self.accessed[idx].list()

        print "\t\t> Retrieving all data from database {0}".format(
                self.accessed[idx].getID())
        for index, val in enumerate(data):
            print "\t\t\t{0} : Item ({1})".format(index, val)

    def retrieve(self, idx, index):
        data = self.accessed[idx].get(index)

        if data:
            print "\t\t> Item retrieved: {0}".format(data)

    def delete(self, idx, item):
        removed = self.accessed[idx].remove(item)

        if removed:
            print "\t\t> Item removed: {0}".format(item)

    def insert(self, idx, item):
        inserted = self.accessed[idx].add(item)

        if inserted:
            print "\t\t> Item inserted in database ({0}): {1}".format(
                    self.accessed[idx].getID(),
                    item)

    def propagate(self, item):
        print "\t\t> Begin propagating. . ."

        databases = self.accessed[:]
        while True:
            if not databases:
                print "\t\t> No database connected, can't propagate"
                break

            first = databases[0]
            databases.remove(first)
            try:
                first.propagate(databases, item)
                print "\t\t> Propagated to {0}".format(first.getID())
                break
            except:
                print "\t\t> Error propagating."

    def broadcast(self, item):
        print "\t\t> Broadcasting {0} to all connected databases!".format(item)
        
        for db in self.accessed:
            try:
                print "\t\t\t> Database {0}. . .".format(db.getID())
                db.add(item)
            except:
                print "Could't reach database."

def main():

    Pyro4.Daemon().serveSimple({
            Server  : "server.main"
        },
        ns=True, verbose=True)

if __name__ == "__main__":
    main()
