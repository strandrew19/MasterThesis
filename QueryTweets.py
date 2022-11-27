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
    
#Grab information on all retweeters (Name, Description Bio and # of Followers)
main_retweeters_extended = "../Tweet_Retweeters/TwitterHandelsExtended/"
os.chdir(main_retweeters)
list_for_dataframe = []
for dataframe in os.listdir():
    if dataframe[-3:] == 'csv':
        username_df = pd.read_csv(dataframe)
        username_list = username_df[dataframe[:8]].to_list()
        #returns a dictionary with bio information 
        user_dict = get_user_information(username_list)
        #iterate through the dictionary to get user's bio, age and followers
        for user in user_dict:
            #Values are a list: [following, followers, join_date, birthday, location, website, desc]
            list_for_dataframe.append({'Name':user, 'Bio':user_dict[user][6], 'Followers':user_dict[user][1]})
        Extended_Df = pd.DataFrame(list_for_dataframe)
        os.chdir(main_retweeters_extended)
        Extended_Df.to_csv(dataframe)
        os.chdir(main_retweeters)
        list_for_dataframe.clear()
    
input_data = '../Tweet_Retweeters/TwitterHandelsExtended'
neighbours_output = '../Tweet_Retweeters/Neighbors'

#Get min(50, followers) from each of the retweeters to build a full social networks (capped at 50 due to enormous number of retweeters)
os.chdir(main_retweeters_extended)
 
for dataframe in os.listdir():
    print(dataframe)
    if dataframe[-3:] == 'csv':
        target_df = pd.read_csv(dataframe)
        follower_max = 50
        list_of_dicts = []
        print(len(target_df.Name.to_list()))
        list_of_dicts.append(get_users_followers(target_df.Name.to_list()[:], env=env_path, limit=50, write_out=False))
        Results_df = pd.DataFrame(list_of_dicts)
        os.chdir(neighbours_output)
        Results_df.to_csv(f'{dataframe}')
        os.chdir(input_data)
        list_of_dicts.clear
        
retweet_Neighbors = "../Neighbors/"
os.chdir(retweet_Neighbors)   
list_of_names = []
for dataframe in os.listdir():
    if dataframe[-3:] == 'csv':
        data = pd.read_csv(dataframe)
        data = data.loc[:, data.columns.drop(data.columns[0])]
        data = data.transpose()   
        for i in data[0]:
            if i:
                # print(i)
                list_of_names += i.split("'")[1::2]
retweet_subNeighbors = "../SubNeighbors/"
os.chdir(retweet_Neighbors)         
pd.DataFrame(list(set(list_of_names)), columns=['Names']).to_csv('FullNameSet.csv')    
