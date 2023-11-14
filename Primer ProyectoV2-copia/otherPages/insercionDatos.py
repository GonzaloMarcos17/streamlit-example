# Librerias: 

import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, GridUpdateMode # GridOptionsBuilder para meterle mas opciones a las tablas
from streamlit_modal import Modal
from st_mui_dialog import st_mui_dialog
from PIL import Image
import base64
from css import Css

# Documentos necesarios: 

logo = Image.open("pictures/ideaingenieria-200x200-72p-rgb.png")
logoPrincipal = Image.open("pictures/ideaingenieria-300x250-75p-rgb.png")
df       = pd.read_csv("dfPruebaV2.csv")

# Creamos variables necesarias:
 
UTD      = df["UTD"].unique()
gestores = df["Gestor"].unique()

# Configuración de la página: 

st.set_page_config(
    page_title            = "Insercción de datos",
    page_icon             =  logo,
    layout                = "wide",
    initial_sidebar_state = "collapsed" 
)

st.image(logoPrincipal, 
         caption = "",
         width   = 200
)

# Class css code:

css = Css()
css.getBgPicutre()
#css.deleteHeaderMenu()

# Form: 

datos = st.session_state

def main(): 

    global df
    
    with st.form("Inserción de nuevos datos", clear_on_submit = True):

        col3, col4 = st.columns(2)

        with col3:

            expediente = st.text_input("Expediente", 
                        value            = "", 
                        max_chars        =  5, 
                        key              = "expediente", # mirar keys -> para el manejo de estado y actualizaciones (session state)
                        type             = "default", 
                        help             = None, 
                        autocomplete     = None, 
                        on_change        = None, 
                        args             = None, 
                        kwargs           = None,
                        placeholder      = None,
                        disabled         = False, 
                        label_visibility = "visible"
                        )
            
            utd = st.selectbox("UTD", 
                        UTD, 
                        index        = 0, 
                        # placeholder ="Selecciona una opción", 
                        key          = "UTD"
                        )
            
            fechaApertura = st.date_input("Fecha apertura", 
                        value            = None, 
                        min_value        = None, 
                        max_value        = None, 
                        key              = "fechaApertura", 
                        help             = None, 
                        on_change        = None, 
                        args             = None, 
                        kwargs           = None,
                        format           =  "DD/MM/YYYY",
                        disabled         = False, 
                        label_visibility = "visible"
                        )
        
        with col4:

            gestor = st.selectbox("Gestor", gestores, 
                        index         = 0, 
                        # placeholder ="Selecciona una opción", 
                        key         = "gestor"
                        )
            
            with st.expander("Observaciones"):

                obs = st.text_area("", placeholder= "Escriba aqui los comentarios...", key= "obs")

            st.form_submit_button(label="Enviar", 
                        help                = None, 
                        on_click            = None, 
                        args                = None, 
                        kwargs              = None, 
                        type                = "secondary", 
                        disabled            = False, 
                        use_container_width = False
                        )
    st.write(datos)
    st.write(datos["expediente"])
   

if __name__ =="__main__":
    main()