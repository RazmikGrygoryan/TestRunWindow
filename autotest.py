from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pytest


users = ['Freddy', 'Chip', 'Darth']
passws = ['sdafdsaf', '231231312', 'p012-1;s1']


def generate_creds():
    pairw = []
    for user in users:
        for passw in passws:
            pairw.append(pytest.param((user, passw), id=f'{user}, {passw}'))
    return pairw

# @pytest.mark.parametrize(
#     'creds',
#     [
#         pytest.param(('nonono', 'killer'), id='Anakin'),
#         pytest.param(('degenerate', 'dima18300'), id='Friends'),
#         pytest.param(('lox033', 'bazar777'), id='Danya')
#     ]
# )


@pytest.mark.parametrize('creds', generate_creds())
def test1(creds):
    options = Options()
    options.add_argument('--headless')
    login, passw = creds
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 40)
    driver.implicitly_wait(7)
    driver.get('https://tastystrike.com/')
    driver.find_element(By.XPATH, '(//a[@id="fastreg_block"])[2]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-signup-button-clicked="fast_auth"]').click()
    driver.find_element(By.XPATH, '//input[@placeholder="Введите логин"]').send_keys(login)
    driver.find_element(By.XPATH, '//input[@placeholder="Введите пароль"]').send_keys(passw)
    driver.find_element(By.CSS_SELECTOR, '[data-signup-button-clicked="fast_auth_2"]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//p[@class="error"]')))
    error = driver.find_element(By.XPATH, '//p[@class="error"]').text
    assert ('Неверный логин или пароль' == error)


@pytest.fixture()
def page(request):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(7)
    param = request.param
    if param == 'offersshop':
        driver.get('https://tastystrike.com/offersshop')
    elif param == 'contract':
        driver.get('https://tastystrike.com/contract')
    return driver


@pytest.mark.parametrize('page', ['offersshop'], indirect=True)
def test_offersshop(page):
    options = Options()
    options.add_argument('--headless')
    title = page.find_element(By.CSS_SELECTOR, '[class="offershop-heading"]')
    assert title.text == 'SECRET STORE'


@pytest.mark.parametrize('page', ['contract'], indirect=True)
def test_contract_2(page):
    options = Options()
    options.add_argument('--headless')
    title = page.find_element(By.CSS_SELECTOR, 'h1')
    assert title.text == 'КОНТРАКТЫ TASTYSTRIKE'
