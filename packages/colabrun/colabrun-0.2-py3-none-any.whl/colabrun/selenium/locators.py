from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    GO_BUTTON = (By.ID, 'submit')

class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass
class UploadPageLocators(object):
    INPUT= (By.XPATH,'//div[@id="upload-prompt-box"]//input')
    TITLE=(By.XPATH,'//ytcp-mention-textbox[contains(@class,"title-textarea")]//div[@id="textbox"]')
    DESCRIPTION=(By.XPATH,'//textarea[@name="description"]')
    TAG=(By.XPATH,'//input[@class="video-settings-add-tag"]')
    NOTIFY=(By.XPATH,'//div[contains(@class,"upload-item-alert")]/div[@class="yt-alert-content"]/div[@class="yt-alert-message"]')
    IS_ON_PUBLISH=(By.XPATH,'//div[@class="save-cancel-buttons"]/button[contains(.,"Publish") and not(@disabled)]')
    PUBLISH=(By.XPATH,'//div[@class="save-cancel-buttons"]/button[contains(.,"Publish")]')
    LANGUAGE_BUTTON=(By.ID,'yt-picker-language-button')
    LANGUAGE_ENGLISH_US=(By.XPATH,"//button[contains(.,\"English\")]")
    CUSTOM_THUMB_BUTTON = (By.XPATH, "//div[@class=\"custom-thumb-container\"]//button")
    CUSTOM_THUMB=(By.XPATH,"//div[@class=\"custom-thumb-container\"]//input")
    THUMB_AVAIL=(By.XPATH,'//div[contains(@class,"custom-thumb")]//img')
    VIDEO_LINK=(By.XPATH,"//div[@class=\"upload-item-sidebar-text\"]/div[@class=\"watch-page-link\"]/a")
    START_BUTTON_UPLOAD=(By.XPATH,'//div[@id="start-upload-button-single"]')
    RESTORE_BUTTON=(By.XPATH,'//button[@id="restoreTab"]')
    FAIL_UPLOAD_STRIKE=(By.XPATH,'//div[@id="active-uploads-containbutton"]//div[contains(.,"cannot upload")]')
class LoginPageLocators(object):
    LANG_CHOOSE_BUTTON=(By.XPATH,"//div[@id=\"lang-chooser\"]")
    LANG_IT = (By.XPATH, "//*[@id=\"lang-chooser\"]/div[2]/div[@data-value=\"it\"]")
    LANG_EN = (By.XPATH, "//*[@id=\"lang-chooser\"]/div[2]/div[@data-value=\"en\"]")
    EMAIL_LOGIN=(By.ID,"identifierId")
    PASS_WORD_LOGIN=(By.NAME,"password")
    RECO_EMAIL_BUTTON = (By.XPATH, "//form//div[contains(text(),\"Confirm your recovery email\")]")
    EMAIL_RECO=(By.ID,"knowledge-preregistered-email-response")
    EMAIL_RECO2= (By.ID, "identifierId")
    PROFILE_INDENTIFIER = (By.XPATH,"//div[@id=\"profileIdentifier\" and contains(@data-email,\"@\")]")
    VERIFY_NEXT = (By.ID, "identifierNext")
    DONE_BUTTON=(By.XPATH,"//div[@role=\"button\" and contains(text(),\"Done\")]")
class EditPageLocators(object):
    PUBLISH_BUTTON=(By.XPATH, "//button[contains(@class,\"vm-video-publish\") and @data-video-id]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class,\"save-changes-button\")]")
class WatchPageLocators(object):
    SUBS_BUTTON=(By.XPATH,"//div[@id=\"subscribe-button\"]//yt-formatted-string[text()=\"Subscribe\"]");
class AboutMeLocators(object):
    FIRST_NAME=(By.XPATH,"//input[@aria-label=\"First\"]")
    LAST_NAME = (By.XPATH, "//input[@aria-label=\"Last\"]")
    SUR_NAME=(By.XPATH, "//input[@aria-label=\"Surname\"]")
    FULL_NAME=(By.XPATH, "//input[@aria-label=\"Name\"]")

    FIRST_NAME_ROLE = (By.XPATH, "(//*[@role=\"dialog\"]//input)[1]")
    LAST_NAME_ROLE = (By.XPATH, "(//*[@role=\"dialog\"]//input)[2]")

    OK_BUTTON=(By.XPATH,"(//*[@role=\"dialog\"]//div[@role=\"button\"])[4]")
    CONFIRM_BUTTON=(By.XPATH,"(//*[@role=\"dialog\"]//div[@role=\"button\"])[4]")