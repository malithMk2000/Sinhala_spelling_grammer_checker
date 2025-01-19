import pandas as pd
from Levenshtein import distance
import re

class SinhalaLanguageChecker:
    def __init__(self, spell_dict_path, grammar_dict_path):
        """
        Initialize the language checker with dictionaries for spelling and grammar
        """
        try:
            # Load spelling dictionary
            self.spell_df = pd.read_excel(spell_dict_path)
            # Create set of correct words for faster lookup
            self.correct_words = set(self.spell_df[self.spell_df['label'] == 1]['word'].values)

            # Load grammar rules and clean column names
            self.grammar_df = pd.read_excel(grammar_dict_path)
            self.grammar_df.columns = self.grammar_df.columns.str.strip()

            # Validate required columns exist
            required_columns = {'verb', 'subject', 'corrected_verb'}
            if not all(col in self.grammar_df.columns for col in required_columns):
                missing_cols = required_columns - set(self.grammar_df.columns)
                raise ValueError(f"Missing required columns in grammar file: {missing_cols}")

            # Create verb conjugation patterns
            self.verb_patterns = self._create_verb_patterns()

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Could not find the file: {e.filename}")
        except Exception as e:
            raise Exception(f"Error initializing the checker: {str(e)}")

    def _create_verb_patterns(self):
        """Create verb conjugation patterns from the grammar dataset"""
        patterns = {}
        for _, row in self.grammar_df.iterrows():
            verb = row['verb'].strip()
            subject = row['subject'].strip()
            corrected = row['corrected_verb'].strip()

            if verb not in patterns:
                patterns[verb] = {}

            patterns[verb][subject] = corrected
        return patterns

    def tokenize(self, text):
        """Split Sinhala text into words"""
        words = re.findall(r'[\u0D80-\u0DFF]+', text)
        return [word.strip() for word in words if word.strip()]

    def get_spelling_suggestions(self, word, max_distance=2):
        """Get spelling suggestions for a word"""
        word = word.strip()
        suggestions = []

        # Find similar words using Levenshtein distance
        for correct_word in self.correct_words:
            dist = distance(word, correct_word)
            if dist <= max_distance:
                suggestions.append((correct_word, dist))

        # Return top 5 suggestions sorted by distance
        return [word for word, _ in sorted(suggestions, key=lambda x: x[1])][:5]

    def check_spelling(self, word):
        """Check if a word is spelled correctly and get suggestions"""
        word = word.strip()
        if word in self.correct_words:
            return True, word, []
        else:
            suggestions = self.get_spelling_suggestions(word)
            return False, suggestions[0] if suggestions else word, suggestions

    def conjugate_verb(self, verb, subject):
        """Conjugate verb based on subject"""
        verb = verb.strip()
        subject = subject.strip()

        if verb in self.verb_patterns and subject in self.verb_patterns[verb]:
            return self.verb_patterns[verb][subject]
        return verb

    def correct_sentence(self, sentence):
        """
        Correct both spelling and grammar while preserving content.
        Detect subject dynamically in the sentence and adjust verb conjugation.
        """
        words = self.tokenize(sentence)
        if len(words) < 2:
            return sentence, False, {}
    
        # Initialize variables
        spelling_errors = {}
        corrected_words = []
        is_changed = False
        subject = None
    
        # Identify the subject from the sentence
        for word in words:
            if word in self.grammar_df['subject'].values:
                subject = word
                break
    
        if not subject:
            # If no subject is found, return as is
            return sentence, False, {}
    
        # Check and correct spelling for all words
        for word in words:
            is_correct, corrected_word, suggestions = self.check_spelling(word)
            if not is_correct:
                spelling_errors[word] = suggestions
                corrected_words.append(corrected_word)
                is_changed = True
            else:
                corrected_words.append(word)
    
        # Correct verb based on the identified subject
        for idx, word in enumerate(corrected_words):
            if word in self.verb_patterns:
                corrected_verb = self.conjugate_verb(word, subject)
                if corrected_verb != word:
                    corrected_words[idx] = corrected_verb
                    is_changed = True
    
        corrected_sentence = ' '.join(corrected_words)
        return corrected_sentence, is_changed, spelling_errors


    def check_text(self, text):
        """
        Check and correct text while preserving content
        """
        result = {
            'spelling_errors': {},
            'grammar_analysis': []
        }

        # Split into sentences
        sentences = re.split(r'[။।.]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        for sentence in sentences:
            corrected, is_changed, spelling_errors = self.correct_sentence(sentence)
            result['spelling_errors'].update(spelling_errors)
            result['grammar_analysis'].append({
                'sentence': sentence,
                'is_correct': not is_changed,
                'suggested_correction': corrected if is_changed else sentence,
                'confidence': 1.0 if not is_changed else 0.8
            })

        return result

