import pandas as pd

from funcoes_auxiliares.crawler import *
from funcoes_auxiliares.request import *

newRows = resquest_new_rows()
pre_proces_new_rows(newRows)

crawler()