import pandas as pd

from funcoes_auxiliares.request_openDataSus import *
from funcoes_auxiliares.request_integraSus import *

request_vacinados()

newRows = resquest_new_rows()
pre_proces_new_rows(newRows)