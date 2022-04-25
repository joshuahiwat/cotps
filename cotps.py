import configparser, csv, pytz, time, warnings, os

from flask import (
    Flask,
    request,
    json,
)
from datetime import date
from datetime import datetime
from discord import (
    Webhook,
    RequestsWebhookAdapter,
)
from selenium import webdriver

warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)


def startchrome(chromedriver):
    options = webdriver.ChromeOptions()

    options.add_argument('--window-size=1024,768')
    options.add_argument('--log-level=3')

    # Run Chrome invisible or not
    if int(runheadless) == 1:
        options.add_argument("--headless")
        options.add_argument("--start-maximized");
    # END IF

    # Where is chromedriver present on your system.
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    return driver


# END DEF

def dologincheck(driver, refreshtime):
    # messageboxes('Logged in: ' + str(driver.execute_script("return localStorage['IS_LOGIN']")))
    if driver.execute_script("return localStorage['IS_LOGIN']") != 'Y':
        setcountrycode(driver, refreshtime)
        logintocotps(driver, refreshtime)
        gototransactionhall(driver, refreshtime)
    # else:
    # messageboxes('Still logged in')
    # END IF


# END DEF

def logintocotps(driver, refreshtime):
    driver.get('https://cotps.com/#/pages/login/login')
    time.sleep(refreshtime)
    ele = driver.find_elements_by_class_name('uni-input-input')
    # messageboxes("Inputting phone number")
    ele[0].send_keys(os.getenv("username"))
    time.sleep(1)
    # messageboxes("Inputting password")
    ele[1].send_keys(os.getenv("password"))
    time.sleep(1)
    # messageboxes("Finding and clicking login")
    loginbutton = driver.find_elements_by_class_name('login')
    loginbutton[0].click()
    time.sleep(refreshtime)


# END DEF

def setcountrycode(driver, refreshtime):
    driver.get('https://cotps.com/#/pages/phonecode/phonecode?from=login')
    time.sleep(refreshtime)
    ele = driver.find_elements_by_class_name('uni-input-input')
    # messageboxes("Inputting country code")
    ele[0].send_keys(countrycode)
    time.sleep(1)
    # messageboxes("Finding and clicking confirm")
    varcommit = driver.find_element_by_xpath(
        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button')
    varcommit.click()
    time.sleep(refreshtime)


def gototransactionhall(driver, refreshtime):
    driver.get('https://cotps.com/#/pages/transaction/transaction')
    time.sleep(refreshtime)


def gotoreferralrewards(driver, refreshtime):
    driver.get('https://cotps.com/#/pages/userCenter/myTeam')
    time.sleep(refreshtime)


def claimreferralfees(driver, refreshtime):
    try:
        # Claim LV1
        varfees = float(driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view['
            '1]/uni-view[2]/uni-view[2]').text)
        varconfirm = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()
        time.sleep(refreshtime)

        # Claim LV2
        varfees = float(varfees) + float(driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view['
            '1]/uni-view[2]/uni-view[2]').text)
        varconfirm = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]')
        varconfirm.click()
        time.sleep(refreshtime / 2)
        varconfirm = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()
        time.sleep(refreshtime)

        # Claim LV3
        varfees = float(varfees) + float(driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view['
            '1]/uni-view[2]/uni-view[2]').text)
        varconfirm = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[3]')
        varconfirm.click()
        time.sleep(refreshtime / 2)
        varconfirm = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()

        time.sleep(refreshtime)

    except ValueError:
        return False


# END DEF

def getwalletinfo(driver, walletinfo, refreshtime):
    try:
        # get current wallet
        testvar = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view[2]')
        currentwallet = float(testvar.text)
        walletinfo[0] = currentwallet

        # get current amount in transactions
        testvar = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[1]/uni-view[2]')
        currentintransaction = float(testvar.text)
        walletinfo[1] = currentintransaction

    except ValueError:
        gototransactionhall(driver, refreshtime)
    # END TRY
    return walletinfo


# END DEF

def getandsellorder(driver, refreshtime):
    try:
        varorder = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button')
        varorder.click()
        time.sleep(refreshtime)
        try:
            varsell = driver.find_element_by_xpath(
                '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view['
                '7]/uni-view/uni-view/uni-view[6]/uni-button[2]')
            varsell.click()
            time.sleep(refreshtime)
        except ValueError:
            return False
    except ValueError:
        return False
    return True


# END DEF

def getorderdetails(driver, refreshtime, orderdict):
    try:
        varordernumber = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view['
            '8]/uni-view/uni-view/uni-view[2]/uni-text[2]/span').text
        vartransactionamount = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view['
            '8]/uni-view/uni-view/uni-view[3]/uni-text[2]/span').text
        varprofit = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view['
            '8]/uni-view/uni-view/uni-view[4]/uni-text[2]/span').text
        vartotal = driver.find_element_by_xpath(
            '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view['
            '8]/uni-view/uni-view/uni-view[5]/uni-text[2]/span').text
        orderdict.update({"ordered": varordernumber})
        orderdict.update({"transactional": vartransactionamount})
        orderdict.update({"profit": varprofit})
        orderdict.update({"total": vartotal})
        time.sleep(refreshtime)
    except ValueError:
        gototransactionhall(driver, refreshtime)
    # END TRY
    return orderdict


# END DEF

def orderconfirm():
    time.sleep(refreshtime)
    varconfirm = driver.find_element_by_xpath(
        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-button')
    varconfirm.click()


# END DEF

def clearorderdict():
    orderdict = {
        "ordernum": "",
        "timeofsale": "",
        "transactionamount": "",
        "profit": "",
        "total": ""
    }
    return orderdict


# END DEF

def writecsvheader(csvfile):
    with open(csvfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Order Number", "Time of Sale", "Transaction Amount", "Profit", "Total"])


# END DEF

def writedicttocsv(csvfile, orderdict):
    if int(usecsvfile) == 1:
        try:
            with open(csvfile, 'a') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(
                    [orderdict.get("ordernum"), orderdict.get("timeofsale"), orderdict.get("transactionamount"),
                     orderdict.get("profit"), orderdict.get("total")])
                return True
        except ValueError:
            return False


# Main Function
def start():
    global usecsvfile, refreshtime, countrycode

    config = configparser.ConfigParser()
    config.sections()

    config.read('config.cfg')

    # Provide chromedriver location
    chromedriver = config['DEFAULT']['chromedriver']
    # Provide the email and password
    username = os.getenv("username")
    password = os.getenv("password")
    countrycode = config['DEFAULT']['countrycode']
    # How long for each page refresh
    refreshtime = int(config['DEFAULT']['refreshment'])
    # How long to wait between each check to see if in transaction went to 0
    timebetweeneachcheck = int(config['DEFAULT']['timebetweenchecks'])
    # Setting Timezone
    est = pytz.timezone(config['DEFAULT']['timezone'])
    # Use CSV file? True/False
    usecsvfile = config['DEFAULT']['securefile']
    # setting CSV file location
    csvfile = config['DEFAULT']['csvfile']
    # setting wallet percentage to start new transaction
    walletpercentagetostart = config['DEFAULT']['walletpercentagetostart']
    # OR set an amount to start
    walletamounttostart = config['DEFAULT']['walletamounttostart']
    # Hide Chrome
    runheadless = config['DEFAULT']['headless']
    # Discord webhook URL
    discordwebhookurl = config['DEFAULT']['discolouration']

    # initializing variable
    walletinfo = [0, 0]

    # Begin order dict
    orderdict = clearorderdict()

    # Checks if csv exists
    if int(usecsvfile) == 1:
        file_exists = os.path.exists(csvfile)
        if not bool(file_exists):
            writecsvheader(csvfile)
        # END IF
    # END IF

    # Gets current time and sets timezone
    today = date.today()
    now = datetime.now(est)
    currentdate = today.strftime("%m-%d")
    currenttime = now.strftime("%H:%M")

    # start browser
    driver = startchrome(chromedriver)

    # set countrycode
    setcountrycode(driver, refreshtime)

    # Login to cotps
    logintocotps(driver, refreshtime)

    # Begin in transaction watch cycle
    while True:

        dologincheck(driver, refreshtime)

        today = date.today()
        now = datetime.now(est)
        currentdate = today.strftime("%m-%d")
        currenttime = now.strftime("%H:%M")

        # check and claim referral rewards
        gotoreferralrewards(driver, refreshtime)
        claimreferralfees(driver, refreshtime)

        # Goto Transaction Hall
        gototransactionhall(driver, refreshtime)

        # get wallet info and see if anything is in transaction
        walletinfo = getwalletinfo(driver, walletinfo, refreshtime)

        # Get in transaction amount
        currentwallet = float(walletinfo[0])
        intranswallet = float(walletinfo[1])
        totalassets = intranswallet + currentwallet
        walletbalancepercentage = round(100 / (totalassets / currentwallet), 2)

        # Did all my money come back yet
        orderdicttxthisrun = 0
        orderdictprofitthisrun = 0

        # start transactions when wallet percentage reaches at least the % set in config OR the amount set to start
        if (float(walletbalancepercentage) >= float(walletpercentagetostart) or (
                float(currentwallet) >= float(walletamounttostart))):

            while True:

                # Buy an Order
                if getandsellorder(driver, refreshtime):
                    # Get order details
                    orderdict = getorderdetails(driver, refreshtime, orderdict)

                    # Click Confirm button
                    orderconfirm()
                    today = date.today()
                    now = datetime.now(est)
                    currentdate = today.strftime("%m-%d")
                    currenttime = now.strftime("%H:%M")
                    timestamp = currentdate + ' ' + currenttime
                    orderdict.update({"timescale": str(timestamp)})
                    orderdicttxthisrun = float(orderdicttxthisrun) + float(orderdict.get("transactional"))
                    orderdictprofitthisrun = round(float(orderdictprofitthisrun) + float(orderdict.get("profit")), 2)

                    # Write current Order to CSV
                    writedicttocsv(csvfile, orderdict)

                    # Clear dictionary for next order
                    orderdict = clearorderdict()

                    # Get current wallet
                    walletinfo = getwalletinfo(driver, walletinfo, refreshtime)

                    # What is my current wallet
                    currentwallet = float(walletinfo[0])

                    # If less than $5, stop purchasing
                    if currentwallet <= 5:
                        # breaks out of loop when money is too low
                        break
                    # END IF
                else:
                    # break out of loop when clicking sell buttons don't work
                    break
                # END IF
            # END WHILE
        # END IF
        dologincheck(driver, refreshtime)
        time.sleep(timebetweeneachcheck)
    # END WHILE


# END DEF

@app.route('/webhook')
def webhook():
    start()
    return 'Webhooks with Python'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)  # Settings for PM2
    # app.run(debug=True)
