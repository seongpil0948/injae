def login(driver, login_url, redirect_url, user):
  driver.get(f'{login_url}?returnUrl={redirect_url}')
  driver.find_element_by_id('id').send_keys(user['id'])
  driver.find_element_by_id('pw').send_keys(user['password'])
  driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
  return driver







