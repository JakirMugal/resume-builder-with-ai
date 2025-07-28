
def get_values_between_string(t1, t2, text, find_word,remove=False):
    """
    Extracts and evaluates a substring between two delimiters (t1 and t2) that follows a specified word (find_word).

    Args:
        t1 (str): The starting delimiter.
        t2 (str): The ending delimiter.
        text (str): The text to search within.
        find_word (str): The word to find before extracting the substring.

    Returns:
        Any: The evaluated result of the extracted substring, or None if an error occurs.
    """
    try:
        # Find the index of the first occurrence of find_word in the text
        first_index = text.index(find_word)
        
        # Slice the text to start from the find_word
        text = text[first_index:]
        
        # Find the first occurrence of t1 after find_word
        start_index = text.index(t1)
        text = text[start_index:]
        
        count_t1 = 0
        count_t2 = 0
        
        # Iterate through the text to find the matching t1 and t2
        for i in range(len(text)):
            # If the counts of t1 and t2 match and t1 has been encountered at least once, break the loop
            if count_t1 == count_t2 and count_t1 != 0:
                break
            
            # Increment count_t1 if the current character is t1
            if text[i] == t1:
                count_t1 += 1
            
            # Increment count_t2 if the current character is t2
            if text[i] == t2:
                count_t2 += 1
        
        # Extract the text between the delimiters and replace JSON-like values with Python equivalents
        text = text[:i].replace('null', 'None').replace('false', 'False').replace('true', 'True')
        if remove:
            text=text[1:-1]
        try:
            # Evaluate and return the extracted text
            return eval(text)
        except:
            print("Issue in EVAL. So return Text only")
            return text
    
    except ValueError as ve:
        # Handle ValueError, e.g., when find_word is not found in the text
        print(f"ValueError: {ve}")
        return None
    except SyntaxError as se:
        # Handle SyntaxError, e.g., if eval encounters a syntax error
        print(f"SyntaxError: {se}")
        return None
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        return None
def get_all_values_between_string(t1, t2, text, find_word,remove=False):
    """
    Extracts and evaluates all substrings between two delimiters (t1 and t2) that follow each occurrence of a specified word (find_word).

    Args:
        t1 (str): The starting delimiter.
        t2 (str): The ending delimiter.
        text (str): The text to search within.
        find_word (str): The word to find before extracting substrings.

    Returns:
        List[Any]: A list of evaluated results of the extracted substrings, or an empty list if no results are found or an error occurs.
    """
    results = []

    # Count occurrences of find_word
    find_word_count = text.count(find_word)

    for _ in range(find_word_count):
        # Call the existing function to get values
        value = get_values_between_string(t1, t2, text, find_word,remove)
        if value is not None:
            results.extend(value if isinstance(value, list) else [value])
        
        # Remove the processed segment and find the next occurrence
        start_index = text.find(find_word)
        if start_index != -1:
            text = text[start_index + len(find_word):]
        else:
            break
    
    return results