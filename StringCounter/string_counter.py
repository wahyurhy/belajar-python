# pip install pyinstaller
# pyinstaller --onefile count_words.py

import xml.etree.ElementTree as ET
from collections import Counter
import re

def count_words_and_list_in_strings_xml(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Ensure the XML is valid and contains resources
        if root.tag != 'resources':
            raise ValueError("File does not contain valid 'resources' root element")
        
        # Extract all text values and collect valid words
        word_list = []
        word_pattern = re.compile(r'\b\w+\b')  # Regex to match valid words
        
        for string_element in root.findall('string'):
            if string_element.text:  # If the string has text
                words = word_pattern.findall(string_element.text)  # Extract valid words
                word_list.extend(words)
        
        # Count total words and create a frequency dictionary
        total_words = len(word_list)
        word_count = Counter(word_list)
        
        return total_words, word_count
    except FileNotFoundError:
        print("The file was not found. Please check the path and try again.")
    except ET.ParseError:
        print("The file is not a valid XML file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        print("\n=== Word Count Program ===")
        file_path = input("Enter the path to your strings.xml file (or type 'exit' to quit): ").strip()
        
        if file_path.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            # Get word price
            price_per_word = float(input("Masukkan harga per kata : ¥"))
            if price_per_word <= 0:
                print("Harga per kata harus lebih besar dari 0. Silakan coba lagi.")
                continue
        except ValueError:
            print("Input tidak valid. Masukkan angka yang valid untuk harga per kata.")
            continue
        
        result = count_words_and_list_in_strings_xml(file_path)
        
        if result:
            total_words, word_count = result
            print("\nWord frequency list:")
            for word, count in word_count.items():
                print(f"{word}: {count}")
            
            total_price = total_words * price_per_word
            print(f"\nThe total number of valid words in the strings.xml file is: {total_words}")
            print(f"The total price is: ¥{total_price:.2f}")