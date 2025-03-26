import tabula

pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

tabelas = tabula.read_pdf(pdf_path, pages=3, multiple_tables=True, pandas_options={"header": None})

for i, tabela in enumerate(tabelas):
    print(f"Tabela {i + 1}:")
    print(tabela)
    print()
