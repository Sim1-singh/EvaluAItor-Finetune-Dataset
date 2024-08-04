import sys
import os
from pathlib import Path
import shutil
import gzip
import json

def dicts_to_jsonl(data_list: list, filename: str, compress: bool = False) -> None:
    """
    Method saves list of dicts into jsonl file.
    :param data: (list) list of dicts to be stored,
    :param filename: (str) path to the output file. If suffix .jsonl is not given then methods appends
        .jsonl suffix into the file.
    :param compress: (bool) should file be compressed into a gzip archive?
    """
    sjsonl = '.jsonl'
    sgz = '.gz'
    # Check filename
    if not filename.endswith(sjsonl):
        filename = filename + sjsonl
    # Save data
    
    if compress:
        filename = filename + sgz
        with gzip.open(filename, 'w') as compressed:
            for ddict in data_list:
                jout = json.dumps(ddict) + '\n'
                jout = jout.encode('utf-8')
                compressed.write(jout)
    else:
        with open(filename, 'w+') as out:
            for ddict in data_list:
                jout = json.dumps(ddict) + '\n'
                out.write(jout)

if (__name__ == "__main__"):
    if(len(sys.argv) < 2):
        print("At least 1 argument expected")
    else:
        results_dir = "results"
        if(not Path(results_dir).exists() or Path(results_dir).is_file()):
            os.mkdir(results_dir)
        i = 1
        while(i < len(sys.argv)):
            # load data into list of dict
            dirname = sys.argv[i]
            json_list = []
            for filename in os.listdir("datasets/"+dirname):
                f = Path("datasets/" + dirname, filename)
                if f.suffix == ".json":
                    with open(f, "r", encoding="utf8") as readfile:
                        obj = json.load(readfile)
                        json_list.append(obj)

            # delete current file
            outpath = Path("results/" + dirname + ".jsonl")
            if outpath.exists() and outpath.is_file():
                os.remove(outpath)

            # write new file
            dicts_to_jsonl(json_list, str(outpath), compress=False)
            i+=1
