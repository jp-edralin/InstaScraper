import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from followerScraper import followerList

def numberFormat(x):
    
    if x[-1] == 'k':
        output = x[:-1]
        output = int(output.replace('.',''))*100
    elif x[-1] == 'm':
        output = x[:-1]
        output = int(output.replace('.',''))*100000
    else:
        output = int(x.replace(',',''))

    return output
    
df_names = pd.DataFrame(columns = ['Name','FirstName','Handle','FollowerCount','FollowingCount','Ratio'])
row = 0;

while row < len(followerList):
    print(row)
    
    #specify the url
    url = 'https://instagram.com/'+followerList[row]

    #query the website and return the html to the variable 'page'
    try:
        page = urllib.request.urlopen(url)
    except urllib.request.HTTPError:
        break
    #page = Request(url)

    #parse the html using beautiful soup and store in variable 'soup'
    html = BeautifulSoup(page,'html.parser')

    #extract title
    title = html.find('title').text.strip()

    #extract name
    name = title.split(' (')[0]
    firstName = name.split(' ')[0].capitalize()

    #extract handle
    handle = title[title.find("(")+1:title.find(")")]

    #get follower count
    content = html.find('meta',attrs={'name':'description'})['content'].split()
    follower_count = numberFormat(content[0])    

    #get following count
    following_count = numberFormat(content[2])
    
    #get ratio
    ratio = round(follower_count/following_count,3)

    #add to dataframe
    df_names.loc[row] = [name,firstName,handle,follower_count,following_count,ratio]
    row+=1  

#merge names csv with dataframe
df_names = pd.read_csv("testNames.csv")
df_baby = pd.read_csv("babyNames.csv")

df_joint = pd.merge(df_names, df_baby[["name", "sex"]], how="left", left_on = "FirstName", right_on = "name")
df_joint_edited = df_joint

