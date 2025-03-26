from bs4 import BeautifulSoup
import requests

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    internal_links = soup.find_all('a', class_='internal-link')

    if internal_links:
        print("Tags com a classe 'internal-link' encontradas:")
        for tag in internal_links:
            print(tag['href'])
    else:
        print("Nenhuma tag com a classe 'internal-link' foi encontrada.")
else:
    print(f"Erro ao acessar o site. Código de status: {response.status_code}")
