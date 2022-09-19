import settings as settings
import P4 as P4
from P4 import P4Exception
from datetime import datetime as dt

#perforce_main('denis.balikhin', 'm2ue4m2ue4', 'ssl:perforcesrv:1666')
perforce_host = ''

def work_in_depo(p4):
    perforce_update(p4, settings.get_PerforceSettingsByName('Depot'), settings.get_PerforceSettingsByName('Workspace'))

def perforce_main(p4):
    perforce_login(p4, True)
    work_in_depo(p4)

def perforce_login(p4, show_profile=False):
    print('Profile settings: ' + settings.get_PerforceSettingsByName('Name'))
    if show_profile:
        for key in settings.get_PerforceSettings():
            print(key +'=' + settings.get_PerforceSettingsByName(key))

    print('Start Py Perforce : ' + settings.get_PerforceSettingsByName('Host'))
    settings.print_log('Start Perforce: ' + settings.get_PerforceSettingsByName('Host'))
    if p4.user:
        print('Found API Perforce user: ' + settings.get_PerforceSettingsByName('User'))
    else:
        print('Accces API driver not found ' + settings.get_PerforceSettingsByName('Host'))

    try:
        p4.user = settings.get_PerforceSettingsByName('User')
        p4.password = settings.get_PerforceSettingsByName('Pwd')

        session = p4.connect()
    except P4Exception:
        for e in session.errors:  # Display errors
            print(e)
            settings.print_log('Error connect perforce: ' + e, 2)
    if session.connected():
        print('Succes and ready for command : '+str(session))
        settings.print_log('Try Update depot: ' + str(session))
        session.run_login() #pass
    else:
        print('Perforce Not Connected')

class P4ProgressHandler(P4.Progress):
    curr_syncfile = ''
    curr_syncunits = -1
    #def init(self, type):
        #print( "Progress.init with '%s'" % type)
    def update(self, units):
        tn = dt.now().strftime("%H:%M:%S.%f")
        print("Progress PERFORCE Syncing [%s : %s]" % (tn, units))
        self.curr_syncunits = units
    #def setTotal(self, total):
        #P4.Progress.setTotal(self, total)
        #print("Progress.setTotal with '%s' " % total)
    def setDescription(self, description, units):
        print("Progress PERFORCE Syncing ['%s' # %s]" % (description, self.curr_syncunits))
        self.curr_syncfile = description
    def done(self, fail):
        if fail > 0:
            print("Failed Sync : %s " % self.curr_syncfile)
            settings.print_log('Failed Sync : ' + self.curr_syncfile, 2)


def perforce_update(p4, depot, workspace):
    try:
        start_tn = dt.now()
        p4.progress = P4ProgressHandler()
        settings.print_log('Try Update depot: ' + depot, 0)
        print('Try Update depot: '+depot)
        client = p4.fetch_client()
        print(client['View'])
        p4.client = workspace
        print('Workspace: '+p4.client)
        #p4 sync //depot/UE_Perforce01/...#head
        print('Try Sync get last changes: '+"{}...#head".format(depot))
        settings.print_log('Try Sync get last changes: ' + "{}...#head".format(depot), 0)
        # sync = p4.run_sync("-f", "{}...#head".format(depot))
        sync = p4.run("sync", "{}...#head".format(depot))
        print('SYNC : '+str(sync))
        used_tn = dt.now() - start_tn
        tn = dt.now().strftime("%H:%M:%S")
        print('Perforce Syncing finished : ' + depot + ' finished time ' + tn + ' Used_time: ' + str(used_tn))
        settings.print_log('Perforce Syncing finished : ' + depot + ' finished time ' + tn + ' Used_time: ' + str(used_tn), 0)
    except P4Exception:
        for e in p4.errors:  # Display errors
            print('Perforce Error Sync fired: ' + e)
            settings.print_log('Perforce Error Sync fired: ' + e, 2)
            #unlink: C:\MI_Cantrollermonitor.uasset: The process cannot access the file because it is being used by another process.
            syncfile = e.replace("unlink: ", "")
            syncfile = syncfile.replace(": The process cannot access the file because it is being used by another process.", "")
            settings.print_log('Perforce Error Sync need forced file: ' + syncfile, 2)
            print('Try Force Sync File: ' + "{}#head".format(syncfile))
            settings.print_log('Try Force Sync File: ' + "{}#head".format(syncfile), 0)
            settings.print_log('Try Force Run command : sync -f ' + "{}#head".format(syncfile), 0)
            syncForce = p4.run("sync", "-f", "{}#head".format(syncfile))
            print('SYNC Force: '+str(syncForce))
            settings.print_log('SYNC Force: ' + str(syncForce), 0)
    else:
        used_tn = dt.now() - start_tn
        settings.print_log('SYNC finished log : ' + str(sync), 0)
        print('Perforce Updated no exception! Used_time: ' + str(used_tn))
        settings.print_log('Perforce Updated no exception! Used_time: ' + str(used_tn), 0)
        p4.disconnect()
        print('Perforce disconnected')
    finally:
        used_tn = dt.now() - start_tn
        print('Perforce Finally Updated. Used_time: '+str(used_tn))
        settings.print_log('Perforce Finally Updated. Used_time: ' + str(used_tn), 0)

def get_perforce_info(show_info=False):
    p4 = P4.P4(port=settings.get_PerforceSettingsByName('Host'))
    info = p4.run("info")  # Run "p4 info" (returns a dict)
    if show_info:
        print('Print Info:')
        for key in info[0]:  # and display all key-value pairs
            print(str(key) + "=" + info[0][key])
    return info

def update():
    print(P4.P4.identify())
    perforce_host = settings.get_PerforceSettingsByName('Host')
    p4 = P4.P4(port=perforce_host)
    perforce_main(p4)

update()

