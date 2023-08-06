import pandas as pd
import numpy as np
def manna(a):
    a=a+".csv"
    df = pd.read_csv(a)
    df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
    df.index = df['Date']
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])

    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]
    train = new_data[:987]
    valid = new_data[987:]
    preds = []
    for i in range(0,valid.shape[0]):
        a = train['Close'][len(train)-248+i:].sum() + sum(preds)
        b = a/248
        preds.append(b)
    rms=np.sqrt(np.mean(np.power((np.array(valid['Close'])-preds),2)))
    return(rms)