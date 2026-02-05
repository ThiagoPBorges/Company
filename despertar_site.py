from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def despertar_site():
    url = "https://thiagopborges.streamlit.app/"
    
    print("⏰ Iniciando o script de despertar o site...")

    # Configuração para rodar sem tela
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Instala o driver do Chrome automaticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        print(f"✅ Acesso realizado em: {url}")
        
        # Espera um pouco para garantir que o Streamlit carregou
        time.sleep(10) 
        
        print(f"Título da página encontrada: {driver.title}")
        print("🚀 Site acordado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao tentar acessar: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    despertar_site()