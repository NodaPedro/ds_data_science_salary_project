import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def glassdor_scrapper(number_of_jobs):
    jobs = list()
    o = {}

    target_url = "https://www.glassdoor.com/Job/united-states-data-science-jobs-SRCH_IL.0,13_IN1_KO14,26.htm"

    driver = webdriver.Chrome()

    driver.get(target_url)

    driver.maximize_window()
    time.sleep(4)

    content = driver.page_source.encode('utf-8').strip()

    soup = BeautifulSoup(content, "html.parser")

    allJobsContainer = soup.find("ul", {"class": "JobsList_jobsList__lqjTr"})

    while len(allJobsContainer) < number_of_jobs:

        content = driver.page_source.encode('utf-8').strip()

        soup = BeautifulSoup(content, "html.parser")

        # Closing the pop-up sign-in box
        try:
            driver.find_element(By.CSS_SELECTOR, '#left-column > div.JobsList_wrapper__EyUF6 > div > button').click()
            time.sleep(2)
            try:
                driver.find_element(By.XPATH, "/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button").click()
            except NoSuchElementException or ElementClickInterceptedException:
                pass
        except:
            continue

    allJobsContainer = soup.find("ul", {"class": "JobsList_jobsList__lqjTr"})

    i=0
    for job in allJobsContainer:
        try:
            o["name_of_company"] = job.find("span", {"class": "EmployerProfile_compactEmployerName__LE242"}).text
        except:
            o["name_of_company"] = -1

        try:
            o["company_rating"] = job.find("div", {"class": "EmployerProfile_ratingContainer__ul0Ef"}).text
        except:
            o["company_rating"] = -1

        try:
            o["job_title"] = job.find("a", {"class": "JobCard_jobTitle___7I6y"}).text
        except:
            o["job_title"] = -1

        try:
            o["job_location"] = job.find("div", {"class": "JobCard_location__rCz3x"}).text
        except:
            o["job_location"] = -1

        try:
            o["job_salary"] = job.find("div", {"class": "JobCard_salaryEstimate__arV5J"}).text
        except:
            o["job_salary"] = -1

        try:
            o["job_description"] = job.find("div", {"class": "JobCard_jobDescriptionSnippet__yWW8q"}).text.split(
                'Skills:')[0].strip()
        except:
            o["job_description"] = -1

        try:
            o["job_skills"] = job.find("div", {"class": "JobCard_jobDescriptionSnippet__yWW8q"}).text.split(
                'Skills:')[1].strip()
        except:
            o["job_skills"] = -1

        try:
            button = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{i}'
                                                   ']/div/div/div[1]/div[1]/a[2]')
            driver.implicitly_wait(2)
            ActionChains(driver).move_to_element(button).click(button).perform()
            i += 1
            try:
                o["company_overview"] = driver.find_element(By.CLASS_NAME, 'JobDetails_companyOverviewGrid__3t6b4').text
            except:
                o["company_overview"] = -1
        except:
            o["company_overview"] = -1

        jobs.append(o)
        o = {}
        print(jobs)

        if len(jobs) >= number_of_jobs:
            break

    driver.close()

    return pd.DataFrame(jobs)


df = glassdor_scrapper(999)
df.to_csv('jobs_999.csv', index=True, encoding='utf-8')
