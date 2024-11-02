import pandas as pd
import re

class TextDataProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = None

    def load_and_filter_data(self):
        # Load the data with specific column names
        self.data = pd.read_csv(self.input_file, header=0, names=['index', 'content', 'label'])
        print("Data loaded successfully.")

        # Filter out rows where label is 1
        self.data = self.data[self.data['label'] != 1]
        self.data['label'] = self.data['label'].apply(lambda x: 1 if x == 2 else x)

        print("Filtered out rows with label 1.")

    def clean_content(self):
        # Define a function for comprehensive cleaning
        def clean_text(text):
            if isinstance(text, str):
                # Remove hashtags
                text = re.sub(r'#\w+', '', text)
                # Replace multiple spaces with a single space
                text = re.sub(r'\s{2,}', ' ', text)
                # Remove characters like "…"
                text = re.sub(r'[…]', '', text)
                # Remove ... or ..
                text = re.sub(r'[.]{2,}', '', text)
                # Remove all special characters except alphanumeric and spaces
                text = re.sub(r'[^A-Za-z0-9\s\-]', '', text)
                # Remove emojis and symbols (using Unicode ranges)
                emoji_pattern = re.compile(
                    "[\U0001F600-\U0001F64F"  # emoticons
                    "\U0001F300-\U0001F5FF"  # symbols & pictographs
                    "\U0001F680-\U0001F6FF"  # transport & map symbols
                    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
                    "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
                    "\U00002702-\U000027B0"  # Dingbats
                    "\U000024C2-\U0001F251"  # enclosed characters
                    "\U0001F004-\U0001F0CF"  # playing cards
                    "\U0001F18E-\U0001F251"  # squared & other symbols
                    "\U0001F910-\U0001F928"  # additional emoticons
                    "\U0001F970-\U0001F976"  # new emoticons
                    "\U0001F97A-\U0001F9A0"  # additional animals & nature
                    "\U0001F9B0-\U0001F9B9"  # additional body parts
                    "\U0001F9C0-\U0001F9C2"  # food
                    "\U0001F9D0-\U0001F9E6"  # additional people & fantasy
                    "\U0001F9F0-\U0001F9FF"  # objects & miscellaneous
                    "\U0001FAE0-\U0001FAE8"  # new emojis
                    "]+", flags=re.UNICODE)
                text = emoji_pattern.sub(r'', text)
                # Remove common emoticons
                text = re.sub(r'[:;=][oO\-]?[D\)\]\(\]/\\OpP]', '', text)
                # Remove any remaining excessive whitespace
                text = text.strip()
                # Lowercase the text for uniformity
                text = text.lower()
            return text

        # Apply cleaning to the 'content' column
        self.data['content'] = self.data['content'].apply(clean_text)
        print("Cleaned hashtags, excess whitespace, unwanted characters, and emoticons from content.")

    def save_processed_data(self):
        # Save the cleaned data to the output CSV
        self.data.to_csv(self.output_file, index=False, header=True)
        print(f"Processed data saved to {self.output_file}")
