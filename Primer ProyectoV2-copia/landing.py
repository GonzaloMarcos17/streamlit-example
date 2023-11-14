import streamlit as st
import pandas as pd
import numpy as np
from streamlit_oauth import OAuth2Component
import requests
import json
import base64

from st_pages import add_page_title, show_pages, Page

from PIL import Image
from css import Css

css = Css()

# Documentos necesarios: 

logo          = Image.open("pictures\\ideaingenieria-200x200-72p-rgb.png")
logoPrincipal = Image.open("pictures\\ideaingenieria-300x250-75p-rgb.png")
imagenFondo   = Image.open("pictures\\Imagen_IDEA-removebg-preview.png")

# Configuración general de la página: 
st.set_page_config(
    page_title            = "Insercción de datos",
    page_icon             =  logo,
    layout                = "wide",
    initial_sidebar_state = "expanded" 
)

show_pages(pages=
            [
              Page("landing.py", "Home"),
              Page("otherPages/edicionDatos.py", "Edición de datos"),
              Page("otherPages/insercionDatos.py", "Inserción de datos" ) 
            ]
        )

st.image(logoPrincipal, 
         caption = "",
         width   = 200
)

# class css code:

css.getBgPicutre()
#css.deleteHeaderMenu()

col1, col2 = st.columns(2)

with col1:
    st.image(imagenFondo, 
             caption = "",
             width   = 300
    )

    css.hideFullScreen()

with col2:
    st.markdown(
        """
                # Bienvenidos
        """
    )

#st.write(st.session_state)

st.selectbox("elige", ["perro", "gato"])