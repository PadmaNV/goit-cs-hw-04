import threading
from collections import defaultdict
from pathlib import Path
import time

def search_in_files(files, keywords, results):
    for file in files:
        try:
            with open(file, "r") as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(file)
        except IOError as e:
            print(f"Error reading file {file}: {e}")

def main_threading(file_paths, keywords):
    start_time = time.time()
    num_threads = 4
    files_per_thread = len(file_paths) // num_threads
    threads = []
    results = defaultdict(list)

    for i in range(num_threads):
        start = i * files_per_thread
        end = None if i == num_threads - 1 else start + files_per_thread
        thread_files = file_paths[start:end]
        thread = threading.Thread(
            target=search_in_files, args=(thread_files, keywords, results)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return results

if __name__ == "__main__":
    # Приклад виклику
    file_paths = list(Path("./example").glob("*.txt"))
    keywords = ["keyword1", "keyword2"]
    results = main_threading(file_paths, keywords)
    print(results)
