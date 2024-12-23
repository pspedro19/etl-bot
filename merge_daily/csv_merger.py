import os
import pandas as pd
import logging
from datetime import datetime
import re

# Configuración del logging
def setup_logging():
    """Configura el sistema de logging con formato timestamp y nivel de detalle."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(
        filename=f'logs\csv_merger_{timestamp}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Mapeo de columnas según especificaciones
COLUMN_MAPPING = {
    'Fecha': 'Date',
    'Date': 'Date',
    'Último': 'Close',
    'Ultimo': 'Close',
    'Price': 'Close',
    'Cierre': 'Close',
    'Apertura': 'Open',
    'Open': 'Open',
    'Máximo': 'High',
    'High': 'High',
    'Mínimo': 'Low',
    'Low': 'Low',
    'Vol.': 'Volume',
    '% var.': 'Change%',
    'Change %': 'Change%'
}

def find_csv_files(directory, pattern):
    """
    Encuentra archivos CSV que coincidan con el patrón especificado.
    
    Args:
        directory (str): Ruta del directorio a buscar
        pattern (str): Patrón base para buscar archivos
    
    Returns:
        list: Lista de rutas de archivos CSV encontrados
    """
    csv_files = []
    pattern_regex = re.compile(f"{re.escape(pattern)}(?:\s*\(\d+\))?.csv$")
    
    for file in os.listdir(directory):
        if pattern_regex.match(file):
            csv_files.append(os.path.join(directory, file))
            logging.info(f"Archivo encontrado: {file}")
    
    return csv_files

def read_and_standardize_csv(file_path):
    """
    Lee y estandariza un archivo CSV según el mapeo de columnas definido.
    
    Args:
        file_path (str): Ruta del archivo CSV a procesar
    
    Returns:
        pandas.DataFrame: DataFrame con columnas estandarizadas
    """
    try:
        # Leer CSV con manejo de fechas
        df = pd.read_csv(file_path, parse_dates=['Date'])
        
        # Registrar columnas originales para debugging
        original_columns = df.columns.tolist()
        logging.info(f"Columnas originales en {os.path.basename(file_path)}: {original_columns}")
        
        # Renombrar columnas según el mapeo
        renamed_columns = {}
        for col in df.columns:
            if col in COLUMN_MAPPING:
                renamed_columns[col] = COLUMN_MAPPING[col]
        
        df = df.rename(columns=renamed_columns)
        
        # Verificar columnas requeridas
        required_columns = {'Date', 'Close'}
        missing_columns = required_columns - set(df.columns)
        
        if missing_columns:
            logging.warning(f"Columnas faltantes en {os.path.basename(file_path)}: {missing_columns}")
            raise ValueError(f"Faltan columnas requeridas: {missing_columns}")
        
        return df
    
    except Exception as e:
        logging.error(f"Error procesando {os.path.basename(file_path)}: {str(e)}")
        raise

def merge_csv_files(directory_data, directory_output, pattern):
    """
    Función principal para combinar archivos CSV.
    
    Args:
        directory (str): Directorio donde se encuentran los archivos
        pattern (str): Patrón base para identificar los archivos
    """
    logging.info(f"Iniciando proceso de combinación de archivos CSV para patrón '{pattern}' en {directory_data}")
    
    try:
        # Encontrar archivos CSV
        csv_files = find_csv_files(directory_data, pattern)
        if not csv_files:
            logging.warning(f"No se encontraron archivos CSV con el patrón '{pattern}'")
            return
        
        # Lista para almacenar los DataFrames procesados
        dfs = []
        
        # Procesar cada archivo
        for file_path in csv_files:
            try:
                df = read_and_standardize_csv(file_path)
                dfs.append(df)
                logging.info(f"Archivo procesado exitosamente: {os.path.basename(file_path)}")
            except Exception as e:
                logging.error(f"Error en archivo {os.path.basename(file_path)}: {str(e)}")
                continue
        
        if not dfs:
            logging.error(f"No se pudo procesar ningún archivo correctamente para el patrón '{pattern}'")
            return
        
        # Combinar todos los DataFrames
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Eliminar duplicados basados en la fecha
        combined_df = combined_df.drop_duplicates(subset=['Date'], keep='first')
        
        # Ordenar por fecha
        combined_df = combined_df.sort_values('Date', ascending=False)
        
        # Generar nombre del archivo de salida
        output_filename = f"{pattern}_TOTAL.csv"
        output_path = os.path.join(directory_output, output_filename)
        
        # Guardar resultado
        combined_df.to_csv(output_path, index=False)
        logging.info(f"Archivo combinado guardado exitosamente: {output_filename}")
        
        # Registrar estadísticas finales
        logging.info(f"Estadísticas finales para {pattern}:")
        logging.info(f"- Archivos procesados: {len(csv_files)}")
        logging.info(f"- Total de registros: {len(combined_df)}")
        logging.info(f"- Columnas en archivo final: {combined_df.columns.tolist()}")
        
        return True
    
    except Exception as e:
        logging.error(f"Error en el proceso de combinación para '{pattern}': {str(e)}")
        return False

def process_all_patterns(directory_data, directory_output, patterns):
    """
    Procesa múltiples patrones de archivos CSV.
    
    Args:
        directory_data (str): Directorio donde se encuentran los archivos
        directory_output (str): Directorio donde se guardaran los archivos
        patterns (list): Lista de patrones a procesar
    """
    setup_logging()
    logging.info(f"Iniciando procesamiento de múltiples patrones")
    
    successful_patterns = 0
    failed_patterns = 0
    
    for pattern in patterns:
        logging.info(f"Procesando patrón: {pattern}")
        print(f"Procesando patrón: {pattern}")
        
        if merge_csv_files(directory_data, directory_output, pattern):
            successful_patterns += 1
        else:
            failed_patterns += 1
    
    # Resumen final
    logging.info(f"\nResumen de procesamiento:")
    logging.info(f"- Patrones procesados exitosamente: {successful_patterns}")
    logging.info(f"- Patrones con errores: {failed_patterns}")
    logging.info(f"- Total de patrones: {len(patterns)}")
    
    print(f"\nProceso completado:")
    print(f"- Patrones exitosos: {successful_patterns}")
    print(f"- Patrones fallidos: {failed_patterns}")

if __name__ == "__main__":
    # Ejemplo de uso con múltiples patrones
    directory_data = r"c:\Users\acer a10\Documents\BITLINK\Repositorios\merge-csv-data\data"
    directory_output = r"c:\Users\acer a10\Documents\BITLINK\Repositorios\merge-csv-data\output"
    patterns = [       
        "Bovespa Historical Data",
        "XPT_USD Historical Data",
        "XAU_USD Historical Data",
        "USD_ZAR Historical Data",
        "USD_TRY Historical Data",
        "USD_MXN Historical Data",
        "USD_INR Historical Data",
        "USD_EUR Historical Data",
        "USD_COP Historical Data",
        "USD_CNY Historical Data",
        "USD_CLP Historical Data",
        "USD_BRL Historical Data",
        "USD_ARS Historical Data",
        "United States 10-Year Bond Yield Historical Data",
        "United States 2-Year Bond Yield Historical Data",
        "Silver Futures Historical Data",
        "Shanghai Shenzhen CSI 300 Historical Data",
        "SGD_USD Historical Data",
        "S&P_BMV IPC Historical Data",
        "S&P CLX IPSA Historical Data",
        "PLN_USD Historical Data",
        "Platinum Futures Historical Data",
        "Nasdaq 100 Historical Data",
        "MXN_USD Historical Data",
        "Mexico 10-Year Bond Yield Historical Data",
        "Gold Futures Historical Data",
        "FTSE_JSE All Share Historical Data",
        "FTSE Latin America All Cap Historical Data",
        "FTSE Emerging Historical Data",
        "Copper Futures Historical Data",
        "Colombia 10-Year Bond Yield Historical Data",
        "Colombia 5-Year Bond Yield Historical Data",
        "COLCAP Historical Data",
        "CNY_USD Historical Data",
        "Chile 10-Year Bond Yield Historical Data",
        "CHF_EUR Historical Data",
        "BRL_USD Historical Data",
        "Brent Oil Futures Historical Data",
        "Brazil 10-Year Bond Yield Historical Data",
    ]
    
    try:
        process_all_patterns(directory_data, directory_output, patterns)
        print("\nProceso completado. Revisa el archivo de log para más detalles.")
    except Exception as e:
        print(f"\nError en el proceso principal: {str(e)}")
        print("Revisa el archivo de log para más detalles.")