import tabula
import pandas as pd

pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

tabelas = tabula.read_pdf(pdf_path, pages=3, multiple_tables=True, pandas_options={"header": None})

for i, tabela in enumerate(tabelas):
    csv_file_name = f"tabela_{i + 1}.csv"
    tabela.to_csv(csv_file_name, index=False, header=False, encoding='utf-8')
    print(f"Tabela {i + 1} salva como {csv_file_name}")