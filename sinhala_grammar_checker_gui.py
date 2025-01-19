import tkinter as tk
from tkinter import messagebox
from SinhalaLanguageChecker import SinhalaLanguageChecker  # Import the checker class

# Initialize the checker with the dictionary files
try:
    checker = SinhalaLanguageChecker(
        'P:/Windows/git/Sinhala_spelling_grammer_checker/SinhalaGrammarChecker/data-spell-checker.xlsx',  # Path to the spelling dictionary
        'P:/Windows/git/Sinhala_spelling_grammer_checker/SinhalaGrammarChecker/grammar.xlsx'             # Path to the grammar dictionary
    )
except Exception as e:
    messagebox.showerror("Error", f"Failed to initialize the grammar checker: {str(e)}")
    exit()

# Define the function for grammar checking
def check_grammar():
    input_text = input_textbox.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter a sentence!")
        return

    # Process the text
    result = checker.check_text(input_text)
    grammar_analysis = ""
    spelling_errors = ""
    corrected_paragraph = input_text  # Start with the original paragraph

    # Process grammar analysis
    for analysis in result['grammar_analysis']:
        original = analysis['sentence']
        if not original.endswith("."):
            original += "."
        if not analysis['is_correct']:
            suggestion = analysis['suggested_correction']
            if not suggestion.endswith("."):
                suggestion += "."
            grammar_analysis += f"Original: {original}\nSuggestion: {suggestion}\n"
            # Replace the incorrect sentence with the suggestion
            corrected_paragraph = corrected_paragraph.replace(original, suggestion)
        else:
            grammar_analysis += f"Original: {original}\n"

    # Process spelling errors
    for word, suggestions in result['spelling_errors'].items():
        spelling_errors += f"Error: {word}\nSuggestions: {', '.join(suggestions)}\n"
        # Check if suggestions are available
        if suggestions:
            # Correct the spelling errors by replacing with the first suggestion
            corrected_paragraph = corrected_paragraph.replace(word, suggestions[0])
        else:
            # If no suggestions are available, you can choose to leave the word as is or handle it differently
            corrected_paragraph = corrected_paragraph.replace(word, word)
    # Combine outputs
    output_text = f"Grammar Analysis:\n{grammar_analysis}\nSpelling Errors:\n{spelling_errors}"
    output_textbox.delete("1.0", tk.END)
    output_textbox.insert(tk.END, output_text)

    # Display the corrected paragraph
    corrected_paragraph_label.config(text="Corrected Paragraph:")
    corrected_paragraph_textbox.delete("1.0", tk.END)
    corrected_paragraph_textbox.insert(tk.END, corrected_paragraph)


# Create the main GUI window
root = tk.Tk()
root.title("Sinhala Grammar Checker")
root.geometry("1000x600")
root.configure(bg="blue")

# Add a label for input
input_label = tk.Label(root, text="Enter Sentence:", font=("Arial", 14, "bold"), bg="blue", fg="white")
input_label.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_scroll_y = tk.Scrollbar(input_frame, orient=tk.VERTICAL)

input_textbox = tk.Text(
    input_frame,
    height=10,
    width=100,
    font=("Arial", 12),
    wrap=tk.WORD,  # Use word wrapping to avoid horizontal scrolling
    yscrollcommand=input_scroll_y.set
)
input_textbox.grid(row=0, column=0)

input_scroll_y.config(command=input_textbox.yview)

input_scroll_y.grid(row=0, column=1, sticky="ns")

# Add a button for checking grammar
check_button = tk.Button(root, text="Check Grammar", font=("Arial", 12, "bold"), bg="green", fg="white", command=check_grammar)
check_button.pack(pady=20)

# Add a label for corrected analysis
output_label = tk.Label(root, text="Analysis and Suggestions:", font=("Arial", 14, "bold"), bg="blue", fg="white")
output_label.pack(pady=10)

# Add scrollable output textbox
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_scroll_y = tk.Scrollbar(output_frame, orient=tk.VERTICAL)
output_scroll_x = tk.Scrollbar(output_frame, orient=tk.HORIZONTAL)

output_textbox = tk.Text(
    output_frame,
    height=20,
    width=100,
    font=("Arial", 12),
    wrap=tk.NONE,
    yscrollcommand=output_scroll_y.set,
    xscrollcommand=output_scroll_x.set
)
output_textbox.grid(row=0, column=0)

output_scroll_y.config(command=output_textbox.yview)
output_scroll_x.config(command=output_textbox.xview)

output_scroll_y.grid(row=0, column=1, sticky="ns")
output_scroll_x.grid(row=1, column=0, sticky="ew")

# Add a label and textbox for the corrected paragraph
corrected_paragraph_label = tk.Label(root, text="Corrected Paragraph:", font=("Arial", 14, "bold"), bg="blue", fg="white")
corrected_paragraph_label.pack(pady=10)

corrected_paragraph_frame = tk.Frame(root)
corrected_paragraph_frame.pack(pady=10)

corrected_paragraph_textbox = tk.Text(
    corrected_paragraph_frame,
    height=10,
    width=100,
    font=("Arial", 12),
    wrap=tk.WORD
)
corrected_paragraph_textbox.grid(row=0, column=0)

# Run the main loop
root.mainloop()
