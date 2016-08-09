import requests
import sqlite3, os
from bs4 import BeautifulSoup
import json
import time
from time import sleep

#This program is required for cell_Interface.py, cell_toDB.py, and json_LineScrape.py to work.

#This program creates the soup object from the ATCC cell line database, runs the user interface, creates a cells table in cell.db (if it does not currently exist), and creates a json file titled cell_LineScrpe.json (if one does not exist)

#Contributors to this code include Padraic Cunningham. His contributions can be seen at http://stackoverflow.com/questions/38670187/different-results-from-beautifulsoup-each-time/38673300?noredirect=1#comment64749316_38673300 
def from_soup():
    lst = []
    url_lst = ['http://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx']#gets first url pages
    for i in range (2,123): #completes url list for all 121 pages
        url_lst.append('https://www.atcc.org/Products/Cells_and_Microorganisms/Cell_Lines/Human/Alphanumeric.aspx?dsNav=Ro:'+str(i*10-10)+',Ns:P_Product_Name%7c101%7c1%7c')

    with requests.Session() as s:
        s.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"})

    for url in url_lst:
        soup = BeautifulSoup(s.get(url).content)
        for li in soup.select("ul.product-list li.product.clearfix"):
            name = li.select("div.product-header.clearfix a")[0].text.strip()
            name = name.replace('\xae','').replace('\u2122','')
            # print (y.replace('\xae','').replace('\u2122',''))
            d = {"Name": name}
            for div in li.select("div.search-item"):
                k = div.strong.text
                d[k.rstrip(":")] = " ".join(div.text.replace(k, "", 1).split())
            lst.append(d)
            
    for i in range (len(lst)):
        try:
            lst[i]['Name']
        except KeyError:
            lst[i]['Name'] = 'N/A'
            
        try:
            lst[i]['Organism']
        except KeyError:
            lst[i]['Organism'] = 'N/A'
            
        try:
            lst[i]['Cell Type']
        except KeyError:
            lst[i]['Cell Type'] = 'N/A'
            
        try:
            lst[i]['Disease']
        except KeyError:
            lst[i]['Disease'] = 'N/A'  

        try:
            lst[i]['Tissue']
        except KeyError:
            lst[i]['Tissue'] = 'N/A'            
    return lst
    
def printHomeMenu(lst_, pgStr):
 
    sl = []
    prntStr = (" Page " + pgStr + ' ').center(80,"*")
    print (prntStr)
    pgInt = int(pgStr)

    if pgInt == 122:
        for i in range (0,1):
            print (str(i+1) +": "+lst_[10*(pgInt-1)+i]['Name'])
        print ('')    
        ask = input ("Press enter to select all, select page number by typing 'p' followed by the number (ex. p9), or type 'esc' to exit: ")
        print ('')
        print ('')
        firstEntry = 10*(pgInt-1)
        sl.append(ask)
        sl.append(pgStr)
        sl.append(pgInt)
        sl.append(firstEntry)
        return sl
    
    else: 
        for i in range (0,10):
            print (str(i+1) +": "+lst_[10*(pgInt-1)+i]['Name'])
        print ('')    
        ask = input ("Enter choices separated by spaces, select page number by typing 'p' followed by the number (ex. p9), press enter to select all, or type 'esc' to exit: ")
        print ('')
        print('')
        firstEntry = 10*(pgInt-1)
        sl.append(ask)
        sl.append(pgStr)
        sl.append(pgInt)
        sl.append(firstEntry)
        return sl    

def cell_toDB (lst_):        
    conn = sqlite3.connect('cell.db')
    c = conn.cursor()
    
    try:
        c.execute ('CREATE TABLE cells (name, organism, tissue, type, disease)')
        
        conn.commit()
        
        for i in range (len(lst_)):
            args = []         
                
            args.append(lst_[i]['Name'])
            args.append(lst_[i]['Organism'])
            args.append(lst_[i]['Tissue'])
            args.append(lst_[i]['Cell Type'])
            args.append(lst_[i]['Disease'])
                
            c.execute('INSERT INTO cells (name, organism, tissue, type, disease) VALUES (?, ?, ?, ?, ?);', args)
            conn.commit()
    except:
        pass
    
    conn.close()  

def json_LineScrape(lst_):
    try:
        with open("cell_LineScrape.json", "r") as f:
            load_JsonFile = json.load(f)
    except FileNotFoundError:        
        with open ('cell_LineScrape.json', 'w') as f:
            json.dump(lst_, f)    
        
    return None    
        
def main ():
    lst = from_soup()  

    cell_toDB (lst)    
    json_LineScrape (lst)

    print ((time.strftime('%A, %m/%d/%Y, at %I:%M')).center(80, '*'))
    whereToGo = printHomeMenu(lst, '1')
    go = True
    while go:
        
        if whereToGo[0] == '':
            print ((' Return all on page ' + whereToGo[1] + ' ').center(80, '*'))
            if whereToGo[1] == '122':
                for i in range (0,1):
                    print ((' Entry '+ str(i+1) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                    print ('Name: '+lst[whereToGo[3]+i]['Name'])
                    print ('Organism: '+lst[whereToGo[3]+i]['Organism'])
                    print ('Tissue: '+lst[whereToGo[3]+i]['Tissue'])
                    print ('Cell Type: '+lst[whereToGo[3]+i]['Cell Type'])
                    print ('Disease: '+lst[whereToGo[3]+i]['Disease'])
                    print('')
                    
                print('')    
                ask = input("Press enter to return or type 'esc' to quit: ")
                print ('')
                print ('')
                print ('')
                if ask == '':
                    whereToGo = printHomeMenu(lst, whereToGo[1])
                elif ask == 'esc':
                    go = False
                    break
                else: 
                    print ((" Invalid entry ").center(80,"*"))
                    print ('')
                    go = False 
                    break
            else:        
                for i in range (0,10):
                    print ((' Entry '+ str(i+1) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                    print ('Name: '+lst[whereToGo[3]+i]['Name'])
                    print ('Organism: '+lst[whereToGo[3]+i]['Organism'])
                    print ('Tissue: '+lst[whereToGo[3]+i]['Tissue'])
                    print ('Cell Type: '+lst[whereToGo[3]+i]['Cell Type'])
                    print ('Disease: '+lst[whereToGo[3]+i]['Disease'])
                    print('')
                ask = input("Press enter to return or type 'esc' to quit: ")
                print ('')
                print ('')
                print ('')
                if ask == '':
                    whereToGo = printHomeMenu(lst, whereToGo[1])
                elif ask == 'esc':
                    go = False
                    break
                else: 
                    print ((" Invalid entry ").center(80,"*"))
                    print ('')
                    go = False   
                    break
                    
                
        elif 'p' in whereToGo[0]:
            x = whereToGo[0].replace('p','')
                
            if int(x)>122 or int(x)<1:
                print ((' Page number must be between 1 and 122 ').center(80,'*'))
                go = False
                                
            else:
                whereToGo = printHomeMenu (lst, x)
                
        elif whereToGo[0].replace(' ','').isdigit():
            if whereToGo[1] == "122":
            
                y = [int(i) for i in whereToGo[0].split(' ')]
                for i in range (len(y)):
                    if y[i] > 1 or y[i]<0:
                        print ((" Invalid entry ").center(80,"*"))
                        go = False
                        break     
                if go:        

                    print ((" Search of " + whereToGo[0] + " on page " + whereToGo[1] + ' ').center(80,"*")) 
                    print (('').center(80,'*'))
                    print ('')
                    for i in range (len(y)):
                        print ((' Entry '+ str(y[i]) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                        choose = y[i]-1
                        print ("Name: " + lst[whereToGo[3]+choose]["Name"])
                        print ("Organism: " + lst[whereToGo[3]+choose]["Organism"])
                        print ("Tissue: " + lst[whereToGo[3]+choose]["Tissue"])
                        print ("Cell Type: " + lst[whereToGo[3]+choose]["Cell Type"])
                        print ("Disease: " + lst[whereToGo[3]+choose]["Disease"])
                        print ('')
                    ask = input ("Press enter to return or type 'esc' to quit: ")    
                    print ('')
                    print ('')
                    print ('')
                    if ask == '':
                        whereToGo = printHomeMenu(lst, whereToGo[1])
                    elif ask == 'esc':
                        go = False   
                        break
                    else: 
                        print ((" Invalid entry ").center(80,"*"))
                        print ('')
                        go = False
                 
            else:    
                y = [int(i) for i in whereToGo[0].split(' ')]
                for i in range (len(y)):
                    if y[i] > 10 or y[i]<0:
                        print (("Invalid entry").center(80,"*"))
                        go = False
                        break     
                if go:        
                 
                    print ((" Search of " + whereToGo[0] + " on page " + whereToGo[1] + ' ').center(80,"*")) 
                    print (('').center(80,'*'))
                    print ('')
                    for i in range (len(y)):
                        print ((' Entry '+ str(y[i]) + ' on page '+ whereToGo[1] + ' ').center(80,'*'))
                        choose = y[i]-1
                        print ("Name: " + lst[whereToGo[3]+choose]["Name"])
                        print ("Organism: " + lst[whereToGo[3]+choose]["Organism"])
                        print ("Tissue: " + lst[whereToGo[3]+choose]["Tissue"])
                        print ("Cell Type: " + lst[whereToGo[3]+choose]["Cell Type"])
                        print ("Disease: " + lst[whereToGo[3]+choose]["Disease"])
                        print ('')
                    ask = input ("Press enter to return or type 'esc' to quit: ")    
                    print ('')
                    print ('')
                    print ('') 
                    
                    if ask == '':
                        whereToGo = printHomeMenu(lst, whereToGo[1])
                    elif ask == 'esc':
                        go = False   
                        break
                    else: 
                        print ((" Invalid entry ").center(80,"*"))
                        print ('')
                        go = False
                
        elif whereToGo[0] == 'esc':
            go = False
            
        else:  
            print ((" Invalid entry ").center(80,"*"))
            print ('')
            go = False

            
if __name__ == '__main__':
    main()        