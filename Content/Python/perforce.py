import P4 as P4
from P4 import P4Exception

def work_in_depo(p4):
    perforceinfo(p4, True)
    depo2 = "//depot/WHP_UE5"
    #perforce_update(p4, "//depot/Test_Poj_01", "denis.balikhin_pc-14-025_8545")
    perforce_update(p4, "//depot/Test01", "denbaster_DESKTOP-IERDB91_350")

def perforce_main(user, passw, perforce):
    #p4 = P4.P4(client="denbaster_DESKTOP-IERDB91_350", port="1666")
    p4 = P4.P4(port=perforce)
    p4.user = user
    p4.password = passw

    print('Start Py Perforce with workspace: '+p4.client)
    if p4.user:
        print('Found API Perforce user : '+p4.user+' host:'+p4.host+' port:'+p4.port)
    else:
        print('Accces API driver not found ')

    com1 = 'p4 sync //depot/Test_Poj_01/...#head'
    try:
        session = p4.connect()
    except P4Exception:
        for e in p4.errors:  # Display errors
            print(e)
    if p4.connected():
        print('Succes and ready for command : '+str(session))
        p4.run_login() #pass
        work_in_depo(p4) #main working place
    else:
        print('Perforce Not Connected')

def perforce_update(p4, depot, workspace):
    try:
        print('Try Update depot:')
        client = p4.fetch_client()
        print(client['View'])
        p4.client = workspace
        print('Workspace: '+p4.client)
        sync = p4.run_sync("-f", "{}/...#head".format(depot))
        print('SYNC : '+str(sync))
    except P4Exception:
        for e in p4.errors:  # Display errors
            print(e)
    finally:
        p4.disconnect()

def perforceinfo(p4,outinfo_bool):
    info = p4.run("info")  # Run "p4 info" (returns a dict)
    if outinfo_bool:
        print('Print Info:')
        for key in info[0]:  # and display all key-value pairs
            print(str(key) + "=" + info[0][key])
    return info

perforce_main('denbaster', 'm2ue5m2ue5', '3.25.99.243:1666')
#perforce_main('denis.balikhin', 'm2ue4m2ue4')
