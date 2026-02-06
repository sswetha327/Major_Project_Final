from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Create analyzer object (loads VADER lexicon internally)
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    
    # Check for explicit negative indicators
    negative_words = ['not', 'no', 'never', 'none', 'nothing', 'nowhere', 'neither', 'nobody', 'cannot', "can't", "won't", "don't", "didn't", "doesn't", "isn't", "aren't", "wasn't", "weren't"]
    positive_words = ['good', 'great', 'excellent', 'amazing', 'fantastic', 'wonderful', 'perfect', 'love', 'best', 'awesome']
    negative_descriptors = ['bad', 'terrible', 'awful', 'horrible', 'disappoint', 'worse', 'worst', 'poor', 'cheap', 'flaw', 'issue', 'problem', 'damage', 'not impressed', 'questionable', 'mediocre']
    neutral_indicators = ['okay', 'ok', 'average', 'decent', 'fair', 'could be better', 'some minor issues']
    
    text_lower = text.lower()
    
    # Check for explicit negative sentiment patterns
    if any(word in text_lower for word in negative_words) and any(word in text_lower for word in positive_words):
        # Negation of positive words (e.g., "not good", "not amazing")
        return "Negative"
    elif any(word in text_lower for word in negative_descriptors):
        # Direct negative descriptors
        return "Negative"
    elif any(phrase in text_lower for phrase in neutral_indicators):
        # Neutral indicators
        return "Neutral"
    elif compound >= 0.1:  # Increased threshold for positive
        return "Positive"
    elif compound <= -0.05:  # Keep threshold for negative
        return "Negative"
    else:
        return "Neutral"


# TEST BLOCK — to check if this file works alone
if __name__ == "__main__":
    print(analyze_sentiment("This phone is amazing"))
    print(analyze_sentiment("Worst phone ever"))
    print(analyze_sentiment("Phone is okay"))

