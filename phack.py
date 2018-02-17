# import scipy
from scipy.stats import ttest_ind as ttest
import requests
import numpy as np

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

def test_ttest(nrep,nqs):
    pvec = []
    g1 = np.random.random([nrep,nqs])
    g2 = np.random.random([nrep,nqs])
    for i in range(nqs):
        t,p = ttest(g1[:,i],g2[:,i])
        pvec.append(p)
    return pvec

def rep_test_ttest(nrep,nqs,reps):
    pval_vec = []
    for i in range(reps):
        p = test_ttest(nrep, nqs)
        pval_vec.append(np.min(p))
    pval_vec = np.array(pval_vec)
    return np.mean(pval_vec < .05)

deal_with_data(rd)