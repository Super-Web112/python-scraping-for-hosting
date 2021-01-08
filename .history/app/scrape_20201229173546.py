from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from app.models import ItalianName, City
import csv
import os

@login_required(login_url="/login/")
def scrape_data(request):
    scrape_name = request.GET.get('scrape_name', None)
    start_id = request.GET.get('start_id', None)
    end_id = request.GET.get('end_id', None)
    option = webdriver.ChromeOptions()
    option.add_argument("window-size=1280,800")
    # option.add_argument("--headless")
    # Setup wait for later
    # wait = WebDriverWait(driver, 10)
    
    driver = ''
    url = ''
    id = int(start_id)
    while(id <= int(end_id)):
        csv_file = "csv_files/"+scrape_name+"_"+str(id)+".csv"
        if os.path.exists(csv_file):
            os.remove(csv_file)
        try:
            CLICK_NEXT_BUTTON = True
            CLICK_NEXT_BUTTON_NUM = 0;
            aaaaaaaaaa = 0
            while (CLICK_NEXT_BUTTON):
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
                driver.set_window_position(0, 0)
                # driver.set_window_size(0, 0)
                url = 'https://sfera.sferabit.com/servizi/alboonlineBoot/index.php?id='+str(id)
                driver.get(url)
                original_window = driver.current_window_handle
                # Check we don't have other windows open already
                assert len(driver.window_handles) == 1
                driver.switch_to.window(driver.window_handles[0])
                driver.implicitly_wait(10)
                name_input = driver.find_element(By.ID, 'filtroRagioneSociale')
                name_input.send_keys(scrape_name)
                # ActionChains(driver).move_to_element(name_input).key_up('Francesco', name_input).perform()
                # ActionChains(driver).move_to_element(name_input).send_keys(name_input, 'Francesco').perform()
                # ActionChains(driver).move_to_element(name_input).key_down(Keys.CONTROL).send_keys('Francesco').key_up(Keys.CONTROL).perform()
                send_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
                ActionChains(driver).move_to_element(send_button).click(send_button).perform()
                driver.implicitly_wait(10)
                
                if (CLICK_NEXT_BUTTON):
                    for i in range(CLICK_NEXT_BUTTON_NUM):
                        next_button = driver.find_elements(By.CSS_SELECTOR, '#risultatoRicerca a')[2]
                        ActionChains(driver).move_to_element(next_button).click(next_button).perform()
                        driver.implicitly_wait(10)
                
                pros_num_table = driver.find_element(By.CSS_SELECTOR, '#risultatoRicerca>table')
                pros_num_td = pros_num_table.find_elements(By.TAG_NAME, 'td')[1].get_attribute('innerHTML').strip().split(' ')
                pros_now_num = pros_num_td[0].strip()
                pros_total_num = pros_num_td[2].strip()
                print(pros_now_num)
                print(pros_total_num)
                if(pros_total_num in pros_now_num):
                    CLICK_NEXT_BUTTON = False
                else:
                    CLICK_NEXT_BUTTON = True
                    
                modal_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.buttonAnagrafica')

                for modal_button in modal_buttons:
                    ActionChains(driver).move_to_element(modal_button).click(modal_button).perform()
                    driver.implicitly_wait(30)
                    fonts = driver.find_elements(By.CSS_SELECTOR, '#modalPersona td')
                    address = name = birth = email = pec = tel = phone = ''
                    if(len(fonts) > 5):
                        use_nums = [2, 3, 5]
                        first_pros = []
                        result_pros = []
                        for use_num in use_nums:
                            first_pros.extend(fonts[use_num].get_attribute("innerHTML").strip().split("<br>"))
                        for first_pro in first_pros:
                            temp = first_pro.replace("&nbsp;", " ").strip()
                            temp1 = temp.lower()
                            temp_flag = ('foro di appartenenza' in temp1) or (('data' in temp1) and ('nascita' in temp1)) or ('email' in temp1) or ('pec' in temp1) or ('tel' in temp1) or ('cell' in temp1)
                            if(temp_flag):
                                result_pros.append(temp)
                        for result_pro in result_pros:
                            if(":" in result_pro):
                                rows = result_pro.split(":")
                                temp = rows[0].lower()
                                if("foro di appartenenza" in temp):
                                    address = rows[1].strip()
                                if("data" in temp):
                                    birth = rows[1].strip()
                                if("email" in temp):
                                    email = result_pro.split(">")[1].strip()[:-3]
                                if("pec" in temp):
                                    pec = result_pro.split(">")[1].strip()[:-3]
                                if("tel" in temp):
                                    tel = rows[1].strip()
                                if("cell" in temp):
                                    phone = rows[1].strip()
                        name = fonts[1].get_attribute("innerHTML").split("<b>")[1].strip().split("</b>")[0].strip()
                        print(address)
                        print(name)
                        print(birth)
                        print(email)
                        print(pec)
                        print(tel)
                        print(phone)
                        with open(csv_file, mode='a') as employee_file:
                            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            employee_writer.writerow([address, name, birth, email, pec, tel, phone])
                        aaaaaaaaaa = aaaaaaaaaa + 1
                        print(aaaaaaaaaa)
                        close_buttons = driver.find_element(By.CSS_SELECTOR, "button.btn-secondary")
                        driver.implicitly_wait(10)
                        ActionChains(driver).move_to_element(close_buttons).click(close_buttons).perform()
                        driver.implicitly_wait(10)
                CLICK_NEXT_BUTTON_NUM = CLICK_NEXT_BUTTON_NUM + 1
                print(CLICK_NEXT_BUTTON)
                print(CLICK_NEXT_BUTTON_NUM)
                driver.implicitly_wait(10)
                driver.quit()
        except:
            driver.quit()
            print("id="+str(id)+" is not support.")
            continue
        finally:
            # driver.implicitly_wait(10)
            # driver.quit()
            id = id + 1
            print(str(id))
        
    
    data = {
        'is_taken': 'sdfsdfsdfsdfsdf'
    }
    return JsonResponse(data)


@login_required(login_url="/login/")
def scrape_aaa(request):
    ItalianName.objects.all().delete()
    # username = request.GET.get('username', None)
    option = webdriver.ChromeOptions()
    option.add_argument("window-size=1280,800")
    # option.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    driver.set_window_position(0, 0)
    driver.get('https://www.nomix.it/nomi-italiani-maschili-e-femminili.php')
    urls = {'https://www.nomix.it/nomi-italiani-maschili-e-femminili.php', 'https://www.nomix.it/nomi-italiani-lettera-B.php', 'https://www.nomix.it/nomi-italiani-lettera-C.php', 'https://www.nomix.it/nomi-italiani-lettera-D.php', 'https://www.nomix.it/nomi-italiani-lettera-E.php', 'https://www.nomix.it/nomi-italiani-lettera-F.php', 'https://www.nomix.it/nomi-italiani-lettera-G.php', 'https://www.nomix.it/nomi-italiani-lettera-I.php', 'https://www.nomix.it/nomi-italiani-lettera-L.php', 'https://www.nomix.it/nomi-italiani-lettera-M.php', 'https://www.nomix.it/nomi-italiani-lettera-NO.php', 'https://www.nomix.it/nomi-italiani-lettera-PQ.php', 'https://www.nomix.it/nomi-italiani-lettera-R.php', 'https://www.nomix.it/nomi-italiani-lettera-S.php', 'https://www.nomix.it/nomi-italiani-lettera-TUV.php', 'https://www.nomix.it/nomi-italiani-lettera-WZ.php'}
    for url in urls:
        driver.get(url)
        driver.implicitly_wait(10)
        original_window = driver.current_window_handle
        # Check we don't have other windows open already
        assert len(driver.window_handles) == 1
        driver.switch_to.window(driver.window_handles[0])
        tables = driver.find_elements(By.TAG_NAME, 'table')
        male_tds = tables[2].find_elements(By.TAG_NAME, 'td')
        for male_td in male_tds:
            td_content = male_td.get_attribute('innerHTML')
            if('<div' not in td_content):
                if('strong' in td_content):
                    td_content = td_content.replace('&nbsp;', '')
                    td_content = td_content.replace('<strong>', '')
                    td_content = td_content.replace('</strong>', '').strip()
                else:
                    td_content = td_content.replace('&nbsp;', '')
                    td_content = td_content.strip()
                print(td_content)
                italy_name = ItalianName(names_col=td_content, gender_col='male')
                italy_name.save()
                # italy_name.names_col = td_content
                # italy_name.gender_col = 'male'
                # italy_name.save()
        male_tds = tables[3].find_elements(By.TAG_NAME, 'td')
        for male_td in male_tds:
            td_content = male_td.get_attribute('innerHTML')
            if('<div' not in td_content):
                if('strong' in td_content):
                    td_content = td_content.replace('&nbsp;', '')
                    td_content = td_content.replace('<strong>', '')
                    td_content = td_content.replace('</strong>', '').strip()
                else:
                    td_content = td_content.replace('&nbsp;', '')
                    td_content = td_content.strip()
                print(td_content)
                italy_name = ItalianName(names_col=td_content, gender_col='male')
                italy_name.save()
        driver.implicitly_wait(10)
    driver.quit()
    data = {
        'is_taken': 'sdfsdfsdfsdfsdf'
    }
    return JsonResponse(data)
@login_required(login_url="/login/")
def scrape_name(request):
    # username = request.GET.get('username', None)
    i = 1080
    driver = ''
    while(i<=1086):
        try:
            option = webdriver.ChromeOptions()
            option.add_argument("window-size=1280,800")
            # option.add_argument("--headless")
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
            driver.get('https://sfera.sferabit.com/servizi/alboonlineBoot/index.php?id='+str(i))
            original_window = driver.current_window_handle
            # Check we don't have other windows open already
            assert len(driver.window_handles) == 1
            driver.switch_to.window(driver.window_handles[0])

            name_input = driver.find_element(By.ID, 'filtroRagioneSociale')
            name_input.send_keys('an')
            send_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
            ActionChains(driver).move_to_element(send_button).click(send_button).perform()
            driver.implicitly_wait(10)
            td = driver.find_element(By.CSS_SELECTOR, '#risultatoRicerca>table.table tr>td:last-child').get_attribute('innerHTML')
            td = td.split(" ")[-2].strip()
            city = City(url_id=i, city_name=td)
            city.save()
        except:
            print(str(i)+" does not support")
        finally:
            i = i + 1
            driver.quit()
    data = {
        'is_taken': 'sdfsdfsdfsdfsdf'
    }
    return JsonResponse(data)