from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from colabrun.common import utils, config, Requests
from colabrun.selenium import page
import time, shutil,requests,os
import multiprocessing

class Client():
    def __init__(self, id, email):
        self.id = id
        self.email = email.strip()
        self.root_path = utils.get_dir('auto_browser')
        self.cookie_load_folder = self.root_path + self.email
        self.driver = None
        self.cookie_cur_folder = self.cookie_load_folder
        self.mf_server=os.getenv("MF_SERVER", config.ServerAdress.MF_SERVER)
        self.colab_url=os.getenv("COLAB_URL", config.ServerAdress.COLAB_URL)
        self.timeout=int(os.getenv("CLIENT_TIMEOUT",config.Client.CLIENT_TIMEOUT))
        self.ff_root_folder=os.getenv("FF_ROOT_FOLDER", config.Client.FF_ROOT_FOLDER)
        self.ff_ext= os.getenv("FF_EXT", config.Client.FF_EXT)
        self.gecko_log=os.getenv("GECKO_LOG",config.Client.GECKO_LOG)
    def setup(self, ff_version="52"):

        firefox_binary = self.ff_root_folder + "FirefoxSetup"+ff_version+"/core/firefox"+self.ff_ext
        executable_path = self.ff_root_folder + "geckodriver_"+ff_version+self.ff_ext
        mail_server = os.getenv("MAIL_SERVER", config.ServerAdress.MAIL_SERVER)
        email_obj = requests.post(f"{mail_server}/automail/api/mail/get/",json={"gmail":self.email}).json()
        if "gmail" not in email_obj:
            return False
        self.pass_word = email_obj["pass_word"]
        self.reco_email = email_obj["recovery_email"]
        utils.load_cookie(self.cookie_load_folder, self.email)
        profile = webdriver.FirefoxProfile(self.cookie_load_folder)
        set_preference=profile.set_preference
        set_preference("dom.webdriver.enabled", False)
        set_preference("webdriver_enable_native_events", False)
        set_preference("webdriver_assume_untrusted_issuer", False)
        set_preference("media.peerconnection.enabled", False)
        set_preference("media.navigator.permission.disabled", False)
        self.driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=firefox_binary,
                                        executable_path=executable_path,service_log_path=self.gecko_log+"/gecko_log.log")
        self.cookie_cur_folder = self.driver.capabilities.get('moz:profile')
        return True

    def check_login(self):
        self.driver.get("https://www.youtube.com/upload")
        login_page = page.LoginPage(self.driver)
        #CookieMismatch
        if login_page.is_login():
            try:
                login_page.change_language()
            except:
                pass
            try:
                login_page.click_next_verify()
            except:
                pass
            try:
                login_page.click_profile_indentifier()
            except:
                pass
            try:
                login_page.email_login = self.email+Keys.RETURN
                time.sleep(3)
            except:
                pass
            try:
                login_page.pass_word_login = self.pass_word+Keys.RETURN
                time.sleep(3)
            except:
                pass
            try:
                login_page.click_cofirm_reco(self.reco_email)
            except:
                pass
            try:
                login_page.click_done_button()
            except:
                pass
            time.sleep(5)
            self.driver.get("https://www.youtube.com/upload")
            login_page = page.LoginPage(self.driver)
            if login_page.is_login():
                print("Login  Fail")
                return False
        return True

    def colab_set_client_id(self):
        #set client id
        try:
            self.driver.get(self.colab_url)
            time.sleep(5)
            action = ActionChains(self.driver)
            pp_input = self.driver.find_element_by_xpath("//paper-input[contains(@value,\"@@client_id\")]")
            action.move_to_element(pp_input)
            action.click(pp_input)
            action.send_keys(Keys.END)
            for _ in range(0, 15):
                action.send_keys(Keys.BACK_SPACE)
            action.send_keys('"'+str(self.id)+'"')
            action.perform()
        except:
            return False
            pass
        return True
    def check_is_disconnected(self):
        try:
            e = self.driver.find_element_by_xpath("//paper-dialog//h2[contains(text(),\"Runtime disconnected\")]")
            if e.is_displayed():
                return True
        except:
            pass
        return False
    def colab_keep_running(self):
        try:
            if "restart-1" in requests.get(self.mf_server +"/client/check-restart/"+str(self.id)).text:
                return False
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menu-button-caption\") and contains(text(),\"Help\")]").click()
            Requests.get(self.mf_server + "/client/ping/" + str(self.id) + "/1")
        except:
            pass
        return True
    def colab_keep_run_all(self):
        try:
            if "restart-1" in requests.get(self.mf_server + "/client/check-restart/" + str(self.id)).text:
                return False
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menu-button-caption\") and contains(text(),\"Runtime\")]").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menuitem-content\") and contains(text(),\"Run all\")]").click()
            time.sleep(3)
            self.driver.find_element_by_xpath("//paper-dialog//paper-button[@id=\"ok\"]").click()
        except:
            pass
        try:
            Requests.get(self.mf_server + "/client/ping/" + str(self.id) + "/1")
        except:
            pass
        return True

    def colab_start_and_wait(self):
        Requests.get(self.mf_server +"/client/type/"+str(self.id)+"/1")
        try:
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menu-button-caption\") and contains(text(),\"Runtime\")]").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menuitem-content\") and contains(text(),\"Factory reset runtime\")]").click()
            time.sleep(3)
            self.driver.find_element_by_xpath("//paper-dialog//paper-button[@id=\"ok\"]").click()
        except:
            pass
        time.sleep(5)
        try:
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menu-button-caption\") and contains(text(),\"Runtime\")]").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                "//div[contains(@class,\"goog-menuitem-content\") and contains(text(),\"Run all\")]").click()
            time.sleep(3)
            self.driver.find_element_by_xpath("//paper-dialog//paper-button[@id=\"ok\"]").click()
        except:
            pass
        while True:
            try:
                rs = requests.get(self.mf_server + "/client/type-check/" + str(self.id)).text
                if int(rs) == 3: #timeout
                    return False
                if int(rs) == 1:
                    return True
                time.sleep(30)
            except Exception as e:
                print(e)
                pass

    def log_error(self,code):
        try:
            Requests.get(self.mf_server  + "/client/error/" + str(self.id) + "/"+code)
        except:
            pass
    def restart(self):
        Requests.get(self.mf_server + "/client/setw/" + str(self.id)+"/3") #restart local
        self.close()
        self.cookie_load_folder = self.root_path + self.email
        self.driver = None

        self.cookie_cur_folder = self.cookie_load_folder
        self.execute()
    def execute(self):
        #load 52 ff
        try:
            next= True
            if not self.setup(ff_version="52"):
                self.log_error("1")
                next = False
                return
            if not self.check_login():
                self.log_error("2")
                next = False
            self.close()
            #load 68 ff
            if next:
                if not self.setup(ff_version="68"):
                    self.log_error("3")
                    return
                time.sleep(3)
                if not self.check_login():
                    self.log_error("4")
                    next = False
            if next:
                time.sleep(3)
                if not self.colab_set_client_id():
                    self.log_error("5")
                    next = False
            if next:
                time.sleep(3)
                if not self.colab_start_and_wait():
                    self.log_error("6")
                    next = False

            # while self.colab_keep_running():
            #     if self.check_is_disconnected():
            #         return self.restart()
            #     time.sleep(30)
            while self.colab_keep_run_all():
                time.sleep(60)

        except:
            pass
        self.close()


    def start(self):
        self.processx = multiprocessing.Process(target=self.execute)
        self.processx.start()

    def wait(self):
        self.processx.join(self.timeout)
        if self.processx.is_alive():
            self.processx.terminate()
            self.processx.join()

    def join(self):
        self.threadx.join()


    def close(self):
        if self.driver:
            try:
                utils.save_cookie(self.cookie_cur_folder, self.email)
            except:
                pass
            try:
                self.driver.close()
                self.driver.quit()
            except:
                pass
            try:
                shutil.rmtree(self.cookie_cur_folder)
            except:
                pass
            try:
                shutil.rmtree(self.cookie_load_folder)
            except:
                pass




