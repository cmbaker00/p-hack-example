# import scipy
from scipy.stats import ttest_ind as ttest
import requests

response = requests.get('https://docs.google.com/spreadsheet/ccc?key=1BP4mcPosl2V5U_Q9HwJ9VriwdSS4LaSMXILXsEOPKfA&output=csv')
rd = response.content.decode()

def deal_with_data(resp):
    lb = resp.find('\n')
    flag = 0
    csp = 0
    while flag == 0:
        nspt = resp.find(',',csp)
        print(resp[csp:nspt])
        csp = nspt + 1
        if nspt > lb:
            flag = 1
            break

deal_with_data(rd)