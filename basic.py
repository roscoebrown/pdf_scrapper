from tabula.io import convert_into

pdf =  "FINAL SP Production Mascot Oil Field F21.pdf"
csv_file_name = 'First'

convert_into(pdf,f'{csv_file_name}data.csv',output_format="csv")
