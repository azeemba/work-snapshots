
import time
import pathlib
import argparse
import pywinctl

from datatypes import Process

def parse_args():
    parser = argparse.ArgumentParser(description="Write windows to CSV file")
    parser.add_argument("csv_file", help="Path to the CSV file", type=pathlib.Path)
    parser.add_argument("timestamp", help="Identifier for the current time", type=str)
    parser.add_argument("-p", "--filtered-process", help="Process name(s) to filter out", action='append', default=[])

    return parser.parse_args()

def get_current_windows(filter_list: list[str]):
    t5 = time.monotonic_ns()
    windows = pywinctl.getAllWindows()
    titleProcessMap = pywinctl.getAllAppsWindowsTitles()
    invert_dict = {}
    for process, val in titleProcessMap.items():
        if process in filter_list:
            continue

        for title in val:
            if title == "":
                # filter out processes with no title
                continue
            invert_dict[title] = process

    data: list[Process] = []
    for w in windows:
        if w.getParent() == 0 and w.title in invert_dict:
            data.append(Process(invert_dict[w.title], w.title, w.isActive))
    t6 = time.monotonic_ns()
    print(f"Pulling process data took {(t6-t5)/1e9} seconds.")

    return data

def write_processes(csv_path: pathlib.Path, processes: list[Process], timestamp: str):
    filepath = csv_path
    csv_rows = []
    for p in processes:
        name = p.name.replace(",", "")
        title = p.title.replace(",", "")
        isActive = "1" if p.isActive else "0"
        # writing naively for now. Will change to db later anyways.
        csv_rows.append(f"{timestamp}, {name}, {title}, {isActive}\n")

    with open(filepath, "a", encoding="utf-8") as fh:
        fh.writelines(csv_rows)


if __name__ == "__main__":
    args = parse_args()
    print(args)
    w = get_current_windows(args.filtered_process)
    print(w)

    write_processes(args.csv_file, w, args.timestamp)