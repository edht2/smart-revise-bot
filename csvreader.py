from pathlib import Path

CSV_DELIM = '|'
CSV_COMMENT = '#'

""" Simple utility I made to read csv files (with comments) """
def read_csv(path:str) -> list[tuple[int]]:
    read = []
    with open(path, "r") as serial:
        while line := serial.readline():
            if line[0] == CSV_COMMENT: continue
            delim = line.strip().split(CSV_DELIM)
            read.append(
                tuple(d.strip() for d in delim)
            )
    return read

def write_csv(path:str, towrite:list[tuple[str]]) -> None:
    with open(path, "w") as serial:
        for q in towrite:
            qw = ""
            for qp in q:
                qw += f"{qp}{CSV_DELIM}"
            serial.write(qw[:-1]+"\n")