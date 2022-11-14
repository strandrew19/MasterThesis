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

#Tweets of Interest
Tweets_and_Dates = {'https://twitter.com/RobertKennedyJr/status/1567255994597605376':'06.09.22',
'https://twitter.com/RobertKennedyJr/status/1570118647825272836':'14.09.22',
'https://twitter.com/RobertKennedyJr/status/1572273992052121605':'20.09.22',
'https://twitter.com/RobertKennedyJr/status/1573736774265761792':'24.09.22',
'https://twitter.com/RobertKennedyJr/status/1575221570959593472':'28.09.22',
'https://twitter.com/RobertKennedyJr/status/1575847936516161536':'30.09.22',
'https://twitter.com/RobertKennedyJr/status/1577305009863249920':'04.10.22'
}

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

#Rename Column to correspond to the date and write to csv
main_retweeters = "../Tweet_Retweeters/TwitterHandels/"
os.chdir(main_retweeters)
for dict_key in Tweets_and_Dates:
    Tweets_and_Dates[dict_key].rename(columns={"RobertKennedyJr": f"{Tweets_and_Dates[dict_key]}"}, errors="raise")
    Tweets_and_Dates[dict_key].to_csv(f'{Tweets_and_Dates[dict_key]}.csv')

#
main_retweeters_info = "../Tweet_Retweeters/TwitterHandelsExtended/"
main_retweeters = "../Tweet_Retweeters/TwitterHandelsExtended/"
os.chdir(main_retweeters)
get_user_information


name_list = []
dup_list = []
for dataset in os.listdir():
    print(dataset)
    dataframe = pd.read_csv(dataset)
    for i in range(len(dataframe)):
        if dataframe.Name[i] in name_list:
            dup_list.append(i)
        name_list.append(dataframe.Name[i])
    dataframe = dataframe.drop(dataframe.index[dup_list]).reset_index(drop=True)
    dataframe = dataframe.drop(dataframe.columns[0], axis=1)
    dataframe.to_csv(dataset)