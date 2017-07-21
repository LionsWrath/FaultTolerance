# -*- coding: utf-8 -*-

import Pyro4

def changeName(server):
    print "\n" + "="*30 + "\n"
    n = raw_input("\t> Digite o novo nome do servidor: ")

    server.init(n)

    return True

def connectDatabase(server):
    print "\n" + "="*30 + "\n"
    n = raw_input("\t> Digite o id da database: ")

    db = Pyro4.Proxy(ns.lookup(n))

    server.accessDatabase(db)

    return True

def leaveDatabase(server):
    print "\n" + "="*30 + "\n"
    n = raw_input("\t> Digite o id da database: ")
    
    db = Pyro4.Proxy(ns.lookup(n))

    server.disconnectDatabase(db)

    return True

def listDatabases(server):
    server.listDatabases()

    return True

def getAll(server):
    print "\n" + "="*30 + "\n"
    idx = raw_input("\t> Digite o índice da database: ")

    server.retrieveAll(int(idx))

    return True

def getValue(server):
    print "\n" + "="*30 + "\n"
    idx = raw_input("\t> Digite o indice da database: ")
    index = raw_input("\t> Digite o identificador do elemento: ")

    server.retrieve(int(idx), int(index))

    return True

def deleteValue(server):
    print "\n" + "="*30 + "\n"
    idx = raw_input("\t> Digite o indice da database: ")
    value = raw_input("\t> Digite o elemento: ")

    server.delete(int(idx), value)

    return True

def insertValue(server):
    print "\n" + "="*30 + "\n"
    idx = raw_input("\t> Digite o indice da database: ")
    value = raw_input("\t> Digite o elemento: ")

    server.insert(int(idx), value)

    return True

def propagateValue(server):
    print "\n" + "="*30 + "\n"
    value = raw_input("\t> Digite o elemento: ")

    server.propagate(value)

    return True

def broadcastValue(server):
    print "\n" + "="*30 + "\n"
    value = raw_input("\t> Digite o elemento: ")

    server.broadcast(value)

    return True

def ping(server):
    print "\n" + "="*30 + "\n"

    option = ''
    while option != "y" and option != "n":
        option = raw_input(
                "\t> Deseja deletar conexões falhas?(y/n) ")

    delete = False
    if option == "y":
        delete = True

    server.ping(delete)

    return True


with Pyro4.locateNS() as ns:
    db_1 = Pyro4.Proxy(ns.lookup("one.db"))
    db_2 = Pyro4.Proxy(ns.lookup("two.db"))
    db_3 = Pyro4.Proxy(ns.lookup("three.db"))

    server = Pyro4.Proxy(ns.lookup("server.main"))
    server.init('test')

    server.accessDatabase(db_1)
    server.accessDatabase(db_2)
    server.accessDatabase(db_3)

    loop = True
    while (loop):
        print "\n" + "="*30 + "\n"

        dummy = lambda *args : False

        commands = [
                #Normal ones
                "Mudar nome do servidor",
                "Conectar nova database",
                "Desconectar database",
                "Listar databases",
                "Retornar valores em uma database",
                "Retornar valor por índice",
                "Deletar valor por conteúdo",
                "Inserir valor em database",
                
                #Complex ones
                "Propagar valor",
                "Broadcast de valor",
                "Ping",

                "Sair"
        ]

        print "Comandos:"
        for idx,val in enumerate(commands, start=1):
            print "\t" + str(idx) + " : " + val

        c = raw_input("\n> Digite o que deseja realizar: ")

        loop = {
                "1" : changeName,
                "2" : connectDatabase,
                "3" : leaveDatabase,
                "4" : listDatabases,
                "5" : getAll,
                "6" : getValue,
                "7" : deleteValue,
                "8" : insertValue,
                "9" : propagateValue,
                "10": broadcastValue,
                "11": ping
                }.get(c, dummy)(server)
    
    server.disconnectAll()

    print "Finalizando cliente. . ."
