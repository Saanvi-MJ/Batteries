import pandas as pd
import os
import plotly.express as px

metadata_file = "metadata.csv"
data_folder = "data"

metadata = pd.read_csv(metadata_file)

metadata['relative_age'] = metadata.groupby('battery_id')['test_id'].rank()

params_df = metadata[['battery_id', 'test_id', 'relative_age', 'Re', 'Rct']]

fig_re = px.line(params_df, x='relative_age', y='Re', color='battery_id',
                 title="Estimated Electrolyte Resistance (Re) vs Battery Age",
                 labels={'relative_age': 'Relative Age', 'Re': 'Electrolyte Resistance (Ohms)'})
fig_re.show()

fig_rct = px.line(params_df, x='relative_age', y='Rct', color='battery_id',
                  title="Charge Transfer Resistance (Rct) vs Battery Age",
                  labels={'relative_age': 'Relative Age', 'Rct': 'Charge Transfer Resistance (Ohms)'})
fig_rct.show()

impedance_data = []
for idx, row in metadata.iterrows():
    file_path = os.path.join(data_folder, row['filename'])
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['battery_id'] = row['battery_id']
        df['test_id'] = row['test_id']
        df['relative_age'] = row['relative_age']
        impedance_data.append(df)


impedance_data = pd.concat(impedance_data, ignore_index=True)

fig_impedance = px.scatter(impedance_data, x='Voltage_measured', y='Current_measured', 
                           color='relative_age', facet_col='battery_id', 
                           title="Battery Impedance Evolution with Aging",
                           labels={'Voltage_measured': 'Voltage (V)', 'Current_measured': 'Current (A)', 
                                   'relative_age': 'Relative Age'})
fig_impedance.show()
