from selenium import webdriver
driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
target = "https://pan.baidu.com/"
driver.get(target)
driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[6]/div/div[6]/div[2]/a').click()
driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[6]/div/div[3]/form/p[5]/input[2]').send_keys('name')
driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[6]/div/div[3]/form/p[6]/input[2]').send_keys('key')
driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[6]/div/div[3]/form/p[9]/input').click()