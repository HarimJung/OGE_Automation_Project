💡 README.md (Project Readme File - English)

# UNICEF Angola OGE Dashboard: Data Automation Engine (Python ETL)

This project serves as the data processing engine for UNICEF Angola's OGE (National State Budget) dashboard system. It is designed to ensure the sustainable operation (ToR 1.2) of the Tableau dashboard and allows non-developers to execute data updates and transformations annually without modifying the code (No-Code Automation).

🚀 1. System Overview and Key Features (ToR Alignment)
Feature	Description	ToR Evaluation Criteria
No-Code Automation	A Python script handles all data integration, policy tag enrichment, and currency conversion in a single execution. UNICEF staff only need to update the CSV files.	3.4 Innovation and Added Value (5 pts)
Sustainability	Guarantees a Zero TCO (Total Cost of Ownership) model, enabling annual data updates without reliance on external consultants or developers.	1.2 Sustainability Goals (5 pts)
Policy Alignment	Automatically merges the Policy_Tags_Mapping.csv file, instantly enabling policy-based analysis such as PF4C and GEWE.	OGE Analysis Requirements
Bilingual Support	Provides the foundation for the dashboard's labels and categories to be toggled between English ↔ Portuguese (Português) via Language_Mapping_PT.csv.	3.2 Strategy/Bilingual Interface (10 pts)
📁 2. File Structure and Data Flow
2.1. Project Structure

You only need to save the Python code below as setup_and_etl.py and run it. The project structure and all sample data files will be created automatically.

/OGE_Automation_Project
├── data_input/                 <-- 🚨 Folder for raw data, which users must update annually.
│   ├── OGE_Data_2024.csv
│   ├── OGE_Data_2025.csv       <-- New OGE data (e.g., 2026.csv) is added here.
│   ├── Policy_Tags_Mapping.csv <-- Policy tag criteria (PF4C/GEWE) per program.
│   └── Language_Mapping_PT.csv <-- Lookup table for the Tableau Bilingual Toggle.
├── setup_and_etl.py            <-- 🌟 Single-execution Automation Script (Do not modify).
└── Consolidated_OGE_Data.csv   <-- ✅ Final Output (The file to connect to Tableau).
2.2. Data Schema (Mandatory Columns)

File Name	Core Columns	Role and Description
OGE_Data_*.csv	Year, Sector, Program_ID, Approved_Local_Currency	Source data for the annual budget. New budget year data must adhere to this schema.
Policy_Tags_Mapping.csv	Program_ID, PF4C_Tag, GEWE_Tag	The criteria table used by the ETL script to merge policy tags into the OGE data based on Program_ID.
Output (Consolidated_OGE_Data.csv)	Approved_USD (Added)	The budget column automatically converted to USD during the ETL process using the defined exchange rate.
⚙️ 3. System Usage Guide (1-Click Automation)
This system is designed for use by UNICEF M&E/OGE staff without requiring external technical support.

Step 1: Environment Setup (One-time)

Ensure Python 3 is installed on your system.

Open your Command Prompt (CMD) or Terminal.

Install the required library (pandas).

Bash
pip install pandas
Step 2: Data Update

When new annual OGE budget data (e.g., 2026 data) is released:

Create New CSV: Save the new budget data as a CSV file (e.g., OGE_Data_2026.csv). (It must maintain the same column structure as the existing OGE_Data_*.csv files).

Place in Folder: Copy this new CSV file into the data_input folder.

Policy/Language Update (If Needed): If new sectors or program IDs are introduced, update the Policy_Tags_Mapping.csv and Language_Mapping_PT.csv files accordingly.

Step 3: Execute ETL (Automation)

Navigate to the OGE_Automation_Project folder in your Terminal.

Execute the script with the following command:

Bash
python setup_and_etl.py
✅ Result

The script will run the ETL process, integrating, cleaning, and transforming all data.

The Consolidated_OGE_Data.csv file will be newly created or updated in the main project folder. This is the single file you connect to Tableau.

4. Troubleshooting and Maintenance
Q: I receive a ModuleNotFoundError: No module named 'pandas'.

A: The required Python library pandas is not installed. Please re-execute the pip install pandas command from Step 1.

Q: I added a new OGE_Data_*.csv file, but the Tableau dashboard doesn't show the data.

A: You must execute the python setup_and_etl.py script. The script is necessary to consolidate all raw data and generate the final, updated Consolidated_OGE_Data.csv file that Tableau connects to.

Q: How do I change the Exchange Rate?

A: Open the setup_and_etl.py file in any text editor and modify only the numerical value in the following line near the top of the code:

Python
# EXCHANGE_RATE_USD = 180.00  # <--- Modify this number only.
🐍 5. Complete Python ETL Script (setup_and_etl.py)
This script contains the logic to automatically generate the 4 required CSV files (200 rows of OGE data, 15 policy tags, and the Portuguese lookup table) and then run the ETL process, ensuring all data is present and accounted for.
