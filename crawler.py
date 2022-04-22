# --------------------------- #
# Crawler for MajSoul website #
# --------------------------- #
'''
This python file records the crawler for the dataset.
A selenium-based crawler was used in order to tackle
dynamic rendering of the data on the MajSoul website.
'''

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

# Path to Chromedriver
PATH = "/Users/enjuichang/chromedriver"
driver = webdriver.Chrome(PATH)

# Input URL
# URLs = ["https://amae-koromo.sapk.ch/player/73362382/16.12.9.11.8"]
URLs = ["https://amae-koromo.sapk.ch/player/73495327/16"]

# Stroage
rank_ls = []
score_ls = []
datetime_ls = []

# Handling multiple URLs (Could crawl muliple users if needed)    
for j in range(len(URLs)):

    # Get URL
    driver.get(URLs[j])
    time.sleep(1)

    # Set up body element for scrolling
    elem = driver.find_element_by_tag_name("body")

    # Get numeber of entry to set limit of scrolling
    num_entry = int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='MuiBox-root css-1u3q4k3']/div/p"))).text)
    counter = 1

    # Main loop 
    while counter <= num_entry:

        # Xpath for the time, rank, and score of the user given row
        xpath_datetime = f"//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div[@aria-rowindex='{counter}']/div[@aria-colindex='4']"
        xpath_rank = f"//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div[@aria-rowindex ='{counter}']/div[@aria-colindex='2']"
        xpath_score = f"//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div[@aria-rowindex ='{counter}']//span[@class='MuiTypography-root MuiTypography-body2 css-57o7bk']/a|//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div[@aria-rowindex ='{counter}']//span[@class='MuiTypography-root MuiTypography-body2 css-6adruz']/a"
                    
        # Check if row is rendered
        try:
            # Crawl the data
            datetime = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_datetime)))
            rank = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_rank)))
            score = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_score)))

            # Post-process the score text with regular expression
            modified_score = re.compile(r'\[.?\d+\]').findall(score[0].text)[0][1:-1]

            # Append data
            datetime_ls.append(datetime[0].text)
            rank_ls.append(int(rank[0].text))
            score_ls.append(int(modified_score))

            print("row:", counter)

            # Swtich to next row
            counter += 1

        # Handle exception when row is not rendered
        except:

            # first get the current last row
            last_elem_index = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div")))[-1].get_attribute('aria-rowindex')
            # Assign condition
            new_elem_index = last_elem_index

            # Scroll until a new row is rendered
            while last_elem_index==new_elem_index:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                new_elem_index = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div")))[-1].get_attribute('aria-rowindex')
            
            # Crawl the data
            datetime = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_datetime)))
            rank = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_rank)))
            score = WebDriverWait(driver,2).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_score)))

            # Post-process the score text with regular expression
            modified_score = re.compile(r'\[.?\d+\]').findall(score[0].text)[0][1:-1]

            # Append data
            datetime_ls.append(datetime[0].text)
            rank_ls.append(int(rank[0].text))
            score_ls.append(int(modified_score))

            print("row:", counter)

            # Switch to  next row
            counter += 1
    
# Quit scraper
driver.quit()

# Save to CSV
outputDF = pd.DataFrame({"time": datetime_ls, "rank":rank_ls, "score": score_ls})
outputDF.to_csv("./dataset_2.csv")
