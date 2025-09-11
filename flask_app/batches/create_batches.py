import os
import json
from dotenv import load_dotenv 

def create_phrase_batches():
    load_dotenv() 
    meta_path = os.getenv("META_DATA")
    word_dict = {}
    for item in os.listdir(meta_path):
        item_path = os.path.join(meta_path, item)
        if os.path.isdir(item_path):
            for video in os.listdir(item_path):
                x = video.split("_")
                word = x[len(x) - 1].split(".")[0]
                clip = video
                if word and clip:
                    if word not in word_dict:
                        word_dict[word] = []
                    # Avoid duplicates
                    if clip not in word_dict[word]:
                        word_dict[word].append(clip)

    batches = {}
    batch_index = 0
    batches[f"batch_{batch_index}"] = {}
    # print(word_dict)
    
    for word in word_dict.keys():
        print(word)
        batches[f"batch_{batch_index}"][word] = word_dict[word]
        if(len(batches[f"batch_{batch_index}"]) == 2):
            batch_index += 1
            batches[f"batch_{batch_index}"] = {}

    file_path = "batches.json"
    with open(file_path, "w") as f:
        json.dump(batches, f, indent=4)
    print("batches created successfully")


create_phrase_batches()