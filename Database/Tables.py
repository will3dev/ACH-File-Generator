import sys
from os import path

class Tables:
    BUNDLE_DIR = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
    BUNDLE_DIR
    DB_ORIGINATORS = './DATA/originators.db'
    DB_RECEIVERS = './DATA/receivers.db'
    ORIGINATORS = path.join(BUNDLE_DIR, "..", "DATA", "originators.db")
    RECEIVERS = path.join(BUNDLE_DIR, "..", "DATA", "receivers.db")

t = Tables()
print(t.ORIGINATORS)
print(t.RECEIVERS)