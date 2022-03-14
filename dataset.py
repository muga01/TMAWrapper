import json
import glob
import pandas as pd

TXT_ALPHABET_SIZE = {
    # Category:[Text size in MB, Alphabet size]
    "rand2": [5.1, 2],
    "rand4": [5.1, 4],
    "rand8": [5.1, 8],
    "rand16": [5.1, 16],
    "rand32": [5.1, 32],
    "rand64": [5.1, 64],
    "rand128": [5.1, 128],
    "rand250": [16, 250],
    "protein": [8.3, 64],
    "genome": [4.5, 64],
    "italianTexts": [5, 128],
    "englishTexts": [6.3, 128]
}

PATTERN_LENGTH = [8, 16, 32, 64, 128]

COLUMNS = {
    'Category': None,
    'Text Size [MB]': None,
    'Pattern Length': None,
    'Alphabet Size': None,
    'Time [ms]': None,
    'Speed [GB/s]': None,
    'Algorithm': None
}


def dataset(data_path):
    json_files = glob.glob(data_path)
    # print(json_files)
    rows = []
    for f in json_files:
        with open(f) as new_f:
            data = json.load(new_f)
        # print(data)
        # Fill Columns Template for each category found
        COLUMNS['Category'] = data['TEXT']
        COLUMNS['Text Size [MB]'] = float(TXT_ALPHABET_SIZE[data['TEXT']][0])
        COLUMNS['Alphabet Size'] = TXT_ALPHABET_SIZE[data['TEXT']][1]

        for algo in data['ALGO']:
            COLUMNS['Algorithm'] = algo['NAME']
            # Read execution time and pattern length
            i = 0
            for time in algo['DATA']:
                COLUMNS['Time [ms]'] = float(time['SEARCH'])
                COLUMNS['Pattern Length'] = PATTERN_LENGTH[i]
                COLUMNS['Speed [GB/s]'] = (COLUMNS['Text Size [MB]'] / COLUMNS['Time [ms]']) * 1000 / 1024
                i += 1

                # One row completed, push to rows
                rows.append(COLUMNS.copy())

                # print(COLUMNS)

    # print(rows)
    # print(len(rows))
    return rows


dt = dataset('./data/*')

df = pd.DataFrame(data=dt)
df.to_csv('dataset.csv', index=False)
print(df.head(1))
