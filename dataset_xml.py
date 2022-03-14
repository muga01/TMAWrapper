import xml.etree.ElementTree as ET
import pandas as pd
import glob

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
EXP_CODE = {
    # EXP:[Alphabet size,Text size in MB]
    'EXP1646960336': [2, 1],
    'EXP1646960382': [2, 2],
    'EXP1646960465': [2, 4],
    'EXP1646960622': [4, 1],
    'EXP1646960651': [4, 2],
    'EXP1646960702': [4, 4],
    'EXP1646960793': [8, 1],
    'EXP1646960814': [8, 2],
    'EXP1646960850': [8, 4],
    'EXP1646960913': [16, 1],
    'EXP1646960933': [16, 2],
    'EXP1646960963': [16, 4],
    'EXP1646961015': [32, 1],
    'EXP1646961033': [32, 2],
    'EXP1646961061': [32, 4],
    'EXP1646961108': [64, 1],
    'EXP1646961125': [64, 2],
    'EXP1646961151': [64, 4],
    'EXP1646961195': [128, 1],
    'EXP1646961212': [128, 2],
    'EXP1646961237': [128, 4],
    'EXP1646961281': [250, 1],
    'EXP1646961298': [250, 2],
    'EXP1646961323': [250, 4],
    'EXP1646961366': [250, 5],
    # 'EXP1646961417': [250, 16],
    'EXP1646961469': [19, 1],
    'EXP1646961488': [19, 2],
    'EXP1646961516': [20, 4],
    'EXP1646961566': [20, 6.8],
    'EXP1646961646': [4, 1],
    'EXP1646961675': [4, 2],
    'EXP1646961724': [4, 4],
    'EXP1646961812': [104, 1],
    'EXP1646961831': [113, 2],
    'EXP1646961861': [116, 4],
    'EXP1646961912': [62, 1],
    'EXP1646961931': [63, 2],
    'EXP1646961962': [88, 4],
    'EXP1646962015': [114, 8],
    'EXP1646962107': [134, 16],
    'EXP1646962283': [155, 32],
    'EXP1646962626': [178, 64],
    'EXP1646963300': [218, 128]
}

PATTERN_LENGTH = [8, 16, 32, 64, 128, 256]

RECORD = {
    'Category': None,
    'Text Size [MB]': None,
    'Pattern Length': None,
    'Alphabet Size': None,
    'Time [ms]': None,
    'Speed [GB/s]': None,
    'Algorithm': None,
}
BEST = {'Best Algo': None}


def dataset_from_xml(path):
    """
    :param path: Path to experiment folder
    :return: List of rows dictionary
    """
    ROWS = []
    BEST_COL = []
    for exp in glob.glob(path):
        tree = ET.parse(exp)
        root = tree.getroot()

        RECORD['Category'] = root.find('TEXT').text
        exp_code = root.find('CODE').text
        RECORD['Text Size [MB]'] = EXP_CODE[exp_code][1]
        RECORD['Alphabet Size'] = EXP_CODE[exp_code][0]
        best_times = []
        for bests in root.findall('BEST'):
            for d in bests.findall('DATA'):
                best_times.append(d.text)
        # print(best_times)
        for kids_root in root.findall('ALGO'):
            RECORD['Algorithm'] = kids_root.find('NAME').text
            i = 0
            for kids_root_data in kids_root.findall('DATA'):
                RECORD['Time [ms]'] = float(kids_root_data.find('SEARCH').text)
                RECORD['Pattern Length'] = int(PATTERN_LENGTH[i])

                RECORD['Speed [GB/s]'] = (float(RECORD['Text Size [MB]']) / RECORD['Time [ms]']) * 1000 / 1024

                if kids_root_data.find('SEARCH').text == best_times[i]:
                    BEST['Best Algo'] = kids_root.find('NAME').text
                    BEST_COL.append(BEST.copy())
                else:
                    BEST['Best Algo'] = None
                    BEST_COL.append(BEST.copy())

                ROWS.append(RECORD.copy())
                i += 1

    return ROWS, BEST_COL


rows, best = dataset_from_xml('./results/*/*.xml')
df1 = pd.DataFrame(data=rows)
df2 = pd.DataFrame(data=best)
df = df1.join(df2)
df.to_csv('string_pattern_matching.csv', index=False)
print(len(rows), len(best))
