import streamlit as st
import base64

class Css():
    def __init__(self):
       pass

    def deleteHeaderMenu(self):
        'Esta funcion elinima los puntos de arriba a la derecha'

        hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
             """
        return st.markdown(hide_st_style, unsafe_allow_html=True)
    
    def getBgPicutre(self):
    
        photo = "pictures\\fondos-IDEA_1920x1080-C_2023.jpg"
        f = open(photo, "rb")
        imgCode = f.read()
        backGround = base64.b64encode(imgCode).decode()
    
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{backGround}");
        background-size: auto;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
        return st.markdown(page_bg_img, unsafe_allow_html=True)
    
    def hideFullScreen(self):
        'Esta función elimina el botón de ampliar a pantalla completa las imágenes'

        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''

        return st.markdown(hide_img_fs, unsafe_allow_html=True)

    def style(self) -> str:
        style ="""
    <style>
        [data-testid="stHeader"]{
            background-color: transparent;
        }
        .img-circle {
            border-radius: 50%;
            width: 40px;
            height: 40px;
            vertical-align: middle;
            margin-right: 10px;
        }

    </style>
    """
        return st.markdown(style, unsafe_allow_html=True)
    
    # He sacado esto de style:

        #     .name-with-img {
        #     display: flex;
        #     align-items: center;
        #     font-size: 14px;
        #     font-weight: bold;
        #     justify-content: flex-end;
        #     position: fixed;
        #     z-index: 20000000000;
        #     top: 4px;
        #     width: 100%;
        #     left: 0px;
        #     right: 0px;
        #     padding-right: 83px;
        # }
