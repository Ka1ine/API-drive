from datetime import datetime
from quickstart import upload

data_frame = "CRIAR DATA FRAME PARA MANDAR PARA O DRIVE"

date_now = datetime.now()
file_name = f"Seller Reputation - {date_now.strftime('%d-%m-%y')}" + ".csv"
data_frame.to_csv(file_name, sep=',', index=False)
folder_id = ['1pJsqI16zD3HF6Ja1x20QUcgut4bDPU0I']
dir_name = ""
upload(file_name, dir_name, folder_id)
