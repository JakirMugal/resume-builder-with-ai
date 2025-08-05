
import selenium.webdriver as wd
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.common.action_chains import ActionChains
import json
from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import shutil



def scrape_and_upload(base_path, url,number_of_jobs=2):
    # svc = wd.ChromeService(executable_path=binary_path)
    # options = wd.ChromeOptions()
    # options.add_argument("--headless=new") 
    # driver = wd.Chrome(service=svc,options=options)
    chrome_path = shutil.which("chromium")  # find chromium in the system
    driver_path = shutil.which("chromedriver")  # find chromedriver in the system

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    actions = ActionChains(driver)
    actions.move_by_offset(50, 50).click().perform()
    urls_ele = driver.find_elements(By.XPATH,'//a[contains(@class,"full-link")]')
    urls = [url.get_attribute('href') for url in urls_ele]
    time.sleep(10)
    html_path = rf"{base_path}\job_data"
    meta_path = rf"{base_path}\link_path_data.json"

    os.makedirs(html_path, exist_ok=True)
    meta={}
    if len(url)<=number_of_jobs:
        filtered_urls=urls
    else:
        filtered_urls = urls[:number_of_jobs]
    for num,url in enumerate(filtered_urls):
        if 'jobs/view' not in url:
            continue
        print(f"{num} Process location url : {url}")
        filename = url.split('?')[0].split('/')[-1]+'.html'
        full_path = os.path.join(html_path, filename)
        meta[filename]={'path':full_path,'link':url}
        if os.path.exists(full_path):
            print(f"{filename} already present.....")
            continue
        driver.get(url)
        time.sleep(15)
        content=driver.page_source
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
    with open(meta_path,'w') as file:
        file.write(json.dumps(meta))
    driver.quit()
# url = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&f_E=3&f_TPR=&f_WT=2&position=1&pageNum=0"
# base_path = r"E:\study\GitHub\RESUME-BUILDER-WITH-AI"
# scrape_and_upload(url=url,base_path=base_path)



