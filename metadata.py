from transformers import pipeline
from extraction import extract_text
import os

# It's good practice to define the model name as a constant
SUMMARIZATION_MODEL = "google/pegasus-xsum"
summarizer = None

def initialize_summarizer():
    """Initializes the summarization pipeline."""
    global summarizer
    if summarizer is None:
        print("Initializing summarization model...")
        summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL)
        print("Model initialized.")

def generate_summary(text, max_length=150, min_length=30):
    """
    Generates a summary for the given text using the pre-loaded pipeline.
    """
    if summarizer is None:
        initialize_summarizer()
        
    # The model works best with text that isn't excessively long.
    # Truncate to the first ~1024 tokens worth of text as a rough approximation.
    # A more robust solution would use the model's tokenizer.
    max_input_length = 4096  # Approximation
    if len(text) > max_input_length:
        text = text[:max_input_length]

    summary_list = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary_list[0]['summary_text']

def get_file_stats(file_path, text_content):
    """
    Generates basic statistics for a file.
    """
    return {
        "file_name": os.path.basename(file_path),
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "word_count": len(text_content.split())
    }

def generate_metadata(file_path):
    """
    Generates a full set of metadata for a given file.
    """
    print(f"Processing file: {file_path}")
    # 1. Extract text
    text_content = extract_text(file_path)
    if not text_content or text_content == 'File not found':
        print(f"Could not extract text from {file_path}")
        return None

    # 2. Generate summary
    summary = generate_summary(text_content)
    
    # 3. Get file stats
    stats = get_file_stats(file_path, text_content)

    # 4. Combine into a structured metadata object
    metadata = {
        "summary": summary,
        **stats  # Merges the stats dictionary
    }
    
    return metadata

if __name__ == '__main__':
    # Initialize the model once
    initialize_summarizer()

    test_file = 'documents/test.txt'
    
    # Ensure the test file exists
    if not os.path.exists(test_file):
        print(f"Test file not found at {test_file}. Please create it.")
    else:
        metadata = generate_metadata(test_file)
        if metadata:
            import json
            print("\nGenerated Metadata:")
            print(json.dumps(metadata, indent=2)) 