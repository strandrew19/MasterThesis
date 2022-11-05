from io import StringIO, BytesIO
import os
import re
from time import sleep
import random
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import pandas as pd
import platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib
from time import sleep
import random
import json
import dotenv
import os
from pathlib import Path

from typing import Optional, Sequence

current_dir = Path(__file__).parent.absolute()


env_file = os.getenv("SCWEET_ENV_FILE", current_dir.parent.joinpath(".env"))
dotenv.load_dotenv(env_file, verbose=True)


def load_env_variable(key, default_value=None, none_allowed=False):
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed!")
    return v


def get_email(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("SCWEET_EMAIL", none_allowed=True)


def get_password(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("SCWEET_PASSWORD", none_allowed=True)


def get_username(env):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable("SCWEET_USERNAME", none_allowed=True)


class WebDriverException(Exception):
    """
    Base webdriver exception.
    """

    def __init__(self, msg: Optional[str] = None, screen: Optional[str] = None, stacktrace: Optional[Sequence[str]] = None) -> None:
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self) -> str:
        exception_msg = "Message: %s\n" % self.msg
        if self.screen:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class InvalidSwitchToTargetException(WebDriverException):
    """
    Thrown when frame or window target to be switched doesn't exist.
    """
    pass


class NoSuchFrameException(InvalidSwitchToTargetException):
    """
    Thrown when frame target to be switched doesn't exist.
    """
    pass


class NoSuchWindowException(InvalidSwitchToTargetException):
    """
    Thrown when window target to be switched doesn't exist.

    To find the current set of active window handles, you can get a list
    of the active window handles in the following way::

        print driver.window_handles

    """
    pass


class NoSuchElementException(WebDriverException):
    """
    Thrown when element could not be found.

    If you encounter this exception, you may want to check the following:
        * Check your selector used in your find_by...
        * Element may not yet be on the screen at the time of the find operation,
          (webpage is still loading) see selenium.webdriver.support.wait.WebDriverWait()
          for how to write a wait wrapper to wait for an element to appear.
    """
    pass


class NoSuchAttributeException(WebDriverException):
    """
    Thrown when the attribute of element could not be found.

    You may want to check if the attribute exists in the particular browser you are
    testing against.  Some browsers may have different property names for the same
    property.  (IE8's .innerText vs. Firefox .textContent)
    """
    pass


class NoSuchShadowRootException(WebDriverException):
    """
    Thrown when trying to access the shadow root of an element when it does not
    have a shadow root attached.
    """
    pass


class StaleElementReferenceException(WebDriverException):
    """
    Thrown when a reference to an element is now "stale".

    Stale means the element no longer appears on the DOM of the page.


    Possible causes of StaleElementReferenceException include, but not limited to:
        * You are no longer on the same page, or the page may have refreshed since the element
          was located.
        * The element may have been removed and re-added to the screen, since it was located.
          Such as an element being relocated.
          This can happen typically with a javascript framework when values are updated and the
          node is rebuilt.
        * Element may have been inside an iframe or another context which was refreshed.
    """
    pass


class InvalidElementStateException(WebDriverException):
    """
    Thrown when a command could not be completed because the element is in an invalid state.

    This can be caused by attempting to clear an element that isn't both editable and resettable.
    """
    pass


class UnexpectedAlertPresentException(WebDriverException):
    """
    Thrown when an unexpected alert has appeared.

    Usually raised when  an unexpected modal is blocking the webdriver from executing
    commands.
    """

    def __init__(self, msg: Optional[str] = None, screen: Optional[str] = None, stacktrace: Optional[Sequence[str]] = None, alert_text: Optional[str] = None) -> None:
        super().__init__(msg, screen, stacktrace)
        self.alert_text = alert_text

    def __str__(self) -> str:
        return f"Alert Text: {self.alert_text}\n{super().__str__()}"


class NoAlertPresentException(WebDriverException):
    """
    Thrown when switching to no presented alert.

    This can be caused by calling an operation on the Alert() class when an alert is
    not yet on the screen.
    """
    pass


class ElementNotVisibleException(InvalidElementStateException):
    """
    Thrown when an element is present on the DOM, but
    it is not visible, and so is not able to be interacted with.

    Most commonly encountered when trying to click or read text
    of an element that is hidden from view.
    """
    pass


class ElementNotInteractableException(InvalidElementStateException):
    """
    Thrown when an element is present in the DOM but interactions
    with that element will hit another element due to paint order
    """
    pass


class ElementNotSelectableException(InvalidElementStateException):
    """
    Thrown when trying to select an unselectable element.

    For example, selecting a 'script' element.
    """
    pass


class InvalidCookieDomainException(WebDriverException):
    """
    Thrown when attempting to add a cookie under a different domain
    than the current URL.
    """
    pass


class UnableToSetCookieException(WebDriverException):
    """
    Thrown when a driver fails to set a cookie.
    """
    pass


class RemoteDriverServerException(WebDriverException):
    """
    """
    pass


class TimeoutException(WebDriverException):
    """
    Thrown when a command does not complete in enough time.
    """
    pass


class MoveTargetOutOfBoundsException(WebDriverException):
    """
    Thrown when the target provided to the `ActionsChains` move()
    method is invalid, i.e. out of document.
    """
    pass


class UnexpectedTagNameException(WebDriverException):
    """
    Thrown when a support class did not get an expected web element.
    """
    pass


class InvalidSelectorException(WebDriverException):
    """
    Thrown when the selector which is used to find an element does not return
    a WebElement. Currently this only happens when the selector is an xpath
    expression and it is either syntactically invalid (i.e. it is not a
    xpath expression) or the expression does not select WebElements
    (e.g. "count(//input)").
    """
    pass


class ImeNotAvailableException(WebDriverException):
    """
    Thrown when IME support is not available. This exception is thrown for every IME-related
    method call if IME support is not available on the machine.
    """
    pass


class ImeActivationFailedException(WebDriverException):
    """
    Thrown when activating an IME engine has failed.
    """
    pass


class InvalidArgumentException(WebDriverException):
    """
    The arguments passed to a command are either invalid or malformed.
    """
    pass


class JavascriptException(WebDriverException):
    """
    An error occurred while executing JavaScript supplied by the user.
    """
    pass


class NoSuchCookieException(WebDriverException):
    """
    No cookie matching the given path name was found amongst the associated cookies of the
    current browsing context's active document.
    """
    pass


class ScreenshotException(WebDriverException):
    """
    A screen capture was made impossible.
    """
    pass


class ElementClickInterceptedException(WebDriverException):
    """
    The Element Click command could not be completed because the element receiving the events
    is obscuring the element that was requested to be clicked.
    """
    pass


class InsecureCertificateException(WebDriverException):
    """
    Navigation caused the user agent to hit a certificate warning, which is usually the result
    of an expired or invalid TLS certificate.
    """
    pass


class InvalidCoordinatesException(WebDriverException):
    """
    The coordinates provided to an interaction's operation are invalid.
    """
    pass


class InvalidSessionIdException(WebDriverException):
    """
    Occurs if the given session id is not in the list of active sessions, meaning the session
    either does not exist or that it's not active.
    """
    pass


class SessionNotCreatedException(WebDriverException):
    """
    A new session could not be created.
    """
    pass


class UnknownMethodException(WebDriverException):
    """
    The requested command matched a known URL but did not match any methods for that URL.
    """
    pass


def log_in(driver, env, timeout=20, wait=4):
    email = get_email(env)  # const.EMAIL
    password = get_password(env)  # const.PASSWORD
    username = get_username(env)  # const.USERNAME

    driver.get('https://twitter.com/i/flow/login')

    email_xpath = '//input[@autocomplete="username"]'
    password_xpath = '//input[@autocomplete="current-password"]'
    username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'

    sleep(random.uniform(wait, wait + 1))

    # enter email
    email_el = driver.find_element("xpath",email_xpath)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(email)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))
    # in case twitter spotted unusual login activity : enter your username
    if check_exists_by_xpath(username_xpath, driver):
        username_el = driver.find_element("xpath",username_xpath)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(username)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(Keys.RETURN)
        sleep(random.uniform(wait, wait + 1))
    # enter password
    password_el = driver.find_element("xpath",password_xpath)
    password_el.send_keys(password)
    sleep(random.uniform(wait, wait + 1))
    password_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))

def check_exists_by_xpath(xpath, driver):
    timeout = 3
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    return True

def get_data(card, save_images=False, save_dir=None):
    """Extract data from tweet card"""
    image_links = []

    try:
        username = card.find_element("xpath",'.//span').text
    except:
        return

    try:
        handle = card.find_element("xpath",'.//span[contains(text(), "@")]').text
    except:
        return

    try:
        postdate = card.find_element("xpath",'.//time').get_attribute('datetime')
    except:
        return

    try:
        text = card.find_element("xpath",'.//div[2]/div[2]/div[1]').text
    except:
        text = ""

    try:
        embedded = card.find_element("xpath",'.//div[2]/div[2]/div[2]').text
    except:
        embedded = ""

    # text = comment + embedded

    try:
        reply_cnt = card.find_element("xpath",'.//div[@data-testid="reply"]').text
    except:
        reply_cnt = 0

    try:
        retweet_cnt = card.find_element("xpath",'.//div[@data-testid="retweet"]').text
    except:
        retweet_cnt = 0

    try:
        like_cnt = card.find_element("xpath",'.//div[@data-testid="like"]').text
    except:
        like_cnt = 0

    try:
        elements = card.find_elements("xpath",'.//div[2]/div[2]//img[contains(@src, "https://pbs.twimg.com/")]')
        for element in elements:
            image_links.append(element.get_attribute('src'))
    except:
        image_links = []

    # if save_images == True:
    #	for image_url in image_links:
    #		save_image(image_url, image_url, save_dir)
    # handle promoted tweets

    try:
        promoted = card.find_element("xpath",'.//div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = False
    if promoted:
        return

    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements("xpath",'.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)

    # tweet url
    try:
        element = card.find_element("xpath",'.//a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        return

    tweet = (
        username, handle, postdate, text, embedded, emojis, reply_cnt, retweet_cnt, like_cnt, image_links, tweet_url)
    return tweet


def init_driver(headless=True, proxy=None, show_images=False, option=None):
    """ initiate a chromedriver instance 
        --option : other option to add (str)
    """

    # create instance of web driver
    chromedriver_path = chromedriver_autoinstaller.install()
    # options
    options = Options()
    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        print("using proxy : ", proxy)
    if show_images == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    if option is not None:
        options.add_argument(option)
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(100)
    return driver

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def check_exists_by_link_text(text, driver):
    try:
        driver.find_element(By.LINK_TEXT,text)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(xpath, driver):
    timeout = 3
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    return True


def dowload_images(urls, save_dir):
    for i, url_v in enumerate(urls):
        for j, url in enumerate(url_v):
            urllib.request.urlretrieve(url, save_dir + '/' + str(i + 1) + '_' + str(j + 1) + ".jpg")


def get_user_information(users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)

    users_info = {}

    for i, user in enumerate(users):

        log_user_page(user, driver)

        if user is not None:

            try:
                following = driver.find_element_by_xpath(
                    '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/followers")]/span[1]/span[1]').text
            except Exception as e:
                # print(e)
                return

            try:
                element = driver.find_element_by_xpath('//div[contains(@data-testid,"UserProfileHeader_Items")]//a[1]')
                website = element.get_attribute("href")
            except Exception as e:
                # print(e)
                website = ""

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                # print(e)
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[3]').text
                birthday = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                location = driver.find_element_by_xpath(
                    '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
            except Exception as e:
                # print(e)
                try:
                    join_date = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[2]').text
                    span1 = driver.find_element_by_xpath(
                        '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                    if hasNumbers(span1):
                        birthday = span1
                        location = ""
                    else:
                        location = span1
                        birthday = ""
                except Exception as e:
                    # print(e)
                    try:
                        join_date = driver.find_element_by_xpath(
                            '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
                        birthday = ""
                        location = ""
                    except Exception as e:
                        # print(e)
                        join_date = ""
                        birthday = ""
                        location = ""
            print("--------------- " + user + " information : ---------------")
            print("Following : ", following)
            print("Followers : ", followers)
            print("Location : ", location)
            print("Join date : ", join_date)
            print("Birth date : ", birthday)
            print("Description : ", desc)
            print("Website : ", website)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            if i == len(users) - 1:
                driver.close()
                return users_info
        else:
            print("You must specify the user")
            continue

def keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position,
                  save_images=False):
    """ scrolling function for tweets crawling"""

    save_images_dir = "/images"

    if save_images == True:
        if not os.path.exists(save_images_dir):
            os.mkdir(save_images_dir)

    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.5, 1.5))
        # get the card of tweets
        page_cards = driver.find_elements("xpath",'//article[@data-testid="tweet"]')  # changed div by article
        for card in page_cards:
            tweet = get_data(card, save_images, save_images_dir)
            if tweet:
                # check if the tweet is unique
                tweet_id = ''.join(tweet[:-2])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    last_date = str(tweet[2])
                    print("Tweet made at: " + str(last_date) + " is found.")
                    writer.writerow(tweet)
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break
        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            scroll += 1
            print("scroll ", scroll)
            sleep(random.uniform(0.5, 1.5))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.5, 1.5))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position


def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_retweets(users, tweets, headless, env, follow=None, verbose=1, wait=2, limit=float('inf')):
     """ get the the individuals who have retweeted a tweet """
     # initiate the driver
     driver = init_driver(headless=headless)
     sleep(wait)
     # log in (the .env file should contain the username and password)
     # driver.get('https://www.twitter.com/login')
     log_in(driver, env, wait=wait)
     sleep(wait)
     # followers and following dict of each user
     retweet_users = {}

     for user in users:
        for tweet in tweets[user]:
            # if the login fails, find the new log in button and log in again.
            if check_exists_by_link_text("Log in", driver):
                print("Login failed. Retry...")
                login = driver.find_element(By.LINK_TEXT,"Log in")
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                driver.execute_script("arguments[0].click();", login)
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                sleep(wait)
                log_in(driver, env)
                sleep(wait)
            #case 2
            if check_exists_by_xpath('//input[@name="session[username_or_email]"]', driver):
                print("Login failed. Retry...")
                sleep(wait)
                log_in(driver, env)
                sleep(wait)
            print("Crawling " + user + " " + follow)
            driver.get('https://twitter.com/' + user + '/status/' + tweet + '/retweets')
            sleep(random.uniform(wait - 0.5, wait + 0.5))
        # check if we must keep scrolling
        scrolling = True
        last_position = driver.execute_script("return window.pageYOffset;")
        follows_elem = []
        follow_ids = set()
        is_limit = False
        while scrolling and not is_limit:
            # get the card of following or followers
            # this is the primaryColumn attribute that contains retweers
            primaryColumn = driver.find_element("xpath",'//div[contains(@data-testid,"primaryColumn")]')
            # extract only the Usercell
            page_cards = primaryColumn.find_elements("xpath",'//div[contains(@data-testid,"UserCell")]')
            for card in page_cards:
                # get the retweeters element
                element = card.find_element("xpath",'.//div[1]/div[1]/div[1]//a[1]')
                follow_elem = element.get_attribute('href')
                # append to the list
                follow_id = str(follow_elem)
                follow_elem = '@' + str(follow_elem).split('/')[-1]
                if follow_id not in follow_ids:
                    follow_ids.add(follow_id)
                    follows_elem.append(follow_elem)
                if len(follows_elem) >= limit:
                    is_limit = True
                    break
                if verbose:
                    print(follow_elem)
            print("Found " + str(len(follows_elem)) + " " + follow)
            scroll_attempt = 0
            while not is_limit:
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    # end of scroll region
                    if scroll_attempt >= 2:
                        scrolling = False
                        break
                    else:
                        sleep(random.uniform(wait - 0.5, wait + 0.5))  # attempt another scroll
                else:
                    last_position = curr_position
                    break

        retweet_users[user] = follows_elem

     return retweet_users


def get_retweeters(users, tweets,  env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    retweeters = get_retweets(users, tweets, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(retweeters, f)
        print(f"file saved in {file_path}")
    return retweeters

if __name__ == "__main__":
    #List of Twitter usernames, Dictionary with username:tweet_id, .env file (see scweet documentation)
    # get_retweeters()
