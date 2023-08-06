import rats.modules.ratparser as ratparser
import pandas as pd
import plotly_express as px


def interscanplot(df, timescale=1000000):
    title = df['board'].astype('str').unique()[0]
    df = df[['function', 'time', 'llc']].drop_duplicates()
    df = df.set_index(['function', 'llc']).diff()
    df = df.reset_index()
    df = df.iloc[1:]
    df.loc[:, 'timescale'] = timescale
    df.loc[:, 'time'] = df['time']/df['timescale']
    df = df.sort_values('function', ascending=False)

    fig = px.violin(df, x='time', y='function', color='function', orientation='h',
                    title=title).update_traces(side='positive', width=2.5)
    fig.update_yaxes(type='category')
    fig.update_layout(plot_bgcolor='#fff')

    return fig


def test_case(absolutepath, f):
    try:
        df = pd.read_feather(f'../feathereddataframes/{f}.feather')
    except Exception:
        print('df not found')
        filename = absolutepath
        testclass = ratparser.RatParse(filename)
        df = testclass.dataframeoutput()

    fig = interscanplot(df)
    fig.show()


file = 'RATS simulation 1587681937.txt'
# test_case(f'/users/steve/documents/workwaters/{file}',file)
