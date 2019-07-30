import itertools

from explicit import waiter, XPATH
from selenium import webdriver


def login(driver):
    username = #insert username here
    password = #insert password here

    # Load page
    driver.get("https://www.instagram.com/accounts/login/")

    # Login
    waiter.find_write(driver, "//input[@name='username']", username, by=XPATH)
    waiter.find_write(driver, "//input[@name='password']", password, by=XPATH)
    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    # Wait for the user dashboard page to load
    waiter.find_element(driver, "//a/span[@aria-label='Find People']", by=XPATH)


def scrape_followers(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Follower(s)' link
    # driver.find_element_by_partial_link_text("follower").click()
    xpathMod = "//a[@href='/"+account+"/followers/']"
    waiter.find_element(driver, xpathMod, by=XPATH).click()

    # Wait for the followers modal to load
    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # At this point a Followers modal pops open. If you immediately scroll to the bottom,
    # you hit a stopping point and a "See All Suggestions" link. If you fiddle with the
    # model by scrolling up and down, you can force it to load additional followers for
    # that person.

    # Now the modal will begin loading followers every time you scroll to the bottom.
    # Keep scrolling in a loop until you've hit the desired number of followers.
    # In this instance, I'm using a generator to return followers one-by-one
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            yield waiter.find_element(driver, follower_css.format(follower_index)).text

        # Instagram loads followers 12 at a time. Find the last follower element
        # and scroll it into view, forcing instagram to load another 12
        # Even though we just found this elem in the previous for loop, there can
        # potentially be large amount of time between that call and this one,
        # and the element might have gone stale. Lets just re-acquire it to avoid
        # that
        last_follower = waiter.find_element(driver, follower_css.format(follower_index))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)

account = #insert username here
driver = webdriver.Chrome()
try:
    login(driver)
    # Print the first 75 followers for the "instagram" account
    print('Followers of the "{}" account'.format(account))
    followerList = []
    for count, follower in enumerate(scrape_followers(driver, account=account), 1):
        print("\t{:>3}: {}".format(count, follower))
        followerList.append(follower)
        if count >= 10:
            break

    print(followerList)
finally:
    driver.quit()

        
