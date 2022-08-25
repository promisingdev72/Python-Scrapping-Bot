from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pandas as pd
import requests
import lxml.html
import time
import json
import math

FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&f=exch_nasd,geo_usa,sh_float_u10,sh_price_u10,sh_relvol_o2"
NASDAQ_URL = "https://api.nasdaq.com/api/quote/{}/info?assetclass=stocks"
DEGIRO_URL = "https://trader.degiro.nl/trader/#/products?productType=1&searchText={}&country=-1&stockList=-1&stockListType=index&isInUSGreenList=false"
LOGIN_USERNAME = 'Paulopes6'
LOGIN_PASSWORD = 'TestDegiro91'


def main():
	TodayMoney = 100
	headers = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
	}
	session = requests.Session()
	session.headers.update(headers)
	r = session.get(FINVIZ_URL)
	x = lxml.html.fromstring(r.text)
	stocks = x.xpath("//*[@class='screener-link-primary']/text()")
	counter = 0
	transactionNumber = 0
	initialPrice = []
	nextPrice = []
	res = []
	buyList = []
	flagMiss = []
	newContract = False
	endContract = False
	timeSize = 5
	amountOfstock = 0
	amountOfstockForsell = 0
	isinResult = []
	isin = ''
	for stock in stocks:
		data = session.get(NASDAQ_URL.format(stock))
		res = data.json()
		try:
			initialPrice.append(float(res['data']['primaryData']['lastSalePrice'].replace('$','')))
		except:
			flagMiss.append(stock)
			continue
	for i in range(len(flagMiss)):
		stocks.remove(flagMiss[i])
	print("\n" , "This is Tickers: ", stocks, "\n")
	print(" This is initial price: ", initialPrice , "\n")
	while counter < timeSize:
		counter += 1
		time.sleep(10)
		nextPrice.clear()
		print("\n" , counter , " Step is searching...\n It takes 5mins, Please wait\n")
		for stock in stocks:
			data = session.get(NASDAQ_URL.format(stock))
			res = data.json()
			try:
				nextPrice.append(float(res['data']['primaryData']['lastSalePrice'].replace('$','')))
			except:
				continue
			if len(nextPrice) == len(initialPrice):
				print("\n" , counter , "Step Price: " , nextPrice , "\n")
				i = 0
				while i < len(initialPrice):
					exchangeRate = initialPrice[i]*10000*1
					nextRate = nextPrice[i]*10000
					if transactionNumber < 3:
						if exchangeRate <= nextRate:
							if not buyList:
								isinResult.clear()
								buyList.append(stocks[i])
								comparePrice = nextPrice[i]
								amountOfstock = math.floor(TodayMoney/comparePrice)
								driver = webdriver.Chrome()
								driver.set_window_size(1200, 800)
								driver.get(DEGIRO_URL.format(stocks[i]))


								try:
									WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(LOGIN_USERNAME)
								except TimeoutException:
									print ("Loading took too much time!")

								try:
									WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(LOGIN_PASSWORD)
								except TimeoutException:
									print ("Loading took too much time!")
									
								try:
									WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
								except TimeoutException:
									print ("Loading took too much time!")


								try:
									WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.TAG_NAME, "tbody")))
									isinString = driver.find_elements_by_xpath("//tbody/tr/td[2]")
									for length in range(len(isinString)):
										isinResult.append(isinString[length].text)
										res = isinResult[length].split(' / ')
										if res[0] == stocks[i]:
											isin = res[1]
								except TimeoutException:
									print ("There is no matched data.")
									continue

								try:
									WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "duvfw-AB"))).click()
								except TimeoutException:
									print ("Loading took too much time!")
									break

								try:
									WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "_3ayi1oaj"))).send_keys(isin)
								except TimeoutException:
									print("Loading took too much time!")
									break

								try:
									compareTxt = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1hM5sC_u']/div[1]/button/span[2]"))).text
									compareText = compareTxt[0:3]
								except TimeoutException:
									print("Loading took too much time!")

								if compareText.lower() == "ndq":

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "_2ALhJK48"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@name='orderTypeForm']/fieldset/div[2]/div[1]"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-name='portal']/div/div/button[2]"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_3JvmSTh1']/input"))).send_keys(amountOfstock)
									except TimeoutException:
										print("Loading took too much time!")
										break
									
									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1EePFV3d']/button"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_6KWtNGL8']/button[2]")))
									except TimeoutException:
										print("Stock was not bought")

									time.sleep(5)

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//fieldset/div/div/button[2]"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@name='orderTypeForm']/fieldset/div[2]/div[1]"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break
										
									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-name='portal']/div/div/button[3]"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1EePFV3d']/fieldset/div[3]/div/div/input"))).send_keys(amountOfstock)
									except TimeoutException:
										print("Loading took too much time!")
										break
										
									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1EePFV3d']/fieldset/div[2]/div[2]/div/input"))).send_keys(str(comparePrice))
									except TimeoutException:
										print("Loading took too much time!")
										break

									try:
										WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1EePFV3d']/button"))).click()
									except TimeoutException:
										print("Loading took too much time!")
										break
								else:
									driver.quit()
									continue
								
								
								print("Bought this stock: " , stocks[i] , "\n")


								sellTime = 0
								while True:
									time.sleep(5)
									sellTime += 1
									print("5s Passed")
									data = session.get(NASDAQ_URL.format(stocks[i]))
									res = data.json()
									currentPrice = float(res['data']['primaryData']['lastSalePrice'].replace('$',''))
									print("currentPrice: " , currentPrice)
									if sellTime == 5:
										transactionNumber += 1
										print("This is transactionNumber:" , transactionNumber)

										driver = webdriver.Chrome()
										driver.set_window_size(1200, 800)
										driver.get(DEGIRO_URL.format(stocks[i]))
										loginUsername = driver.find_element_by_xpath("//input[@id='username']")
										loginPassword = driver.find_element_by_xpath("//input[@id='password']")
										loginBtn = driver.find_element_by_xpath("//button[@type='submit']")
										loginUsername.send_keys(LOGIN_USERNAME)
										loginPassword.send_keys(LOGIN_PASSWORD)
										loginBtn.click()

										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-name='openOrder']/td[1]/button[2]"))).click()
										except TimeoutException:
											print("There is no click event")
										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='t1MR4yCW']/button[2]"))).click()
										except TimeoutException:
											print("There is no click event")

										try:
											WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.TAG_NAME, "tbody")))
											isinString = driver.find_elements_by_xpath("//tbody/tr/td[2]")
											for length in range(len(isinString)):
												isinResult.append(isinString[length].text)
												res = isinResult[length].split(' / ')
												if res[0] == stocks[i]:
													isin = res[1]
										except TimeoutException:
											print ("There is no matched data.")
											continue

										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "duvfw-AB"))).click()
										except TimeoutException:
											print ("Loading took too much time!")
											break

										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "_3ayi1oaj"))).send_keys(isin)
										except TimeoutException:
											print("Loading took too much time!")
											break
										
										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "_2ALhJK48"))).click()
										except TimeoutException:
											print("Loading took too much time!")
											break
										
										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//fieldset/div/div/button[2]"))).click()
										except TimeoutException:
											print("Loading took too much time!")
											break

										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@name='orderTypeForm']/fieldset/div[2]/div[1]"))).click()
										except TimeoutException:
											print("Loading took too much time!")
											break

										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-name='portal']/div/div/button[2]"))).click()
										except TimeoutException:
											print("Loading took too much time!")
											break
										
										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_3JvmSTh1']/input"))).send_keys(amountOfstock)
										except TimeoutException:
											print("Loading took too much time!")
											break
										
										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1EePFV3d']/button"))).click()
										except TimeoutException:
											print("Loading took too much time!")
											break

										try:
											WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_6KWtNGL8']/button[2]")))
										except TimeoutException:
											print("Stock was not sold")

										buyList.clear()
										print("Sold this stock: " , stocks[i])
										initialPrice.pop(i)
										nextPrice.pop(i)
										stocks.pop(i)
										i -= 1
										newContract = True
										break
									if buyList and buyList[0] == stocks[i]:
										if currentPrice >= comparePrice*1.01 or currentPrice <= comparePrice*0.99:
											transactionNumber += 1
											print("This is transactionNumber:" , transactionNumber)

											driver = webdriver.Chrome()
											driver.set_window_size(1200, 800)
											driver.get(DEGIRO_URL.format(stocks[i]))
											
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(LOGIN_USERNAME)
											except TimeoutException:
												print ("Loading took too much time!")

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(LOGIN_PASSWORD)
											except TimeoutException:
												print ("Loading took too much time!")
												
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
											except TimeoutException:
												print ("Loading took too much time!")

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-name='openOrder']/td[1]/button[2]"))).click()
											except TimeoutException:
												print("There is no click event")
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='t1MR4yCW']/button[2]"))).click()
											except TimeoutException:
												print("There is no click event")

											try:
												WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.TAG_NAME, "tbody")))
												isinString = driver.find_elements_by_xpath("//tbody/tr/td[2]")
												for length in range(len(isinString)):
													isinResult.append(isinString[length].text)
													res = isinResult[length].split(' / ')
													if res[0] == stocks[i]:
														isin = res[1]
											except TimeoutException:
												print ("There is no matched data.")
												continue

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "duvfw-AB"))).click()
											except TimeoutException:
												print ("Loading took too much time!")
												break

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "_3ayi1oaj"))).send_keys(isin)
											except TimeoutException:
												print("Loading took too much time!")
												break
											
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "_2ALhJK48"))).click()
											except TimeoutException:
												print("Loading took too much time!")
												break
											
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//fieldset/div/div/button[2]"))).click()
											except TimeoutException:
												print("Loading took too much time!")
												break

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@name='orderTypeForm']/fieldset/div[2]/div[1]"))).click()
											except TimeoutException:
												print("Loading took too much time!")
												break

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-name='portal']/div/div/button[2]"))).click()
											except TimeoutException:
												print("Loading took too much time!")
												break
											
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_3JvmSTh1']/input"))).send_keys(amountOfstock)
											except TimeoutException:
												print("Loading took too much time!")
												break
											
											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_1EePFV3d']/button"))).click()
											except TimeoutException:
												print("Loading took too much time!")
												break

											try:
												WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='_6KWtNGL8']/button[2]")))
											except TimeoutException:
												print("Stock was not sold")


											buyList.clear()
											print("Sold this stock: " , stocks[i])
											initialPrice.pop(i)
											nextPrice.pop(i)
											stocks.pop(i)
											i -= 1
											newContract = True
											break
								if newContract == True:
									break
					else:
						endContract = True
						break
					i += 1
				if endContract == True:
					break
				else:
					initialPrice.clear()
					initialPrice.extend(nextPrice)
		if endContract == True:
			break
		if buyList:
			timeSize += 1
	print("This is last price: " , nextPrice , "\n")
	print("Today transaction is ended")
main()