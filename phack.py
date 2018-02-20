from scipy.stats import ttest_ind as ttest
import requests
import numpy as np

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
        nspt_com = resp.find(',', csp)
        if nspt_com == -1:
            nspt_com = np.inf
        nspt_r = resp.find('\r', csp)
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
            lb = resp.find('\n', csp)
            if lb == -1:
                lb = len(resp) + 1
            continue
        c_row.append(resp[csp:nspt])
        if nspt == len(resp):
            output.append(c_row)
            flag = 1
        csp = nspt + 1
    return output


def test_ttest(nrep, nqs):
    pvec = []
    g1 = np.round(5*np.random.random([nrep, nqs]))
    g2 = np.round(5*np.random.random([nrep, nqs]))
    for ii in range(nqs):
        t, p = ttest(g1[:, ii], g2[:, ii])
        pvec.append(p)
    return pvec


def rep_test_ttest(nrep, nqs, reps):
    pval_vec = []
    for ireptest in range(reps):
        p = test_ttest(nrep, nqs)
        pval_vec.append(np.min(p))
    pval_vec = np.array(pval_vec)
    return np.mean(pval_vec < .05)


def np_array_flt_int(ar):
    return np.array([int(val) for val in ar])


def ttest_single_split(data, split_index):
    y_index = data[:, split_index] == 'Yes'
    n_index = data[:, split_index] == 'No'
    for ii in range(data.shape[1]):
        if ii == split_index:
            continue
        y_data = data[y_index, ii] == 'Yes'
        n_data = data[n_index, ii] == 'Yes'
        if len(n_data) < 2 or len(y_data) < 2:
            continue
        tvalue, pvalue = ttest(y_data, n_data)
        if pvalue < .05 and tvalue != -np.inf:
            print("""
            If you like {0}, there is a {1}% chance that you like {2}
            If you don't like {0}, there is a {3}% chance that you like {2}
            Pvalue = {4}
            """.format(data[0, split_index], np.round(100*np.mean(y_data), 2),
                       data[0, ii], np.round(100 * np.mean(n_data), 2), np.round(pvalue, 2)
                       )
                  )


d = np.array(deal_with_data(rd))
d = d[:, 1:d.shape[1]]
cols_to_test = range(d.shape[1])
for i in cols_to_test:
    ttest_single_split(d, i)
