import pandas as pd
import numpy as np
import string


class HyAIA:
    def __init__(self, df):
        self.data = df
        self.columns = df.columns
        self.data_binarios, self.binarios_columns = self.get_binarios()
        self.data_cuantitativos, self.cuantitativos_columns = self.get_cuantitativos()
        self.data_categoricos, self.categoricos_columns = self.get_categoricos()

    # % Métodos para Análisis de Datos
    # Método para obtener las columnas y dataframe binarios
    def get_binarios(self):
        col_bin = []
        for col in self.data.columns:
            if self.data[col].nunique() == 2:
                col_bin.append(col)
        return self.data[col_bin], col_bin

    # Método para obtener columnas y dataframe cuantitativos
    def get_cuantitativos(self):
        col_cuantitativas = self.data.select_dtypes(include='number').columns
        return self.data[col_cuantitativas], col_cuantitativas

    # Método para obtener columnas y dataframe categóricos
    def get_categoricos(self):
        col_categories = self.data.select_dtypes(exclude='number').columns
        col_cat = []
        for col in col_categories:
            if self.data[col].nunique() > 2:
                col_cat.append(col)
        return self.data[col_cat], col_cat

    # Remueve los puntos dentro de una cadena
    @staticmethod
    def remove_punctuation(x):
        try:
            x = ''.join(ch for ch in x if ch not in string.punctuation)
        except:
            print(f'{x} no es una cadena de caracteres')
            pass
        return x

    @staticmethod
    def remove_digits(x):
        try:
            x = ''.join(ch for ch in x if ch not in string.digits)
        except:
            print(f'{x} no es una cadena de caracteres')
            pass
        return x

    # remover espacios en blanco
    @staticmethod
    def remove_whitespace(x):
        try:
            x = ' '.join(x.split())
        except:
            pass
        return x

    # convertir a minisculas
    @staticmethod
    def lower_text(x):
        try:
            x = x.lower()
        except:
            pass
        return x

    # convertir a mayusculas
    @staticmethod
    def upper_text(x):
        try:
            x = x.upper()
        except:
            pass
        return x

    # Función que convierta a mayúsculas la primera letra
    @staticmethod
    def capitalize_text(x):
        try:
            x = x.capitalize()
        except:
            pass
        return x

    # reemplazar texto
    @staticmethod
    def replace_text(x, to_replace, replacement):
        try:
            x = x.replace(to_replace, replacement)
        except:
            pass
        return x

    def dqr(self):

        # % Lista de variables de la base de datos
        columns_names = pd.DataFrame(list(self.data.columns.values), columns=['Columns_Names'],
                                     index=list(self.data.columns.values))

        # Lista de tipos de datos del dataframe
        data_dtypes = pd.DataFrame(self.data.dtypes, columns=['Dtypes'])

        # Lista de valores presentes
        present_values = pd.DataFrame(
            self.data.count(), columns=['Present_values'])

        # Lista de valores missing (Valores faltantes/nulos nan)
        missing_values = pd.DataFrame(
            self.data.isnull().sum(), columns=['Missing_values'])

        # Valores unicos de las columnas
        unique_values = pd.DataFrame(columns=['Unique_values'])
        for col in list(self.data.columns.values):
            unique_values.loc[col] = [self.data[col].nunique()]

        # Información estadística
        # Saber si la columna es categorica
        is_categorical = pd.DataFrame(columns=['Is_categorical'])
        for col in list(self.data.columns.values):
            if col in self.categoricos_columns:
                is_categorical.loc[col] = [True]
            else:
                is_categorical.loc[col] = [False]

        # Listado de categorias
        categories_values = pd.DataFrame(columns=['Categories'])
        for col in list(self.data.columns.values):
            if col in self.categoricos_columns:
                unique_cats = self.data[col].dropna().unique()
                if len(unique_cats) <= 10:
                    # se muestran las categorias si son menos de 10
                    categories_list = ', '.join(
                        [str(cat) for cat in unique_cats])
                    categories_values.loc[col] = [categories_list]
                else:
                    # Si  son mas de 10 se muestran 5 y puntos
                    first_5 = ', '.join([str(cat) for cat in unique_cats[:5]])
                    categories_values.loc[col] = [
                        f"{first_5} ... (+{len(unique_cats)-5} más)"]
            else:
                # no categoricas N/A
                categories_values.loc[col] = ['N/A']

        max_values = pd.DataFrame(columns=['Max_values'])
        for col in list(self.data.columns.values):
            if not is_categorical.loc[col, 'Is_categorical']:  # Solo para numéricas
                try:
                    max_values.loc[col] = [self.data[col].max()]
                except:
                    max_values.loc[col] = ['N/A']
            else:
                max_values.loc[col] = ['N/A']  # Para categóricas

        # Lista de valores mínimos
        min_values = pd.DataFrame(columns=['Min_values'])
        for col in list(self.data.columns.values):
            if not is_categorical.loc[col, 'Is_categorical']:  # Solo para numéricas
                try:
                    min_values.loc[col] = [self.data[col].min()]
                except:
                    min_values.loc[col] = ['N/A']
            else:
                min_values.loc[col] = ['N/A']  # Para categóricas

        # Lista de valores con su desviación estándar
        std_values = pd.DataFrame(columns=['Std_deviation'])
        for col in list(self.data.columns.values):
            if not is_categorical.loc[col, 'Is_categorical']:  # Solo para numéricas
                try:
                    std_val = self.data[col].std()
                    std_values.loc[col] = [round(std_val, 2)]
                except:
                    std_values.loc[col] = ['N/A']
            else:
                std_values.loc[col] = ['N/A']  # Para categóricas

        # Lista de valores con la media (NUEVO)
        mean_values = pd.DataFrame(columns=['Mean_values'])
        for col in list(self.data.columns.values):
            if not is_categorical.loc[col, 'Is_categorical']:  # Solo para numéricas
                try:
                    mean_val = self.data[col].mean()
                    mean_values.loc[col] = [round(mean_val, 2)]
                except:
                    mean_values.loc[col] = ['N/A']
            else:
                mean_values.loc[col] = ['N/A']  # Para categóricas

        return columns_names.join(data_dtypes).join(present_values).join(missing_values).join(unique_values).join(is_categorical).join(max_values).join(min_values).join(mean_values).join(std_values).join(categories_values)
