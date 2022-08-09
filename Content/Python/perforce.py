import settings as cfg
import P4 as P4
from P4 import P4Exception

#perforce_main('denis.balikhin', 'm2ue4m2ue4', 'ssl:perforcesrv:1666')
perforce_host = ''

def work_in_depo():
    perforce_update(cfg.get_Settings_field('Depot'), cfg.get_Settings_field('Workspace'))

def perforce_main():
    perforce_login()
    work_in_depo()

def perforce_login(show_profile=False):
    print('Profile settings: ' + cfg.get_Settings_field('Name'))
    if show_profile:
        for key in cfg.get_Settings_profile():
            print(key+'='+cfg.get_Settings_field(key))

    print('Start Py Perforce : '+cfg.get_Settings_field('Host'))
    if p4.user:
        print('Found API Perforce user: '+cfg.get_Settings_field('User'))
    else:
        print('Accces API driver not found '+cfg.get_Settings_field('Host'))

    try:
        p4.user = cfg.get_Settings_field('User')
        p4.password = cfg.get_Settings_field('Pwd')

        session = p4.connect()
    except P4Exception:
        for e in session.errors:  # Display errors
            print(e)
    if session.connected():
        print('Succes and ready for command : '+str(session))
        session.run_login() #pass
    else:
        print('Perforce Not Connected')

def perforce_update(depot, workspace):
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

def get_perforce_info(show_info=False):
    info = p4.run("info")  # Run "p4 info" (returns a dict)
    if show_info:
        print('Print Info:')
        for key in info[0]:  # and display all key-value pairs
            print(str(key) + "=" + info[0][key])
    return info

perforce_host = cfg.get_Settings_field('Host')
p4 = P4.P4(port=perforce_host)
perforce_main()

