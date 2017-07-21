from database import Database
from server import Server

db1 = Database()
db2 = Database()

db1.init('red', list())
db2.init('blue', list())

server = Server()
server.init('test')

server.accessDatabase(db1)
server.accessDatabase(db2)

server.listDatabases()

server.insert(0,'haha')
server.insert(1,'hehe')

server.retrieveAll(0)
server.retrieveAll(1)

server.retrieve(0,0)
server.retrieve(1,0)

server.delete(0,'haha')
#server.delete(1,'hehe')

server.retrieveAll(0)
server.retrieveAll(1)

server.disconnectDatabase(0)
server.disconnectDatabase(0)
