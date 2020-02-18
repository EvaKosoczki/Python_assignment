
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as off
import plotly.graph_objs as go

# off.init_notebook_mode(connected=True)

unem_raw = pd.read_excel(
    r'D:\Programozás\PYTHON\data\munkanelkuli_ter.xls', header=1)
wage_raw = pd.read_excel(
    r'D:\Programozás\PYTHON\data\nettoatlagkereset_ter.xls', header=1)
gdp_raw = pd.read_excel(
    r'D:\Programozás\PYTHON\data\gdpperfo_ter.xls', header=1)
aktiv_raw = pd.read_excel(
    r'D:\Programozás\PYTHON\data\gazd_aktiv_ter.xls', header=1)

aktiva = pd.DataFrame(aktiv_raw)
aktiva.iloc[1, 1] = 'megye'
aktiva.iloc[2, 1] = 'megye'
aktiva.rename(columns={2016: 'twentysixteen'}, inplace=True)
aktiv = pd.DataFrame()
for i in range(1, len(aktiva)):
    if aktiva.iloc[i, 1] == 'megye':
        aktiv[i] = aktiva.iloc[i, :]
aktiv = aktiv.T.set_index('Területi egység').iloc[:, 17:19]


unempl = pd.DataFrame()
unem_raw.rename(columns={'Unnamed: 1': 'Szint'}, inplace=True)
unem = unem_raw.iloc[:, 0:2]
unem = pd.DataFrame(unem)
col = unem_raw.iloc[:, -2]
unem.iloc[2, 1] = 'megye'
unem.iloc[1, 1] = 'megye'
unem['2016'] = pd.Series(col, index=col.index)
unem.rename(columns={'2016': 'Unemployment_2016'}, inplace=True)
for i in range(1, len(unem)):
    if unem.iloc[i, 1] == 'megye':
        unempl[i] = unem.iloc[i, :]
unempl = unempl.T.set_index('Területi egység')


unempl['unemp_rate'] = unempl.Unemployment_2016/aktiv.twentysixteen*100


wage1 = wage_raw.iloc[:, 0]
wage2 = wage_raw.iloc[:, -1]
wage = pd.DataFrame([wage1, wage2])
wage = wage.T.set_index('Területi egység').iloc[0:31, :]
merged = pd.merge(unempl, wage, how='inner', left_index=True,
                  right_index=True, copy=False)
merged.rename(columns={2016: 'Avg_net_monthly_wage_2016'}, inplace=True)


gdp1 = gdp_raw.iloc[:, -1]
gdp2 = gdp_raw.iloc[:, 0]
gdp = pd.DataFrame([gdp2, gdp1]).T
gdp = gdp.iloc[1:31, :].astype(
    {'Területi egység': str}).set_index('Területi egység')
gdp.rename(columns={2016: 'Gdp_per_capita_2016'}, inplace=True)
merged2 = pd.merge(merged, gdp, how='left', left_index=True, right_index=True)
regio = ('Central Hungary', 'Central Hungary', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Transdanubia', 'Great Plain and North',
         'Great Plain and North', 'Great Plain and North', 'Great Plain and North', 'Great Plain and North', 'Great Plain and North', 'Great Plain and North', 'Great Plain and North', 'Great Plain and North')
merged2['Regio'] = regio
merged2.iloc[1, 4] = 2907
merged2.iloc[10, 4] = 2657
merged2.iloc[13, 4] = 1566
merged2.iloc[17, 4] = 2747
Central = merged2.iloc[0:2, :]
Trans = merged2.iloc[2:11, :]
Plain = merged2.iloc[11:20, :]


s_T = [n*55 for n in Trans.iloc[:, 2]]
s_P = [n*55 for n in Plain.iloc[:, 2]]
s_C = [n*55 for n in Central.iloc[:, 2]]
fig = plt.figure(figsize=(12, 12))
ax = plt.gca()
plt.scatter(Central.Gdp_per_capita_2016,
            Central.Avg_net_monthly_wage_2016, s=s_C)
plt.scatter(Trans.Gdp_per_capita_2016, Trans.Avg_net_monthly_wage_2016, s=s_T)
plt.scatter(Plain.Gdp_per_capita_2016, Plain.Avg_net_monthly_wage_2016, s=s_P)
plt.style.use('seaborn-deep')
plt.xlabel('GDP per capita (thousand Ft)', fontsize=14)
plt.ylabel('Avarage monthly net wage (Ft)', fontsize=14)
plt.title('Economic developement of Hungarian counties', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(['Central Hungary', 'Transdanubia-Western H.',
            'Eastern and Northern H.'])
plt.show()

"""
s_C = [n*3.5 for n in Central.iloc[:, 2]]
s_P = [i*3.5 for i in Plain.iloc[:, 2]]
s_T = [t*3.5 for t in Trans.iloc[:, 2]]
Central_Hungary = go.Scatter(x=Central.Gdp_per_capita_2016, y=Central.Avg_net_monthly_wage_2016,
                             mode='markers', name='Central Hungary', hoverinfo='text', text=Central.index, marker=dict(size=s_C))
Great_Plain = go.Scatter(x=Plain.Gdp_per_capita_2016, y=Plain.Avg_net_monthly_wage_2016, mode='markers',
                         name='Eastern and Northern H.', text=Plain.index, hoverinfo='text', marker=dict(size=s_P))
Transdanubia = go.Scatter(x=Trans.Gdp_per_capita_2016, y=Trans.Avg_net_monthly_wage_2016, mode='markers',
                          name='Transdanubia-Western H.', text=Trans.index, hoverinfo='text', marker=dict(size=s_T))
layout = dict(autosize=False, width=1000, height=800, title='Economic developement of Hungarian counties',
              xaxis=dict(title='GDP per capita (thousand Ft)'), yaxis=dict(title='Avarage monthly net wage (Ft)'))
data = dict(data=[Central_Hungary, Great_Plain, Transdanubia], layout=layout)
#off.iplot(data, filename='scatter-mode')"""
