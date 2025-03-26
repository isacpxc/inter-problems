from bs4 import BeautifulSoup
import requests
import re
import os
import zipfile
import shutil
from tqdm import tqdm 

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar o site: {e}")
    exit()

try:
    soup = BeautifulSoup(response.text, 'html.parser')
    internal_links = soup.find_all('a', class_='internal-link')
except Exception as e:
    print(f"Erro ao processar o conteúdo HTML: {e}")
    exit()

filtered_links = []
try:
    for tag in internal_links:
        href = tag.get('href', '')
        if href.endswith('.pdf') and re.search(r"Anexo_[IVX]+", href):
            filtered_links.append(href)
except Exception as e:
    print(f"Erro ao filtrar links: {e}")
    exit()

if filtered_links:
    print("Links filtrados com 'Anexo_x' e terminando com '.pdf':")
    for link in filtered_links:
        print(link)
else:
    print("Nenhum link com 'Anexo_x' e terminando com '.pdf' foi encontrado.")
    exit()

#####download
try:
    os.makedirs("temp_pdfs", exist_ok=True)
except Exception as e:
    print(f"Erro ao criar diretório temporário: {e}")
    exit()

print("Baixando arquivos PDF...")
for link in tqdm(filtered_links, desc="Progresso do Download"):
    file_name = link.split("/")[-1]
    file_path = os.path.join("temp_pdfs", file_name)
    try:
        pdf_response = requests.get(link)
        pdf_response.raise_for_status()
        with open(file_path, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo {file_name}: {e}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo {file_name}: {e}")

try:
    zip_file_name = "anexos.zip"
    print("Compactando arquivos em ZIP...")
    files_to_zip = [os.path.join("temp_pdfs", f) for f in os.listdir("temp_pdfs")]
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for file in tqdm(files_to_zip, desc="Progresso da Compactação"):
            zipf.write(file, arcname=os.path.basename(file))
    print(f"Arquivos compactados em: {zip_file_name}")
except Exception as e:
    print(f"Erro ao criar o arquivo ZIP: {e}")
    exit()

try:
    shutil.rmtree("temp_pdfs")
    print("Arquivos temporários removidos com sucesso.")
except Exception as e:
    print(f"Erro ao remover arquivos temporários: {e}")
