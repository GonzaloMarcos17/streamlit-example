# Librerias basicas:

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import base64
from datetime import datetime

# Componentes streamlit:
from streamlit_oauth import OAuth2Component
from streamlit_modal import Modal
from st_mui_dialog import st_mui_dialog
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, GridUpdateMode # GridOptionsBuilder para meterle mas opciones a las tablas
from st_pages import add_page_title, show_pages, Page

# Configuracion y clases: 
from config import *
from PIL import Image
from css import Css


css = Css()

class FunctionsManager:
    
    def __init__(self): #-> None:
        pass

    def pages():
        show_pages(pages=
                    [
                      Page("landing.py", "Home"),
                      Page("otherPages/edicionDatos.py", "Edición de datos"),
                      Page("otherPages/insercionDatos2.py", "Inserción de datos" ) 
                    ]
                )