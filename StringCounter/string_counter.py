# pip install pyinstaller
# pip install prettytable openpyxl
# pyinstaller --onefile count_words.py

import xml.etree.ElementTree as ET
from collections import Counter
import re
from tkinter import Tk, filedialog
from prettytable import PrettyTable  # For tabular display
import openpyxl  # For Excel file creation

def select_file_with_file_manager():
    """Open a file dialog to select strings.xml."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    root.attributes("-topmost", True)  # Bring the dialog to the front
    file_path = filedialog.askopenfilename(
        title="Select strings.xml file",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def save_summary_to_excel(summary_data):
    """Save the summary data to an Excel file."""
    # Open a file dialog to select where to save the Excel file
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save Summary Table as Excel"
    )
    root.destroy()

    if save_path:  # If a valid save location was selected
        # Create an Excel workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Summary Table"
        
        # Add headers
        headers = ["File Name", "Total Words", "Total Price (¥)"]
        sheet.append(headers)
        
        # Add data
        for data in summary_data:
            sheet.append([data["file_name"], data["total_words"], f"{data['total_price']:.2f}"])
        
        # Save the file
        workbook.save(save_path)
        print(f"Summary table saved to: {save_path}")
    else:
        print("Save operation cancelled.")

def count_words_and_list_in_strings_xml(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Ensure the XML is valid and contains resources
        if root.tag != 'resources':
            raise ValueError("Invalid XML file with no 'resources' root element.")
        
        # Extract all text values and collect valid words
        word_list = []
        word_pattern = re.compile(r'\b\w+\b')  # Regex to match valid words
        
        for string_element in root.findall('string'):
            if string_element.text:  # If the string has text
                words = word_pattern.findall(string_element.text.lower())  # Convert to lowercase
                # Filter out single-character words (letters and numbers)
                filtered_words = [word for word in words if len(word) > 1]
                word_list.extend(filtered_words)
        
        # Count total words and create a frequency dictionary
        total_words = len(word_list)
        word_count = Counter(word_list)
        
        return total_words, word_count
    except FileNotFoundError:
        print(messages["file_not_found"])
    except ET.ParseError:
        print(messages["invalid_file"])
    except Exception as e:
        print(f"{messages['error_occurred']} {e}")

def display_table(word_count):
    """Display the word count in a tabular format."""
    table = PrettyTable()
    table.field_names = ["Word", "Count"]  # Column headers
    for word, count in word_count.items():
        table.add_row([word, count])
    print(table)

def display_summary(summary_data):
    """Display the summary of all processed files."""
    summary_table = PrettyTable()
    summary_table.field_names = ["File Name", "Total Words", "Total Price (¥)"]  # Column headers
    for data in summary_data:
        summary_table.add_row([data["file_name"], data["total_words"], f"¥{data['total_price']:.2f}"])
    print("\n=== Summary Table ===")
    print(summary_table)

if __name__ == "__main__":
    # Language selection
    languages = {
        "en": {
            "welcome": "=== Word Count Program ===",
            "manual_or_file": "Choose an option:\n1. Manual path input\n2. Use file manager",
            "input_file": "Enter the path to your strings.xml file (or type 'exit' to quit): ",
            "input_price": "Enter the price per word (in yen): ¥",
            "invalid_price": "Price per word must be greater than 0. Please try again.",
            "invalid_input": "Invalid input. Please enter a valid number for the price per word.",
            "word_list": "Word frequency list:",
            "total_words": "The total number of valid words in the strings.xml file is: ",
            "total_price": "The total price is: ",
            "file_not_found": "The file was not found. Please check the path and try again.",
            "invalid_file": "The file is not a valid XML file.",
            "error_occurred": "An error occurred:",
            "process_another": "Do you want to process another file? (yes/no): ",
            "save_summary": "Do you want to save the summary table to Excel? (yes/no): ",
            "goodbye": "Goodbye!"
        },
        "jp": {
            "welcome": "=== 単語カウントプログラム ===",
            "manual_or_file": "オプションを選択してください:\n1. 手動でパスを入力\n2. ファイルマネージャーを使用",
            "input_file": "strings.xmlファイルのパスを入力してください（終了するには 'exit' と入力してください）: ",
            "input_price": "1単語あたりの価格を入力してください（円）: ¥",
            "invalid_price": "1単語あたりの価格は0より大きくする必要があります。もう一度お試しください。",
            "invalid_input": "無効な入力です。有効な数字を入力してください。",
            "word_list": "単語頻度リスト:",
            "total_words": "strings.xmlファイルの有効な単語の総数: ",
            "total_price": "総価格: ",
            "file_not_found": "ファイルが見つかりませんでした。パスを確認して、もう一度お試しください。",
            "invalid_file": "ファイルは有効なXMLファイルではありません。",
            "error_occurred": "エラーが発生しました: ",
            "process_another": "別のファイルを処理しますか？ (yes/no): ",
            "save_summary": "要約表をExcelに保存しますか？ (yes/no): ",
            "goodbye": "さようなら！"
        }
    }

    print("Select language / 言語を選択してください:")
    print("1. English")
    print("2. 日本語")
    lang_choice = input("Your choice / 選択: ").strip()
    lang_code = "jp" if lang_choice == "2" else "en"
    messages = languages[lang_code]

    summary_data = []  # To store summary of all processed files

    while True:
        print(f"\n{messages['welcome']}")
        print(messages["manual_or_file"])
        option = input("Your choice: ").strip()
        
        if option == "1":
            file_path = input(messages["input_file"]).strip()
        elif option == "2":
            file_path = select_file_with_file_manager()
            if not file_path:  # No file selected
                print(messages["file_not_found"])
                continue
        else:
            print("Invalid option. Please choose 1 or 2.")
            continue
        
        if file_path.lower() == 'exit':
            print(messages["goodbye"])
            break
        
        try:
            # Get word price
            price_per_word = float(input(messages["input_price"]))
            if price_per_word <= 0:
                print(messages["invalid_price"])
                continue
        except ValueError:
            print(messages["invalid_input"])
            continue
        
        result = count_words_and_list_in_strings_xml(file_path)
        
        if result:
            total_words, word_count = result
            print(f"\n{messages['word_list']}")
            display_table(word_count)  # Display results in a table
            
            total_price = total_words * price_per_word
            print(f"\n{messages['total_words']} {total_words}")
            print(f"{messages['total_price']} ¥{total_price:.2f}")
            
            # Append to summary data
            summary_data.append({
                "file_name": file_path.split("/")[-1],  # Get the file name from the path
                "total_words": total_words,
                "total_price": total_price
            })
        
        # Display summary table
        display_summary(summary_data)

        # Ask if user wants to process another file
        process_another = input(messages["process_another"]).strip().lower()
        if process_another != "yes":
            # Ask if user wants to save summary
            save_summary = input(messages["save_summary"]).strip().lower()
            if save_summary == "yes":
                save_summary_to_excel(summary_data)
            print(messages["goodbye"])
            break