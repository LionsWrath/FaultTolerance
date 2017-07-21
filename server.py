import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server(object):

    name = ''
    accessed = []

    def init(self, name):
        self.name = name

    def getDatabase(self, idx):
        try:
            return self.accessed[idx]
        except:
            print "\t\t> The database {0} does not exist!".format(idx)
            return False

    def accessDatabase(self, db):
        if db in self.accessed:
            print "\t> Server({0}) already accessed".format(
                    db.getID())
            return

        self.accessed.append(db)

        print "\t> Server ({0}) accessed database ({1})".format(
                self.name, db.getID())

    def disconnectDatabase(self, db):
        self.accessed.remove(db)

        print "\t> Server ({0}) disconnected from database.".format(
                self.name)

    def disconnectAll(self):
        print "\t> Disconnecting all databases. . ."
        for db in self.accessed:
            self.disconnectDatabase(db)

    def listDatabases(self):
        print "\t\t> Databases List:"
        for idx, val in enumerate(self.accessed):
            print "\t\t\t{0} : Database ({1})".format(
                    idx, 
                    val.getID())

    def retrieveAll(self, idx):
        database = self.getDatabase(idx)
        if not database:
            return

        data = database.list()

        print "\t\t> Retrieving all data from database {0}".format(
                database.getID())
        for index, val in enumerate(data):
            print "\t\t\t{0} : Item ({1})".format(index, val)

    def retrieve(self, idx, index):
        database = self.getDatabase(idx)
        if not database:
            return

        data = database.get(index)

        if data:
            print "\t\t> Item retrieved: {0}".format(data)
        else:
            print "\t\t> Item does not exist on {0}".format(
                    database.getID())

    def delete(self, idx, item):
        database = self.getDatabase(idx)
        if not database:
            return

        removed = database.remove(item)

        if removed:
            print "\t\t> Item removed: {0}".format(item)
        else:
            print "\t\t> Item does not exist on {0}".format(
                    database.getID())

    def insert(self, idx, item):
        database = self.getDatabase(idx)
        if not database:
            return

        inserted = database.add(item)

        if inserted:
            print "\t\t> Item inserted in database ({0}): {1}".format(
                    database.getID(),
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
                print "\t\t\t> Could't reach database."

    def ping(self, delete=False):
        print "\t\t> Checking servers . . ."
        toDelete = []

        for idx,db in enumerate(self.accessed):
            try:
                db.ping()
                print "\t\t\t> Ping: Database {0}. . . OK".format(
                        idx)
            except:
                print "\t\t\t> Pink: Database {0}. . . ERROR".format(
                        idx)
                if delete:
                    toDelete.append(db)

        for db in toDelete:
            self.diconnectDatabase(db)
        
def main():

    Pyro4.Daemon().serveSimple({
            Server  : "server.main"
        },
        ns=True, verbose=True)

if __name__ == "__main__":
    main()
