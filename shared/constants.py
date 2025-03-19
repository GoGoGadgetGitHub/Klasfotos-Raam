from os import path

LOC_DOCUMENTS = path.expanduser('~') + "\\Documents"
LOC_PICTURES = path.expanduser('~') + "\\Pictures"
LOC_SKOLE = LOC_PICTURES + "\\SKOLE 2021"
LOC_ASSETS = f"{LOC_DOCUMENTS}\\Verwerking\\assets\\"
LOGO = f"{LOC_ASSETS}logo\\abf_logo.png"
LOC_FONTS = f"{LOC_ASSETS}\\fonts"
STYLE = ""

with open(f"{LOC_ASSETS}stylesheet\\Combinear.qss", 'r') as style:
    STYLE = style.read()