#-- Funciones para busquedas --#
import re
import Constants as cs
import numpy as py
import pandas as pd
from natsort import index_natsorted
import numpy as np
from datetime import datetime, timedelta

class Functions():

    def readCsv(self):
        """Lee el archivo .csv dentro de la carpeta.  
            -return:s
                -archive: Devuelve el dataframe del archivo leido con el Pandas."""

        archive = pd.read_csv(cs.ARCHIVE, na_values=cs.NULLVALUES) #Abrimos el archivo y los \N lo transformo a NaN.
        archive = archive.fillna("NaN") #Se transforman las celdas vacias a NaN.
        
        # Cambio de la columna de fecha de inicio y fin acorde a un formato dia/mes/año Hora:Minutos.
        archive[cs.DF_FIN] = pd.to_datetime(archive[cs.DF_FIN], format = '%d/%m/%Y %H:%M')
        archive[cs.DF_INICIO] = pd.to_datetime(archive[cs.DF_INICIO], format = '%d/%m/%Y %H:%M')
        return archive
        
    def verify_userID(self, user_id, df):
        """Verifica el user ID y busca las sesiones en un DataFrame.
            - args:
                - user_id: ID del usuario a buscar en el DataFrame.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la lista encontrada, sino id invalido."""
        
        # Verifico si el USERID ingresado es correcto.
        result = self.__regexValidation(regex = cs.REGEX_ID, value = user_id)

        if result:
            if result.group() in df.values:
                df = df.loc[df[cs.DF_USUARIO] == result.group()] #result.group, devuelve el matcheo.
                return True, df
            else:
                return False, f"\033[1;31m{cs.NAME_NOT_FOUND} {user_id}\033[0;0m"
        else:
            return False, f"\033[1;33m{cs.INVALID_ID_FORMAT} {user_id}\033[0;0m"

    def show_user(self, user_id, df):
        """Verifica el user ID y busca las sesiones en un DataFrame.
            - args:
                - user_id: ID del usuario a buscar en el DataFrame.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la lista encontrada, sino id invalido."""
        
        # Obtenemos la lista con el usuario.
        get_user = self.verify_userID(user_id = user_id, df = df)

        # Si no encuentra el usuario, retorna error en el id.
        if(get_user[0] == False):
            return get_user
        else:
            df = get_user[1]

        # Quito las columnas de tráfico.
        df.pop(cs.DF_OUTPUT_OCTECTS)
        df.pop(cs.DF_INPUT_OCTECTS)

        return True, df.reset_index(drop = True)


    def user_session_by_date(self, user_id, date_min, df, date_max = None):
        """Verifica el user ID y busca las sesiones en un DataFrame.
            - args:
                - user_id: ID del usuario a buscar en el DataFrame.
                - date_min: Fecha mínima a buscar.
                - date_max: Fecha máxima a buscar.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la lista encontrada, sino id invalido."""
        
        # Traer lista de usuario.
        new_df = self.verify_userID(user_id = user_id, df = df)

        # Si no encuentra el usuario, retorna error en el id.
        if(new_df[0] == False):
            return new_df
        else:
            df = new_df[1]

        # Quito las columnas de tráfico.
        df.pop(cs.DF_OUTPUT_OCTECTS)
        df.pop(cs.DF_INPUT_OCTECTS)

        # Booleano para saber si la fecha maxima existe o no.
        date_max_null = (date_max == None)

        if (date_max_null):
            r_date = self.__transformDate(date_min = date_min)
        else:
            r_date = self.__transformDate(date_min = date_min,  date_max = date_max)

        if(r_date == True):
            # Si el dato maximo es nulo, generamos una fecha en el mismo dia
            if (date_max_null):
                # Agregamos horas a las fechas y generamos una fecha, a un día despues de la fecha inicial.
                date_max = date_min + " " + cs.ADD_FINAL_HOUR
                date_min += " " + cs.ADD_INITIAL_HOUR
                
            else:
                # Agregamos horas a las fechas.
                date_min += " " + cs.ADD_INITIAL_HOUR
                date_max += " " + cs.ADD_FINAL_HOUR

            # Devuelve la lista del usuario  entre fechas
            df = df.loc[(df[cs.DF_INICIO] >= date_min) & (df[cs.DF_FIN] <= date_max)]
            return True, df.reset_index(drop = True)
        else:
            return False, f"\033[1;33m{cs.INVALID_DATE_FORMAT} {date_min} or {date_max}\033[0;0m"


    def user_sessionTime(self, user_id, df):
        """Verifica el user ID y muestra el tiempo total de sesiones en el DataFrame.
            - args:
                - user_id: ID del usuario a buscar en el DataFrame.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna el valor total de la session, sino id invalido."""
        
        # Traer lista de usuario.
        new_df = self.verify_userID(user_id = user_id, df = df)

        # Si no encuentra el usuario, retorna error en el id.
        if(new_df[0] == False):
            return new_df
        else:
            df = new_df[1]

        # Contado de cantidad de sesión.
        total = df[cs.DF_SESSION_TIME].sum()
        return True, timedelta(seconds = total)
                

    def verify_mac(self, mac, df):
        """Verifica cantidad de veces utilizado la MAC en el DataFrame.
            - args:
                - mac: MAC a buscar en el DataFrame.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la tabla de la MAC agrupada, sino MAC invalido."""

        # Verifico si la MAC ingresada es correcta.
        result = self.__regexValidation(regex = cs.REGEX_MAC, value = mac)

        if result:
            # Nos traemos la tabla con la MAC.
            df = df.loc[df[cs.DF_MAC] == result.group()]
            df = df.loc[:,[cs.DF_MAC, cs.DF_USUARIO]] # Recortamos las columnas solo a MAC y USUARIO.

            if result.group() in df.values:
                # reset_index: Pandas lo que hace es cambiar el nombre de la columna de la sumas de repetidos con el nombre indicado en REPEAT_CONNECTIONS
                df = df.groupby([cs.DF_MAC, cs.DF_USUARIO]).size().reset_index(name = cs.REPEAT_CONNECTIONS) #result.group, devuelve el matcheo.
                return True, df.reset_index(drop = True)
                
            else:
                return False, f"\033[1;31m{cs.MAC_NOT_FOUND} {mac}\033[0;0m"
        else:
            return False, f"\033[1;33m{cs.INVALID_MAC_FORMAT} {mac}\033[0;0m"


    def users_macs(self, user_id, df):
        """Verifica la cantidad de MACs que utiliza un usuario en el DataFrame.
            - args:
                - user_id: ID del usuario a buscar en el DataFrame.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la tabla de la MAC agrupada, sino MAC invalido."""

        # Traer lista de usuario.
        new_df = self.verify_userID(user_id = user_id, df = df)

        # Si no encuentra el usuario, retorna error en el id.
        if(new_df[0] == False):
            return new_df
        else:
            df = new_df[1]

        # Traemos las MAC del Usuario ingresado
        df = df.groupby(by = [cs.DF_MAC]).size().reset_index(name = cs.REPEAT_CONNECTIONS)
        return True, df
        #return True, new_df.iloc[:, :-1] # Elimino la ultima lista de la tabla.


    def verify_mac_ap(self, mac_ap, date_min, df, date_max = None):
        """Vericamos usuarios conectados a una MAC de un AP por rango de fechas.
            - args:
                - macAP: Dirección MAC del AP a buscar en el DataFrame.
                - date_min: Fecha mínima a buscar.
                - date_max: Fecha maxima a buscar. No es necesario colocarlo.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la tabla de la MAC del AP agrupada, sino MAC de AP invalido."""  
             
        # Verifico si la MAC AP ingresada es correcta.
        result = self.__regexValidation(regex = cs.REGEX_MACAP, value = mac_ap)

        # Booleano para saber si la fecha maxima existe o no.
        date_max_null = (date_max == None)

        if(date_max_null):
            r_date = self.__transformDate(date_min = date_min)
        else:
            r_date = self.__transformDate(date_min = date_min,  date_max = date_max)

        if (r_date == False and not date_max_null):
            return False, f"\033[1;33m{cs.INVALID_DATE_FORMAT} {date_min} y {date_max}\033[0;0m"
        elif (r_date == False and date_max_null):
            return False, f"\033[1;33m{cs.INVALID_DATE_FORMAT} {date_min}\033[0;0m"

        if (result and r_date):

            if result.group() in df.values:
                
                # Nos traemos la tabla con el MAC del AP.
                df = df.loc[df[cs.DF_MAC_AP] == result.group()]
                # Recortamos las columnas solo a MAC, USUARIO, FECHA MINIMA y FECHA MAXIMA.
                df = df.loc[:,[cs.DF_MAC, cs.DF_USUARIO, cs.DF_INICIO, cs.DF_FIN]]

                # Si el dato maximo es nulo, generamos una fecha en el mismo dia
                if (date_max_null):
                    # Agregamos horas a las fechas y generamos una fecha, a un día despues de la fecha inicial.
                    date_max = date_min + " " + cs.ADD_FINAL_HOUR
                    date_min += " " + cs.ADD_INITIAL_HOUR
                    
                else:
                    # Agregamos horas a las fechas.
                    date_min += " " + cs.ADD_INITIAL_HOUR
                    date_max += " " + cs.ADD_FINAL_HOUR

                # Buscamos mediante fecha de inicio y final
                df = df.loc[(df[cs.DF_INICIO] >= date_min) & (df[cs.DF_FIN] <= date_max)]

                # Traemos las MAC del AP ingresado
                df = df.groupby([cs.DF_MAC, cs.DF_USUARIO, cs.DF_INICIO, cs.DF_FIN]).size().reset_index(name = cs.REPEAT_CONNECTIONS)
                return True, df
                #return True, df.iloc[:, :-1] # Elimino la ultima lista de la tabla.
            else:
                return False, f"\033[1;31m{cs.MAC_AP_NOT_FOUND} {mac_ap}\033[0;0m"
        else:
            return False, f"\033[1;33m{cs.INVALID_MAC_AP_FORMAT} {mac_ap}\033[0;0m"


    def verify_traffic(self, user_id, df):
        """Verificamos el trafico de subida y bajada de un usuario, expresado en Mb.
            - args:
                - user_id: ID del usuario a buscar en el DataFrame.
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna una lista, como primer valor un booleano si devuelve tabla o no y como segundo valor, la tabla o un mensaje de error."""
        
        # Traer lista de usuario.
        new_df = self.verify_userID(user_id = user_id, df = df)

        # Si no encuentra el usuario, retorna error en el id.
        if(new_df[0] == False):
            return new_df
        else:
            df = new_df[1]

        # Contado de cantidad de bajada.
        download = df[cs.DF_INPUT_OCTECTS].sum()
        # Contado de cantidad de subida.
        upload = df[cs.DF_OUTPUT_OCTECTS].sum()

        download = self.__bytesTransform(bytes = download)
        upload = self.__bytesTransform(bytes = upload)

        return True, f"{cs.USER} '{user_id}' {cs.HAS}\n{cs.UPLOAD} {upload}\n{cs.DOWNLOAD} {download}"


    def verify_ap_traffic(self, df):
        """Mostramos los AP ordenados por trafico total.
            - args:
                - df: DataFrame obtenido con el Pandas.
            - return: Retorna la lista de los APs."""
        
        # Recortamos a columnas en AP, Bajada y Subida
        df = df.loc[:,[cs.DF_MAC_AP, cs.DF_INPUT_OCTECTS, cs.DF_OUTPUT_OCTECTS]] # ":,[Algo]" Es para traer valores de columnas.

        # Realizamos la suma de la columna de subida y bajada
        # agg: Es nuevo de pandas, sirve para trabajar agrupando columnas de manera diferente.
        # reset_index(): Te elimina la ultima columna de conteo de groupby, y ademas te agrega un index en la primera columna [0,1,2...]
        df = df.groupby([cs.DF_MAC_AP]).agg(
            Suma_Subida = (cs.DF_INPUT_OCTECTS,'sum'),
            Suma_Bajada = (cs.DF_OUTPUT_OCTECTS,'sum'),
            ).reset_index()

        # Elimina la ultima fila que queda en vacio, y pone NaN.
        # El iloc trabaja con columnas en formato de entero, es decir del 0 al x valor de las columnas.
        df = df.iloc[:-1, :]

        # Realizamos una suma total por fila.
        # Transformamos a lista de python. 
        col_list = list(df) # [Mac_AP, suma_subida, suma_bajada]
        # Quitamos la columna MAC AP. 
        col_list.remove(cs.DF_MAC_AP) # [suma_subida, suma_bajada]
        #Realizamos la suma de las filas en las columnas [suma_subida, suma_bajada] y lo agregamos en tráfico total.
        df['Tráfico_Total']=df[col_list].sum(axis = 1) # axis=1 es igual a sumar las filas, axis=0 es la suma de las columnas

        #Ordenamos el Trafico Total de forma descendiente.
        df = df.sort_values(by='Tráfico_Total', key=lambda x: np.argsort(index_natsorted(df['Tráfico_Total'], reverse=True)))

        # Transformamos todos los valores a bytes, megabytes y gigabytes.
        df['Suma_Subida'] = df['Suma_Subida'].apply(lambda x: self.__bytesTransform(x))
        df['Suma_Bajada'] = df['Suma_Bajada'].apply(lambda x: self.__bytesTransform(x))
        df['Tráfico_Total'] = df['Tráfico_Total'].apply(lambda x: self.__bytesTransform(x))

        return df.reset_index(drop = True)


    #-- Utilities --#
    def __regexValidation(self, regex, value):
        """Validamos si el valor ingresado es correcto segun la regex.
            - args:
                - regex: Dirección MAC del AP a buscar en el DataFrame.
                - value: Fecha mínima a buscar.
            - return: Retorna el objeto matcheado o None en caso de no matchear."""

        range = re.compile(regex) #Compilamos la expresión regular.
        value.rstrip()
        return range.fullmatch(value) #Verificamos ingresado por usuario.

    # Metodo para hacer publico la validacion del regex (punto 6)
    def get_regex_validation(self, regex, value):
        return self.__regexValidation(regex, value)

    def __transformDate(self, date_min, date_max = None):
        """Transformar y verificar si la fechas ingresada es correcta.
            - args:
                - date_min: Fecha minima a comparar en el DataFrame.
                - date_max: Fecha maxima a comparar en el DataFrame, si es None solo busca en una sola fecha.
            - return: Retorna, None, en caso de que las fechas ingresadas es incorrecta.
            o retorna Verdadero o Falso si el RE compila correctamente.""" 

        # Compilamos expresiones regulares.
        date_range = re.compile(cs.REGEX_DATE)
        #time_range = re.compile(cs.REGEX_HOUR)

        # Verificamos si lo ingresado por el usuario es correcto.
        r_date_min = date_range.fullmatch(date_min)

        # Verificamos si el usuario ingreso un tiempo maximo, y si lo ingresado es correcto.
        if(date_max != None):
            r_date_max = date_range.fullmatch(date_max)
        else:
            r_date_max = True
        
        if (r_date_min and r_date_max):
            return True # Devuelve verdadero en caso de que las fechas esten bien escritas.
        else:
            return False # Devuelve falso en caso de que el formato de fecha sea incorrecto.

    def __bytesTransform(self, bytes):
        """Transformar bytes a megabytes.
            - args:
                - bytes: Bytes a transformar a Megabites.
            - return: Retorna una lista con el primer valor un string, diciendo el tipo de dato.
            y como segundo valor un int con el valor en megabytes o gigabyte."""

        if (bytes >= 1048576): ## (1024 al cuadrado)
            megabytes = (bytes / 1048576) ## (1024 al cuadrado)
            if (megabytes >= 1024):
                gigabytes = (megabytes / 1024)
                return f"{int(gigabytes)} {cs.GIGABYTES}"
            else:
                return f"{int(megabytes)} {cs.MEGABYTES}"
        else:
            return f"{int(bytes)} {cs.BYTES}"
    #-- Utilities