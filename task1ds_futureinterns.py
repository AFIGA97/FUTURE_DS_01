# -*- coding: utf-8 -*-


import pandas as pd

# Load the dataset
df = pd.read_csv('/content/sentimentdataset.csv')

# Show basic info
df.info()

# Show first few rows
df.head()

df.head()

df.info()

# Drop unnecessary columns
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

# Check for missing values
print(df.isnull().sum())

# Fill or drop missing values if needed
df = df.dropna(subset=['Text'])  # make sure Text is not null

# Reset index
df.reset_index(drop=True, inplace=True)

# Quick check
df.head()

from textblob import TextBlob

# Calculate polarity score
df['Polarity'] = df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Categorize sentiment
def classify_sentiment(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

df['Predicted_Sentiment'] = df['Polarity'].apply(classify_sentiment)

# Compare with original
df[['Text', 'Sentiment', 'Predicted_Sentiment']].head()

from collections import Counter

# Convert all hashtags to lowercase and split them
all_hashtags = df['Hashtags'].str.lower().str.replace('#', '').str.split()
flat_list = [hashtag for sublist in all_hashtags for hashtag in sublist]

# Count frequencies
hashtag_counts = Counter(flat_list)

# Convert to DataFrame for plotting
hashtag_df = pd.DataFrame(hashtag_counts.items(), columns=['Hashtag', 'Count']).sort_values(by='Count', ascending=False)

hashtag_df.head(10)

!pip install matplotlib seaborn wordcloud

import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Sentiment distribution
sns.countplot(data=df, x='Sentiment')
plt.title("Sentiment Distribution")
plt.show()

# WordCloud of hashtags
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(flat_list))
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Hashtags")
plt.show()

# Sentiment Distribution by Platform
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Platform', hue='Sentiment')
plt.title("Sentiment by Platform")
plt.xlabel("Platform")
plt.ylabel("Number of Posts")
plt.legend(title='Sentiment')
plt.show()

#Sentiment Distribution by Country
plt.figure(figsize=(12, 6))
top_countries = df['Country'].value_counts().head(10).index
sns.countplot(data=df[df['Country'].isin(top_countries)], x='Country', hue='Sentiment')
plt.title("Sentiment by Country (Top 10)")
plt.xticks(rotation=45)
plt.show()

#Sentiment by Hour of the Day
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='Hour', hue='Sentiment', palette='viridis')
plt.title("Sentiment by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Number of Posts")
plt.show()

import pandas as pd

# Load your dataset (assuming it's already in `df`)
df = df.copy()

# Split the hashtags string into a list of hashtags
df['Hashtag_List'] = df['Hashtags'].apply(lambda x: x.split())

# Explode the list into multiple rows (1 hashtag per row)
hashtags_df = df.explode('Hashtag_List')

# Rename for clarity
hashtags_df = hashtags_df.rename(columns={'Hashtag_List': 'Hashtag'})

# Drop empty hashtags (in case)
hashtags_df = hashtags_df[hashtags_df['Hashtag'].notnull() & (hashtags_df['Hashtag'] != '')]

# Count top hashtags
top_hashtags = hashtags_df['Hashtag'].value_counts().reset_index()
top_hashtags.columns = ['Hashtag', 'Count']

# Export this to CSV for Tableau
top_hashtags.to_csv('top_hashtags.csv', index=False)

import pandas as pd

# Load your dataset
# Assuming your data is in 'sentimentdataset.csv'
df = pd.read_csv('sentimentdataset.csv')

# Now you can copy it
df = df.copy()

# Split the hashtags string into a list of hashtags
df['Hashtag_List'] = df['Hashtags'].apply(lambda x: x.split())

# Explode the list into multiple rows (1 hashtag per row)
hashtags_df = df.explode('Hashtag_List')

# Rename for clarity
hashtags_df = hashtags_df.rename(columns={'Hashtag_List': 'Hashtag'})

# Drop empty hashtags (in case)
hashtags_df = hashtags_df[hashtags_df['Hashtag'].notnull() & (hashtags_df['Hashtag'] != '')]

# Count top hashtags
top_hashtags = hashtags_df['Hashtag'].value_counts().reset_index()
top_hashtags.columns = ['Hashtag', 'Count']

# Export this to CSV for Tableau
top_hashtags.to_csv('top_hashtags.csv', index=False)
