import glob
import pandas as pd

jaams = {}
for file in glob.glob('data/jaams/*.txt'):
	df = pd.read_csv(file)
	jaams[file.split('/')[-1][:-4]] = df

#possible interesting column names
col_names = ['AWARD_ID', 
    'SUGGESTED_AWARD_NO',
    'REQ_AWARD_ID', 
    'CLM_DOCUMENT_NUMBER',
    'MERCHANT_DOCUMENT_NUMBER',
    'PAYMENT_DOCUMENT_ID',
    'DOCUMENT_TYPE_CODE',
    'DOCUEMNT_SUB_TYPE']

for k, v in jaams.iteritems():
    print ('{}: '.format(k))
    for col in col_names:
        try:
            v[col]
            print ('unique {} values:'.format(col))
            print (pd.unique(v[col].values.ravel()))
        except:
            pass
    print ('')

