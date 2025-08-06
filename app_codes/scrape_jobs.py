import requests
from scrapy import Selector
import os
import json
import time
def scrape_and_upload(base_path, url,number_of_jobs=2):
    response = requests.get(url)
    response = Selector(text=response.text)
    urls = response.xpath('//a[contains(@class,"full-link")]/@href').getall()
    time.sleep(1)
    html_path = os.path.join(base_path, "job_data")
    meta_path = os.path.join(base_path, "link_path_data.json")

    os.makedirs(html_path, exist_ok=True)
    meta={}
    if len(url)<=number_of_jobs:
        filtered_urls=urls
    else:
        filtered_urls = urls[:number_of_jobs]
    for num,url in enumerate(filtered_urls):
        if 'jobs/view' not in url:
            continue
        filename = url.split('?')[0].split('/')[-1]+'.html'
        full_path = os.path.join(html_path, filename)
        meta[filename]={'path':full_path,'link':url}
        if os.path.exists(full_path):
            print(f"{filename} already present.....")
            continue
        time.sleep(1)
        response = requests.get(url)
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
    with open(meta_path,'w') as file:
        file.write(json.dumps(meta))
    return {"html_path":html_path,"json_path":meta_path}
# url = "https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=India&geoId=102713980&f_E=3&f_TPR=&f_WT=2&position=1&pageNum=0"
# base_path = r"E:\study\GitHub\RESUME-BUILDER-WITH-AI/test2"
# scrape_and_upload(url=url,base_path=base_path)
