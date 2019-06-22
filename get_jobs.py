import os
import re
import sys
import time
import json
import pprint
from selenium import webdriver
from datetime import datetime
from pymongo import MongoClient

# REPLACE With your LinkedIn Credentials
USERNAME = ""
PASSWORD = ""

def mongodb_init():
    client=MongoClient('mongodb://34.73.180.107:27017')
    db=client.smartcareer
    return db

def mongodb_get_collection(db,item):
    col=db[item]
    return col

def mongodb_put_doc(doc):
    db=mongodb_init()
    col=mongodb_get_collection(db,'jobdescription')

    try:
        re=col.insert_one(doc)
        ret=re.inserted_id
    except:
        ret=doc['JobID']
          
    return ret

def clean_item(item):
    item = item.replace('\n', ' ')
    item = item.strip()
    return item


def generate_scrape_url(scrape_url):
    title = input("Enter job title: ")
    print('\nSelect period from the given options. Type 1, 2, 3 or 4 and press ENTER')
    print('1. Past 24 Hours')
    print('2. Past Week')
    print('3. Past Month')
    print('4. Anytime')
    period = '1'
    uname = 'bsong7003@gmail.com'
    passwd = 'Belsong0!'

#    period = input("Period: ")
#    uname = input("Username: ")
#    passwd = input("Password: ")

    while not period.isnumeric() or not 0 < int(period) < 5:
        print('\nERROR: Invalid Input. Try again.')
        period = input("Period: ")

    scrape_url += title
    if period == '1':
        scrape_url += '&f_TPR=r86400'
    elif period == '2':
        scrape_url += '&f_TPR=r604800'
    elif period == '3':
        scrape_url += '&f_TPR=r2592000'

    scrape_url += '&location=United States'

    valid_title_name = title.strip().replace(' ', '_')
    valid_title_name = re.sub(r'(?u)[^-\w.]', '', valid_title_name)
    output_filename = valid_title_name + '_' + datetime.today().strftime("%Y%m%d") + '.json'

    return scrape_url, output_filename, uname, passwd


if "__main__":
    chrome_driver = os.getcwd() + "/chromedriver.exe"
    base_url = "https://www.linkedin.com/jobs/search?keywords="
    sign_in_url = "https://www.linkedin.com/uas/login?fromSignIn=true"
    main_obj = {}
    all_jobs = []
    job_postings = []
    page = 1

    job_search_url, filename, USERNAME, PASSWORD = generate_scrape_url(base_url)

    print('\nSTATUS: Opening website')
    browser = webdriver.Chrome(chrome_driver)
    browser.get(sign_in_url)
    time.sleep(1)

    print('STATUS: Signing in')
    browser.find_element_by_id('username').send_keys(USERNAME)
    time.sleep(1)

    browser.find_element_by_id('password').send_keys(PASSWORD)
    time.sleep(1)

    browser.find_element_by_class_name('login__form_action_container ').click()
    time.sleep(1)

    print('STATUS: Searching for jobs\n')
    browser.get(job_search_url)
    jobs = browser.find_elements_by_class_name('result-card__full-card-link')

    if len(jobs) == 0:
        jobs = browser.find_elements_by_class_name('jobs-search-result-item')

        if len(jobs) == 0:
            jobs = browser.find_elements_by_xpath(
                    "//li[@class='occludable-update artdeco-list__item p0 ember-view']")
            if len(jobs) == 0:
                print('STATUS: No jobs found. Press any key to exit scraper')
                browser.quit()
                exit = input('')
                sys.exit(0)

    all_jobs = jobs

    while True:
        print('STATUS: Scraping Page ' + str(page))
        index = 0
        while index < len(jobs):
            obj = {}
            job = jobs[index]

            job.click()
            time.sleep(2)

            current_url = browser.current_url
            job_id = current_url[current_url.find('currentJobId=') + 13: current_url.find('currentJobId=') + 23]
            obj['JobID'] = job_id

            job_div = None
            while True:
 
                try:
                    job_div = browser.find_element_by_xpath("//div[@class='job-view-layout jobs-details ember-view']")
                    break
                except:
                    time.sleep(1)
                    browser.execute_script("window.history.go(-1)")


            try:
                job_title = clean_item(job_div.find_element_by_xpath("//h1[@class='jobs-details-top-card__job-title t-20 t-black t-normal']").text)
                obj['Job Title'] = job_title
            except:
                obj['Job Title'] = ''

            try:
                company = clean_item(job_div.find_element_by_xpath("//a[@class='jobs-details-top-card__company-url ember-view']").text)
                obj['Company'] = company
            except:
                obj['Company'] = ''

            try:
                location = clean_item(job.find_element_by_tag_name('h5').text)
                obj['Location'] = location
            except:
                obj['Location'] = ''

            try:
                description = clean_item(job_div.find_element_by_xpath("//div[@class='display-flex justify-space-between mb1']/following-sibling::span").text)
                obj['Description'] = description
            except:
                obj['Description'] = ''

            other_fields_list = job_div.find_element_by_id('job-details').find_elements_by_class_name('jobs-box__group')

            for list_item in other_fields_list:
                field_name = list_item.find_element_by_tag_name('h3').text
                field_text = list_item.text.replace(field_name, '')

                field_name = clean_item(field_name)
                field_text = clean_item(field_text)

                obj[field_name] = field_text

            doc_id=mongodb_put_doc(obj)
            print('post id: ', doc_id)
 #           job_postings.append(obj)
 #           main_obj['postings'] = job_postings

 #           with open(filename, 'w', encoding='utf-8') as outfile:
 #               json.dump(job_postings, outfile, indent=2, ensure_ascii=False)

            jobs = browser.find_elements_by_xpath("//li[@class='occludable-update artdeco-list__item p0 ember-view']")
            index += 1

        next_page = job_search_url + '&start=' + str(page*25)
        browser.get(next_page)
        page += 1
        time.sleep(5)
        jobs = browser.find_elements_by_xpath("//li[@class='occludable-update artdeco-list__item p0 ember-view']")

        if len(jobs) == 0:
            break

    print('\nSTATUS: Scraping complete. Check output file for scraped data')
    print('STATUS: Press any key to exit scraper')
    browser.quit()
    exit = input('')
    sys.exit(0)


