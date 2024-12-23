# ETL-Bot: Financial Data Collection and Processing

## Overview
ETL-Bot is a comprehensive data pipeline for collecting, processing, and analyzing financial market data from various sources. The project consists of three main components:

1. **Daily Data Collection** (`data_daily/`)
   - Automated web scraping for daily financial indicators
   - Configurable endpoints via CSV

2. **Non-Daily Data Collection** (`data_different_daily/`)
   - Specialized scraping for economic indicators (GDP, CPI, Interest Rates)
   - Data cleaning and standardization

3. **Data Merging** (`merge_daily/`)
   - Consolidation of historical financial data
   - Robust error handling and logging
   - Support for multiple file versions

## Requirements

### System Requirements
- Python 3.7+
- Google Chrome
- ChromeDriver (matching Chrome version)
- Git

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Project Structure
```
ETL-bot/
├── data_daily/
│   ├── bot.py              # Daily data collection script
│   └── EndPoint.csv        # Configuration for data endpoints
├── data_different_daily/
│   ├── scrape_investing.py # Economic indicators scraper
│   ├── clean_data.py       # Data cleaning utilities
│   ├── clean_data/        # Processed data output
│   └── output/            # Raw data output
└── merge_daily/
    ├── csv_merger.py      # Data consolidation script
    ├── data/             # Source CSV files
    ├── logs/            # Processing logs
    └── output/          # Consolidated outputs
```

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/[username]/ETL-bot.git
cd ETL-bot
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **ChromeDriver Setup**
- Download matching version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/)
- Place in `C:/chromedriver-win64/chromedriver-win64/` (Windows)
- Configure Chrome profile if needed

## Component Usage

### 1. Daily Data Collection
```bash
cd data_daily
python bot.py
```
- Configure endpoints in `EndPoint.csv`
- Collects daily financial market data

### 2. Economic Indicators Collection
```bash
cd data_different_daily
python scrape_investing.py
```
- Collects GDP, CPI, and interest rate data
- Outputs to `output/` directory
- Run `clean_data.py` for data standardization

### 3. Data Merging
```bash
cd merge_daily
python csv_merger.py
```
- Consolidates historical data files
- Handles duplicates and file versioning
- Creates `*_TOTAL.csv` files in `output/`

## Error Handling and Logging
- Detailed logs in `merge_daily/logs/`
- Format: `csv_merger_YYYYMMDD_HHMMSS.log`
- Includes processing details and error reports

## Data Sources
- Financial market indicators
- Economic indicators (GDP, CPI, Interest Rates)
- Currency exchange rates
- Market indices
- Commodity prices
- Bond yields

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Submit pull request

## Contact
For questions or support:
- Email: 96pedroelias96@gmail.com
- GitHub Issues: [Project Issues](https://github.com/pspedro19)

## License
MIT License - See LICENSE file for details