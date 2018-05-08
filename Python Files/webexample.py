# import webbrowser
# new = 2


# url = "https://smart-clock-example-caoimhemalone.c9users.io/index.php"
# webbrowser.open(url,new=new)

import webbrowser

url = "https://smart-clock-example-caoimhemalone.c9users.io/index.php"

# MacOS
#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
chrome_path = '/usr/bin/google-chrome %s'


webbrowser.get(chrome_path).open(url)