Esta carpeta V2 es el siguiente paso del desarrollo del proyecto de redes, en los que se estructurará el código siguiendo la misma nomenclatura
y formato, además de añadir herramientas como el estado de sesión y la prueba de uso de apps multipagina. 

### Para centrar Botones con CSS o HTML

``` python
# Crear el botón y aplicar estilo CSS para centrarlo
st.write("<div class='centered-button'>"
         "<button>User Login</button>"
         "</div>",
         unsafe_allow_html=True)

# Aplicar estilos CSS para centrar el botón
st.markdown(
    """
    <style>
    .centered-button {
        display: flex;
        justify-content: center;
    }
    </style>
    """
    , unsafe_allow_html= True
)
```

### Para probar cambiar el formato de la fecha en los forms
```python
fechaApertura = pd.to_datetime(st.date_input("Fecha apertura", 
            value            = None, 
            min_value        = None, 
            max_value        = None, 
            #key              = "fechaApertura", 
            help             = None, 
            on_change        = None, 
            args             = None, 
            kwargs           = None,
            format           =  "DD/MM/YYYY",
            disabled         = False, 
            label_visibility = "visible"
            ), format = "%d/%m/%Y").dt.strftime("%d/%m/%Y")
```

### Para eliminar la marca de agua de Streamlit:

```python
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
```

### Para convertir una imagen en texto: base64


```python
def getImgAsBase64(file):

    with open(file, "rb") as f:
        data = f.read()

    return base64.b64encode(data).decode()

image = getImgAsBase64("path")
# background position es opcional, ver que tamaño es el ideal
def bakgroundStyle(image):

    pageBgImg = f"""
    <style>
    [data-testid="stAppViewContainer"]{{
    background-image: url("data:image/png;base64,{image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
    }}
    [data-testid="stHeader"]{{
     background-color: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"]{{
    right: 2rem;
    }}
    </style>
    """    
```
## No se si se va a usar: 
```python
def agregarNuevaEntrada(expediente, utd, fechaApertura, gestor, obs):

    nuevaEntrada = pd.Series({
        "Expediente": expediente,
        "UTD": utd,
        "Fecha": fechaApertura,
        "Gestor": gestor,
        "Observaciones": obs
    }, index = ['Expediente', 'UTD', 'Fecha', 'Gestor', 'Observaciones']
    )

    df = df._append(nuevaEntrada, ignore_index = True)
```

## AG-GRID:

```python
gd = GridOptionsBuilder.from_dataframe(df1)

gd.configure_pagination(enabled                = True,
                        paginationAutoPageSize = False,
                        paginationPageSize     = 10 
                        )

gd.configure_default_column(resizable   = True, 
                                filterable  = True, 
                                sorteable   = True, 
                                editable    = False, 
                                groupable   = False)

gd.configure_auto_height(autoHeight= True)

# si quiero poner un checkbox para elegir entre eleccion unica o multiple:

tipo_seleccion = st.radio("Tipo de selecion:", options= ["unica", "multiple"])

gd.configure_selection(selection_mode             = tipo_seleccion, 
                        use_checkbox               = True 
                        #pre_selected_rows         = [], 
                        #rowMultiSelectWithClick   = False, 
                        #suppressRowDeselection    = False, 
                        #suppressRowClickSelection = False, 
                        #groupSelectsChildren      = True, 
                        #groupSelectsFiltered      = True
                        )

gridoptions = gd.build()
grid_table  = AgGrid(df1, 
                        gridOptions            = gridoptions, 
                        columns_auto_size_mode = ColumnsAutoSizeMode.FIT_CONTENTS,
                        update_mode            = GridUpdateMode.VALUE_CHANGED, #SELECTION_CHANGED, 
                        theme                  = "material")

```


       if "Expediente" not in st.session_state:
            st.session_state.Expediente = ''
        if "UTD" not in st.session_state:
            st.session_state.UTD = dropdownUTD[0]
        if "motivo" not in st.session_state:
            st.session_state.motivo = dropdownMotivo[0]
        if "fe_apertura_definitiva" not in st.session_state:
            st.session_state.fe_apertura_definitiva = "today"
        if "gestor" not in st.session_state:
            st.session_state.gestor = dropdownGestores[0]
        if "gestor_expediente" not in st.session_state:
            st.session_state.gestor_expediente = dropdownGestores[0]
        if "fecha_cierre" not in st.session_state:
            st.session_state.fecha_cierre = "today"

        def reset_widgets():
            st.session_state["Expediente"] = ''
            st.session_state["UTD"] = dropdownUTD[0]  # Asume que el primer valor es el valor predeterminado.
            st.session_state["motivo"] = dropdownMotivo[0]
            st.session_state["gestor"] = dropdownGestores[0]
            st.session_state["gestor_expediente"] = dropdownGestores[0]
            st.session_state["fe_apertura_definitiva"] = "today"
            st.session_state["fecha_cierre"] = None

reset_widgets():


# Comandos básicos:

```powershell
python -m venv .venv # crear entorno

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # por si no me deja ejecutar scripts

.\.venv\Scripts\activate # activar el entorno

pip install -r requirements.txt # instalar los requerimientos
```