import pandas as pd
import requests


def get_daily_data(state, start, end, columns=None):
    template = f'https://api.covidtracking.com/v1/states/{state}/daily.csv'
    rows = []
    header = []
    content = requests.get(template).text.split('\n')

    for idx, entry in enumerate(content):
        if idx != 0:
            rows.append(entry.split(','))
        else:
            header.extend(entry.split(','))

    df = pd.DataFrame(rows, columns=header)
    df['date'] = pd.to_datetime(df['date'])

    if not columns:
        columns = ['date', 'state',
                   'positive', 'positiveIncrease',
                   'death', 'deathIncrease']

    df = df[columns]
    df.dropna(subset=['date'], inplace=True)

    if not start and not end:
        try:
            start = pd.to_datetime(start)
            end = pd.to_datetime(end)
        except RuntimeError as e:
            print(e)
            raise

    df = df[df['date'] >= start]
    df = df[df['date'] <= end]
    df.reset_index(drop=True, inplace=True)

    return df

