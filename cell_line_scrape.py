from bs4 import BeautifulSoup
import requests, time

# This file creates the get_soup and from_soup functions used throughout the project
# This code creates the user interface that allows for searching of the cells in the terminal

def get_soup(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup
    
def from_soup(soup, myCellsList):
    cellsList = soup.find_all('li', {'class' : 'product clearfix'}) #finding all cell html into a list
    
    for i in range (len(cellsList)): #iterating through each cell entry html
        ottdDict = {} 
        ottdDict['Name'] = cellsList[i].h3.text.strip() #gets the generic name and ATCC name into the format '10.014 pRSV-T  <ATCCr CRL-11515T> or '143B  (ATCCr CRL-8303T)
        genName = ottdDict['Name'].split('(ATCC')[0].strip()
        ATCCName = ottdDict['Name'].split('(ATCC')[1]
        if 'CRL' in ATCCName:
            ATCCName = ATCCName.split('CRL-')
            #print (ottdDict['Name'])
            ATCCName = ATCCName[1].replace(')','')
            ATCCList = list(ATCCName)
            ATCCList.pop()
            ATCCName = (''.join(ATCCList))
            ATCCName = ' (ATCC CRL-' + ATCCName + ')'
        elif 'CCL' in ATCCName:  
            ATCCName = ATCCName.split('CCL-')
            ATCCName = ATCCName[1].replace(')','')
            ATCCList = list(ATCCName)
            ATCCList.pop()
            ATCCName = (''.join(ATCCList))
            ATCCName = ' (ATCC CCL-' + ATCCName + ')'

        elif 'HTB' in ATCCName:  
            ATCCName = ATCCName.split('HTB-')
            ATCCName = ATCCName[1].replace(')','')
            ATCCList = list(ATCCName)
            ATCCList.pop()
            ATCCName = (''.join(ATCCList))
            ATCCName = ' (ATCC HTB-' + ATCCName + ')'
        else:
            ottdDict['GenName'] = genName
            ottdDict ['ATCCName'] = ''
        
        ottdDict['GenName'] = genName
        ottdDict ['ATCCName'] = ATCCName
        #ottd stands for organ, type, tissue, disease
        
        
              
        
        ottd = cellsList[i].find_all('strong') #grabs values that are present out of org, type, tiss, and dis
        
        k = 1
        ottdList = []
        while k < len(ottd):
            ottdList.append (ottd[k].get_text())
            k += 1
        #ottdList result is in the format['Organism:', 'Cell Type:', 'Tissue:', 'Disease:']    
        
        for l in range(len(ottdList)): #strips the ottdList elements of the colon
            ottdList[l] = ottdList[l].strip(':')#result for ottdList is in the format ['Organism', 'Cell Type', 'Tissue', 'Disease']
         
        abcdList = []     
        abcd = cellsList[i].find_all('em') #grabs values for org, type, tiss, and disease
        
        for item in abcd:
            abcdList.append(item.text.strip()) #result is in the format {'Homo sapiens, human', 'Bone, 'Osteosarcoma'}
 
        
        #start adding to ottdDict 
        
        if len(abcdList) == 4: #all attributes present (ottd)
            ottdDict['Organism'] = abcdList[0]
            ottdDict['Cell Type'] = abcdList[1]
            ottdDict['Tissue'] = abcdList[2]
            ottdDict['Disease'] = abcdList[3]
            
        elif len(abcdList) == 1: #only organism is present
            ottdDict['Organism'] = abcdList[0]
            ottdDict['Cell Type'] = 'N/A'
            ottdDict['Tissue'] = 'N/A'
            ottdDict['Disease'] = 'N/A'
            
        #3 attributes present (-Disease)    
        elif len(abcdList) == 3:
            if 'Organism' in ottdList and 'Cell Type' in ottdList and 'Tissue' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = abcdList[1]
                ottdDict['Tissue'] = abcdList[2]
                ottdDict['Disease'] = 'N/A'
            
        #3 attributes present (-Tissue)    
            
            elif 'Organism' in ottdList and 'Cell Type' in ottdList and 'Disease' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = abcdList[1]
                ottdDict['Disease'] = abcdList[2]   
                ottdDict['Tissue'] = 'N/A'    
            
        #3 attributes present (-Type)    
            
            elif 'Organism' in ottdList and 'Tissue' in ottdList and 'Disease' in ottdList:
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Tissue'] = abcdList[1]
                ottdDict['Disease'] = abcdList[2]   
                ottdDict['Cell Type'] = 'N/A'        
            
        #2 attributes present (Org and Type)    

        elif len(abcdList) == 2:    
            if 'Organism' in ottdList and 'Cell Type' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = abcdList[1]
                ottdDict['Tissue'] = 'N/A'
                ottdDict['Disease'] = 'N/A'
            
        #2 attributes present (Org and Tissue)    
            
            elif 'Organism' in ottdList and 'Tissue' in ottdList: 
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Cell Type'] = 'N/A'
                ottdDict['Disease'] = 'N/A'   
                ottdDict['Tissue'] = abcdList[1]    
            
        #2 attributes present (Org and Disease)    
            
            elif 'Organism' in ottdList and'Disease' in ottdList:
                ottdDict['Organism'] = abcdList[0]
                ottdDict['Tissue'] = 'N/A'
                ottdDict['Disease'] = abcdList[1]   
                ottdDict['Cell Type'] = 'N/A'

        elif len(abcdList) == 0:
            ottdDict['Organism'] = 'N/A'
            ottdDict['Tissue'] = 'N/A'
            ottdDict['Disease'] = 'N/A'   
            ottdDict['Cell Type'] = 'N/A'    
   
        myCellsList.append(ottdDict)  
    
    
    return myCellsList    
    
def print_cell(srchblCL, celValStr, page = 1): #remove page default?
    celValList = [int(e) for e in celValStr.split()]
    str1 = ', '.join(str(e) for e in celValList)
    print()
    print ()
    print ((' Results for search of ' + str1 +' on page ' + str(page)).center(80, '*'))
    print ()

    
    for item in celValList:
        print (('').center(80, '*'))
        print ('Generic Name: ' + srchblCL[item-1]['GenName'])
        print ('ATCC Name: ' + srchblCL[item-1]['ATCCName'])
        print ('Organism: ' + srchblCL[item-1]['Organism'])
        print ('Cell Type: ' + srchblCL[item-1]['Cell Type'])
        print ('Tissue: ' + srchblCL[item-1]['Tissue'])
        print ('Disease: ' + srchblCL[item-1]['Disease'])
        print ()
        print ()
    
def main():
    lst = []
    urls = ['http://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx']#gets first url pages
    for i in range (2,123): #completes url list for all 121 pages
        urls.append('https://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx?dsNav=Ro:'+str(i*10-10)+',Ns:P_Product_Name%7c101%7c1%7c')
    print ()
    print ()
    print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))

    print ()
    num = [0,'1']
    print (('Page 1').center(80,'*')) 
    gotSoup = get_soup(urls[0]) #main page
    from_soup (gotSoup, lst) #main page
   
    for i in range (len(lst)): #main page 
        genName = lst[i]['Name'].split('(ATCC')[0].strip()
        ATCCName = lst[i]['Name'].split('(ATCC')[1]
        if 'CRL' in lst[i]['Name']:
            ATCCName = ATCCName.split('CRL-')
            ATCCName = ATCCName[1].replace(')','')
            ATCCList = list(ATCCName)
            ATCCList.pop()
            ATCCName = (''.join(ATCCList))
            ATCCName = ' (ATCC CRL-' + ATCCName + ')'
        elif 'CCL' in lst[i]['Name']:  
            ATCCName = ATCCName.split('CCL-')
            ATCCName = ATCCName[1].replace(')','')
            ATCCList = list(ATCCName)
            ATCCList.pop()
            ATCCName = (''.join(ATCCList))
            ATCCName = ' (ATCC CCL-' + ATCCName + ')'

        elif 'HTB' in lst[i]['Name']:  
            ATCCName = ATCCName.split('HTB-')
            ATCCName = ATCCName[1].replace(')','')
            ATCCList = list(ATCCName)
            ATCCList.pop()
            ATCCName = (''.join(ATCCList))
            ATCCName = ' (ATCC HTB-' + ATCCName + ')'    
        print (str(i+1) + ': ' + genName + ATCCName)
    
    
    
    
 
    go = True
    
    
    while go:
        print ()
        print ()
        ask1 = input ("Enter numbers separated by spaces, select page number by typing 'p' followed by the number (ex. p9), press enter to select all, or type 'esc' to exit: ") #Numbers separated as spaces look like '1 2 3' #, enter 'n' for next page, or return to select all: 
    
        #used to determine if input is string with integer values
        invalid = False
        intStr = ask1.replace(' ', '') #format '15910'
    
        if ',' in ask1:
            print ('Invalid Entry: ' + ask1)
            go = True
            
        elif ask1: #what to do if value is entered     
            if ask1 == 'esc':
                go = False
                break
                
            #elif intStr == 'n'
            elif 'p' in ask1:
                print ()
                print ()
                print('*'.center(80,'*'))
                num = ask1.split('p')
                if not int(num[1]) > 0 and int(num[1]) < 123:
                    print ('Invalid Entry: '+ ask1)
                    go = True
                else:
                    print (('Page ' + num[1]).center(80,'*'))
                    lst = []
                    gotSoup = get_soup(urls[int(num[1])-1]) #entered page
                    from_soup (gotSoup, lst)          
                   
                    for i in range (len(lst)): #entered page 
                        genName = lst[i]['Name'].split('(ATCC')[0].strip()
                        ATCCName = lst[i]['Name'].split('(ATCC')[1]                   
                        if 'CRL' in ATCCName:
                            ATCCName = ATCCName.split('CRL-')
                            ATCCName = ATCCName[1].replace(')','')
                            ATCCList = list(ATCCName)
                            ATCCList.pop()
                            ATCCName = (''.join(ATCCList))
                            ATCCName = ' (ATCC CRL-' + ATCCName + ')'
                        elif 'CCL' in ATCCName:  
                            ATCCName = ATCCName.split('CCL-')
                            ATCCName = ATCCName[1].replace(')','')
                            ATCCList = list(ATCCName)
                            ATCCList.pop()
                            ATCCName = (''.join(ATCCList))
                            ATCCName = ' (ATCC CCL-' + ATCCName + ')'

                        elif 'HTB' in ATCCName:  
                            ATCCName = ATCCName.split('HTB-')
                            ATCCName = ATCCName[1].replace(')','')
                            ATCCList = list(ATCCName)
                            ATCCList.pop()
                            ATCCName = (''.join(ATCCList))
                            ATCCName = ' (ATCC HTB-' + ATCCName + ')'   

                        else:
                            ATCCName = ''
                        print (str(i+1) + ': ' + genName + ATCCName)

            
            elif not intStr.isdigit():    
                print ('Invalid Entry: ' + ask1)
                go = True
                
            else: #if string contains integers we search for value 
                checkVals = [int(e) for e in ask1.split()]
                for i in range(len(checkVals)):
                    if checkVals[i] > len(lst) or checkVals[i] < 0:
                        print ('Invalid Entry: ' + str(checkVals[i]))
                        go = True
                        invalid = True
                        
                while not invalid:
                    try:
                        print_cell (lst, ask1, num[1])
                    except:
                        print_cell (lst,ask1)
                    print()
                    ask2 = input ("Press enter to return or type 'esc' to quit: ") #needs to be edited for additional pages
                    print ()
                    if not ask2: #if returning
                        str1 = ', '.join(str(e) for e in intStr)
                        print ()
                        print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
                        # Allow for all pages to be printed with the header 
                        print ()
                        print (('Page ' + num[1]).center(80,'*'))
                        for i in range (len(lst)):
                            genName = lst[i]['Name'].split('(')[0].strip()
                            ATCCName = lst[i]['Name'].split('(')[1]
                            if 'CRL' in ATCCName:
                                ATCCName = ATCCName.split('CRL-')
                                ATCCName = ATCCName[1].replace(')','')
                                ATCCList = list(ATCCName)
                                ATCCList.pop()
                                ATCCName = (''.join(ATCCList))
                                ATCCName = ' (ATCC CRL-' + ATCCName + ')'
                            elif 'CCL' in ATCCName:  
                                ATCCName = ATCCName.split('CCL-')
                                ATCCName = ATCCName[1].replace(')','')
                                ATCCList = list(ATCCName)
                                ATCCList.pop()
                                ATCCName = (''.join(ATCCList))
                                ATCCName = ' (ATCC CCL-' + ATCCName + ')'

                            elif 'HTB' in ATCCName:  
                                ATCCName = ATCCName.split('HTB-')
                                ATCCName = ATCCName[1].replace(')','')
                                ATCCList = list(ATCCName)
                                ATCCList.pop()
                                ATCCName = (''.join(ATCCList))
                                ATCCName = ' (ATCC HTB-' + ATCCName + ')'   

                            else:
                                ATCCName = ''
                            print (str(i+1) + ': ' + genName + ATCCName)
                        go = True
                        break
                    elif ask2 == 'esc':
                        go = False
                        break
                    
                    else:
                        print ('Invalid Entry: ' + ask2)
                        print ('Goodbye')
                        go = False
                        break  
        
        elif not ask1: #executed for select all
            print_cell(lst, ' '.join([str(e+1) for e in list(range(10))]))
            print ()
            ask2 = input ("Press enter to return or type 'esc' to quit: ") #needs to be edited for additional pages
            print ()
            if not ask2:
                print ()
                print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
                # Allow for all pages to be printed with the header 
                print ()
                print (('Page '+ num[1]).center(80,'*'))
                for i in range (len(lst)):
                    genName = lst[i]['Name'].split('(')[0].strip()
                    ATCCName = lst[i]['Name'].split('(')[1]
                    if 'CRL' in lst[i]['Name']:
                        ATCCName = ATCCName.split('CRL-')
                        ATCCName = ATCCName[1].replace(')','')
                        ATCCList = list(ATCCName)
                        ATCCList.pop()
                        ATCCName = (''.join(ATCCList))
                        ATCCName = ' (ATCC CRL-' + ATCCName + ')'
                    elif 'CCL' in lst[i]['Name']:  
                        ATCCName = ATCCName.split('CCL-')
                        ATCCName = ATCCName[1].replace(')','')
                        ATCCList = list(ATCCName)
                        ATCCList.pop()
                        ATCCName = (''.join(ATCCList))
                        ATCCName = ' (ATCC CCL-' + ATCCName + ')'

                    elif 'HTB' in lst[i]['Name']:  
                        ATCCName = ATCCName.split('HTB-')
                        ATCCName = ATCCName[1].replace(')','')
                        ATCCList = list(ATCCName)
                        ATCCList.pop()
                        ATCCName = (''.join(ATCCList))
                        ATCCName = ' (ATCC HTB-' + ATCCName + ')'   

                    else:
                        ATCCName = ''
                   
                    print (str(i+1) + ': ' + genName + ATCCName)
                go = True
                
            elif ask2 == 'esc':
                go = False
                break
            else: 
                print ('Invalid Entry: ' + ask2)
                print ('Goodbye')
                go = False
                break
        else: 
            print ('Invalid Entry: ' + ask1)
            go = True
            
            
if __name__ == '__main__':
    main()  