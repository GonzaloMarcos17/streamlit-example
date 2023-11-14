import pandas as pd
import numpy as np

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, GridUpdateMode # GridOptionsBuilder para meterle mas opciones a las tablas
from streamlit_modal import Modal

from streamlit_oauth import OAuth2Component
import requests
import time
import json
import base64

from PIL import Image
from css import Css
from datetime import datetime


# Documentos necesarios: 

logo          = Image.open("pictures\\ideaingenieria-200x200-72p-rgb.png")
logoPrincipal = Image.open("pictures\\ideaingenieria-300x250-75p-rgb.png")

# Creamos una instancia del componente OAuth2 con las credenciales y URLs de autorización

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
 

# Clases importadas: 

css = Css()

# Class css code:

css.hideFullScreen()
css.getBgPicutre()
#css.deleteHeaderMenu()

##### Prueba 4edicion datos 
def callbackButtons(cadena):
        st.session_state[cadena] = True
def dateInputWidget(dateValue, dateLabel): # Funcion que trata las fechas cuyo valor es NULL en la bbdd para evitar problemas de formato
    if dateValue == "NaT":
        return st.date_input(label = dateLabel,
                            value            = None,
                            key              = None,
                            format           =  "DD-MM-YYYY",
                            disabled         = False,
                            label_visibility = "visible"
                            )
    else:
        formattedDate = datetime.strptime(dateValue, '%Y-%m-%dT%H:%M:%S')
        return st.date_input(label = dateLabel,
                            value            = formattedDate,
                            key              = None,
                            format           =  "DD-MM-YYYY",
                            disabled         = False,
                            label_visibility = "visible"
                            )

st.write(st.session_state)

if "df" in st.session_state:
    df = st.session_state["df"]
    dateColumns = ['fe_apertura_definitiva', 'fe_informe', 'fecha_cierre', 'fe_recepcion', 'fecha_cierre_tecnico']
    for col in dateColumns:
        if df[col].dtype != 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col], format= "ISO8601")
            st.session_state["df"] = df
# Widgets:
colSelection, colFilter = st.columns([0.8,0.2])
with colSelection:
    dictSelections = {
                "Único": "unico",
                "Múltiple": "multiple"
                }
    options= list(dictSelections.keys())
    selectionType = st.radio("Tipo de selección:", options)#options=["unica", "multiple"], horizontal= True)
    selectionMode = dictSelections[selectionType]

with colFilter:
    filterExp = st.text_input("Busque por número de expediente:",
                               max_chars= 10,
                               on_change=None
                               )
# Creamos un flujo para el filtro: ESTE ES BASICO, SE PUEDE ACOMPLEJAR
if filterExp:
    df = df[df["expediente"] == filterExp]
# Construimos la base para la visualización interactiva de la tabla:
config = GridOptionsBuilder.from_dataframe(df)
# Configuramos el tipo dde selección y habilitamos el uso de checkboxes (para seleccionar las filas en cuestion)
config.configure_selection(selection_mode = selectionMode,
                            use_checkbox   = True
                            )
# Configuramos la visualización de la tabla: Cuántas filas por página
config.configure_pagination(enabled                 = True,
                            paginationAutoPageSize = False,
                            paginationPageSize     = 10
                            )
#Aplicamos las configuraciones de la tabla (podrám ser comunes para todas) y la montamos:
options = config.build()
grid = AgGrid(df,
              gridOptions            = options,
              columns_auto_size_mode = ColumnsAutoSizeMode.FIT_CONTENTS,
              update_mode            = GridUpdateMode.SELECTION_CHANGED,
              theme                  = "material"
              )

selection = grid["selected_rows"] # esto es una lista DE DICCIONARIOS

confirmation = Modal("Atención", key= any)

if selection:
    dropdownGestores = df["gestor"].unique().tolist()
    dropdownUTD      = df["UTD"].unique().tolist()
    dropdownMotivo   = df["motivo"].unique().tolist()
    dropdownTipoInf  = df["tipo_informado"].unique().tolist()
        
    colEdit,colDelete = st.columns([0.07,0.93]) # Añadir espacios en blanco
    
    with colEdit:
       edit   = st.button("Editar", on_click= callbackButtons, args= ("edit",))
    with colDelete:
        delete = st.button("Eliminar")
    
    if st.session_state.edit:
        for row in selection:
        #selectedRows = row # Cojo el segundo item de la lista, que es un diccionario con todo el contenido de la fila
            editableRow  = dict(list(row.items())[1:]) # cojo todos los elementos del diccionario menos el primero, que es informativo (mostrar si es necesario)
            # Se divide en diferentes columnas:
        col1, col2, col3 = st.columns(3)
        with col1:
            expedienteEd = st.text_input("Expediente",
                    value            = editableRow["expediente"],
                    max_chars        =  10,
                    key              = None,
                    disabled         = True,
                    label_visibility = "visible"
                    )
            fe_apertura_definitivaEd = dateInputWidget(dateValue= editableRow["fe_apertura_definitiva"],
                                                                            dateLabel= "Fecha apertura definitiva")
            gestorEd = st.selectbox("Gestor apertura",
                    dropdownGestores,  # Se trata del gestor que abre el expediente
                    index         = dropdownGestores.index(editableRow["gestor"]),
                    # placeholder = "Selecciona una opción",
                    key           = None,
                    )
            fe_informeEd = dateInputWidget(dateValue= editableRow["fe_informe"], # FECHA CRD
                                                            dateLabel= "Fecha informe")
            gestor_expedienteEd = st.selectbox("Gestor informe", dropdownGestores,  # Se trata del gestor que administra el expediente
                    index         = dropdownGestores.index(editableRow["gestor_expediente"]),
                    # placeholder ="Selecciona una opción",
                    key           = None,
                    )
            motivoEd = st.selectbox("Motivo",
                    dropdownMotivo,
                    index        = dropdownMotivo.index(editableRow["motivo"]),
                        # placeholder ="Selecciona una opción",
                        key          = None,
                        )
        with col2:
            facturacionEd = st.number_input("Facturación",
                    min_value =0.0,
                    max_value =999999.99,
                    value     = float(editableRow["facturacion"]),
                    step      = 0.1
                    )
            plazoEd = st.number_input("plazo",
                    min_value = None,
                    max_value = None,
                    value     = None,
                    format= "%f"
                    )
            tipoEd = st.text_input("Tipo", # Tiene que ser en mayusculas
                    value            = editableRow["tipo"],
                    key              = None,
                    type             = "default",
                    disabled         = False,
                    label_visibility = "visible"
                    )
            tipo_informadoEd = st.selectbox("Tipo Informado",
                    dropdownTipoInf,
                    index         = dropdownTipoInf.index(editableRow["tipo_informado"]),
                    # placeholder = "Selecciona una opción",
                    key           = None,
                    )
            utdEd = st.selectbox("UTD",
                    dropdownUTD,
                    index         = dropdownUTD.index(editableRow["UTD"]), #editableRow["UTD"],
                    # placeholder = "Selecciona una opción",
                    key           = None,
                    )
            diasSubsanacionEd = st.number_input("Días de subsanación",
                    min_value = None,
                    max_value = None,
                    value     = editableRow["dias_subsanacion"],
                    step= 1
                    )
        with col3:
            gestor_cierreEd = st.selectbox("Gestor de cierre", dropdownGestores,  # Se trata del gestor que administra el expediente
                    index         = dropdownGestores.index(editableRow["gestor_cierre"]),
                    # placeholder = "Selecciona una opción",
                    key           = None,
                    )
            fecha_cierreEd = dateInputWidget(dateValue= editableRow["fecha_cierre"],
                                                                        dateLabel= "Fecha cierre")
            fecha_cierre_tecnicoEd = dateInputWidget(dateValue= editableRow["fecha_cierre_tecnico"],
                                                                        dateLabel= "Fecha cierre Técnico")
            obs = st.text_area("Observaciones", placeholder= "Escriba aqui los comentarios...",
                               height= 200)
            submitted = st.button("Enviar")#, on_click= callbackButtons, args= ("submitted",))

        if submitted:
            confirmation.open()
            
        if confirmation.is_open():
            with confirmation.container():
                st.markdown(""" ### ¿Deseas guardar los cambios? """)
                yes = st.button("Sí")
                no  = st.button("No")
                if yes == True:
                    # Este diccionario deberá personalizarse para cada cuestionario, al igual que los campos meniconados anteriormente
                    dictNewData = {
                        "expediente": expedienteEd,
                        "fe_apertura_definitiva": fe_apertura_definitivaEd,
                        "gestor": gestorEd,
                        "fe_informe": fe_informeEd,
                        "gestor_expediente": gestor_expedienteEd,
                        "motivo": motivoEd,
                        "facturacion": facturacionEd,
                        "plazo": plazoEd,
                        "tipo": tipoEd,
                        "tipo_informado": tipo_informadoEd,
                        "UTD": utdEd,
                        "dias_subsanacion": diasSubsanacionEd,
                        "gestor_cierre": gestor_cierreEd,
                        "fecha_cierre": fecha_cierreEd,
                        "fecha_cierre_tecnico": fecha_cierre_tecnicoEd,
                        "observaciones": obs,
                    }
                    # Cambiamos los None por NULL para poder ejecutar la query en SQL y evitar porblemas de compatibilidad
                    # Debemos eliminar los [ ] de las listas para evitar porblemas de compatibilidad
                    keys = list(dictNewData.keys())
                    stringKeys = ', '.join(keys)
                    # Accedo a las valores del diccionario, configurando como quiero que aparezcan los missing values (None -> NULL)
                    values = list(dictNewData.values())
                    stringValues = ', '.join([f"'{value}'" if value is not None else 'NULL' for value in values])
                    # Establecemos el query y lo ejecutamos con las clases DbManager y DataManager
                    # Crear la lista de asignaciones de clave-valor para SET
                    update_list = [f"{key} = '{value}'" if value is not None else f"{key} = NULL" for key, value in dictNewData.items()]

                    # Unir la lista de asignaciones en una cadena
                    update_values = ', '.join(update_list)

                    # Construir la consulta SQL
                    query = f"UPDATE hc_expedientes_ibe_bck SET {update_values} WHERE expediente = '{expedienteEd}'"
                    
                    # query = f"UPDATE hc_expedientes_ibe_bck SET {stringKeys} = {stringValues} WHERE expediente = {expedienteEd}"
                    
                    # Limpiamos el caché para que en la próxima query se regenere y se muestre la tabla más actualizada
                    #FunctionsManager.reloadDf(self)
                    #st.cache_resource.clear()
                    confirmation.close()
                if no == True:
                    confirmation.close()
          


# df = fun.getDataFrame()

# dropdownGestores = df["gestor"].unique().tolist()
# dropdownUTD      = df["UTD"].unique().tolist()
# dropdownMotivo   = df["motivo"].unique().tolist()
# dropdownTipoInf  = df["tipo_informado"].unique().tolist()

# col1, col2 = st.columns(2)

# with col1:
#     tipo_seleccion = st.radio("Tipo de seleción:", options= ["unica", "multiple"])

# with col2: 
#     filterExp = st.text_input("Busque por número de expediente:",
#                               max_chars= 10,
#                               on_change=None )

# gd = GridOptionsBuilder.from_dataframe(df)

# gd.configure_selection(selection_mode          = tipo_seleccion, 
#                     use_checkbox               = True 
#                     #pre_selected_rows         = [], 
#                     #rowMultiSelectWithClick   = False, 
#                     #suppressRowDeselection    = False, 
#                     #suppressRowClickSelection = False, 
#                     #groupSelectsChildren      = True, 
#                     #groupSelectsFiltered      = True
#                     )

# gd.configure_pagination(enabled                = True,
#                         paginationAutoPageSize = False,
#                         paginationPageSize     = 10 
#                         )

# gridoptions = gd.build()

# if filterExp:
#     df = df[df['expediente'] == filterExp]

# gridTable  = AgGrid(df, 
#                      gridOptions            = gridoptions, 
#                      columns_auto_size_mode = ColumnsAutoSizeMode.FIT_CONTENTS,
#                      update_mode            = GridUpdateMode.SELECTION_CHANGED, 
#                      theme                  = "material")

# selection = gridTable["selected_rows"] # esto es una lista

# if selection: 
#     if tipo_seleccion == "unica":
#         edit   = st.button("Editar", disabled=False)
#         delete = st.button("Eliminar", disabled=False)

#         if edit:
#             for row in selection:
#                 #selectedRows = row # Cojo el primer item de la lista, que es un diccionario con todo el contenido de la fila
#                 editableRow  = dict(list(row.items())[1:]) # cojo todos los elementos del diccionario menos el primero, que es informativo (mostrar si es necesario)
#                 #st.write(editableRow)

#                 col1, col2, col3 = st.columns(3)
#                 with col1: 
#                     expedienteEd = st.text_input("Expediente", 
#                             value            = editableRow["expediente"], 
#                             max_chars        =  10, 
#                             key              = None, #"Expediente", 
#                             type             = "default", 
#                             help             = None, 
#                             autocomplete     = None, 
#                             on_change        = None, 
#                             args             = None, 
#                             kwargs           = None,
#                             placeholder      = None,
#                             disabled         = False, 
#                             label_visibility = "visible"
#                             )
#                     fe_apertura_definitivaEd = st.date_input("Fecha apertura definitiva", 
#                             value            = datetime.strptime(editableRow["fe_apertura_definitiva"],  '%Y-%m-%dT%H:%M:%S'),  
#                             min_value        = None, 
#                             max_value        = None, 
#                             key              = None, #"fe_apertura_definitiva", 
#                             help             = None, 
#                             on_change        = None, 
#                             args             = None, 
#                             kwargs           = None,
#                             format           =  "DD-MM-YYYY",
#                             disabled         = False, 
#                             label_visibility = "visible"
#                             )
#                     gestorEd = st.selectbox("Gestor apertura", 
#                             dropdownGestores,  # Se trata del gestor que abre el expediente
#                             index         = dropdownGestores.index(editableRow["gestor"]), 
#                             # placeholder ="Selecciona una opción", 
#                             key           = None, #"gestor"
#                             )
#                     fe_informeEd = st.date_input("Fecha informe", 
#                             value            = datetime.strptime(editableRow["fe_informe"],  '%Y-%m-%dT%H:%M:%S'), 
#                             min_value        = None, 
#                             max_value        = None, 
#                             key              = None, #"fe_apertura_definitiva", 
#                             help             = None, 
#                             on_change        = None, 
#                             args             = None, 
#                             kwargs           = None,
#                             format           =  "DD-MM-YYYY",
#                             disabled         = False, 
#                             label_visibility = "visible"
#                             )
#                     gestor_expedienteEd = st.selectbox("Gestor informe", dropdownGestores,  # Se trata del gestor que administra el expediente
#                             index         = dropdownGestores.index(editableRow["gestor_expediente"]), 
#                             # placeholder ="Selecciona una opción", 
#                             key           = None, #"gestor_expediente"
#                             )
#                     motivoEd = st.selectbox("Motivo", 
#                             dropdownMotivo, 
#                             index        = dropdownMotivo.index(editableRow["motivo"]), 
#                             # placeholder ="Selecciona una opción", 
#                             key          = None, #"motivo"
#                             )
#                     facturacionEd = st.number_input("Facturación",
#                             min_value =None,
#                             max_value =None,
#                             value     = editableRow["facturacion"],
#                             step      = 0.1                         
#                             )                                       

#                 with col2:
#                     plazoEd = st.number_input("plazo",
#                             min_value = None,
#                             max_value = None,
#                             value     = None,
#                             format= "%f"                         
#                             )
                    
#                     tipoEd = st.text_input("Tipo", # Tiene que ser en mayusculas
#                             value            = editableRow["tipo"], 
#                             max_chars        =  None, 
#                             key              = None, #"Expediente", 
#                             type             = "default", 
#                             help             = None, 
#                             autocomplete     = None, 
#                             on_change        = None, 
#                             args             = None, 
#                             kwargs           = None,
#                             placeholder      = None,
#                             disabled         = False, 
#                             label_visibility = "visible"
#                             )
#                     tipo_informadoEd = st.selectbox("Tipo Informado", 
#                             dropdownTipoInf, 
#                             index        = dropdownTipoInf.index(editableRow["tipo_informado"]), 
#                             # placeholder ="Selecciona una opción", 
#                             key          = None, 
#                             ) 
#                     utdEd = st.selectbox("UTD", 
#                             dropdownUTD, 
#                             index        = dropdownUTD.index(editableRow["UTD"]), #editableRow["UTD"], 
#                             # placeholder ="Selecciona una opción", 
#                             key          = None, #"UTD"
#                             )
#                     diasSubsanacionEd = st.number_input("Días de subsanación",
#                             min_value = None,
#                             max_value = None,
#                             value     = None,
#                             format= "%f"                         
#                             )
#                 with col3:
#                     gestor_cierreEd = st.selectbox("Gestor de cierre", dropdownGestores,  # Se trata del gestor que administra el expediente
#                             index         = dropdownGestores.index(editableRow["gestor_cierre"]), 
#                             # placeholder ="Selecciona una opción", 
#                             key           = None,
#                             )
#                     fecha_cierreEd = st.date_input("Fecha cierre", 
#                             value            = None, # "today", 
#                             min_value        = None, 
#                             max_value        = None, 
#                             key              = None,#"fecha_cierre", 
#                             help             = None, 
#                             on_change        = None, 
#                             args             = None, 
#                             kwargs           = None,
#                             format           =  "DD-MM-YYYY",
#                             disabled         = False, 
#                             label_visibility = "visible"
#                             )
#                     fecha_cierre_tecnicoEd = st.date_input("Fecha cierre Técnico", 
#                             value            = None, # "today", 
#                             min_value        = None, 
#                             max_value        = None, 
#                             key              = None,#"fecha_cierre", 
#                             help             = None, 
#                             on_change        = None, 
#                             args             = None, 
#                             kwargs           = None,
#                             format           =  "DD-MM-YYYY",
#                             disabled         = False, 
#                             label_visibility = "visible"
#                             )
#                     with st.expander("Observaciones"):
#                         obs = st.text_area("Observaciones", placeholder= "Escriba aqui los comentarios..." #key= "obs"
#                                        )

#     elif tipo_seleccion == "multiple":
#         edit   = st.button("Editar", disabled=True  , help= "Por favor, para editar seleccione solo una fila")
#         delete = st.button("Eliminar", disabled=False) 

# else:
#     edit   = st.button("Editar", disabled=True  , help= "Por favor, seleccione al menos una fila")
#     delete = st.button("Eliminar", disabled=True, help= "Por favor, seleccione al menos una fila")
