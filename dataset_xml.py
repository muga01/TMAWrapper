import xml.etree.ElementTree as ET
import pandas as pd
import glob

PATTERN_LENGTH = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

RECORD = {
    'Category': None,
    'Text Size [MB]': None,
    'Pattern Length': None,
    'Alphabet Size': None,
    'Time [ms]': None,
    'Algorithm': None,
}
BEST = {'Best Algo': None}


def read_html(exp_path):
    html_files = glob.glob(exp_path + f'/*.html', recursive=True)
    for f in html_files:
        if 'index' in f: continue
        with open(f) as html:
            first_line = html.readline()
            required_portion = first_line.split('</h2>')[-2].split(' ')
        return float(required_portion[4]), float(required_portion[8]) / 1024 / 1024


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
        # print(read_html('results/' + exp_code),exp_code)
        a_size, t_size = read_html('results/' + exp_code)
        RECORD['Alphabet Size'] = a_size
        RECORD['Text Size [MB]'] = t_size
        best_times = []
        for bests in root.findall('BEST'):
            for d in bests.findall('DATA'):
                best_times.append(d.text)
        for kids_root in root.findall('ALGO'):
            RECORD['Algorithm'] = kids_root.find('NAME').text
            i = 0
            for kids_root_data in kids_root.findall('DATA'):
                # print(kids_root_data.find('SEARCH').text)
                if kids_root_data.find('SEARCH') is None:
                    continue
                RECORD['Pattern Length'] = PATTERN_LENGTH[i]
                RECORD['Time [ms]'] = kids_root_data.find('SEARCH').text
                if RECORD['Time [ms]'] == best_times[i]:
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
df.to_csv('dataset/string_pattern_matching.csv', index=False)
print(len(rows), len(best))
