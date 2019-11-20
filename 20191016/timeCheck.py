from datetime import datetime as dt

if __name__ == '__main__':

    try:
        TimeStr1 = '14:59'
        TimeObj1 = dt.strptime(TimeStr1,'%H:%M')

        TimeStr2 = dt.now().strftime('%H:%M')
        TimeObj2 = dt.strptime(TimeStr2,'%H:%M')

    except Exception as e:
        print('ErrMsg:', e)
        
  
    print(TimeObj1 == TimeObj2)

