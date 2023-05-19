#######
# use like: python pyabsa_script.py input_data.parquet lexicon.csv  
#######
import re
import pandas as pd
# import pyabsa as pyabsa
from pyabsa import AspectPolarityClassification as APC
# from sklearn.metrics import precision_score, accuracy_score
from statistics import mean
import sys

# Define command-line arguments
if len(sys.argv) != 3:
    print("Usage: python script_name.py input_df.csv input_lexicon.txt")
    sys.exit(1)

# Read command-line arguments
input_df_path = sys.argv[1]
input_lexicon_path = sys.argv[2]

# Read input DataFrame and lexicon
df = pd.read_parquet(input_df_path)
lexicon = pd.read_csv(input_lexicon_path)
lexicon = lexicon['Lexicon'].tolist()

# Define a function that will surround the terms we want to run APC on with the needed tokens
def highlight_focuswords(string, lexicon):
    outputs = []
    for term in lexicon:
        for match in re.finditer(term, string):
            outputs.append(string[:match.start()] + '[ASP]' + term + '[ASP]' + string[match.end():])
    return outputs

# Function to convert a score to -1, 1, or 0
def categorize_score(score, negative_threshold, positive_threshold):
    if score < negative_threshold:
        return -1
    elif score > positive_threshold:
        return 1
    else:
        return 0

df = df[(df['Final_Climate_Change_Level_Label'] == 'High') | (df['Final_Climate_Change_Level_Label'] == 'Medium')].reset_index(drop=True)
df = df.drop(['Sentiment_Label', 'Sentiment_Label_R', 'Level_Climate_Change_Topic', 'Level_Climate_Change_Topic_R', 'was_I_retarded?'], axis=1)

samples = []
sample_article_index = []
for i, article in enumerate(df['Text']):
    new_samples = highlight_focuswords(article, lexicon)
    sample_article_index.extend([i] * len(new_samples))
    samples.extend(new_samples)
    print(str(article))

print(samples[23])

# Initialize classifier
classifier = APC.SentimentClassifier('english',
                                     auto_device=True,  # False means load model on CPU
                                     cal_perplexity=True,
                                     )
print("sample len: "+ str(len(df)))
print("sample len: "+ str(len(df)))
print("sample len: "+ str(len(df)))
print("sample len: "+ str(len(df)))
print("sample len: "+ str(len(df)))
print("sample len: "+ str(len(df)))

# Perform inference
apc_result = classifier.predict(samples,
                                print_result=True,  # print the result
                                ignore_error=True,  # ignore the error when the model cannot predict the input
                                )

# Map sentiment values to numerical values
sentiment_mapping = {"Positive": 1, "Negative": -1, "Neutral": 0}

# Convert inference result to a DataFrame and calculate the mean(sentiment*confidence) for each lexicon word in each inputted article
df_result = pd.DataFrame(apc_result, columns=apc_result[0])
df_result = df_result.explode(['aspect', 'sentiment', 'confidence'], ignore_index=True)
df_result['article_index'] = sample_article_index
df_result = df_result.groupby('article_index').agg({'sentiment': lambda x: list(x), 'confidence': lambda x: list(x)})
df_result['final_sentiment'] = df_result.apply(lambda row: mean([sentiment_mapping[s] * c for s, c in zip(row['sentiment'], row['confidence'])]), axis=1)

df_result['final_sentiment'] = df_result['final_sentiment'].apply(lambda x: categorize_score(x, 0, 0))
df_result['final_sentiment'].value_counts()
df



df.to_parquet(f"{input_df_path}_lexicon_{input_lexicon_path}.parquet")
