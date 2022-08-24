import settings as settings
import P4 as P4
from P4 import P4Exception

#perforce_main('denis.balikhin', 'm2ue4m2ue4', 'ssl:perforcesrv:1666')
perforce_host = ''

def work_in_depo(p4):
    perforce_update(p4, settings.get_Settings_field('Depot'), settings.get_Settings_field('Workspace'))

def perforce_main(p4):
    perforce_login(p4, True)
    work_in_depo(p4)

def perforce_login(p4, show_profile=False):
    print('Profile settings: ' + settings.get_Settings_field('Name'))
    if show_profile:
        for key in settings.get_Settings_profile():
            print(key +'=' + settings.get_Settings_field(key))

    print('Start Py Perforce : ' + settings.get_Settings_field('Host'))
    if p4.user:
        print('Found API Perforce user: ' + settings.get_Settings_field('User'))
    else:
        print('Accces API driver not found ' + settings.get_Settings_field('Host'))

    try:
        p4.user = settings.get_Settings_field('User')
        p4.password = settings.get_Settings_field('Pwd')

        session = p4.connect()
    except P4Exception:
        for e in session.errors:  # Display errors
            print(e)
    if session.connected():
        print('Succes and ready for command : '+str(session))
        session.run_login() #pass
    else:
        print('Perforce Not Connected')

def perforce_update(p4, depot, workspace):
    try:
        print('Try Update depot:')
        client = p4.fetch_client()
        print(client['View'])
        p4.client = workspace
        print('Workspace: '+p4.client)
        #p4 sync //depot/UE_Perforce01/...#head
        print('Try Sync Force : '+"{}/...#head".format(depot))
        sync = p4.run_sync("-f", "{}/...#head".format(depot))
        print('SYNC : '+str(sync))
    except P4Exception:
        for e in p4.errors:  # Display errors
            print(e)
    finally:
        p4.disconnect()

def get_perforce_info(show_info=False):
    p4 = P4.P4(port=settings.get_Settings_field('Host'))
    info = p4.run("info")  # Run "p4 info" (returns a dict)
    if show_info:
        print('Print Info:')
        for key in info[0]:  # and display all key-value pairs
            print(str(key) + "=" + info[0][key])
    return info

def update():
    print(P4.P4.identify())
    perforce_host = settings.get_Settings_field('Host')
    p4 = P4.P4(port=perforce_host)
    perforce_main(p4)

update()

