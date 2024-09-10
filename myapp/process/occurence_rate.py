import pandas as pd

def OCR_calc(input_file_path, output_file_path, bin_width=0.1):
    def occurence_per_interval(a_val, b_val, min_mag, max_mag):
        occurence_rate = (10 ** (a_val - b_val * min_mag) - 10 ** (a_val - b_val * max_mag)) / 100
        return occurence_rate

    def column_appender(column_name, df, occurence_data, index):
        if column_name in df:
            df.at[index, column_name] = occurence_data
        else:
            df[column_name] = 0
            df.at[index, column_name] = occurence_data
        return df

    def occurence_calculation_loop(fault_data, bin_width=0.1):
        fault_data['Bins'] = 0
        for index, fault in fault_data.iterrows():
            current = round(fault['Min Magnitude'], 1)
            interval_count = 0
            while current < round(fault['Max Magnitude'], 1):
                next_val = round(current + bin_width, 1)
                interval_str = f'{current} - {next_val}'
                occurence_rate = occurence_per_interval(
                    fault['a-value'], fault['b-value'], current, next_val)
                current = next_val
                fault_data = column_appender(
                    f'OCR_{interval_count}', fault_data, occurence_rate, index)
                interval_count += 1
            fault_data.at[index, 'Bins'] = interval_count
        return fault_data

    summary_data = pd.read_excel(input_file_path)
    occurence_per_interval_data = occurence_calculation_loop(summary_data, bin_width=bin_width)
    occurence_per_interval_data.to_excel(output_file_path, index=False)

# Example usage:
# process_summary_data_and_export("input_file_path.xlsx", "output_file_path.xlsx", bin_width=0.1)
