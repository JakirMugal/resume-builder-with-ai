import os
from scrapy import Selector
import json
import re
def get_details(text):
    pattern = r"^(.*?)\s+hiring\s+(.*?)\s+in\s+(.*?)\s+\|"
    match = re.search(pattern, text)
    assert match, "Not matched"
    company = match.group(1)
    position = match.group(2)
    location = match.group(3)
    return {
        'company':company,
        'position':position,
        'location':location
    }
def get_details_from_html(base_path):
    job_description_path = rf"{base_path}\job_description.json"
    html_path = rf"{base_path}\job_data"
    link_path_data = rf"{base_path}\link_path_data.json"
    with open(link_path_data,'r') as file:
        json_data = json.loads(file.read())
    meta={}

    for job_name,data in json_data.items():
        print(f'Processing {job_name}')
        if 'jobs/view' not in data['link']:
            continue
        file_path = os.path.join(html_path,data['path'])
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        selector = Selector(text = html_content)
        job_description = '\n'.join(selector.xpath('//div[contains(@class,"description")]//text()').getall())
        page_title = selector.xpath('//title/text()').get()
        assert page_title and job_description , "Data not found"
        meta[job_name] = {
            'path':data['path'],
            'link':data['link'],
            'description':job_description,
            **get_details(page_title)
        }

    with open(job_description_path,'w') as file:
        file.write(json.dumps(meta))
# base_path = r"E:\study\GitHub\RESUME-BUILDER-WITH-AI"
# get_details_from_html(base_path=base_path)




