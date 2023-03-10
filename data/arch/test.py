import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from csv import writer

#This version scrapes endlessly, without any loop and manually finds the next page, clicks on it, and continues to scrape.

#The time bot should wait before scrape
timeout = 5

#Basics
url = 'https://www.rossmann.pl/promocje?Page='
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
#options.headless = False
browser = webdriver.Firefox(executable_path=r'C:\usr\local\bin\geckodriver.exe', options = options)
        # browser.maximize_window()
browser.get(url)

#Exporting to CSV function
def AddToCSV(List):
    with open("Output.csv", "a+", newline='') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerow(List)

# Accepting the cookies
#button = browser.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
#button.click()

time.sleep(3)

#The main program:
while True:
    try:
        #All the links
        elements = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="row inspirations"]/div/div[@class="tile-product"]/a[@class="tile-product__name"]')))
        for element in elements:
            #Get href
            href = element.get_attribute('href')
            print(href)
            #Open new window with specific href
            browser.execute_script("window.open('" +href +"');")
            #Switch to new window
            browser.switch_to.window(browser.window_handles[1])

            #Scraped details
            Name = WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, 'h1'))).text
            Old_Price = browser.find_element(By.XPATH, value='//span[@class="regular"]').text
            New_Price = browser.find_element(By.XPATH, value='//span[@class="promo"]').text
            

            #Pushing to CSV
            row_list = [Name, Old_Price, New_Price]
            AddToCSV(row_list)

            #Close the new window
            browser.close()
            #Back to main window
            browser.switch_to.window(browser.window_handles[0])

        #Scrolling down to end of page so it can click on the next page button
            element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="pages align-items-center center "]')))
            browser.execute_script("arguments[0].scrollIntoView(false);", element)
            time.sleep(5)
        #Next Page button click
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="pages align-items-center center "]/a[3]'))).click()
        time.sleep(3)
    except:
        break

browser.quit()
