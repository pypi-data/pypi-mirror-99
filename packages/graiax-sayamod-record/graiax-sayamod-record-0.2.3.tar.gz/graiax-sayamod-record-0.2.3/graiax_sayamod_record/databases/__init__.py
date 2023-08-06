import os
from . import *


db_filepath = os.path.join(os.getcwd(), "data", "graiax_sayamod_record", "db")
if not os.path.exists(db_filepath):
    os.makedirs(db_filepath)