from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
nltk.download("vader_lexicon")
nltk.download('stopwords')
import re

def getScoreSentiment(text):
    sia = SentimentIntensityAnalyzer()
    clean=re.sub(r'[^\w\s]','',text)
    aux = set(clean.split(" ")) - set(stopwords.words('english'))
    aux = ' '.join(aux)
    scores = sia.polarity_scores(aux)
    return scores