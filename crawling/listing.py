import pandas as pd


# Patient Listing By Input
patient_list = input('Fill In PatientID: ').split()
patient_list.sort()

# # Patient Listing By Patient List
# df = pd.read_csv(r'C:\Users\Admin\Downloads\patientlistingbypcno.csv', dtype='string')
# patient_list = list(df['PCNO'])
# patient_list.sort()

# # Patient Listing By Last Seen
# df = pd.read_excel(r'C:\Users\Admin\Downloads\patientlistingbypcno.xlsx', names=['PID', 'NAME', 'PCNO'], sheet_name=None, dtype='string')
# df_all = pd.concat(df).reset_index(drop=True)
# patient_list = list(df_all['PCNO'][0:-1])
# patient_list.sort()

# # Patient Listing By PCNO
# df = pd.read_excel(r'C:\Users\Admin\Downloads\patientlistingbypcno.xls', header=None, sheet_name=None, dtype='string')
# df_all = pd.concat(df).reset_index(drop=True)
# patient_list = list(df_all[0][0:-1])
# patient_list.sort()