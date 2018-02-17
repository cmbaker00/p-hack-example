# import scipy
from scipy.stats import ttest_ind as ttest
import requests
import numpy as np

response = requests.get('https://docs.google.com/spreadsheet/ccc?key=18ErdR3Vs3hKYYPQOoAxQ2YNwvACTJzK5iwx37UOQbOc&output=csv')
rd = response.content.decode()

def deal_with_data(resp):
    output = []
    lb = resp.find('\n')
    flag = 0
    csp = 0
    c_row = []
    while flag == 0:
        nspt_com = resp.find(',',csp)
        if nspt_com == -1:
            nspt_com = np.inf
        nspt_r = resp.find('\r',csp)
        if nspt_r == -1:
            nspt_r = np.inf
        nspt = np.min([nspt_com, nspt_r])
        if nspt == np.inf:
            nspt = len(resp)
        else:
            nspt = int(nspt)
        if nspt > lb:
            output.append(c_row)
            c_row = []
            # flag = 1
            csp = lb + 1
            lb = resp.find('\n',csp)
            if lb == -1:
                lb = len(resp) + 1
            continue
        # print(resp[csp:nspt])
        c_row.append(resp[csp:nspt])
        csp = nspt + 1
        if nspt == len(resp):
            flag = 1
    return output

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

d = deal_with_data(rd)
print(np.array(d))