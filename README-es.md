# ETL-Bot: Recopilación y Procesamiento de Datos Financieros

## Descripción General
ETL-Bot es un pipeline de datos completo para recopilar, procesar y analizar datos del mercado financiero de diversas fuentes. El proyecto consta de tres componentes principales:

1. **Recolección de Datos Diarios** (`data_daily/`)
   - Web scraping automatizado para indicadores financieros diarios
   - Endpoints configurables mediante CSV

2. **Recolección de Datos No Diarios** (`data_different_daily/`)
   - Scraping especializado para indicadores económicos (PIB, IPC, Tasas de Interés)
   - Limpieza y estandarización de datos

3. **Fusión de Datos** (`merge_daily/`)
   - Consolidación de datos financieros históricos
   - Manejo robusto de errores y registro de actividades
   - Soporte para múltiples versiones de archivos

## Requisitos

### Requisitos del Sistema
- Python 3.7+
- Google Chrome
- ChromeDriver (versión compatible con Chrome)
- Git

### Dependencias de Python
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto
```
ETL-bot/
├── data_daily/
│   ├── bot.py              # Script de recolección diaria
│   └── EndPoint.csv        # Configuración de endpoints
├── data_different_daily/
│   ├── scrape_investing.py # Scraper de indicadores económicos
│   ├── clean_data.py       # Utilidades de limpieza de datos
│   ├── clean_data/        # Datos procesados
│   └── output/            # Datos sin procesar
└── merge_daily/
    ├── csv_merger.py      # Script de consolidación
    ├── data/             # Archivos CSV fuente
    ├── logs/            # Registros de procesamiento
    └── output/          # Salidas consolidadas
```

## Instrucciones de Instalación

1. **Clonar el Repositorio**
```bash
git clone https://github.com/[username]/ETL-bot.git
cd ETL-bot
```

2. **Crear Entorno Virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar Dependencias**
```bash
pip install selenium pandas webdriver-manager python-dateutil pytz
```

4. **Configuración de ChromeDriver**
- Descargar versión compatible desde [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/)
- Ubicar en `C:/chromedriver-win64/chromedriver-win64/` (Windows)
- Configurar perfil de Chrome si es necesario

## Uso de Componentes

### 1. Recolección de Datos Diarios
```bash
cd data_daily
python bot.py
```
- Configurar endpoints en `EndPoint.csv`
- Recolecta datos financieros diarios

### 2. Recolección de Indicadores Económicos
```bash
cd data_different_daily
python scrape_investing.py
```
- Recolecta datos de PIB, IPC y tasas de interés
- Guarda en el directorio `output/`
- Ejecutar `clean_data.py` para estandarización

### 3. Fusión de Datos
```bash
cd merge_daily
python csv_merger.py
```
- Consolida archivos de datos históricos
- Maneja duplicados y versionado de archivos
- Crea archivos `*_TOTAL.csv` en `output/`

## Manejo de Errores y Registro
- Logs detallados en `merge_daily/logs/`
- Formato: `csv_merger_YYYYMMDD_HHMMSS.log`
- Incluye detalles de procesamiento y reportes de errores

## Fuentes de Datos
- Indicadores financieros de mercado
- Indicadores económicos (PIB, IPC, Tasas de Interés)
- Tipos de cambio
- Índices de mercado
- Precios de materias primas
- Rendimientos de bonos

## Contribuciones
1. Hacer fork del repositorio
2. Crear rama de funcionalidad
3. Commit de cambios
4. Enviar pull request

## Contacto
Para preguntas o soporte:
- Email: 96pedroelias96@gmail.com
- Issues de GitHub: [Project Issues](https://github.com/pspedro19)

## Licencia
Licencia MIT - Ver archivo LICENSE para más detalles