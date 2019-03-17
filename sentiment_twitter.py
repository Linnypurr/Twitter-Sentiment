import tweepy
import time
import json
import matplotlib.pyplot as plot
from pandas import Series, DataFrame
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# variables
all_tweet_text = []
number_of_favorites = []
sentiment_compound = []
sentiment_positive = []
sentiment_neutral = []
sentiment_negative = []

consumer_key = "trmAZhAVY12HvpZQmEr4JJmwT"
consumer_secret = "IDyja1suL5kqdlTVoRhHki6jdesZ66js2U0unISFuhyKf7WyGD"
access_key = None
access_secret = None

# Setting up authorization
tweepy_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
tweepy_auth.set_access_token(access_key, access_secret)

twitter_api = tweepy.API(tweepy_auth, parser = tweepy.parsers.JSONParser())

# search query
search_query = '"ASMR" -filter:retweets'

twitter_data = twitter_api.search(q = search_query, count = 100, lang = 'en', result_type = 'mixed')

# print(list(twitter_data.values())[1])
# print("\n")
# print(test_list[10].get('text'))
# print(list(retrieving_twitter_data.values()))
# print(list(retrieving_twitter_data.values())[1])
all_twitter_data = twitter_data.get('statuses')


while (len(all_twitter_data) <= 10000):
    time.sleep(5)
    last_entry = all_twitter_data[-1].get('id')
    twitter_data = twitter_api.search(q=search_query, count=100, lang='en', result_type = 'mixed', max_id = 'last')
    all_twitter_data += twitter_data.get('statuses')[1:]

# print("all done\n")
for index in range(0, len(all_twitter_data)):
    all_tweet_text.append(all_twitter_data[index].get('text'))
    number_of_favorites.append(all_twitter_data[index].get('favorite_count'))
    sentiment_compound.append((analyzer.polarity_scores(all_twitter_data[index].get('text')).get('compound')))
    sentiment_positive.append((analyzer.polarity_scores(all_twitter_data[index].get('text')).get('pos')))
    sentiment_neutral.append((analyzer.polarity_scores(all_twitter_data[index].get('text')).get('neu')))
    sentiment_negative.append((analyzer.polarity_scores(all_twitter_data[index].get('text')).get('neg')))

twitter_dataframe = DataFrame({'Tweet': all_tweet_text,
                                   'Favorites': number_of_favorites,
                                   'Compound': sentiment_compound,
                                   'Positive': sentiment_positive,
                                   'Neutral': sentiment_neutral,
                                   'Negative': sentiment_negative})
twitter_dataframe = twitter_dataframe[['Tweet', 'Favorites', 'Compound', 'Positive', 'Neutral', 'Negative']]

with open("twitter_output.txt", "w") as out_file:
    twitter_dataframe.to_string(out_file)

plot.hist(sentiment_compound, bins=20, facecolor='blue')
plot.xlabel('Compound Score')
plot.xlabel('Number of Tweets')
plot.title('Sentiment Distribution')
plot.show()


abs_compound = []
top_ten_set = set()
for comp in sentiment_compound:
    abs_compound.append(abs(comp))
sorted_compound = sorted(abs_compound)

sorted_ten = sorted_compound[(len(sorted_compound) - 4001) : (len(sorted_compound) - 1)]


for comp in range((len(sorted_ten) - 1), 0, -1):
    if(len(top_ten_set) < 11):
        top_ten_set.add(sorted_ten[comp])
    else:
        break


sorted_top_ten = sorted(top_ten_set)

top_ten_set.clear()
#
for comp in sorted_top_ten:
    for list_index in range(0, len(sentiment_compound)):
        curr_comp = sentiment_compound[list_index]
        if(curr_comp == comp or curr_comp == (comp * -1)):
            text_string = str(all_tweet_text[list_index])
            comp_string = str(curr_comp)
            set_string = text_string + ' ' + comp_string + '\n'
            top_ten_set.add(set_string)


with open("twitter_output.txt", "a") as out_file:
    out_file.write("\nTop Ten Tweets\n")
    for set_item in top_ten_set:
        out_file.write(set_item)
