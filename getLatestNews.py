import newspaper
import textdistance

compare_with="corona Corona Virus virus covid19 Covid19 locckdown Lockdown Quarantine PM Modi quarantine doctors and nurses deaths active cases pandemic italy america spain China masks wash hands precautions India self isolation social distancing novel coraona virus Novel Corona Virus Trump donations donate Deaths Recoveries Recover Coronavirus Cases Case caseCOVID-19  "

def valid(s):
    
    
    if textdistance.hamming.normalized_similarity(s,compare_with)>0.00279:
        return True
    else:
        return False


## to implement: get similarity function commom for international and national news

##################get international news###########################################

international_titles=[]
int_news={}
def init_int_news():
    source1=newspaper.build("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/media-resources/news", memoize_articles=False)
    for i in range(8):

        who_article=source1.articles[i]
        who_article.download()
        who_article.download()
        who_article.parse()
        if valid(who_article.title):
            international_titles.append(who_article.title)
            int_news[who_article.title]=who_article.text[:]
            print( int_news[who_article.title])
    

def send_news():
    init_int_news()
    titles=[]
    news=[]
    x=len(international_titles)
    for i in range(x):
        titles.append(international_titles[i])
        print(international_titles[i])
        news.append(int_news[international_titles[i]])
        print(int_news[international_titles[i]])
    return titles,news


send_news()

#######################################################################################

##################get national news###########################################
"""
national_titles=[]
nat_news={}
source3=newspaper.build("https://www.mohfw.gov.in/", memoize_articles=False)
for i in range(8):
    ind_article=source3.articles[i]
    try:
        ind_article.download()
        ind_article.download()
        ind_article.parse()
        if valid(ind_article.title):
            print(ind_article.title)
            national_titles.append(ind_article.title)
            nat_news[ind_article.title]=ind_article.text[:]
    except:
        print("Something else went wrong")
        
"""
#######################################################################################
