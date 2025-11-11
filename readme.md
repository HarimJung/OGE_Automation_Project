# UNICEF Angola OGE Dashboard: Data Automation Engine (Python ETL)

This project serves as the data processing engine for UNICEF Angola's OGE (National State Budget) dashboard system. It is designed to ensure the sustainable operation of the Tableau dashboard and allows non-developers to execute data updates and transformations annually without modifying the code (No-Code Automation).

## 🚀 1. System Overview and Key Features

| Feature | Description |
|---------|-------------|
| **No-Code Automation** | A Python script handles all data integration, policy tag enrichment, and currency conversion in a single execution. UNICEF staff only need to run the script. |
| **Sustainability** | Guarantees a Zero TCO (Total Cost of Ownership) model, enabling annual data updates without reliance on external consultants or developers. |
| **Policy Alignment** | Automatically merges policy tags (PF4C, GEWE, Climate) enabling comprehensive policy-based analysis. |
| **Bilingual Support** | Provides Portuguese translations via Language_Mapping_PT.csv for dashboard localization. |
| **Quarterly Analysis** | Supports quarterly trend analysis with Quarter field for detailed budget tracking. |

## 📁 2. File Structure and Data Flow

### 2.1. Project Structure

```
/OGE_Automation_Project
├── data_input/                        <-- Raw data folder (auto-generated)
│   ├── OGE_Data_2024.csv             <-- 2024 Budget data (100 rows)
│   ├── OGE_Data_2025.csv             <-- 2025 Budget data (100 rows)
│   ├── Policy_Tags_Mapping.csv       <-- Policy tags (PF4C/GEWE/Climate)
│   └── Language_Mapping_PT.csv       <-- Portuguese translation mapping
├── setup_and_etl.py                  <-- Main automation script
├── requirements.txt                  <-- Python dependencies
├── Consolidated_OGE_Data_Final.csv   <-- Final output for Tableau
└── Language_Mapping_PT_Final.csv     <-- Final Portuguese mapping
```

### 2.2. Data Schema (Output File: Consolidated_OGE_Data_Final.csv)

| Column Name | Type | Description |
|-------------|------|-------------|
| `Year` | Integer | Budget year (2024, 2025, etc.) |
| `Quarter` | Integer | Quarter number (1-4) |
| `Sector` | String | Health, Education, Social Protection, Infrastructure, Rural Development |
| `Program_ID` | String | Unique program identifier (P0001-P0100, P1001-P1100) |
| `Budget_Type` | String | Approved or Proposed |
| `Province` | String | Luanda, Huambo, Bié, Uíge, Cuando Cubango |
| `Approved_Local_Currency` | Integer | Budget amount in Angolan Kwanza (Kz) |
| `Approved_USD` | Float | Budget amount in USD (auto-converted) |
| `PF4C_Tag` | String | Child Focus policy tag |
| `GEWE_Tag` | String | Gender Impact policy tag |
| `Climate_Tag` | String | Climate Impact policy tag |
## ⚙️ 3. System Usage Guide (Quick Start)

### Step 1: Environment Setup (One-time)

1. **Install Python 3.9+** on your system
2. **Clone this repository**:
   ```bash
   git clone https://github.com/HarimJung/OGE_Automation_Project.git
   cd OGE_Automation_Project
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install pandas numpy tabulate
   ```

### Step 2: Run the ETL Script

Simply execute the main script:

```bash
python setup_and_etl.py
```

**What happens:**
- Generates sample OGE data for 2024 and 2025 (200 rows total)
- Creates policy tag mappings (PF4C, GEWE, Climate)
- Generates Portuguese translation mapping
- Consolidates all data into `Consolidated_OGE_Data_Final.csv`
- Performs currency conversion (Kz → USD)
- Outputs preview of final dataset

### Step 3: Connect to Tableau

1. Open Tableau Desktop
2. Connect to **Text File** data source
3. Select `Consolidated_OGE_Data_Final.csv`
4. (Optional) Add `Language_Mapping_PT_Final.csv` as lookup table for bilingual support

## 🔧 4. Customization and Configuration

### Modify Exchange Rate

Edit `setup_and_etl.py`:
```python
EXCHANGE_RATE_USD = 180.00  # Change this value
```

### Add New Year Data

The script automatically generates data for 2024-2025. To add more years, modify the loop in `setup_and_etl.py`:
```python
for year in [2024, 2025, 2026]:  # Add more years
```

### Update Sectors or Provinces

Edit the configuration at the top of `setup_and_etl.py`:
```python
SECTORS = ['Health', 'Education', 'Social Protection', 'Infrastructure', 'Rural Development']
PROVINCES = ['Luanda', 'Huambo', 'Bié', 'Uíge', 'Cuando Cubango']
```

## 📊 5. Output Files Description

### Consolidated_OGE_Data_Final.csv
- **Rows**: 200 (100 per year)
- **Purpose**: Main dataset for Tableau dashboard
- **Contains**: All budget data with policy tags and currency conversions

### Language_Mapping_PT_Final.csv
- **Purpose**: Translation lookup table for bilingual dashboard
- **Contains**: English-Portuguese mappings for sectors, tags, and metrics

### data_input/ folder
Contains intermediate files:
- `OGE_Data_2024.csv` / `OGE_Data_2025.csv`: Raw budget data
- `Policy_Tags_Mapping.csv`: Policy tag assignments
- `Language_Mapping_PT.csv`: Translation mappings

## 🐛 6. Troubleshooting

**Q: ModuleNotFoundError: No module named 'pandas'**
```bash
pip install pandas numpy tabulate
```

**Q: Data not updating in Tableau**
- Re-run `python setup_and_etl.py`
- Refresh data source in Tableau

**Q: Currency conversion is incorrect**
- Check `EXCHANGE_RATE_USD` value in `setup_and_etl.py`
- Re-run the script after making changes

## 📝 7. Project Features

- ✅ **Automated data generation** (2024-2025 budget data)
- ✅ **Policy tag integration** (PF4C, GEWE, Climate Impact)
- ✅ **Quarterly analysis support**
- ✅ **Provincial distribution tracking**
- ✅ **Budget type comparison** (Approved vs Proposed)
- ✅ **Currency conversion** (Kz → USD)
- ✅ **Bilingual support** (English ↔ Portuguese)
- ✅ **YoY growth analysis** (15% growth rate from 2024 to 2025)

## 🤝 8. Contributing

This project is maintained for UNICEF Angola. For questions or improvements, please contact the project maintainer.

## 📄 9. License

This project is developed for UNICEF Angola internal use.