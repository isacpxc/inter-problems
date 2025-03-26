import tabula
import pandas as pd
import zipfile
import os

pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

tabelas = tabula.read_pdf(pdf_path, pages=3, multiple_tables=True, pandas_options={"header": None})

for i, tabela in enumerate(tabelas):
    csv_file_name = f"tabela_{i + 1}.csv"
    tabela.to_csv(csv_file_name, index=False, header=False, encoding='utf-8')
    print(f"Tabela {i + 1} salva como {csv_file_name}")


csv_files = [f"tabela_{i + 1}.csv" for i in range(len(tabelas))]

zip_file_name = "Teste_isac.zip"

with zipfile.ZipFile(zip_file_name, 'w') as zipf:
    for csv_file in csv_files:
        zipf.write(csv_file, os.path.basename(csv_file))
        print(f"Arquivo {csv_file} adicionado ao ZIP.")

print(f"Arquivo ZIP criado: {zip_file_name}")
