# instale o "pip install webdriver-manager selenium"

import sqlite3
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Cria o banco de dados e a conexão:
conexao = sqlite3.connect("raspagemNoticias.sqlite3")
cursor = conexao.cursor()

# Cria a tabela se ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS noticia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        data TEXT,
        descricao TEXT
    );
''')

conexao.commit()

sql = 'INSERT INTO noticia (titulo, data, descricao) VALUES (?, ?, ?)'

# Cria o driver do navegador Chrome, e acessa a página que você desejar:
navegador = Chrome(service=Service(ChromeDriverManager().install()))
navegador.get('https://www.uol.com.br/')

# Encontra a tag 'a', que contém o link que quero fazer acessar na página inicial:
link = navegador.find_element(By.CSS_SELECTOR, 'a[href="https://noticias.uol.com.br/"]')
link.click()

# Encontra a tag section, e pega a tag dentro da section 'a', que contém o link que quero clicar;
# Dessa forma, abre o link da notícia que está em manchete.
primeira_noticia = navegador.find_element(By.CSS_SELECTOR, 'section[class="highlights-portal"] a')
primeira_noticia.click()

for noticia in navegador.find_elements(By.CSS_SELECTOR, 'div[class="headline-container"]'):
    titulo = navegador.find_element(By.TAG_NAME, 'h1').text
    data = navegador.find_element(By.TAG_NAME, 'time').text
    descricao = navegador.find_element(By.TAG_NAME, 'p').text

    # Inserção dos dados no banco
    valores = [titulo, data, descricao]
    cursor.execute(sql, valores)
    conexao.commit()


# Commit e fechamento das conexões
navegador.close()
conexao.commit()
conexao.close()
