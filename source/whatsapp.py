import re
import sys
import pandas as pd
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def extract_data(fpath):
    try:        
        with open(fpath, 'r',encoding='UTF-8') as f:
            exp = re.compile('(\d+/\d+/\d+),\s+(\d+:\d+\s+\w+)\s+-\s(\w+\s\w+\s\w+|\w+\s\w+|\w+)\:(.*?(?=\d+/\d+/\d+,\s+\d+:\d+\s+\w+))',re.DOTALL)
            strings = re.findall(exp, f.read())
        
        data = pd.DataFrame(strings,columns =['Date','Time','Sender','Message'])
        
        time24,msgs,senders = [],[],[]
        
        for _ in data['Time'].tolist():
            time24.append(datetime.strftime(datetime.strptime(_, "%I:%M %p"), "%H:%M:%S:"))
        data['Time'] = time24       
        
        for _ in data['Sender'].tolist():
            senders.append(_.replace(' ','_'))
        data['Sender'] = senders 
               
        for _ in data['Message'].tolist():
            msgs.append(_.strip().replace('\n',' '))
        data['Message'] = msgs 
        
                   
        #-----------------------------#    
        #Deleting unwanted variables
        del msgs,senders,time24,strings
        #-----------------------------#
            
        return data
    except IOError as IO:
        return IO               

def main():
    fpath = input('Enter the file path : ')
    data = extract_data(fpath)
    orig_stdout = sys.stdout
    
    #-----------------------------#    
    #Extracting data from data variable
    sendersdict,newmsgs,count = dict(),list(),0
    
    for sender in set(data['Sender'].tolist()):
        for _ in data['Sender'].tolist():
            if _ == sender:
                newmsgs.append(data['Message'].tolist()[count])
            count += 1
        sendersdict[sender],newmsgs,count = newmsgs,list(),0
    #-----------------------------# 
    
    for sender in sendersdict:
        with open('output/'+sender+'.out','w') as fo:
            print()
            print('------------------------------------------')
            print()
            print('Sender Name : {}'.format(sender))
            print('Message Count : {}'.format(len(sendersdict[sender])))
            
            wcount,ccount = 0,0
            sid = SentimentIntensityAnalyzer()
            
            for msg in sendersdict[sender]:
                wcount += len(msg.split())
                for char in msg: 
                    ccount += 1 
                ss = sid.polarity_scores(msg)
                print(msg)
                for _ in ss:
                    print('{0}: {1}, '.format(_, ss[_]), end='')
                print('\n')
         
            print('\nWord Count : {}'.format(wcount))
            print('\nCharacter Count : {}'.format(ccount))
            print()
            print('------------------------------------------')
            print()
        
if __name__ == '__main__':
    main()
    



    



