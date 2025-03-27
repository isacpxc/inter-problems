import tabula
import pandas as pd
import zipfile
import os
from tqdm import tqdm  

print("O process iniciará em breve...")

try:
    os.makedirs("temp_csv", exist_ok=True)
except Exception as e:
    print(f"Erro ao criar pasta temp_csv: {e}")

pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

try:
    tabelas = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True, pandas_options={"header": None})
except Exception as e:
    print(f"Erro ao ler o arquivo PDF: {e}")
    tabelas = []

print("O process iniciará em breve...")

try:
    for i, tabela in enumerate(tqdm(tabelas, desc="Salvando tabelas como CSV")):
        csv_file_name = f"temp_csv/tabela_{i + 1}.csv"
        tabela.to_csv(csv_file_name, index=False, header=False, encoding='utf-8')
except Exception as e:
    print(f"Erro ao salvar tabelas como CSV: {e}")

try:
    pasta_temp = 'temp_csv'
    arquivos = [f for f in os.listdir(pasta_temp) if f.endswith('.csv')]
except Exception as e:
    print(f"Erro ao listar arquivos CSV: {e}")
    arquivos = []

try:
    if 'tabela_1.csv' in arquivos:
        os.remove(os.path.join(pasta_temp, 'tabela_1.csv'))
        arquivos.remove('tabela_1.csv')
except Exception as e:
    print(f"Erro ao remover tabela_1.csv: {e}")

try:
    caminho_tabela_2 = os.path.join(pasta_temp, 'tabela_2.csv')
    df_principal = pd.read_csv(caminho_tabela_2, encoding='utf-8')
except Exception as e:
    print(f"Erro ao carregar tabela_2.csv: {e}")
    df_principal = pd.DataFrame()

try:
    for arquivo in tqdm(arquivos, desc="Concatenando tabelas"):
        if arquivo != 'tabela_2.csv':
            caminho_arquivo = os.path.join(pasta_temp, arquivo)
            df_auxiliar = pd.read_csv(caminho_arquivo, encoding='utf-8')
            df_principal = pd.concat([df_principal, df_auxiliar.iloc[1:]], ignore_index=True)
except Exception as e:
    print(f"Erro ao concatenar tabelas: {e}")

try:
    df_principal.to_csv('tabela.csv', index=False, encoding='utf-8')
except Exception as e:
    print(f"Erro ao salvar tabela final: {e}")

try:
    for arquivo in tqdm(arquivos, desc="Removendo arquivos da pasta temp_csv"):
        os.remove(os.path.join(pasta_temp, arquivo))
    os.rmdir(pasta_temp)
    print("Processo concluído. Arquivo 'tabela_2.csv' movido para a raiz e pasta 'temp_csv' removida.")
except Exception as e:
    print(f"Erro ao remover pasta temp_csv: {e}")

try:
    zip_file_name = "Teste_isac.zip"
    with tqdm(zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED), desc="Compactando arquivo final") as zipf:
        zipf.write('tabela.csv', os.path.basename('tabela.csv'))
    print(f"Arquivo compactado como {zip_file_name}")
except Exception as e:
    print(f"Erro ao compactar arquivo final: {e}")

try:
    df = pd.read_csv('tabela.csv', encoding='utf-8')
    df.columns = df.columns.str.replace('OD', 'Seg. Odontológica').str.replace('AMB', 'Seg. Ambulatorial')

    df.to_csv('tabela.csv', index=False, encoding='utf-8')
    print("Alterações realizadas e arquivo 'tabela.csv' atualizado!")
except Exception as e:
    print(f"Erro ao substituir textos das colunas: {e}")
