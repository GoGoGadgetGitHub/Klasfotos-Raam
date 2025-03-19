from os import path, getcwd, pardir

'''
def get_local_net_drives():
    drives, total, resume = win32net.NetUseEnum(None, 0)

    net_drives = {}

    for drive in drives:
        for key in drive:
            if key == 'local':
                net_drives[drive['remote'].split('\\')[-1]] = drive[key]

    return net_drives

drives = get_local_net_drives()

LOC_2016 = f"{drives['2016']}\\"
LOC_SKOLE = LOC_2016 + "SKOLE 2021\\"
STYLE = ""
LOC_ASSETS = f"{LOC_DOCUMENTS}verwerking\\assets\\"
LOGO = f"{LOC_ASSETS}logo\\abf_logo.png"
'''

PROJECT = path.join(getcwd())
LOC_DOCUMENTS = path.join(path.expanduser('~'), "Documents")
LOC_PICTURES =  path.join(path.expanduser('~'), "Pictures")
ASSETS = path.join(PROJECT, 'assets')
SCHEMES = path.join(PROJECT, 'schemes')
STYLE = ''

with open(path.join( ASSETS, 'stylesheet', 'Combinear.qss'), 'r') as style:
    STYLE = style.read()
LOGO = path.join(ASSETS, 'abf_logo.png')

with open(path.join(ASSETS, "stylesheet", "Combinear.qss"), 'r') as style:
    STYLE = style.read()
