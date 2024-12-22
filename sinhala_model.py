# Spelling Corrector and Grammar Checker for Sinhala

# Required Libraries
import re
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import wordnet

import json

class SinhalaSpellChecker:
    def __init__(self, word_file="C:/Users/Malith/OneDrive/Desktop/AI mini project/sinhala_words.json"):
        self.spell = SpellChecker(language=None)
        with open(word_file, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        valid_words = [word["word"] for word in words_data if word["label"] == 1]
        for word in valid_words:
            self.spell.word_frequency.add(word)

    def check_spelling(self, text):
    # Tokenize the input text
        tokens = word_tokenize(text)
        
        # Identify misspelled words
        misspelled = self.spell.unknown(tokens)
        corrections = {}
        
        # Generate corrections for misspelled words
        for word in misspelled:
            correction = self.spell.correction(word)
            if correction:  # Ensure correction is not None
                corrections[word] = correction

        # Apply corrections to the text
        corrected_text = text
        for word, correction in corrections.items():
            if word and correction:  # Ensure both are valid
                corrected_text = re.sub(rf"\b{re.escape(word)}\b", correction, corrected_text)
        
        return corrected_text, corrections



class SinhalaGrammarChecker:
    def __init__(self, dataset_file="C:/Users/Malith/OneDrive/Desktop/AI mini project/sinhala_grammar.json"):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        with open(dataset_file, 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)

    def train_model(self):
        sentences = [item["sentence"] for item in self.dataset]
        labels = [item["label"] for item in self.dataset]
        X = self.vectorizer.fit_transform(sentences)
        self.classifier.fit(X, labels)

    def check_grammar(self, text):
        corrections = {}
        X = self.vectorizer.transform([text])
        prediction = self.classifier.predict(X)[0]
        if prediction != "correct":
            corrections[text] = f"Detected error: {prediction}"
        return corrections


# Evaluation Function
def evaluate_model(spell_checker, grammar_checker, paragraphs):
    accuracy_results = []

    for paragraph in paragraphs:
        corrected_text, spell_corrections = spell_checker.check_spelling(paragraph)
        grammar_corrections = grammar_checker.check_grammar(corrected_text)

        total_corrections = len(spell_corrections) + len(grammar_corrections)
        accuracy_results.append({
            "original": paragraph,
            "corrected": corrected_text,
            "spell_corrections": spell_corrections,
            "grammar_corrections": grammar_corrections,
            "total_corrections": total_corrections
        })

    return accuracy_results

# Example Main Program
def main():
    # Initialize components
    spell_checker = SinhalaSpellChecker()
    grammar_checker = SinhalaGrammarChecker()

    # Train grammar model
    grammar_checker.train_model()

    # Evaluate on given paragraphs
    paragraphs = [
        "මම පාඩම්කරනව.",
        "ඔබගෙදර යනවා.",
        "ඔහු පටන්ගත්තේ නැත.",
        "කතා කරනමිනිසුන්ගෙ ආකෘති වැරදියි.",
        "අපිගෙදරපිටට යන්න සූදානම්.",
    ]

    results = evaluate_model(spell_checker, grammar_checker, paragraphs)
    for result in results:
        print("Original:", result["original"])
        print("Corrected:", result["corrected"])
        print("Spell Corrections:", result["spell_corrections"])
        print("Grammar Corrections:", result["grammar_corrections"])
        print("Total Corrections:", result["total_corrections"])
        print("-" * 50)

if __name__ == "__main__":
    main()
