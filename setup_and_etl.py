import pandas as pd
import numpy as np
import random

# --- Configuration (Angola Context) ---
OUTPUT_FILE = 'Consolidated_OGE_Data_Final.csv'
EXCHANGE_RATE_USD = 180.00  # Angola Exchange Rate (1 USD = 180 Kz)
SECTORS = ['Health', 'Education', 'Social Protection', 'Infrastructure', 'Rural Development']
PROGRAM_PREFIXES = ['P0', 'P1']
PROVINCES = ['Luanda', 'Huambo', 'Bié', 'Uíge', 'Cuando Cubango'] # 5 major provinces
BUDGET_TYPES = ['Approved', 'Proposed']
QUARTERS = [1, 2, 3, 4] # Quarterly data added

print("--- 🌟 UNICEF OGE Dashboard Data Automation (Python ETL) V3 (Quarter Added) Started ---")

# --- 1. Auto-generate and Consolidate Virtual CSV Files (Concatenation) ---
all_data = []
print("--- 1. Virtual CSV Files and Data Row Extension Started (Quarter Field Added) ---")

# 1-1. Generate OGE_Data_2024 and OGE_Data_2025 (Total 200 rows)
for year in [2024, 2025]:
    num_rows = 100
    np.random.seed(year + 15) # Change seed for reproducibility
    
    # Assume 15% growth rate for 2025 compared to 2024 to provide meaning for YoY analysis
    base_multiplier = 1.0 if year == 2024 else 1.15 
    
    data = {
        'Year': year,
        'Sector': np.random.choice(SECTORS, num_rows, p=[0.3, 0.3, 0.2, 0.1, 0.1]),
        'Program_ID': [f'{PROGRAM_PREFIXES[year-2024]}{i:03d}' for i in range(1, num_rows + 1)],
        # Approved amount: 2025 is set higher than 2024
        'Approved_Local_Currency': (np.random.rand(num_rows) * 100 + 50) * 1000000 * base_multiplier,
        'Budget_Type': np.random.choice(BUDGET_TYPES, num_rows, p=[0.6, 0.4]),
        'Province': np.random.choice(PROVINCES, num_rows, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
        # ✨ V3.0 New Field 4: Quarter (supports quarterly trend analysis)
        'Quarter': np.random.choice(QUARTERS, num_rows, p=[0.25, 0.25, 0.25, 0.25])
    }
    df = pd.DataFrame(data)
    df['Approved_Local_Currency'] = df['Approved_Local_Currency'].astype(int)
    all_data.append(df)
    # Save to file
    import os
    os.makedirs('data_input', exist_ok=True)
    df.to_csv(f'data_input/OGE_Data_{year}.csv', index=False, encoding='utf-8-sig')
    print(f"✅ OGE_Data_{year}.csv ({len(df)} rows) created and **Quarter** field added.")

# 1-2. Expand Policy Tag Mapping Table (Climate_Tag and dummy data enhancement)
tag_programs = [f'P{year_prefix}{i:03d}' for year_prefix in [0, 1] for i in random.sample(range(1, 101), 30)] # PF4C/GEWE tags for 30% of programs
climate_tagged_programs = [f'P{year_prefix}{i:03d}' for year_prefix in [0, 1] for i in random.sample(range(1, 101), 15)] # Climate tags for 15% of programs

policy_data = {
    'Program_ID': tag_programs + climate_tagged_programs,
    'PF4C_Tag': ['Child Focus'] * len(tag_programs) + ['Not Tagged'] * len(climate_tagged_programs),
    'GEWE_Tag': ['Gender Impact'] * len(tag_programs) + ['Not Tagged'] * len(climate_tagged_programs),
    'Climate_Tag': ['Not Tagged'] * len(tag_programs) + ['Climate Impact'] * len(climate_tagged_programs)
}
# Handle duplicate Program_IDs (a program can have both PF4C/GEWE and Climate tags)
df_policy = pd.DataFrame(policy_data).groupby('Program_ID').agg(lambda x: ', '.join(set(x))).reset_index()
# Handle cases where only 'Not Tagged' remains
for col in ['PF4C_Tag', 'GEWE_Tag', 'Climate_Tag']:
    df_policy[col] = df_policy[col].apply(lambda x: x.replace('Not Tagged, ', '').replace(', Not Tagged', '') if x.count('Not Tagged') > 0 and len(x) > len('Not Tagged') else x)
    df_policy[col] = df_policy[col].apply(lambda x: x if x != 'Not Tagged' else None) # If only 'Not Tagged' remains, treat as NaN to be filled after merge

# Save to file
df_policy.to_csv('data_input/Policy_Tags_Mapping.csv', index=False, encoding='utf-8-sig')
print(f"✅ Policy_Tags_Mapping.csv ({len(df_policy)} tags) created.")

# 1-3. Expand Language Mapping Table (Add Quarter field translation)
language_data = {
    'English_Key': ['Health', 'Education', 'Social Protection', 'Infrastructure', 'Rural Development', 
                    'Child Focus', 'Gender Impact', 'Climate Impact', 'Not Tagged', 
                    'Approved', 'Proposed', 'Approved_Local_Currency', 'Approved_USD', 
                    'Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4', 'Total OGE Growth (YoY)'],
    'Field_Type': ['Sector', 'Sector', 'Sector', 'Sector', 'Sector', 
                   'Policy_Tag', 'Policy_Tag', 'Policy_Tag', 'Policy_Tag', 
                   'Budget_Type', 'Budget_Type', 'Metric', 'Metric', 
                   'Quarter', 'Quarter', 'Quarter', 'Quarter', 'Metric'],
    'Portuguese_Translation': ['Saúde', 'Educação', 'Proteção Social', 'Infraestrutura', 'Desenvolvimento Rural', 
                               'Foco na Criança', 'Impacto de Gênero', 'Impacto Climático', 'Não Classificado', 
                               'Aprovado', 'Proposto', 'Orçamento Aprovado (Moeda Local)', 'Orçamento Aprovado (USD)',
                               'Trimestre 1', 'Trimestre 2', 'Trimestre 3', 'Trimestre 4', 'Crescimento OGE Total (YoY)']
}
df_lang = pd.DataFrame(language_data)
# Save to file
df_lang.to_csv('data_input/Language_Mapping_PT.csv', index=False, encoding='utf-8-sig')
print("✅ Language_Mapping_PT.csv (Portuguese mapping) created and **quarter translation** added.")

df_consolidated = pd.concat(all_data, ignore_index=True)
print(f"\n✨ Step 1: All yearly data consolidated. Total rows: {len(df_consolidated)}.")

# --- 2. Start ETL (Integration, Transformation, Enrichment) Pipeline ---
print("--- 2. ETL (Integration, Transformation, Enrichment) Pipeline Started ---")

# 2-1. Policy Tag Enrichment (Enrichment/Merge - ToR Policy Alignment)
df_merged = pd.merge(df_consolidated, df_policy, on='Program_ID', how='left')

# Policy tag merging and missing value handling
df_merged['PF4C_Tag'] = df_merged['PF4C_Tag'].fillna('Not Tagged')
df_merged['GEWE_Tag'] = df_merged['GEWE_Tag'].fillna('Not Tagged')
df_merged['Climate_Tag'] = df_merged['Climate_Tag'].fillna('Not Tagged')

df_consolidated = df_merged
print("✨ PF4C/GEWE/Climate policy tags automatically merged and missing values handled.")

# 2-2. Currency Conversion (Transformation - Create Approved_USD column)
df_consolidated['Approved_USD'] = df_consolidated['Approved_Local_Currency'] / EXCHANGE_RATE_USD
df_consolidated['Approved_USD'] = df_consolidated['Approved_USD'].round(2)
print(f"✨ Currency conversion completed. (1 USD = {EXCHANGE_RATE_USD} Kz applied)")

# --- 3. Final Results Output ---
print("\n=========================================================================")
print(f"✅ Final Result: Tableau dashboard dataset successfully created.")
print(f"   **Total rows: {len(df_consolidated)}**")
print("   **Analysis fields included:** Year, Quarter, Budget_Type, Province, 3x Policy Tags")
print("=========================================================================\n")

print("--- Final Consolidated Dataset Preview (Top 5 Rows) ---")
# Output including newly added columns
print(df_consolidated[['Year', 'Quarter', 'Sector', 'Program_ID', 'Budget_Type', 'Province', 'Approved_USD', 'PF4C_Tag', 'GEWE_Tag', 'Climate_Tag']].head(5).to_markdown(index=False))

# Save language mapping table as separate file (Tableau Lookup)
df_lang.to_csv('Language_Mapping_PT_Final.csv', index=False)
# Save final consolidated dataset
df_consolidated.to_csv(OUTPUT_FILE, index=False)