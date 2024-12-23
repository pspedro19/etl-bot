import pandas as pd
from datetime import datetime
import re

def split_date(date_str):
    """
    Procesa la fecha con manejo de errores y diferentes formatos
    """
    try:
        # Eliminar comillas si existen
        date_str = date_str.strip('"')
        
        # Extraer el mes de reporte si existe
        report_month = None
        match = re.search(r'\((.*?)\)', date_str)
        if match:
            report_month = match.group(1)
            # Remover la parte del mes de reporte
            main_date = re.sub(r'\s*\(.*?\)', '', date_str).strip()
        else:
            main_date = date_str.strip()
        
        # Intentar diferentes formatos de fecha
        date_formats = [
            '%b %d, %Y',     # Dec 06, 2024
            '%Y-%m-%d',      # 2024-12-06
            '%d/%m/%Y',      # 06/12/2024
            '%B %d, %Y'      # December 06, 2024
        ]
        
        for date_format in date_formats:
            try:
                date_obj = datetime.strptime(main_date, date_format)
                formatted_date = date_obj.strftime('%d/%m/%Y')
                return formatted_date, report_month if report_month else ""
            except ValueError:
                continue
                
        # Si no se pudo procesar con ningún formato, devolver los datos originales
        print(f"Warning: No se pudo procesar la fecha: {date_str}")
        return date_str, ""
        
    except Exception as e:
        print(f"Error procesando la fecha '{date_str}': {str(e)}")
        return date_str, ""

def clean_percentage(value):
    """
    Limpia valores de porcentaje y maneja casos especiales
    """
    try:
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        # Eliminar el símbolo de porcentaje y espacios
        return float(str(value).replace('%', '').strip())
    except Exception as e:
        print(f"Error limpiando porcentaje '{value}': {str(e)}")
        return None

def process_colombia_cpi(input_file='output/interest-rate-decision-168.csv', output_file='clean_data/processed_interest-rate-decision-168.csv'):
    """
    Procesa el archivo de CPI de Colombia
    """
    try:
        # Leer el archivo CSV con manejo de diferentes codificaciones
        try:
            df = pd.read_csv(input_file)
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='latin1')
            
        # Mostrar las primeras filas antes del procesamiento
        print("\nPrimeras filas del archivo original:")
        print(df.head())
        
        # Procesar la columna Release Date
        print("\nProcesando fechas...")
        date_info = df['Release Date'].apply(split_date)
        df['Release Date'] = date_info.apply(lambda x: x[0])
        df['Report Month'] = date_info.apply(lambda x: x[1])

        # Procesar columnas de porcentajes
        print("\nProcesando porcentajes...")
        percentage_cols = ['Actual', 'Forecast', 'Previous']
        for col in percentage_cols:
            if col in df.columns:
                new_col = f'{col}%'
                df[new_col] = df[col].apply(clean_percentage)
                df.drop(columns=[col], inplace=True)

        # Reordenar las columnas
        columns = ['Release Date', 'Report Month', 'Time']
        columns.extend([col for col in df.columns if col.endswith('%')])
        df = df[columns]

        # Guardar el archivo procesado
        df.to_csv(output_file, index=False)
        print(f"\nArchivo procesado exitosamente: {output_file}")
        
        # Mostrar las primeras filas del resultado
        print("\nPrimeras filas del archivo procesado:")
        print(df.head())
        
        # Mostrar información sobre valores nulos o problemas
        print("\nInformación sobre valores nulos:")
        print(df.isnull().sum())
        
    except Exception as e:
        print(f"Error procesando el archivo: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    process_colombia_cpi()