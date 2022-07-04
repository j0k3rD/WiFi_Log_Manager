#------------------------------------------------------------------------------------#
#---------------------Proyecto Final para Autómatas y Gramática----------------------#
# ----------------------Authors: Marcos Miglierina, Aaron Moya-----------------------#
#------------------------------------------------------------------------------------#

import sys
import Constants as cs
from Functions import Functions
from tabulate import tabulate

class Main():

    # Iniciar el programa.
    def start(self):
        self.menu() # Abro el menu, y le mando el archivo abierto del csv

    def menu(self):
        """ Muestreo del menu
            - args:
                - df: DataFrame del archivo .csv cargado. 
                - func: Objeto de funciones"""

        # Instancio las funciones y leo el archivo csv.
        func = Functions()
        df = func.readCsv()

        while True:

            print(f'\033[1;36m{cs.LOGO}\033[0;0m')
            print(f'\033[3;36m{cs.MENU}\033[0;0m') #Mostrar el menu.

            opc = input(cs.ANSWER) #Mostrar opciones.

            # Solucionar error que el usuario ingrese un string o vacio al realizar una consulta.
            if(not opc.isdigit()):
                print(cs.INV_OP2)
                continue
            else:
                opc = int(opc)

            #Listar todas las sesiones del usuario por ID.
            if opc == 1:  

                print(cs.SPACE)
                
                id = input(cs.QUESTION_ID)

                print(cs.SPACE)

                user = func.show_user(user_id = id, df = df)

                if (user[0] == True):
                    print(tabulate(user[1], headers = "keys", tablefmt = "fancy_grid"))
                else:
                    print(user[1])

                print(cs.SPACE)
                input(cs.PRESS_TO_CONTINUE)

            #Listar todas las sesiones del usuario por rango de fecha.
            elif opc == 2:

                print(cs.SPACE)

                id = input(cs.QUESTION_ID)

                print(cs.SPACE)
                r_user_ID = func.get_regex_validation(regex = cs.REGEX_ID, value = id)

                if r_user_ID == None:
                    print(f"\033[1;31m{cs.INVALID_ID_FORMAT} {id}\033[0;0m")
                    print(cs.SPACE)
                    input(cs.PRESS_TO_CONTINUE)
                    continue

                op = input(cs.CHOOSE_DATE)
                print(cs.SPACE)

                if op == "1":
                    date = input(f"\033[3m{cs.DATE_FORMAT}\033[0;0m\n{cs.QUESTION_FECHA}")
                    print(cs.SPACE)
                    user = func.user_session_by_date(user_id = id, date_min = date, df = df)

                elif op == "2":
                    date_min = input(f"\033[3m{cs.DATE_FORMAT}\033[0;0m\n{cs.QUESTION_FECHA_MIN}")
                    print(cs.SPACE)
                    date_max = input(f"\033[3m{cs.DATE_FORMAT}\033[0;0m\n{cs.QUESTION_FECHA_MAX}")
                    print(cs.SPACE)
                    user = func.user_session_by_date(user_id = id, date_min = date_min, date_max = date_max, df = df)

                else:
                    print(cs.INV_OP)
                    continue

                if (user[0] == True):
                    print(tabulate(user[1], headers = "keys", tablefmt = "fancy_grid"))
                else:
                    print(user[1])

                print(cs.SPACE)
                input(cs.PRESS_TO_CONTINUE)

            #Listar el tiempo total de la sesion de un usuario. (hora:minuto:segundo)
            elif opc == 3:

                print(cs.SPACE)

                id = input(cs.QUESTION_ID)

                time = func.user_sessionTime(user_id = id, df = df)

                print(cs.SPACE)

                if (time[0] == True):
                    print(f"\n'{id}' {cs.TOTAL_SESSION_TIME} {time[1]}\n")
                else:
                    print(time[1])

                print(cs.SPACE)
                input(cs.PRESS_TO_CONTINUE)

            #Listar la MAC de un usuario si se conecto con un dispositivo o varios.
            elif opc == 4:

                print(cs.SPACE)

                mac = input(f"\033[3m{cs.MAC_FORMAT}\033[0;0m\n{cs.QUESTION_MAC_CLIENT}")

                print(cs.SPACE)

                table = func.verify_mac(mac = mac, df = df)

                if (table[0] == True):
                    print(tabulate(table[1], headers = "keys", tablefmt = "fancy_grid"))
                else:
                    print(table[1])

                print(cs.SPACE)
                
                input(cs.PRESS_TO_CONTINUE)

            #Listar las dierentes MAC de un usuario.
            elif opc == 5:

                print(cs.SPACE)

                id = input(cs.QUESTION_ID)

                print(cs.SPACE)
                
                user = func.users_macs(user_id = id, df = df)

                if (user[0] == True):
                    print(tabulate(user[1], headers = "keys", tablefmt = "fancy_grid"))
                    #print(user[1].to_string())
                else:
                    print(user[1])

                print(cs.SPACE)

                input(cs.PRESS_TO_CONTINUE)

            #Listar los usuarios conectados a un AP por MAC del AP en una determinada fecha o rango.
            elif opc == 6:

                print(cs.SPACE)

                mac = input(f"\033[3m{cs.MAC_AP_FORMAT}\033[0;0m\n{cs.QUESTION_MAC_AP}")
                print(cs.SPACE)
                r_mac_ap = func.get_regex_validation(regex = cs.REGEX_MACAP, value = mac)

                if r_mac_ap == None:
                    print(f"\033[1;31m{cs.INVALID_MAC_AP_FORMAT} {mac}\033[0;0m")
                    print(cs.SPACE)
                    input(cs.PRESS_TO_CONTINUE)
                    continue
                
                op = input(cs.CHOOSE_DATE)
                print(cs.SPACE)

                if op == "1":
                    date = input(f"\033[3m{cs.DATE_FORMAT}\033[0;0m\n{cs.QUESTION_FECHA}")
                    print(cs.SPACE)
                    table = func.verify_mac_ap(mac_ap = mac, date_min = date , df = df)

                elif op == "2":
                    date_min = input(f"\033[3m{cs.DATE_FORMAT}\033[0;0m\n{cs.QUESTION_FECHA_MIN}")
                    print(cs.SPACE)
                    date_max = input(f"\033[3m{cs.DATE_FORMAT}\033[0;0m\n{cs.QUESTION_FECHA_MAX}")
                    print(cs.SPACE)
                    table = func.verify_mac_ap(mac_ap = mac, date_min = date_min, date_max = date_max, df = df)

                else:
                    print(cs.INV_OP)
                    continue

                if (table[0] == True):
                    print(tabulate(table[1], headers = "keys", tablefmt = "fancy_grid"))
                else:
                    print(table[1])

                print(cs.SPACE)

                input(cs.PRESS_TO_CONTINUE)

            #Listar el tráfico de un usuario en MB diferenciando subida y bajada.
            elif opc == 7:

                print(cs.SPACE)

                user = input(f"{cs.QUESTION_ID}")
                user_ID = func.verify_traffic(user_id = user, df = df)

                print(cs.SPACE)

                print(user_ID[1])

                print(cs.SPACE)
                input(cs.PRESS_TO_CONTINUE)
                print(cs.SPACE)

            #Listar los AP ordenados por tráfico total.
            elif opc == 8:

                print(cs.SPACE)
                
                mac_ap = func.verify_ap_traffic(df = df)

                print(tabulate(mac_ap, headers = "keys", tablefmt = "fancy_grid"))

                print(cs.SPACE)
                input(cs.PRESS_TO_CONTINUE)
                print(cs.SPACE)

            #Salir del menu
            elif opc == 9:
                while True:
                    print(cs.WANT_QUIT)
                    op = int(input(cs.ANSWER))

                    if op == 1:
                        print(cs.EXITING)
                        sys.exit(0)
                    elif op == 2:
                        print(cs.RETURNING)
                        break
                    else:
                        print(cs.INV_OP)
            else:
                print(cs.INV_OP2)

if __name__ == "__main__":
    main = Main()
    main.start()
