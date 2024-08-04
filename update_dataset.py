import sys
import json
from pathlib import Path
import shutil
import os

if (__name__ == "__main__"):
    if(len(sys.argv) < 2):
        print("Expected: python3 update_dataset.py resume_train.jsonl resume_val.jsonl")
    else:
        i = 1
        while(i < len(sys.argv)):
            with open("results/" + sys.argv[i], encoding="utf8") as file:
                dirname = sys.argv[i].split(".")[0]
                outdirpath = Path("datasets/" + dirname) 
                if outdirpath.exists() and outdirpath.is_dir():
                    shutil.rmtree(outdirpath)
                
                os.mkdir(outdirpath)

                ln = 1
                for line in file:
                    json_content = json.loads(line)
                    json_object = json.dumps(json_content, indent = 4)
                    print(dirname + " : " +str(ln))
                    with open("datasets/" + dirname + "/" + str(ln) + ".json", "w+", encoding="utf8") as outfile:
                        outfile.write(json_object)
                    ln+=1
            i+=1