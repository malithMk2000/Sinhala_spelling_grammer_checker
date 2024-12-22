import json
from collections import Counter
import re
from difflib import get_close_matches

class SinhalaLanguageChecker:
    def __init__(self, dictionary_path):
        """Initialize with dictionary of correct Sinhala words"""
        with open(dictionary_path, 'r', encoding='utf-8') as f:
            self.dictionary = json.load(f)
        self.valid_words = {item['word'] for item in self.dictionary}
        
        # Common Sinhala grammar rules (simplified example)
        self.grammar_rules = {
            'subject_verb_agreement': r'([මම|අපි|ඔහු|ඇය|ඔවුන්])\s+\w+\s+([යි|හ|ති])',
            'sentence_end': r'.*[්|ි|ී|ු|ූ|ෙ|ේ|ො|ෝ|ෞ]\s*[.|?|!]'
        }
    
    def get_close_words(self, word, n=3):
        """Find closest matching words for a potentially misspelled word"""
        return get_close_matches(word, self.valid_words, n=n, cutoff=0.6)

    def check_spelling(self, text):
        """Check spelling in given text and return corrections"""
        words = text.split()
        corrections = []
        
        for word in words:
            if word not in self.valid_words:
                suggestions = self.get_close_words(word)
                if suggestions:
                    corrections.append({
                        'original': word,
                        'suggestions': suggestions
                    })
        
        return corrections[:5]  # Return maximum 5 corrections

    def check_grammar(self, text):
        """Check for grammatical errors in text"""
        errors = []
        
        # Check subject-verb agreement
        matches = re.finditer(self.grammar_rules['subject_verb_agreement'], text)
        for match in matches:
            subject, verb = match.groups()
            if not self._verify_subject_verb_agreement(subject, verb):
                errors.append({
                    'type': 'subject_verb_agreement',
                    'context': match.group(),
                    'message': 'Possible subject-verb agreement error'
                })

        # Check sentence endings
        sentences = re.split('[.|?|!]', text)
        for sentence in sentences:
            if sentence.strip() and not re.match(self.grammar_rules['sentence_end'], sentence):
                errors.append({
                    'type': 'sentence_structure',
                    'context': sentence,
                    'message': 'Possible incorrect sentence structure'
                })

        return errors

    def _verify_subject_verb_agreement(self, subject, verb):
        """Helper method to verify subject-verb agreement"""
        # Implement specific Sinhala grammar rules here
        # This is a simplified example
        return True  # Placeholder return

    def process_text(self, text):
        """Process text and return both spelling and grammar corrections"""
        return {
            'spelling_corrections': self.check_spelling(text),
            'grammar_errors': self.check_grammar(text),
            'original_text': text
        }

    def calculate_accuracy(self, test_paragraphs, ground_truth):
        """Calculate accuracy of corrections against ground truth"""
        total_corrections = 0
        correct_corrections = 0
        
        for i, paragraph in enumerate(test_paragraphs):
            results = self.process_text(paragraph)
            # Compare with ground truth
            # This would need to be implemented based on your specific ground truth format
            
        return (correct_corrections / total_corrections) if total_corrections > 0 else 0

def main():
    # Example usage
    checker = SinhalaLanguageChecker('C:/Users/Malith/OneDrive/Desktop/AI mini project/sinhala_words.json')
    
    test_text = """යම් සිංහල වක්‍යයක් මෙතැන ලියන්න"""
    results = checker.process_text(test_text)
    
    print("Spelling Corrections:")
    for correction in results['spelling_corrections']:
        print(f"Word: {correction['original']}")
        print(f"Suggestions: {', '.join(correction['suggestions'])}")
        
    print("\nGrammar Errors:")
    for error in results['grammar_errors']:
        print(f"Type: {error['type']}")
        print(f"Context: {error['context']}")
        print(f"Message: {error['message']}")

if __name__ == "__main__":
    main()