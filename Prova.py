from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class KatalonDemoCuraTest:
    def __init__(self):
        self.servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=self.servico)
        self.tempo_limite = 10  # Tempo em segundos

    def navegar_para_site(self):
        self.navegador.get("https://katalon-demo-cura.herokuapp.com/")

    def clicar_em_agendar(self):
        self.aguardar_e_clicar('//*[@id="btn-make-appointment"]')

    def preencher_login(self, username, password):
        self.navegador.find_element(By.XPATH, '//*[@id="txt-username"]').send_keys(username)
        self.navegador.find_element(By.XPATH, '//*[@id="txt-password"]').send_keys(password)
        self.aguardar_e_clicar('//*[@id="btn-login"]')

    def preencher_detalhes_agendamento(self, data, comentario):
        self.navegador.find_element(By.XPATH, '//*[@id="combo_facility"]').send_keys('Seoul CURA Healthcare Center')
        self.navegador.find_element(By.XPATH, '//*[@id="chk_hospotal_readmission"]').click()
        self.navegador.find_element(By.XPATH, '//*[@id="radio_program_medicaid"]').click()
        self.navegador.find_element(By.XPATH, '//*[@id="txt_visit_date"]').send_keys(data)
        self.navegador.find_element(By.XPATH, '//*[@id="txt_comment"]').send_keys(comentario)
        self.aguardar_e_clicar('//*[@id="btn-book-appointment"]')

    def confirmar_agendamento(self):
        try:
            WebDriverWait(self.navegador, self.tempo_limite).until(
                EC.text_to_be_present_in_element((By.XPATH, '//h2'), "Appointment Confirmation")
            )
            print("Agendamento confirmado com sucesso.")
        except TimeoutException:
            print("Falha na confirmação do agendamento.")

    def aguardar_e_clicar(self, xpath):
        try:
            WebDriverWait(self.navegador, self.tempo_limite).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            self.navegador.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            print(f"Página não encontrada ou o elemento {xpath} não está disponível.")

    def fechar_navegador(self):
        self.navegador.quit()

# Usando a classe
teste = KatalonDemoCuraTest()
teste.navegar_para_site()
teste.clicar_em_agendar()
teste.preencher_login('John Doe', 'ThisIsNotAPassword')
teste.preencher_detalhes_agendamento('19/12/2023', 'Esse é um teste para a vaga de QA')
teste.confirmar_agendamento()
teste.fechar_navegador()
