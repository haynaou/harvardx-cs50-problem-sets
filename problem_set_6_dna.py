import sys
import csv


def main():
    # Check if 2 arguments are provided
    arg = len(sys.argv[1:])
    if arg != 2:
        print("Usage: python dna.py data.csv sequence.txt")
        exit()

    # Read provided arguments
    csv_database = sys.argv[1]
    sequence_text = sys.argv[2]

    # Get dna sequence from sequence_text file
    dna = None
    with open(sequence_text, 'r') as textfile:
        dna = textfile.readline()

    # Open csv database file and compute the longest run 
    # of consecutive repeats of the STR in the DNA sequence.
    # Then print the name of the person who's DNA sequence matches the longest sequence.
    header = []
    with open(csv_database) as csvfile:
        header = get_header(csvfile)
        people = csv.DictReader(csvfile)
        
        # Computer the longest run of consecutive repeats of 
        # every sequence in the header array (DNA sequences of people).
        longest_sequences = {}
        for seq in header[1:]:
            longest_sequences[seq] = longest_run(seq, dna)
        
        # Find the the person who's DNA sequence matches the longest sequence.
        result = find_person(people, longest_sequences)
        print(result)
            

# Finds the person who's sequence matches the longest sequence
def find_person(people, longest_sequences):
    for person in people:
        # We assume that the person's sequences all match with longest_sequences,
        # If a sequence doesn't match, we flip this value to False.
        all_match = True
        
        for seq in longest_sequences.keys():
            if (int(person[seq]) != longest_sequences[seq]):
                # The values doesn't match, we set all_match to False,
                # we also need to break from the loop and check next person.
                all_match = False
                break
        
        # At this point, we check if all sequences match, 
        # if so, we return the name of the person if so.
        if (all_match):
            return person['name']
    
    # At this point, nothing was returned, therefore we return "No Match".
    return "No Match"


# Reads the first line from the file without advancing the file cursor.
def peek_line(file):
    # save the current file cursor position
    position = file.tell()
    # readline advances the cursor
    line = file.readline()
    # put back the cursor at the previous position
    file.seek(position)
    return line


# Gets csv header as array
def get_header(file):
    line = peek_line(file)
    # Remove newline character and convert to array
    column_names = line.replace('\n', '').split(",")
    # Remove first element
    return column_names
  
    
# Computes the longest run of sequences seq in dna.
def longest_run(seq, dna):
    # Variable to keep track of the longest run.
    max_run = 0
    
    # Look at every word of size len(seq) starting from 0 to end minus len(seq).
    for i in range(0, len(dna) - len(seq) + 1):
        # Variable to keep track of how many runs we have counted so far.
        current_run = 0
        dna_substr = dna[i:i + len(seq)]
        
        # If first substring of len(seq) matches, we try to look at next ones of same size
        if dna_substr == seq:
            # Increment the current run since we just found a substring that equals seq.
            current_run += 1
            
            # Look for next words in the string advancing with length of seq.
            for j in range(i + len(seq), len(dna) - len(seq) + 1, len(seq)):
                next_dna_substr = dna[j:j + len(seq)]
                # If next word matches seq, we increment and continue the loop.
                # otherwise, we break since we are looking for only consecutive words.
                if next_dna_substr == seq:
                    current_run += 1
                else:
                    break
            
            # We update the max_run to have latest value we have counted so far.
            max_run = max(max_run, current_run)
    
    return max_run


main()
