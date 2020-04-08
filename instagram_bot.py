from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

import time


class InstagramBot:
  def __init__(self, username, password):
    self.username = username
    self.password = password

    chromedriver_autoinstaller.install()
    self.driver = webdriver.Chrome()


  def login(self):
    self.driver.get("https://www.instagram.com/accounts/login")

    # waiting for the elements to load
    WebDriverWait(self.driver, 10).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "._2hvTZ.pexuQ.zyHYP") ) )

    # finding the inputs and buttons
    usernameInput = self.driver.find_elements_by_css_selector("._2hvTZ.pexuQ.zyHYP")[0]
    passwordInput = self.driver.find_elements_by_css_selector("._2hvTZ.pexuQ.zyHYP")[1]
    loginButton = self.driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF")

    # typing and clicking the inputs and buttons
    usernameInput.send_keys(self.username)
    passwordInput.send_keys(self.password)
    loginButton.click()

    WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, ".piCib") ) )
    print("Successfully logged in as {}.".format(self.username))

  # a method that returns the follow/unfollow button from an instagram profile
  def getFollowButton(self, username):
    self.driver.get("https://www.instagram.com/" + username)
    time.sleep(2)

    textList = ["Follow", "Following", "Requested", "Follow Back"]
    buttons = self.driver.find_elements_by_css_selector('button')

    # the first button that has the text in the list is the good one
    for button in buttons:
      if button.text in textList:
        followButton = button
        break

    return followButton


  def followByUsername(self, username):
    followButton = self.getFollowButton(username)

    if followButton.text == 'Following' or followButton.text == "Requested":
      print("You are already following {}.".format(username))
    else:
      followButton.click()
      print("You have successfully followed {}!".format(username))

    time.sleep(1)


  def unfollowByUsername(self, username):
    unfollowButton = self.getFollowButton(username)

    if unfollowButton.text == 'Follow' or unfollowButton.text == "Follow Back":
      print("You are not following {}.".format(username))
    else:
      unfollowButton.click()
      self.driver.find_element_by_css_selector(".aOOlW.-Cab_").click()

      print("You have successfully unfollowed {}!".format(username))

    time.sleep(.2)


  def likePost(self, url):
    self.driver.get(url)

    # stopping if the account is private
    h2s = self.driver.find_elements_by_css_selector('h2')
    for h2 in h2s:
      if h2.text == "This Account is Private":
        print("You can't like the photo because the account is private.")
        return

    # finding the like button and pressing it, printing a message afterwards
    WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "button.wpO6b") ) )
    likeButton = self.driver.find_element_by_css_selector("button.wpO6b")
    likeButton.click()

    print("You liked the post.")


  # the list of the first people who liked a photo / followed a person
  def getList(self, number, focusElementSelector):
    # returning if we cannot find any followers
    try:
      WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, 'button.sqdOP.L3NKy.y3zKF') ) ) #the follow button
    except:
      print("Did not find any followers.")
      return
    followButtonsList = self.driver.find_elements_by_css_selector('button.sqdOP.L3NKy.y3zKF')

    # finding the focus element
    WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, focusElementSelector) ) )
    focus = self.driver.find_element_by_css_selector(focusElementSelector)

    actionChain = webdriver.ActionChains(self.driver)

    # scroll through the followers list until there are enough of them
    while len(followButtonsList) < number:
      # an element that is clicked to focus the list,
      # to be able to scroll through it using the spacebar
      if len(followButtonsList) < 30:
        focus.click()
        

      # pressing the spacebar to scroll
      actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

      # updating the followers list
      followButtonsList = self.driver.find_elements_by_css_selector('button.sqdOP.L3NKy.y3zKF')
      time.sleep(.2)

    return followButtonsList


  def followList(self, number, focusElementSelector):
    followButtonsList = self.getList(number, focusElementSelector)

    # following the desired number of users
    usersFollowed = 0
    for button in followButtonsList:
      # stopping if we followed enough of them
      if usersFollowed == number:
        print("Successfully followed {} people.".format(number))
        return 
      usersFollowed += 1
      time.sleep(0.5)

      button.click()
    print("Failed. Only followed {}/{} people.".format(usersFollowed, number))


  def followByPageFollowed(self, username, number):
    url = "https://www.instagram.com/"+username
    self.driver.get(url)

    # pressing the button that opens the list of followers
    WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.XPATH, '//a[@href="/'+username+'/followers/"]') ) )
    self.driver.find_element_by_xpath('//a[@href="/'+username+'/followers/"]').click()

    self.followList(number, 'div.isgrP')


  def followByPhotoLiked(self, url, number):
    self.driver.get(url)

    # open the list
    WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, 'button.sqdOP.yWX7d._8A5w5') ) )
    time.sleep(2)
    self.driver.find_element_by_css_selector('button.sqdOP.yWX7d._8A5w5').click()
 
    self.followList(number, 'div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd')


  def comment(self, url, text):
    self.driver.get(url)
    
    WebDriverWait(self.driver, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, '._15y0l button.wpO6b') ) )
    commentButton = self.driver.find_element_by_css_selector("._15y0l button.wpO6b")
    commentButton.click()

    time.sleep(0.5)
    textArea = self.driver.find_element_by_tag_name("textarea")
    textArea.send_keys(text)

    time.sleep(0.5)
    postButton = self.driver.find_element_by_css_selector(".X7cDz button.sqdOP.yWX7d.y3zKF")
    postButton.click()

    print("Success.")


  def logout(self):
    time.sleep(1)
    self.driver.quit()



if __name__ == "__main__":
  print("Hello there! This is a simple instagram bot made with Selenium Webdriver")
  print("It is pretty simple to use: ")
  print("You can type 'help' for a list of commands.")
  print("For each command typed, the bot will execute it.")

  bot = InstagramBot("", "")
  while True:
    print("Please enter a command or 'help' for the list of available commands:")
    command = input()

    if command == "login":
      username = input("Username: ")
      password = input("Password: ")

      bot = InstagramBot(username, password)
      bot.login()

    elif command == "logout":
      bot.logout()

    elif command == "follow-by-username":
      username = input("Username: ")

      bot.followByUsername(username)

    elif command == "unfollow-by-username":
      username = input("username: ")

      bot.unfollowByUsername(username)

    elif command == "follow-by-photo-liked":
      url = input("Photo url: ")
      num = int(input("Number of follows: "))

      bot.followByPhotoLiked(url, num)

    elif command == "follow-by-followed-page":
      username = input("Username: ")
      num = int(input("number of follows: "))

      bot.followByPageFollowed(username, num)

    elif command == "like":
      url = input("Photo url: ")

      bot.likePost(url)

    elif command == "comment":
      url = input("Photo url: ")
      text = input("Text: ")

      bot.comment(url, text)

    elif command == "help":
      text = [
        "'login': log into your account",
        "'logout': log out of your account",
        "'like': like a photo (you need the url of the photo)",
        "'comment': add a comment to a photo (you need the url and the text)",
        "'follow-by-username': follow a page by its username (you need the username)",
        "'follow-by-username': follow a page by its username (you need the username)",
        "unfollow-by-username': unfollow a page by its username",
        "'follow-by-followed-page': follow people who followed a specific page (you need the name of the page and the number of follows)",
        "'follow-by-photo-liked': follow people who liked a specific photo (url and number)"
      ]
      for string in text:
        print(string)
        time.sleep(0.1)

    time.sleep(0.5)
    print()
    