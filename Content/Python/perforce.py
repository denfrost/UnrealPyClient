import P4 as P4
from P4 import P4Exception

def perforce_main():
    #p4 = P4.P4(client="denis.balikhin_pc-14-025_8545", port="1666")
    p4 = P4.P4()
    p4.user = 'denis.balikhin'
    p4.password = 'm2ue4m2ue4'
    print('Start Py Perforce with workspace: '+p4.client)
    if p4.user:
        print('Found API Perforce user : '+p4.user)
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

    perforceinfo(p4, False)
    depo2 = "//depot/WHP_UE5"
    #perforce_update(p4, "//depot/Test_Poj_01")
    perforce_update(p4, depo2)

def perforce_update(p4,depot):
    try:
        print('Try Update depot:')
        client = p4.fetch_client()
        print(client['View'])
        p4.client = "denis.balikhin_pc-14-025_8545"
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

perforce_main()
