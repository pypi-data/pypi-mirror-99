from colabrun.selenium.elements import BasePageElement
from colabrun.selenium.locators import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from colabrun.common.config import ImageResource
from random import randint
import random
from selenium.webdriver.common.keys import Keys
class UploadElement(BasePageElement):
    locator=UploadPageLocators.INPUT
    is_find_hide=True
class TitleUploadElement(BasePageElement):
    locator=UploadPageLocators.TITLE
class DescriptionUploadElement(BasePageElement):
    locator = UploadPageLocators.DESCRIPTION
class TagUploadElement(BasePageElement):
    locator = UploadPageLocators.TAG
class ThumbnailUploadElement(BasePageElement):
    locator = UploadPageLocators.CUSTOM_THUMB
    is_find_hide = True
class VideoLinkUploadElement(BasePageElement):
    locator = UploadPageLocators.VIDEO_LINK
class EmailLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_LOGIN
class PassWordLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.PASS_WORD_LOGIN
class EmailRecoElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_RECO

class EmailRecoElement2(BasePageElement):
    delay = 5
    locator = LoginPageLocators.EMAIL_RECO2
class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""
    def __init__(self, driver):
        self.driver = driver

class UploadPage(BasePage):
    upload_path_element=UploadElement()
    title=TitleUploadElement()
    description=DescriptionUploadElement()
    tag=TagUploadElement()
    thumb=ThumbnailUploadElement()
    video_link=VideoLinkUploadElement()
    def check_language(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON))
        if "English" in self.driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON).text:
            print("Ok English")
        else:
            print("change language")
            self.driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON).click()
            time.sleep(1)
            self.driver.find_element(*UploadPageLocators.LANGUAGE_ENGLISH_US).click()
            time.sleep(3)
    def is_custom_thumb(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(UploadPageLocators.CUSTOM_THUMB_BUTTON))
            return True;
        except Exception as e:
            print(e)
        return False;
    def wait_custom_thumb_avail(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(UploadPageLocators.THUMB_AVAIL))
            return True;
        except Exception as e:
            print(e)
        return False;

    def wait_title_input_avail(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(UploadPageLocators.TITLE))
            return True;
        except Exception as e:
            print(e)
        return False;
    def is_upload_page(self):
        print("check is_upload_page: " + self.driver.current_url)
        return "youtube.com/upload" in self.driver.current_url
    def is_avail_upload(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(UploadPageLocators.START_BUTTON_UPLOAD))
            self.driver.find_element(*UploadPageLocators.START_BUTTON_UPLOAD)
            return True
        except Exception as e:
            print(e)
        return False;
    def click_random_position(self):
        buttons={0:ImageResource.ICON_PUBLIC,1:ImageResource.UPLOAD_BUTTON}
        res=buttons.get(randint(0,1))
        time_click=randint(1,3)
        print(res)
        pos = (100,100)
        print(pos)
        #click_image(res, pos, "left", time_click)

    def publish_no_crash(self):
        try:
            WebDriverWait(self.driver, 1000).until(
                lambda driver: 'Click' in driver.find_element(*UploadPageLocators.NOTIFY).text)
        except:
            pass
        try:
            time.sleep(random.randrange(20)+5)
            WebDriverWait(self.driver, 1000).until(
                EC.element_to_be_clickable(UploadPageLocators.PUBLISH))
            self.driver.find_element(*UploadPageLocators.PUBLISH).click()
        except:
            pass
    def is_cannot_upload_strike(self):
        try:
            self.driver.find_element(*UploadPageLocators.FAIL_UPLOAD_STRIKE)  # check Strike
            return True
        except:
            pass
        return False
    def publish(self):
        #publish check crash
        count=0;
        while count < 1000:
            try:
                if 'Click' in self.driver.find_element(*UploadPageLocators.NOTIFY).text:
                    break
            except:
                pass
            try:
                self.driver.find_element(*UploadPageLocators.RESTORE_BUTTON) #check crash
                return False
            except:
                pass
            try:
                self.driver.find_element(*UploadPageLocators.FAIL_UPLOAD_STRIKE) #check Strike
                return False
            except:
                pass
            count+=1
            time.sleep(1)
        try:
            time.sleep(random.randrange(20)+5)
            WebDriverWait(self.driver, 1000).until(
                EC.element_to_be_clickable(UploadPageLocators.PUBLISH))
            self.driver.find_element(*UploadPageLocators.PUBLISH).click()
        except:
            pass
        return True



class WatchPage(BasePage):
    def subscribe(self):
        try:
            self.driver.find_element(*WatchPageLocators.SUBS_BUTTON).click()
        except:
            pass
class EditPage(BasePage):
    def publish(self):
        try:
            video_id = self.driver.find_element(*EditPageLocators.PUBLISH_BUTTON).get_attribute("data-video-id")
            self.driver.get("https://www.youtube.com/edit?o=U&video_id="+video_id)
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *UploadPageLocators.TITLE))
            if  "hbt2" not in self.driver.find_element(*UploadPageLocators.TITLE).text:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.find_element(
                        *EditPageLocators.SAVE_BUTTON))
                self.driver.find_element(*EditPageLocators.SAVE_BUTTON).click()
                time.sleep(5)
        except:
            pass

class LoginPage(BasePage):
    email_login=EmailLoginElement()
    pass_word_login=PassWordLoginElement()
    email_reco_login=EmailRecoElement()
    email_reco_login2=EmailRecoElement2()
    def is_login(self):
        return "accounts.google.com" in self.driver.current_url
    def is_en_lang(self):
        return "English" in self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).text
    def click_cofirm_reco(self,email_reco):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *LoginPageLocators.RECO_EMAIL_BUTTON))
            self.driver.find_element(*LoginPageLocators.RECO_EMAIL_BUTTON).click()
        except:
            pass
        try:
            self.email_reco_login2=email_reco+Keys.RETURN
        except:
            pass
        try:
            self.email_reco_login=email_reco+Keys.RETURN
        except:
            pass
    def click_next_verify(self):
        self.driver.find_element(*LoginPageLocators.VERIFY_NEXT).click()
        time.sleep(2)
    def click_profile_indentifier(self):
        self.driver.find_element(*LoginPageLocators.PROFILE_INDENTIFIER).click()
        time.sleep(2)
    def change_language(self):
        if self.is_en_lang():
            return
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *LoginPageLocators.LANG_CHOOSE_BUTTON))
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_IT).click()
        time.sleep(2)
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_EN).click()
        time.sleep(2)
    def click_done_button(self):
        self.driver.find_element(*LoginPageLocators.DONE_BUTTON).click()
        time.sleep(2)


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source


class AboutMePage(BasePage):
    def fill_text(self, element, text):
        element = self.driver.find_element(*element)
        element.clear()
        element.send_keys(text)
    def change_name(self, full_name):
        first_name=full_name.split(" ")[0]
        last_name=full_name.split(" ")[1]
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME,first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.SUR_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FULL_NAME, full_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME_ROLE, first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME_ROLE, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.driver.find_element(AboutMeLocators.OK_BUTTON).click()
            time.sleep(3)
            self.driver.find_element(AboutMeLocators.CONFIRM_BUTTON).click()
        except:
            pass