import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
rawdata = os.path.join('C:/Users/RDATS/Desktop/Projects/rawdata')
fullDetails = os.path.join('C:/Users/RDATS/Desktop/Projects/Data')
driver = webdriver.Chrome(executable_path=r"C:\\Users\\RDATS\\Desktop\\Projects\\driver\\chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(5)
keyword = open('keyword.txt')
files = keyword.readlines()
locations = open('Location.txt')
location = locations.readlines()
def yellowpages():
    for loc in location:
        for keyword in files:
            def GetDetailsOfItem(YPLink):
                driver.get(YPLink)
                try:
                    time.sleep(3)
                    Email = driver.find_element_by_css_selector('a[class="email-business"]').get_attribute('href').split(":")[1]
                    print(Email)
                except:
                    Email = ""
                    print(Email)
                return pd.Series([Email]) 

            driver.get("https://www.yellowpages.com/")
            time.sleep(3)
            driver.find_element_by_id("query").send_keys(keyword)
            time.sleep(2)
            driver.find_element_by_id("location").clear()
            time.sleep(2)
            driver.find_element_by_id("location").send_keys(loc)
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            driver.implicitly_wait(10)
            searchurl=driver.current_url    
            data=[]
            loopNoOfTime=True
            count=1
            while loopNoOfTime:
                driver.get(searchurl+'&page='+str(count))
                time.sleep(5)
                if driver.find_elements_by_class_name('result'):
                    print(len(driver.find_elements_by_class_name('result')))
                    count+=1
                    for prod in driver.find_elements_by_class_name('result'):
                        try:
                            CompanyName = prod.find_element_by_class_name('business-name').find_element_by_tag_name('span').text
                            print(CompanyName)
                        except:
                            CompanyName = ""
                        try:
                            Website = prod.find_element_by_class_name('track-visit-website').get_attribute('href')
                            print(Website)
                        except:
                            Website = " "
                        try:
                            YPLink = prod.find_element_by_class_name('business-name').get_attribute('href')
                            print(YPLink)
                        except:
                            YPLink = ""
                        try:
                            Phone = prod.find_element_by_css_selector("div[class='phones phone primary']").text
                            print(Phone)
                        except:
                            Phone = ""
                        try:
                            street = prod.find_element_by_class_name('street-address').text
                            locality = prod.find_element_by_class_name('locality').text
                            Location = street + locality
                            print(Location)
                        except:
                            try:
                                Location = prod.find_element_by_class_name('adr').text
                                print(Location)
                            except:
                                Location = ""
                                print(Location)
                        data.append([CompanyName, Website, Location, Phone, YPLink])
                else:
                    loopNoOfTime=False   
            if len(data)==0:
                driver.close()
            else:
                text = driver.find_element_by_xpath("//div[@class='search-term']/h1").text
                key1 = ''.join(text.split(' ')[:2])
                key2 = ''.join(text.split(' ')[-1:])
                keys = key1 + key2
                datadf = pd.DataFrame(data, columns=['CompanyName', 'Website', 'Location', 'Phone', 'YPLink'])
                datadf.to_csv(os.path.join(rawdata, 'YP_'+keys+'.csv'), index=False)
                if len(datadf) == 0:
                    driver.close()
                else:
                    datadf[['Email']] = datadf[['YPLink']].apply(lambda x: GetDetailsOfItem(x[0]), axis=1)
                    datadf = datadf[['Email', 'CompanyName', 'Website', 'Location', 'Phone', 'YPLink']]
                    datadf.to_csv(os.path.join(fullDetails, 'YellowPages'+keys+'.csv'), index=False)
       
yellowpages()
