import pandas as pd
import os
import plotly.express as px

# File paths
metadata_file = "metadata.csv"
data_folder = "Data"

# Load metadata
metadata = pd.read_csv(metadata_file)

# Add a relative age column (simplified as test_id order; adjust as needed for actual aging criteria)
metadata['relative_age'] = metadata.groupby('battery_id')['test_id'].rank()

# Extract relevant columns
params_df = metadata[['battery_id', 'test_id', 'relative_age', 'Re', 'Rct']]

# Plot 1: Re vs Relative Age
fig_re = px.line(params_df, x='relative_age', y='Re', color='battery_id',
                 title="Estimated Electrolyte Resistance (Re) vs Battery Age",
                 labels={'relative_age': 'Relative Age', 'Re': 'Electrolyte Resistance (Ohms)'})
fig_re.show()

# Plot 2: Rct vs Relative Age
fig_rct = px.line(params_df, x='relative_age', y='Rct', color='battery_id',
                  title="Charge Transfer Resistance (Rct) vs Battery Age",
                  labels={'relative_age': 'Relative Age', 'Rct': 'Charge Transfer Resistance (Ohms)'})
fig_rct.show()

# Now parse the individual CSV files for impedance and other parameters
impedance_data = []
for idx, row in metadata.iterrows():
    file_path = os.path.join(data_folder, row['filename'])
    if os.path.exists(file_path):
        # Read the corresponding file
        df = pd.read_csv(file_path)
        df['battery_id'] = row['battery_id']
        df['test_id'] = row['test_id']
        df['relative_age'] = row['relative_age']
        impedance_data.append(df)

# Combine all loaded data
impedance_data = pd.concat(impedance_data, ignore_index=True)

# Plot 3: Battery Impedance (Voltage vs Current) with Age
fig_impedance = px.scatter(impedance_data, x='Voltage_measured', y='Current_measured', 
                           color='relative_age', facet_col='battery_id', 
                           title="Battery Impedance Evolution with Aging",
                           labels={'Voltage_measured': 'Voltage (V)', 'Current_measured': 'Current (A)', 
                                   'relative_age': 'Relative Age'})
fig_impedance.show()
