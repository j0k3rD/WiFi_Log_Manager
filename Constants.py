#-- Constants de archivo --#

ARCHIVE = "Usuarios WiFi.csv" #Nombre del archivo.
NULLVALUES = "\\N" #Doble \\ porque python se autodetona!

#-- Constants de Main Menu --#

LOGO = """
                --------------------------------------
                        🔧 WiFi Log Manager 🔧
                --------------------------------------
        """

MENU =  """
                Select an Option:

                1. User Session List.
                2. User Session List by Date.
                3. Total User Session Time.
                4. User MAC.
                5. All User MACs.
                6. User conected by AP.
                7. User Traffic.
                8. List AP (Ordered by Total Traffic).
                9. Exit
        """

CHOOSE_DATE = """
                .To search by "Exact Date": Enter 1.
                .To search by "Date Range": Enter 2.


                Option: """

ANSWER = """Option: """

PRESS_TO_CONTINUE = "Press Enter key to Continue.."

WANT_QUIT = """
                    Are you sure you want to go out? 
                    1.Yes
                    2.No
                    """

EXITING = "Exiting.."

RETURNING = "Returning.."

INV_OP = "Invalid Option"

INV_OP2 = "Enter a Correct Option!, Try again.."

SPACE = "\n"

#-- Constants de Preguntas --#

QUESTION_ID = "Enter the UserID: "

QUESTION_FECHA = "Enter the date: "

QUESTION_FECHA_MIN = "Enter the Minimum date: "

QUESTION_FECHA_MAX = "Enter the Maximum date: "

QUESTION_MAC_CLIENT = "Enter the client MAC: "

QUESTION_MAC_AP = "Enter the MAC AP: "

#-- Constants de Busqueda --#

DF_USUARIO = "Usuario"

DF_ID_CONEXION = "ID Conexion"

DF_INICIO = "Inicio de Conexi¢n"

DF_FIN = "Fin de Conexio"

DF_SESSION_TIME = "Session Time"

DF_INPUT_OCTECTS = "Input Octects"

DF_OUTPUT_OCTECTS = "Output Octects"

DF_MAC_AP = "MAC AP"

DF_MAC = "MAC Cliente"

#-- Constants de REGEXs --#

"""RegexID: [a-z]*: debe contener al menos una minusculas y se puede repetir muchas veces.  
[.-]?[a-z]: puede contener al menos un punto pero este debe seguir con al menos una letra, no puede estar al final este punto y guión.  
{3,20}: debe contener entre 3 y 20 caracteres"""

REGEX_ID = ("""^[A-Za-z]*[.-]?[A-Za-z]{3,20}$""")

"""RegexDATE: 
*(PRIMERA PARTE: LOS DIAS) ([0-2][0-9]: el primer caracter puede ser 0,1,2 el segundo puede ir de 0-9  |(3)[0-1]): o si empieza por 3
solo le puede seguir 1 o 2.*
(\)Esto sirve para insertar simbolos.
(/|-): se puede separar por barra o guion  
*(SEGUNDA PARTE: LOS MESES)(((0)[0-9]):si empiza con 0 debe de seguirle un numero del 0-9   
|((1)[0-2])): o si empieza con 1 debe seguirle un 0,1,2   (/|-): se puede separar por barra o guion
\d{4}: acepta todos los numeros del (0-9) y pide que se repitan 4 veces o sea, si o si van 4 numeros juntos por ej: 2019. Si fuese: 201 o 20222
no lo tomaria como válido.
En este caso hasta el año 2025 ya que sino teniamos problemas con el PANDAS."""

REGEX_DATE = ("""^([1-9]|[0][1-9]|[1-2][0-9]|(3)[0-1])(\/|\-)(([1-9]|(0)[1-9])|((1)[0-2]))(\/|\-)(20([0-1][0-9]|[2][0-5]))$""")
#("""^([0-2][0-9]|(3)[0-1])(/|-)(((0)[0-9])|((1)[0-2]))(/|-)\d{4}$""")

# REGEX_HOUR = ("""^(((([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+$))""") #REGEX para hora para HH:MM:SS

# LLaves {X} le decis cuantas veces se pueden repetir esa condición. 
REGEX_MACAP = ("""^(04|DC)(-)(18|9F)(-)(DB|D6)(-)([0-9]{2}|C[0-9]{1})(-)([A-F0-9]{2})(-)([A-F0-9]{2})(:)(UM)$""")

# [0-9A-Fa-f]: Puede ir del 0-9 y ademas tener una letra de la A-F y de la a-f. {2} solo con dos letras
REGEX_MAC = ("""^([0-9A-Fa-f]{2}[-]){5}([0-9A-Fa-f]{2})$""")

#REGEX_HOUR = ("""^[0-5][0-9](:)[0-5][0-9]$""")

#-- Constants de Functions Returns --#

NAME_NOT_FOUND = "\nName not found in DataFrame:"

MAC_NOT_FOUND = "\nMAC not found in DataFrame:"

MAC_AP_NOT_FOUND = "\nMAC AP not found in DataFrame:"

INVALID_ID_FORMAT = "Invalid ID format:"

MAC_FORMAT = "MAC format: xx-xx-xx-xx-xx-xx"

INVALID_MAC_FORMAT = "Invalid MAC format:"

MAC_AP_FORMAT = "MAC AP format: xx-xx-xx-xx-xx-xx:UM"

INVALID_MAC_AP_FORMAT = "Invalid MAC AP format:"

DATE_FORMAT = "DATE format: [00/00/0000] or [00-00-0000]"

INVALID_DATE_FORMAT = "Invalid DATE format:"

TOTAL_SESSION_TIME = "Total Session Time:"

REPEAT_CONNECTIONS = "Inicio de sesiones"

USER = "User"

HAS = "has:"

UPLOAD = "Upload Amount:"

DOWNLOAD = "Download Amount:"

GIGABYTES = "gigabytes"

MEGABYTES = "megabytes"

BYTES = "bytes"

#-- Constantes uso en funciones --#

ADD_INITIAL_HOUR = "00:00"

ADD_FINAL_HOUR = "23:59"
