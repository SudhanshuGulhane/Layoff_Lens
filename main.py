import subprocess

def main():
    query = input("Enter the query: ")
    index_type = input("Which index to search: sparse or dense? ").lower()
    k = input("How many search results to return (k): ")

    # Validate k is an integer
    try:
        k = int(k)
    except ValueError:
        print("Error: Please enter a valid integer for k.")
        return

    if index_type == "sparse":
        # Assuming Pylucene_parser.py is modified to accept arguments for query, k, and index_path
        index_path = '/home/cs242/index_dir/'
        subprocess.run(['python3', 'Pylucene_parser.py', query, str(k), index_path], check=True)
    elif index_type == "dense":
        # BertFaiss.py is prepared to accept arguments for query and k
        # Note: BertFaiss.py does not need the index path as it works with pre-loaded data and models
        subprocess.run(['python3', 'BertFaiss.py', query, str(k)], check=True)
    else:
        print("Error: Invalid index type selected. Please choose either 'sparse' or 'dense'.")

if __name__ == "__main__":
    main()