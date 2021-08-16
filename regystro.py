import time
from selenium import webdriver
from bs4 import BeautifulSoup
import hashlib 

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
browser = webdriver.Firefox(options=options, executable_path = '/usr/bin/geckodriver')
browser.set_window_size(1920, 1080)
browser.get('https://scuolaonline.soluzione-web.it/<YOUR CODE>/login.aspx')



browser.find_element_by_id("LoginPrincipale_UserName").send_keys('<YOUR USERNAME>')
browser.find_element_by_id("LoginPrincipale_Password").send_keys('<YOUR PASSWORD>')
browser.find_element_by_id("LoginPrincipale_LoginButton").click()
time.sleep(5)

html = browser.page_source
if 'alunni' in html:
    print("You're logged in!")
else:
    print("Logging in failed. Perhaps, it was attempted with invalid credentials")

browser.get('https://scuolaonline.soluzione-web.it/<YOUR CODE>/VotiQuotidiani_Voti/List.aspx')
el = browser.find_element_by_id('ContentPlaceHolder1_DropDownListClassi')
for option in el.find_elements_by_tag_name('option'):
    print(option.text)
    if option.text == 'I3^INF':
    # if option.text == 'B2^B':
        option.click()
        break
time.sleep(1)

el = browser.find_element_by_id('ContentPlaceHolder1_DropDownListMateriePerRuolo')
for option in el.find_elements_by_tag_name('option'):
    print(option.text)
    if option.text == 'Tutte':
        option.click()
        break
time.sleep(1)

el = browser.find_element_by_id('ContentPlaceHolder1_ctl01_3_DropDownListPersonaleScolastico_3')
for option in el.find_elements_by_tag_name('option'):
    print(option.text)
    if option.text == 'Tutti':
        option.click()
        break
time.sleep(1)

el = browser.find_element_by_id('ContentPlaceHolder1_ctl01_0_DropDownListBoolean_0')
for option in el.find_elements_by_tag_name('option'):
    print(option.text)
    if option.text == 'Sì':
        option.click()
        break
time.sleep(1)

browser.find_element_by_id("ContentPlaceHolder1_TextBoxDataDa").clear()
time.sleep(1)

browser.find_element_by_id("ContentPlaceHolder1_TextBoxDataDa").send_keys('01/09/2020')
time.sleep(1)

browser.find_element_by_id("ContentPlaceHolder1_TextBoxDataA").clear()
time.sleep(1)

browser.find_element_by_id("ContentPlaceHolder1_TextBoxDataA").send_keys('31/10/2020')
time.sleep(1)

browser.find_element_by_id("ContentPlaceHolder1_ButtonCerca").click()
time.sleep(1)


el = browser.find_element_by_id('ContentPlaceHolder1_GridViewPagerOutSide1_DropDownListPageSize')
for option in el.find_elements_by_tag_name('option'):
    print(option.text)
    if option.text == '200':
        option.click()
        break

html_from_page = browser.page_source
soup = BeautifulSoup(html_from_page, 'html.parser')
# print(soup.prettify())
# browser.quit()


####################################
# from bs4 import BeautifulSoup
# html = open('dumpvoti.html', 'r').read()
# soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())



# for table in soup.find('table', {'class':'noBorder'}):
for table in soup.find_all('table'):
    # print(table['class'])
    if table['class'][0] != 'grid':
        # print("removing")
        table.extract()
# print(soup.prettify())


data = []
table = soup.find_all('table')[0]
table_body = table.find('tbody')

rows = table_body.find_all('tr')
print(type(rows))


for idx, row in enumerate(rows):
    print(idx)
    if idx > 0 and idx < len(rows) - 1:
        tds = row.find_all('td')
        print(tds[2].text.strip()) #data
        print(tds[3].find('a', {'class': 'nomeAlunno'}).text.strip()) #Alunno
        print(tds[4].find('a', {'class': 'aspNetDisabled'}).text.strip()) #materia
        print(tds[5].find('a', {'class': 'aspNetDisabled'}).text.strip()) # professore
        print(tds[6].text.strip())  #modalità
        print(tds[7].find('a', {'class': 'infoVoto'}).find('span').text.strip()) #voto
        id_string = tds[2].text.strip() + \
            tds[3].find('a', {'class': 'nomeAlunno'}).text.strip() + \
            tds[4].find('a', {'class': 'aspNetDisabled'}).text.strip() + \
            tds[5].find('a', {'class': 'aspNetDisabled'}).text.strip() + \
            tds[6].text.strip() +  \
            tds[7].find('a', {'class': 'infoVoto'}).find('span').text.strip()
        print(id_string)
        hash_object = hashlib.md5(id_string.encode())
        md5_hash = hash_object.hexdigest()
        print(md5_hash)

        # for tdx, td in enumerate(tds):
        #     print(tdx, td)
        



# for row in rows:
#     print('#####################')
#     print(row)
#     cols = row.find_all('td')
#     cols = [ele.text.strip() for ele in cols]
#     data.append([ele for ele in cols if ele]) # Get rid of empty values
