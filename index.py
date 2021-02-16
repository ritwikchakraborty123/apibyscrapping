from flask import Flask, request

import requests
from bs4 import BeautifulSoup

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# important
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def conv(str):
  dig=0
  ok=0
  last=10
  for i in str:
    if(i<='9' and i>='0'):
      if(ok):
        dig=dig+int(i)/last
        last*=10 
      else:
        dig=dig*10+int(i) 
    elif(i==','):
      ok=1
  return dig


app = Flask(__name__)
@app.route('/')
def query_example():
  language = request.args.get('language')
  return '''<h1>The language value is: {}</h1>'''.format(language)

@app.route('/api')
def form_example():

  postcode='3705LE'
  huisnummer=74
  geschatte_waarde=500000
  validatie=0
  verhuurd=0
  verbouwing=0
  nieuwbouw=0
  soort_woning='appartement'

  if(request.args.get('postcode')):
    postcode=request.args.get('postcode')
  if(request.args.get('huisnummer')):
    huisnummer=request.args.get('huisnummer')
  if(request.args.get('geschatte_waarde')):
    geschatte_waarde=request.args.get('geschatte_waarde')
  if(request.args.get('validatie')):
    validatie=request.args.get('validatie')
  if(request.args.get('verhuurd')):
    verhuurd=request.args.get('verhuurd')
  if(request.args.get('verbouwing')):
    verbouwing=request.args.get('verbouwing')
  if(request.args.get('nieuwbouw')):
    nieuwbouw=request.args.get('nieuwbouw')
  if(request.args.get('soort_woning')):
    soort_woning=request.args.get('soort_woning')


  browser=webdriver.Chrome('C:/chromedriver/chromedriver.exe')
  URL='https://www.support4tp.nl/aanvraag/nieuw/type/woningtaxatie'

  browser.get(URL)

  Object_Postcode=browser.find_element_by_id('Object_Postcode')
  Object_Huisnummer=browser.find_element_by_id('Object_Huisnummer')
  Object_GeschatteWaarde=browser.find_element_by_id('Object_GeschatteWaarde')
  Object_Type=browser.find_element_by_id('Object_Type')

  # appartement
  # woonhuis
  value=""


  if(soort_woning=='woonhuis' and (not verhuurd) and (not verbouwing) and (not nieuwbouw)):
    value='Woonhuis&Nieuwbouw'
  if(soort_woning=='woonhuis' and (not verhuurd) and (not verbouwing) and nieuwbouw):
    value='Woonhuis'
  if(soort_woning=='woonhuis' and (verhuurd) and (not verbouwing) and (not nieuwbouw)):
    value='Woonhuis&Verbouwing&In verhuurde staat'
  if(soort_woning=='woonhuis' and (not verhuurd) and verbouwing and (not nieuwbouw)):
    value='Woonhuis&Verbouwing'

  if(soort_woning=='woonhuis' and verhuurd and verbouwing and (not nieuwbouw)):
    value='Woonhuis&In verhuurde staat'

  if(soort_woning=='appartement' and (not verhuurd) and (not verbouwing) and (nieuwbouw)):
    value='Appartement&Nieuwbouw'

  if(soort_woning=='appartement' and (not verhuurd) and (not verbouwing) and (not nieuwbouw)):
    value='Appartement' 

  if(soort_woning=='appartement' and (verhuurd) and (not verbouwing) and (not nieuwbouw)):
    value='Appartement&In verhuurde staat'
  if(soort_woning=='appartement' and (not verhuurd) and (verbouwing) and (not nieuwbouw)):
    value='Appartement&Verbouwing'
  if(soort_woning=='appartement' and (verhuurd) and (verbouwing) and (not nieuwbouw)):
    value='Appartement&Verbouwing&In verhuurde staat'


  Object_Postcode.send_keys(postcode);
  Object_Huisnummer.send_keys(huisnummer);
  Object_GeschatteWaarde.send_keys(geschatte_waarde);

  select = Select(browser.find_element_by_id('Object_Type'))
  select.select_by_value(value)

  time.sleep(5)
  
  ans={'status' : 404}
  
  try:
    Object_Postcode.submit()
  except:
    return json.dumps(ans)
  time.sleep(5)
  if(validatie==0):
    btn=browser.find_element_by_xpath('//*[@id="fieldset-Taxateur"]/div[1]/div/label[1]')
    btn.click()

  time.sleep(2)
  wrap=browser.find_element_by_xpath('//*[@id="fieldset-Taxateur"]/div[3]/div')
  ele=wrap.find_elements_by_tag_name('label')
  cnt=1
  li=[]
  for i in ele:
    dic={}
    dic['name']=i.find_element_by_xpath('//*[@id="fieldset-Taxateur"]/div[3]/div/label['+str(cnt)+']/span[1]').text               
    dic['price']=conv(i.find_element_by_xpath('//*[@id="fieldset-Taxateur"]/div[3]/div/label['+str(cnt)+']/span[4]').text)
    # try:
    #   print(i.find_element_by_xpath('//*[@id="fieldset-Taxateur"]/div[3]/div/label['+str(cnt)+']/span[6]/span[2]').text)
    # finally:
    cnt+=1
    li.append(dic)
  browser.quit()

  ans={'status' : 200 , 'value' : li }

  return json.dumps(ans)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)