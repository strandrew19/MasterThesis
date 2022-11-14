import pandas as pd
import os
from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers, get_retweeters

env_path = ".env"
Scrape_Results = "../Scrape_Results/"
Tweet_Scrape_DataFrame = scrape(words=['vaccine', 'vacinated', 'COVID', 'government', 'FDA'], since="2022-09-05", until="2022-10-05", from_account = 'RobertKennedyJr',  interval=1, headless=False, save_images=False, lang="en", resume=False, filter_replies=False, proximity=False, save_dir=Scrape_Results)

#Only one scrape was done so no need to worry about overwritting Tweet_Scrape_CSV
for scrape_csv in os.listdir():
    if scrape_csv[-3:] == 'csv':
        Tweet_Scrape_CSV = pd.read_csv(scrape_csv)

Tweet_Scrape_CSV[['UserName', 'Timestamp', 'Tweet URL']]

#Content of Tweets of Interest
"""
**Sep 6th - It’s shocking that a U.S. president would involve the FBI and Homeland Security in efforts to quash dissent. The First Amendment is not there to safeguard popular speech or government-approved speech.
**Sep 9th - Leaked video shows researchers shared data w/ Israeli Ministry of Health showing serious + long-term side effects with Pfizer’s COVID vaccine, but Israeli health officials told public in an August report that serious side effects were “rare” + short-term.
**Sep 14th - A data leak suggests the real reason health officials don’t want individual vaccine vials examined by independent scientists is that the vials are all different — and the mRNA in the shots is not intact.
**Sep 20th - The paradoxical juxtaposition that has the president declaring the pandemic is over while New York City’s Department of Education fires 850 unvaccinated teachers and aids shows once again that the governmental purpose is coercion and not public health.
**Sep 24th - FDA is advertising the new COVID-19 booster as an “antibody update” to “recharge your immunity” — as if your immune system were a battery that needs recharging or a software system that requires gene therapy “updates.”
**Sep 28th - A federally funded study released Tuesday reported a “positive association” between “vaccine-related aluminum exposure” and “persistent asthma” in children 24-59 months old.
**Sep 30th - Reporting on a new study, U.S. News & World Report this week published an article, “'Breakthrough' Infections After COVID Vaccine Can Help Prevent Future Illness,” which spins vaccine failure as a reason to celebrate.
**Oct 4th - Researchers use GMO mosquitoes to vaccinate humans in an NIH-funded malaria study
"""
#Tweets of Interest
Tweets_and_Dates = {'https://twitter.com/RobertKennedyJr/status/1567255994597605376':'06.09.22',
'https://twitter.com/RobertKennedyJr/status/1570118647825272836':'14.09.22',
'https://twitter.com/RobertKennedyJr/status/1572273992052121605':'20.09.22',
'https://twitter.com/RobertKennedyJr/status/1573736774265761792':'24.09.22',
'https://twitter.com/RobertKennedyJr/status/1575221570959593472':'28.09.22',
'https://twitter.com/RobertKennedyJr/status/1575847936516161536':'30.09.22',
'https://twitter.com/RobertKennedyJr/status/1577305009863249920':'04.10.22'
}

#Full Tweet List
# Tweets_and_Dates = {'https://twitter.com/RobertKennedyJr/status/1567255994597605376':'06.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1567153741631037440':'06.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1567514991841918976':'07.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1567969449906696194':'08.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1568274289291321346':'09.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1568321718355382272':'09.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1568367394032177154':'09.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1569048758632972290':'11.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1569682332336140289':'13.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1569724335341838338':'13.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1570118647825272836':'14.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1570142033624596482':'14.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1570037393218060288':'14.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1570406580566208512':'15.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1571965228987940867':'19.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1571917960834592768':'19.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1572273992052121605':'20.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1572235786866593792':'20.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1573292023695671296':'23.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1573736774265761792':'24.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1574767082004152321':'27.09.22*',
# 'https://twitter.com/RobertKennedyJr/status/1574867433936003083':'27.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1575221570959593472':'28.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1575120590033371138':'28.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1575847936516161536':'30.09.22',
# 'https://twitter.com/RobertKennedyJr/status/1577305009863249920':'04.10.22'
# }

#With each tweet, grab all individuals that have retweeted the tweet (Use get_retweeters from forked Scweet Repo)
retweet_results = "../Tweet_Retweeters/Results/"

for tweet in range(len(Tweet_Scrape_CSV)):
    if Tweet_Scrape_CSV['Tweet URL'][tweet] in Tweets_and_Dates:
        Tweet_Scrape_CSV
        #Remove @ from Twitter Handel
        twitter_handel = Tweet_Scrape_CSV['UserName'][tweet][1:]
        tweet_id = Tweet_Scrape_CSV['Tweet URL'][tweet][-19:]
        #Dictionary rewritten because get_retweeters function doesn't yet differentiate between mutiple tweets when writting to json
        tweets_dict = {twitter_handel:tweet_id}
        #Results written to json
        get_retweeters(list(tweets_dict.keys()), tweets_dict[twitter_handel], env_path, headless=False, file_path=retweet_results)

#Read in the results of get_retweeters and put it in a pandas DataFrame
os.chdir(retweet_results)
for idx, json_file in enumerate(os.listdir()):
    if json_file[-4:] == 'json':
        #Get Tweetid
        tweet_id = Tweet_Scrape_CSV['Tweet URL'][idx][-19:]
        #DataFrames are saved coresponding to date (Easier to track)
        Tweets_and_Dates[tweet_id] = pd.read_json(json_file)

main_retweeters = "../TwitterHandels/"
os.chdir(main_retweeters)
#Rename Column to correspond to the date and write to csv 
for dict_key in Tweets_and_Dates:
    Tweets_and_Dates[dict_key].rename(columns={"RobertKennedyJr": f"{Tweets_and_Dates[dict_key]}"}, errors="raise")
    Tweets_and_Dates[dict_key].to_csv(f'{Tweets_and_Dates[dict_key]}.csv')

