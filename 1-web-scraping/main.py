from bs4 import BeautifulSoup
import requests
import re
import os
import zipfile
import shutil

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    internal_links = soup.find_all('a', class_='internal-link')

    filtered_links = []
    for tag in internal_links:
        href = tag.get('href', '')  
        if href.endswith('.pdf') and re.search(r"Anexo_[IVX]+", href): 
            filtered_links.append(href)

    if filtered_links:
        print("Links filtrados com 'Anexo_x' e terminando com '.pdf':")
        for link in filtered_links:
            print(link)
    else:
        print("Nenhum link com 'Anexo_x' e terminando com '.pdf' foi encontrado.")
else:
    print(f"Erro ao acessar o site. Código de status: {response.status_code}")

##### download

os.makedirs("temp_pdfs", exist_ok=True)

for link in filtered_links:
    file_name = link.split("/")[-1]
    file_path = os.path.join("temp_pdfs", file_name)
    pdf_response = requests.get(link)

    if pdf_response.status_code == 200:
        with open(file_path, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"Arquivo baixado: {file_name}")
    else:
        print(f"Erro ao baixar o arquivo: {file_name}")

zip_file_name = "anexos.zip"
with zipfile.ZipFile(zip_file_name, "w") as zipf:
    for root, _, files in os.walk("temp_pdfs"):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=file)

print(f"Arquivos compactados em: {zip_file_name}")

shutil.rmtree("temp_pdfs")

