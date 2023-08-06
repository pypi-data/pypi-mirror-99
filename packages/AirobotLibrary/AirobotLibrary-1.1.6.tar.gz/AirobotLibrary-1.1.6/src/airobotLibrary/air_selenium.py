import os
import sys
import time
import allure
from selenium import webdriver
from robotlibcore import PY2
from robot.libraries.BuiltIn import RobotNotRunningError
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      FrameKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords,
                                      WindowKeywords)
from airtest import aircv
from airtest_selenium.proxy import Element, WebChrome, WebFirefox, WebRemote, WebElement
from airtest.core.helper import logwrap
from airtest.core.settings import Settings as ST
from airtest.core.cv import Template
from airtest_selenium.utils.airtest_api import loop_find
from typing import Optional, Union, Any

if not hasattr(ST, 'REMOTE_URL'): ST.REMOTE_URL = None
if not hasattr(ST, 'BROWSER'): ST.BROWSER = 'Chrome'

class AirSelenium(
    AlertKeywords,
    BrowserManagementKeywords,
    CookieKeywords,
    ElementKeywords,
    FormElementKeywords,
    FrameKeywords,
    JavaScriptKeywords,
    RunOnFailureKeywords,
    ScreenshotKeywords,
    SelectElementKeywords,
    TableElementKeywords,
    WaitingKeywords,
    WindowKeywords):
    
    def __init__(self, screenshot_root_directory='logs', remote_url=ST.REMOTE_URL, browser=ST.BROWSER, headless=False, alias=None, device=None, executable_path=None, options=None, service_args=None, desired_capabilities=None):
        """
        启动浏览器类型可选: Firefox, Chrome, Ie, Opera, Safari, PhantomJS, 可模拟移动设备
        """
        if browser not in ['Firefox', 'Chrome', 'Ie', 'Opera', 'Safari', 'PhantomJS']:
            raise Exception('浏览器类型不对, 仅可选: Firefox, Chrome, Ie, Opera, Safari, PhantomJS')
        self.remote_url = remote_url
        self.browser = browser
        self.headless = headless
        self.alias = alias 
        self.device = device
        self.executable_path = executable_path
        self.options = options
        self.service_args = service_args
        self.desired_capabilities = desired_capabilities

        self.ctx = SeleniumLibrary(screenshot_root_directory=screenshot_root_directory)
        self.screenshot_directory = ST.LOG_DIR = self.ctx.screenshot_root_directory
        super(AirSelenium, self).__init__(self.ctx)

    @logwrap
    @allure.step
    def open_browser(
        self,
        url: Optional[str] = None,
        browser: str = "Chrome",
        alias: Optional[str] = None,
        remote_url: Union[bool, str] = False,
        headless: Optional[bool] = False,
        options: Any = None,
        device: Optional[str] = None,
        executable_path: Optional[str] = None,
        service_args: Union[dict, None, str] = None,
        desired_capabilities: Union[dict, None, str] = None) -> str:
        """
        启动浏览器类型可选: Firefox, Chrome, Ie, Opera, Safari, PhantomJS, 可模拟移动设备
        """
        if browser not in ['Firefox', 'Chrome', 'Ie', 'Opera', 'Safari', 'PhantomJS']:
            raise Exception('浏览器类型不对, 仅可选: Firefox, Chrome, Ie, Opera, Safari, PhantomJS')
                
        remote_url = remote_url or self.remote_url
        browser = browser or self.browser
        headless = headless or self.headless
        alias  = alias or self.alias
        device = device or self.device
        executable_path = executable_path or self.executable_path
        options or self.options
        service_args = service_args or self.service_args
        desired_capabilities = desired_capabilities or self.desired_capabilities

        if remote_url:
            if browser == 'Chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-setuid-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')        
                if headless:
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--disable-gpu')
                if device:
                    mobile_emulation = {'deviceName': device}
                    chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
                browser_options = chrome_options
            elif browser == 'Firefox':
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument('--disable-dev-shm-usage')        
                if headless:
                    firefox_options.add_argument('--headless')
                    firefox_options.add_argument('--disable-gpu')
                browser_options = firefox_options
            else:
                browser_options = options
            desired_capabilities = desired_capabilities or {}
            desired_capabilities['browserName'] = browser.lower()
            driver = WebRemote(command_executor=remote_url, desired_capabilities=desired_capabilities, options=options or browser_options)
            # ctx.create_webdriver(driver_name='Remote', alias=alias, command_executor=remote_url, options=options, desired_capabilities=desired_capabilities)
        elif browser == 'Chrome': 
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            if headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            if device:
                mobile_emulation = {'deviceName': device}
                chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
            if executable_path:
                driver = WebChrome(executable_path=executable_path, options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, executable_path=executable_path, options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
            else:
                driver = WebChrome(options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
        elif browser == 'Firefox':
            firefox_options = webdriver.FirefoxOptions()
            if headless:
                firefox_options.add_argument('--headless')
                firefox_options.add_argument('--disable-gpu')
            if executable_path:
                driver = WebFirefox(executable_path=executable_path, options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, executable_path=executable_path, options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
            else:
                driver = WebFirefox(options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
        else:
            if executable_path:
                self.create_webdriver(driver_name=browser, alias=alias, executable_path=executable_path, service_args=service_args, desired_capabilities=desired_capabilities)
            else:
                self.create_webdriver(driver_name=browser, alias=alias, service_args=service_args, desired_capabilities=desired_capabilities)
            driver = self.driver
        index = self.ctx.register_driver(driver=driver, alias=alias)
        if url: self.go_to(url)
        return index

    @logwrap
    @allure.step
    def close_browser(self):
        return super(AirSelenium, self).close_browser()
        
    @logwrap
    @allure.step
    def close_all_browsers(self):
        return super(AirSelenium, self).close_all_browsers()

    @logwrap
    @allure.step
    def switch_browser(self, index_or_alias: str):
        return super(AirSelenium, self).switch_browser(index_or_alias)
        
    @logwrap
    @allure.step
    def switch_window(self, locator: Union[list, str] = "MAIN", timeout: Optional[str] = None, browser: str = 'CURRENT'):
        return super(AirSelenium, self).switch_window(locator=locator, timeout=timeout, browser=browser)
        
    @logwrap
    @allure.step
    def set_window_size(self, width: int, height: int, inner: bool = False):
        return super(AirSelenium, self).set_window_size(width, height, inner=inner)

    @logwrap
    @allure.step
    def choose_file(self, locator: Union[WebElement, str], file_path: str):
        return super(AirSelenium, self).choose_file(locator, file_path)

    @logwrap
    @allure.step
    def go_back(self):
        return super(AirSelenium, self).go_back()
    
    @logwrap
    @allure.step
    def press_key(self, locator: Union[WebElement, str], key: str):
        return super(AirSelenium, self).press_key(locator, key)
        
    @logwrap
    @allure.step
    def press_keys(self, locator: Union[WebElement, None, str] = None, *keys: str):
        return super(AirSelenium, self).press_keys(locator=locator, *keys)

    @logwrap
    @allure.step
    def select_checkbox(self, locator: Union[WebElement, str]):
        return super(AirSelenium, self).select_checkbox(locator)

    @logwrap
    @allure.step
    def select_radio_button(self, group_name: str, value: str):
        return super(AirSelenium, self).select_radio_button(group_name, value)
        
    @logwrap
    @allure.step
    def scroll_element_into_view(self, locator: Union[WebElement, str]):
        return super(AirSelenium, self).scroll_element_into_view(locator)
        
    @logwrap
    @allure.step
    def unselect_checkbox(self, locator: Union[WebElement, str]):
        return super(AirSelenium, self).unselect_checkbox(locator)
        
    @logwrap
    @allure.step
    def unselect_all_from_list(self, locator: Union[WebElement, str]):
        return super(AirSelenium, self).unselect_all_from_list(locator)

    @logwrap
    def find_element(self, locator, tag=None, required=True, parent=None):
        web_element = super(AirSelenium, self).find_element(locator=locator, tag=tag, required=required, parent=parent)
        log_res=self._gen_screen_log(web_element)
        return web_element and Element(web_element, log_res)
    
    @logwrap
    @allure.step
    def air_click(self, v):
        """
        Perform the click action on the current page by image identification.

        Args:
            v: target to click, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be clicked.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).click().perform()
        time.sleep(1)
        return _pos

    @logwrap
    @allure.step
    def air_assert(self, v, msg=""):
        """
        Assert target exists on the current page.

        Args:
            v: target to touch, either a Template instance
        Raise:
            AssertionError - if target not found.
        Returns:
            Position of the template.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        return self.driver.assert_template(v=v, msg=msg)

    @logwrap
    @allure.step
    def air_double_click(self, v):
        """
        Perform the double click action on the current page by image identification.

        Args:
            v: target to double click, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be double clicked.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).double_click().perform()
        time.sleep(1)
        return _pos

    @logwrap
    @allure.step
    def air_context_click(self, v):
        """
        Perform the right click action on the current page by image identification.

        Args:
            v: target to right click, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be right clicked.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).context_click().perform()
        time.sleep(1)
        return _pos

    @logwrap
    @allure.step
    def air_mouse_up(self, v):
        """
        Perform the mouse up action on the current page by image identification.

        Args:
            v: target to mouse up, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be mouse up.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).release().perform()
        time.sleep(1)
        return _pos
    
    @logwrap
    @allure.step
    def air_mouse_down(self, v):
        """
        Perform the mouse down action on the current page by image identification.

        Args:
            v: target to mouse down, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be mouse down.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).click_and_hold().perform()
        time.sleep(1)
        return _pos

    @logwrap
    @allure.step
    def air_mouse_over(self, v):
        """
        Perform the mouse over action on the current page by image identification.

        Args:
            v: target to mouse over, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be mouse over.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).perform()
        time.sleep(1)
        return _pos

    @logwrap
    @allure.step
    def air_mouse_out(self, v):
        """
        Perform the mouse out action on the current page by image identification.

        Args:
            v: target to mouse out, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be mouse out.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(v, Template):
            _pos = loop_find(v, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos = v
        x, y = _pos
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x, y).move_by_offset(0, 0).perform()
        time.sleep(1)
        return _pos

    @logwrap
    @allure.step
    def air_drag_and_drop(self, s, t):
        """
        Perform the drag and drop action on the current page by image identification.

        Args:
            v: target to drag and drop, either a Template instance or absolute coordinates (x, y)
        Returns:
            Finial position to be drag and drop.
        """
        if not isinstance(self.driver, (WebChrome, WebFirefox, WebRemote)):
            raise AssertionError('Use this function, the driver is must be WebChrome, WebFirefox or WebRemote')
        if isinstance(s, Template):
            _pos_s = loop_find(s, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos_s = s
        x_s, y_s = _pos_s
        if isinstance(t, Template):
            _pos_t = loop_find(t, timeout=ST.FIND_TIMEOUT, driver=self.driver)
        else:
            _pos_t = t
        x_t, y_t = _pos_t
        # pos = self.driver._get_left_up_offset()
        # pos = (pos[0] + x, pos[1] + y)
        self.driver.action_chains.move_by_offset(x_s, y_s).click_and_hold().move_by_offset(x_t, y_t).release().perform()
        time.sleep(1)
        return _pos_s, _pos_t

    @logwrap
    @allure.step
    def click_element(self, locator, modifier=False, action_chain=False):
        super(AirSelenium, self).click_element(locator=locator, modifier=modifier, action_chain=action_chain)

    @logwrap
    @allure.step
    def click_link(self, locator, modifier=False):
        super(AirSelenium, self).click_link(locator=locator, modifier=modifier)

    @logwrap
    @allure.step
    def click_image(self, locator, modifier=False):
        super(AirSelenium, self).click_image(locator=locator, modifier=modifier)

    @logwrap
    @allure.step
    def click_button(self, locator, modifier=False):
        super(AirSelenium, self).click_button(locator=locator, modifier=modifier)

    @logwrap
    @allure.step
    def input_text(self, locator, text, clear=True):
        super(AirSelenium, self).input_text(locator=locator, text=text, clear=clear)

    @logwrap
    @allure.step
    def input_password(self, locator, password, clear=True):
        super(AirSelenium, self).input_password(locator=locator, password=password, clear=clear)

    @logwrap
    @allure.step
    def double_click_element(self, locator):
        super(AirSelenium, self).double_click_element(locator=locator)

    @logwrap
    @allure.step
    def page_should_contain(self, text, loglevel='TRACE'):
        super(AirSelenium, self).page_should_contain(text=text, loglevel=loglevel)

    @logwrap
    @allure.step
    def page_should_not_contain(self, text, loglevel='TRACE'):
        super(AirSelenium, self).page_should_not_contain(text=text, loglevel=loglevel)

    @logwrap
    @allure.step
    def open_context_menu(self, locator):
        super(AirSelenium, self).open_context_menu(locator=locator)

    @logwrap
    @allure.step
    def mouse_up(self, locator):
        super(AirSelenium, self).mouse_up(locator=locator)
    
    @logwrap
    @allure.step
    def mouse_down(self, locator):
        super(AirSelenium, self).mouse_down(locator=locator)

    @logwrap
    @allure.step
    def mouse_over(self, locator):
        super(AirSelenium, self).mouse_over(locator=locator)

    @logwrap
    @allure.step
    def mouse_out(self, locator):
        super(AirSelenium, self).mouse_out(locator=locator)

    @logwrap
    @allure.step
    def drag_and_drop(self, locator, target):
        super(AirSelenium, self).drag_and_drop(locator=locator, target=target)

    @logwrap
    @allure.step
    def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
        super(AirSelenium, self).drag_and_drop_by_offset(locator=locator, xoffset=xoffset, yoffset=yoffset)

    @logwrap
    @allure.step
    def go_to(self, url):
        super(AirSelenium, self).go_to(url=url)

    def screenshot(self, file_path=None):
        if file_path:
            file = self.capture_page_screenshot(file_path)
            with open(file, 'rb') as fp:
                allure.attach(fp.read(), '截图{}'.format(file_path), allure.attachment_type.PNG)
        else:
            if not self.screenshot_directory:
                file_path = "temp.png"
            else:
                file_path = os.path.join('', "temp.png")
            file = self.capture_page_screenshot(file_path)
            with open(file, 'rb') as fp:
                allure.attach(fp.read(), '截图{}'.format(file_path), allure.attachment_type.PNG)
            screen = aircv.imread(file_path)
            return screen

    def _gen_screen_log(self, element=None, filename=None,):
        if self.screenshot_directory is None:
            return None
        if filename:
            self.screenshot(filename)
        jpg_file_name=str(int(time.time())) + '.png'
        jpg_path=os.path.join('', jpg_file_name)
        # print("this is jpg path:", jpg_path)
        self.screenshot(jpg_path)
        saved={"screen": jpg_file_name}
        if element:
            size=element.size
            location=element.location
            x=size['width'] / 2 + location['x']
            y=size['height'] / 2 + location['y']
            if "darwin" in sys.platform:
                x, y=x * 2, y * 2
            saved.update({"pos": [[x, y]]})
        return saved

    @property
    def log_dir(self):
        try:
            if os.path.isdir(self.screenshot_directory):
                return os.path.abspath(self.screenshot_directory)
            else:
                os.makedirs(self.screenshot_directory)
                return os.path.abspath(self.screenshot_directory)
        except RobotNotRunningError:
            return os.getcwd() if PY2 else os.getcwd()
