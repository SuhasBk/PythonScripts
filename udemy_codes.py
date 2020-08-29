#!/usr/local/bin/python3
import selenium
import sys
from time import sleep
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# specify course URL and download location here :
UDEMY_COURSE_URL = ""
DOWNLOAD_DIR = ""

# specify course section range to download resources; format : [begin, end)
# Examples: 
# If you want resources from sections 3 to 6 : begin = 3, end = 7
# If you want resources of section 10 only : begin = 10, end = 11
SECTION_BEGIN_INDEX = 0
SECTION_END_INDEX = None

# specifying auto download location for 'zip' files only... 'txt' files not included!
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", DOWNLOAD_DIR)

# change MIME type here if required:
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

# to hide browser window (usually not recommended):
# op = Options()
# op.headless = True
# browser = webdriver.Firefox(firefox_profile=fp,options=op,service_log_path="/dev/null")

browser = webdriver.Firefox(firefox_profile=fp, service_log_path="/dev/null")

def login(uname,pwd):
    browser.get(UDEMY_COURSE_URL)
    browser.find_element_by_class_name('c_header__right').find_element_by_tag_name('a').click()
    sleep(1)
    browser.find_element_by_id("email").send_keys(uname+Keys.ENTER)
    sleep(2)
    browser.find_element_by_id("password").send_keys(pwd+Keys.ENTER)
    sleep(5)
    try:
        browser.find_element_by_class_name('a2')
        return False
    except:
        return True

# wait for JS to load for 10 seconds:
def wait_and_find(element,selector,root=browser):
    try:
        WebDriverWait(browser,10).until(EC.element_to_be_clickable((selector,element)))
    except TimeoutException as e:
        print("Something is nasty",e,'\n',element)
    
    return root.find_elements(selector,element)

# handle 'click intercepted' cases:
def click(element):
    browser.execute_script("arguments[0].scrollIntoView();", element)
    element.click()

if __name__ == '__main__':
    if UDEMY_COURSE_URL == "":
        UDEMY_COURSE_URL = input("Enter the URL of the Udemy course:\n> ")
    
    if DOWNLOAD_DIR == "":
        DOWNLOAD_DIR = input("Enter the download directory path:\n> ")

    EMAIL = input("Enter the Udemy account email:\n> ")
    PASSWORD = getpass("\nEnter the password:\n> ")

    try:
        # login to udemy:
        log_count = 0
        logged_in = login(EMAIL, PASSWORD)
        while not logged_in and log_count!=3:
            print("Unable to login... trying again...")
            logged_in = login(EMAIL,PASSWORD)
            log_count+=1
        if not logged_in:
            browser.quit()
            sys.exit("Please check your credentials and try again!")
        else:
            print(f"\nLogged in successfully!\nDownloading zip files to {DOWNLOAD_DIR} directory...")

        # locate course sections on the right:
        side_panel_sections = wait_and_find("section--section--BukKG",By.CLASS_NAME)

        # download resources from specified section range:
        for section in side_panel_sections[SECTION_BEGIN_INDEX - 1 : SECTION_END_INDEX - 1]:
            # expand current section:
            try:
                section.find_element_by_class_name('udi-angle-down').click()
            except:
                pass
            
            # find resources in current section:
            resource_links = wait_and_find("resource-list-dropdown--resource-list-container--y1sNN",By.CLASS_NAME,section)

            for resource_link in resource_links:
                # find sub-resources in each video having resources:
                resources = resource_link.find_elements_by_tag_name('a')
                
                # download zipped source code and ignore other links to websites, txt etc. :
                for resource in resources:
                    # expand resource menu:
                    click(resource_link.find_element_by_tag_name('button'))
                    sleep(2)

                    # if auto clicking fails, handle ultimate control to user:
                    finished = False
                    while not finished:
                        try:
                            # click on a resource:
                            click(resource)
                            finished = True
                        except Exception as e:
                            print(e)
                            input("Click on the '"+resource.text+"' element and press 'Enter' here...")

                    # wait for download to finish or website link to load:
                    sleep(10)
                    
                    # if the resource was link to a website, close the newly opened window and give control back to udemy:
                    if len(browser.window_handles) > 1:
                        browser.switch_to.window(browser.window_handles.pop())
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])

            # acknowledge completion of section
            input(f"\nSection {side_panel_sections.index(section)} completed!\nTake a break or relocate the zip files from {DOWNLOAD_DIR}!\nI will wait till you are ready and press 'Enter' here...😉")
            section.find_element_by_class_name('udi-angle-up').click()
    finally:
        browser.quit()
        print("Thank you for using this software... May the Source be with you.🔥")
