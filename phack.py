# import scipy
from scipy.stats import ttest_ind as ttest
import requests
import numpy as np
import warnings

spreadsheet_id = '1oomfOjU8asC6aB-s-bffhvqzsA9QtdJn8RTU3anmLe0'

response = requests.get('https://docs.google.com/spreadsheet/ccc?key=' + spreadsheet_id + '&output=csv')
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
            csp = lb + 1
            lb = resp.find('\n',csp)
            if lb == -1:
                lb = len(resp) + 1
            continue
        # print(resp[csp:nspt])
        c_row.append(resp[csp:nspt])
        if nspt == len(resp):
            output.append(c_row)
            flag = 1
        csp = nspt + 1
    return output

def test_ttest(nrep,nqs):
    pvec = []
    g1 = np.round(5*np.random.random([nrep,nqs]))
    g2 = np.round(5*np.random.random([nrep,nqs]))
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

def np_array_flt_int(ar):
    return np.array([int(val) for val in ar])


def ttest_single_split(data, split_index):
    y_index = data[:,split_index] == 'Yes'
    n_index = data[:,split_index] == 'No'
    for i in range(data.shape[1]):
        if i == split_index:
            continue
        y_data = data[y_index,i] == 'Yes'
        n_data = data[n_index,i] == 'Yes'
        tvalue, pvalue = ttest(y_data, n_data)


        if pvalue < .05 and tvalue != -np.inf:
            # print(data[0, split_index])
            # print(data[0, i])
            # print(np.mean(y_data))
            # print(np.mean(n_data))
            # print(pvalue)
            print("""
            If you like {0}, there is a {1}% chance that you like {2}
            If you don't like {0}, there is a {3}% chance that you like {2}
            Pvalue = {4}
            """.format(data[0, split_index], np.round(100*np.mean(y_data),2), data[0, i], np.round(100*np.mean(n_data),2), np.round(pvalue,2)
                  )
                  )
            1
d = np.array(deal_with_data(rd))
d = d[:,1:d.shape[1]]
nrows = d.shape[0]
ncols = d.shape[1]
# print(d.shape)
yrep = d[:,2] == 'Yes'
nrep = d[:,2] == 'No'
# print(yrep)
# print(nrep)
# print(ncols)
#
# for i in range(3, ncols):
#     r1 = np_array_flt_int(d[yrep,i])
#     r2 = np_array_flt_int(d[nrep,i])
#     t, p = ttest(r1, r2)
#     print("""
#     {0}, y ave: {1}, n ave: {2}, pvalue: {3}""".format(d[0,i], np.mean(r1), np.mean(r2), p))

# print(rep_test_ttest(20, 30, 5000))
for i in range(ncols):
    ttest_single_split(d, i)
