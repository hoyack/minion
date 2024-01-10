# compare.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import Fore, Style

def calculate_similarity(text1, text2):
    """
    Calculate the cosine similarity between two pieces of text.

    Args:
    text1 (str): The first piece of text.
    text2 (str): The second piece of text.

    Returns:
    float: The cosine similarity between the two texts, scaled to 0-100.
    """
    print("Vectorozing Text")
    print(Fore.BLUE + "TEXT 1:" + Style.RESET_ALL)
    print(text1)
    print(Fore.GREEN + "TEXT 2:" + Style.RESET_ALL)
    print(text2)
    # Vectorizing the text using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculating cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Converting similarity to percentage
    return similarity * 100

# The function can be tested with sample data like this:
# print(calculate_similarity("Sample text one.", "Sample text two."))
