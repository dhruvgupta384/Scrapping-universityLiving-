
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import webdriver_manager
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import json
import pymongo
from bson import json_util
#Conenct mongodb
mongo_uri = "mongodb+srv://dhruvGupta:1234@cluster0.ij2fd.mongodb.net/"
myclient = pymongo.MongoClient(mongo_uri)
mydb = myclient['chapterkings']
mycol = mydb['propertyData']


def parse_json(data):
    return json.loads(json_util.dumps(data))

# Set up Selenium options to run headless
chrome_options = Options()
# chrome_options.add_argument('--headless')

# Initialize the WebDriver/Users/satyam/Downloads/amazonExtractionUsingSelenium.py
# driver = webdriver.Chrome(options=chrome_options)

# Open the URL
url = "https://www.chapter-living.com/booking/"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(5)
where = driver.find_element(By.XPATH,"//*[@id='BookingAvailabilityForm_Residence']")
where.send_keys("CHAPTER KINGS CROSS")
time.sleep(3)
when = driver.find_element(By.XPATH,"//*[@id='BookingAvailabilityForm_BookingPeriod']") 
when.send_keys('SEP 24 - AUG 25 (51 WEEKS)')


time.sleep(4)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='filter-room-type-ensuite']"))).click()
time.sleep(3)
dic_={}
property_name = driver.find_element(By.XPATH,"//*[@id='modal-room-1']/div[4]/div/p[1]").text
print("reached")
suite_name = driver.find_element(By.XPATH,"//*[@id='modal-room-1']/div[4]/div/p[2]/strong").text
per_week_price = driver.find_element(By.XPATH,"//*[@id='modal-room-1']/div[4]/div/p[3]").text

driver.find_element(By.XPATH,"//*[@id='modal-room-1']/div[4]/div/div[2]/a").click()
time.sleep(4)
#enter login credentials
email = driver.find_element(By.XPATH,"//*[@id='login_username']")
email.clear()
email.send_keys("satyampandey921@gmail.com")

password = driver.find_element(By.XPATH,"//*[@id='login_password']")
password.clear()
password.send_keys("Satyam@921")

driver.find_element(By.XPATH,"//*[@id='oa_login_submit']").click()
time.sleep(5)
driver.find_element(By.XPATH,"//*[@id='app-status-block-18518434']/a").click()
time.sleep(6)

driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div/div[2]/div[2]/a").click()
time.sleep(5)
# li_ = driver.find_elements(By.XPATH,"//*[@id='unit-details-section']")

# loop over units
all_unit=[]
for i in range(1,6):
   print(i)
   unit ={ "unit" : driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div["+str(i)+"]/div[1]/h6").text,
    "rent" : driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div["+str(i)+"]/div[1]/div[2]/dd").text,
    "deposit" : driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div["+str(i)+"]/div[1]/div[3]/dd").text,
    "aminities" : driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div["+str(i)+"]/div[1]/div[3]/dd").text,
   "i":i
   }
   table = driver.find_elements(By.XPATH,"//*[@id='unit-details-section']/div/div["+str(i)+"]/div[2]/div[1]/table/tbody/tr")
  
   #loop over spaces
   spacelist = []
   
   for j in range(1,len(table)+1):
      print("table",j)
      try:
         #select space   
         driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div[1]/div[2]/div[1]/table/tbody/tr["+str(j)+"]/td[1]/input").click()
         #select installment
         driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div[1]/div[2]/div[2]/ul/li["+str(j)+"]/input").click()
         #click continue button
        
         driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div["+str(j)+"]/div[2]/div[2]/a").click()
         time.sleep(7)
         driver.execute_script("window.scrollBy(0,3000)","")
         time.sleep(5)
         try:
            print("text",driver.find_element(By.XPATH,"//*[@id='rental-options']/div/div[1]/div[1]/span[1]").text)
         except Exception as e:
            print("this is error",e)
         
         try:
            spaceAndunit = driver.find_element(By.XPATH,"//*[@id='selection-overview']/div/div[2]/div/span[2]").text
            print("space",spaceAndunit)
         except Exception as e:
            print("this is error2",e)   

         totalAmount =  driver.find_element(By.XPATH,"//*[@id='rental-options']/div/ul/li[2]/div[2]/span").text
         print("total",totalAmount)
         spacedata={"spaceAndunit":spaceAndunit,
                  "totalAmount" :totalAmount }
         
         spacelist.append(spacedata)
         print(spacelist,len(spacelist))
         

         
         time.sleep(5)  
         driver.find_element(By.XPATH,"//*[@id='app_step_4']/span").click()
         time.sleep(10)
         driver.find_element(By.XPATH,"//*[@id='unit-details-section']/div/div/div[2]/div[2]/a").click()
         time.sleep(5)
      except:
          pass   
      
   unit["space"] = spacelist
   print(unit)
   unit["propertyName"] = property_name
   unit["suiteName"] = suite_name
   unit["perWeekPrice"] =per_week_price
   mycol.insert_one(parse_json(unit))   


with open("output.json","a+") as file:
   json.dump(all_unit,file)
time.sleep(3)      

