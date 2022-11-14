# Master Thesis

This Repository contains code for my Masters Thesis, "Modeling disinformation with spatial modeling" for Universität Trier. The dataset used in the Master Thesis is avalible in an obfuscated format due to data protection rules and Terms of Service from Twitter.

Special Thanks to https://github.com/Altimis for the open source package Scweet. A forked version of the repository is avalible under https://github.com/strandrew19/Scweet which extends the functionality of the package with the function get_retweeters to grab all individuals that have retweeted a particular tweet. 

<details><summary>Using get_retweeters from strandrew19/Scweet</summary>
<p>
  
To enable the get_retweeters function, ensure that the .env variable has been set to enable logins for twitter scraping (instructions are avalible under the github repo)

get_retweeters has been modeled after get_users_following, get_users_followers and thus all variables are comparable except for the addition of tweets. 

To invoke get_retweeters using the example below:

tweets_dict = {'TwitterUsername':['Number corresponding to tweet']}
test = get_retweeters(list(tweets_dict.keys()), tweets_dict, env_path, headless=False, file_path=repo)

The values of the dictionary correspond to the tweet number that comes immediately after the status.

Remeber to set file_path variable as well to ensure the file will be written out (in json format)
  
</p>
</details>
