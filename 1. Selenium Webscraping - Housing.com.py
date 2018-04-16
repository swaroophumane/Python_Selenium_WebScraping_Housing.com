from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pandas import DataFrame
import time

driver = webdriver.Chrome()
driver.get('https://housing.com/in/buy/search?f=eyJ2IjoyLCJiYXNlIjpbeyJ0eXBlIjoiUE9MWSIsInV1aWQiOiJiOTcyZjYwZGIyNGFhOWVjZDAxMyIsImxhYmVsIjoiRm9ydCJ9LHsidHlwZSI6IlBPTFkiLCJ1dWlkIjoiNDMwM2U4ZTM1Yjk2OWI4MjhhYjciLCJsYWJlbCI6IkNvbGFiYSJ9LHsidHlwZSI6IlBPTFkiLCJ1dWlkIjoiZDAzZWJmNjZiYWRhNGZiZDY3NWEiLCJsYWJlbCI6IkJhbmRyYSBXZXN0In1dLCJzIjoiZCIsInRpbWVTdGFtcCI6MTUyMDI4NjEzNjA5NCwidXNlckNpdHkiOiJhMGZkMzI4MTZmNzM5NjE3NDhjZiJ9')

iter = 1

lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    print(r"Page is Scrolling Down ...Wait({})".format(iter))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    iter += 1

    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight
print(r"Scroll Down Completed ....")
print('-----------------------------------------------------------')
print()

propertyName = []
propertyLocation = []
propertyAddedOn = []
propertyPrice = []
propertyAreaPerFeet = []
propertyAddress = []
propertyMoreInfo = []
propertyEMIAvailability = []
propertyAmenities = []
propertyAgentName = []
propertyAgentType = []

mypagesource = BeautifulSoup(driver.page_source, 'html5lib')

ActionChains(driver).send_keys(Keys.HOME).perform()
ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

try:
    allcards = mypagesource.findAll("div", {"class": "list-card-item"})
    print("Number of AllCards are {}".format(len(allcards)))

    element = driver.find_elements_by_class_name('list-card-item')

    print('The Count of Element is ',len(element))
    recordNumber = 1
    for i in element:
        i.location_once_scrolled_into_view
        actionitem = ActionChains(driver).move_to_element(i)
        time.sleep(2)
        actionitem.click()
        actionitem.perform()
        try:
            tempsource = BeautifulSoup(driver.page_source, 'html5lib')
            time.sleep(2)
            if tempsource.find('div', {'class': 'text'}).text == '100% Verified Listings':
                continue
            else:
                try:
                    print(r"Property Name :-",tempsource.find('div', {'class': 'text'}).text)
                    propertyName.append(tempsource.find('div', {'class': 'text'}).text)
                except:
                    print("No Property Name")
                    propertyName.append("No Property Name")
                try:
                    print(r"Added On/By :-",tempsource.find('div', {'class': 'added-on'}).text)
                    propertyAddedOn.append(tempsource.find('div', {'class': 'added-on'}).text)
                except:
                    print("No Added On Information")
                    propertyAddedOn.append("No Added On Information")
                try:
                    print(r"Price :-", (tempsource.find('div',{'class': 'price-with-unit'}).text).strip())
                    propertyPrice.append((tempsource.find('div', {'class': 'price-with-unit'}).text).strip())
                except:
                    print("No Price Given")
                    propertyPrice.append("No Price Given")
                try:
                    print(r"Area Per Square Feet :-", tempsource.find('span',{'class': 'formatted-price'}).text)
                    propertyAreaPerFeet.append(tempsource.find('span', {'class': 'formatted-price'}).text)
                except:
                    print("No Per Squre Feet")
                    propertyAreaPerFeet.append("No Per Squre Feet")
                try:
                    print(r"Address :-", (tempsource.find("div",{'class': 'landmark'}).select('span')[0]).text)
                    propertyAddress.append((tempsource.find("div", {'class': 'landmark'}).select('span')[0]).text)
                except:
                    print("No Address Provided")
                    propertyAddress.append("No Address Provided")

                if len(propertyLocation) == 0:
	                try:
	                	for i in tempsource.findAll("div",{"class":"lst-loct"}):
	                		propertyLocation.append((i.find('span').text))
	                except:
	                	propertyLocation.append("No Location Found")

                Moreinfo = tempsource.findAll('div', {'class': 'overview-point'})
                try:
                    b = []
                    for a in Moreinfo:
                        Name = (a.find('span', {'class': 'title'}).text).strip()
                        text = (a.find('span', {'class': 'text'}).text).strip()
                        c = ("(" + Name + text + ")")
                        b.append(c)
                    print("Moreinfo", ",".join(b))
                    propertyMoreInfo.append(",".join(b))
                except:
                    print("RERA Registered")
                    propertyMoreInfo.append("RERA Registered")
                try:
                    a = tempsource.find('div', {'class': 'emi-txt'}).text
                    if (len(a) > 0):
                        print(tempsource.find('div', {'class': 'emi-txt'}).text)
                        propertyEMIAvailability.append(tempsource.find('div', {'class': 'emi-txt'}).text)
                    else:
                        print("No-EMI-Option")
                        propertyEMIAvailability.append("No-EMI-Option")
                except:
                    print("No-EMI-Option")
                    propertyEMIAvailability.append("No-EMI-Option")

                try:
                    Amenities = tempsource.findAll('span', {'class': 'amenity-entity'})
                    AllAmenitiesList = []
                    if len(Amenities) > 0:
                        for a in Amenities:
                            AllAmenitiesList.append(a.find('span', {'class': 'text'}).text)
                        print("Amenities :-", ",".join(AllAmenitiesList))
                        propertyAmenities.append(",".join(AllAmenitiesList))
                    else:
                        print("No Amenities")
                        propertyAmenities.append("No Amenities")
                except:
                    print("No Amenities")
                    propertyAmenities.append("No Amenities")

                try:
                    print("Agent Name -", tempsource.find("div",{'class': 'prfl-name'}).text)
                    print("Agent Type -", tempsource.find("div",{'class': 'prfl-type'}).text)
                    propertyAgentName.append(tempsource.find("div", {'class': 'prfl-name'}).text)
                    propertyAgentType.append(tempsource.find("div", {'class': 'prfl-type'}).text)

                except:
                    print("No Agent Information")
                    propertyAgentName.append("No Agent Information")
                    propertyAgentType.append("No Agent Type Information")

                print(
                    "------------------------------------------ Record Number {}".format(recordNumber))
                recordNumber += 1
                time.sleep(2)   
        except:
            print("Selector not Found")
    time.sleep(2)
    propertyLocation.pop()
except:
    print('something Wrong Happened')
else:
    print("Excel File Writing Started.......")
    print("Length of Location", len(propertyLocation))
    print("Length of Name", len(propertyName))
    print("Length of added-on", len(propertyAddedOn))
    print("Length of price", len(propertyPrice))
    print("Length of Area", len(propertyAreaPerFeet))
    print("Length of Address", len(propertyAddress))
    print("Length of More info", len(propertyMoreInfo))
    print("Length of EMI", len(propertyEMIAvailability))
    print("Length of Amenities", len(propertyAmenities))
    print("Length of AgentName", len(propertyAgentName))
    print("Length of AgentType", len(propertyAgentType))
    df = DataFrame({'Property Name': propertyName, 'Property Location': propertyLocation, 'Property Added On': propertyAddedOn, 'Property Price': propertyPrice, 'Property Area': propertyAreaPerFeet,
                    'Property Address': propertyAddress, 'Property More Information/RERA': propertyMoreInfo, 'EMI Option': propertyEMIAvailability, 'Amenities': propertyAmenities, 'Agent Name': propertyAgentName, 'Agent Type': propertyAgentType})
    df = df[["Property Name", "Property Location", "Property Added On", "Property Price", "Property Area",
             "Property Address", "Property More Information/RERA", "EMI Option", "Amenities", "Agent Name", "Agent Type"]]
    df.to_excel('HousingDotComDataExtract.xlsx',sheet_name='Housing-Data', index=False)
    print("Excel File Writing Completed.......")
    print()
    print("Page Scraping is Done")
    driver.quit()
