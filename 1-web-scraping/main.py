from bs4 import BeautifulSoup
import requests
import re

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
