def read_csv(path:str) -> list[tuple[int]]:
    read = []
    with open(path, "r") as serial:
        while line := serial.readline():
            if line[0] == "#": continue
            delim = line.strip().split('|')
            read.append(
                tuple(d.strip() for d in delim)
            )
    return read