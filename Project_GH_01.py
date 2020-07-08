df = pd.read_csv('https://covid19.who.int/WHO-COVID-19-global-data.csv', encoding='utf-8-sig')
df['Date_reported'] = pd.to_datetime(df['Date_reported'])
df.dropna(inplace= True)
df.columns = df.columns.str.strip()
#df.columns

df.sort_values(by= ['Country_code','Date_reported'], ascending= [True, False], inplace= True, na_position='first')
df.drop_duplicates(subset='Country_code', keep= 'first', inplace= True)

#df.info
#df.columns

df2 = pd.read_csv('worldcities.csv')
df2.drop_duplicates(subset='iso2', keep= 'first', inplace= True)
df2 = df2[['country','iso2','lat','lng']]
df2.rename(columns= {'iso2':'Country_code'}, inplace=True)
#df2.columns
#df2.head()
#df2.shape
#df2.info()

#Este código funciona pero tiene inconvenientes si un país no reportó el último día: no aparece en el mapa
#df3 = df[df['Date_reported'] == max(df['Date_reported'])]
#Se usa este mejor

df_inner = pd.merge(df, df2, on = 'Country_code', how = 'inner')
df_inner.dropna(inplace=True)
#df_inner.shape
#df_inner.info()
#df_inner.tail(50)

map1 = folium.Map()

for i in range(0, len(df_inner)):
  folium.Circle(
      location = [df_inner.iloc[i]['lat'], df_inner.iloc[i]['lng']],
      color= 'darkgreen', fill= 'darkgreen',
      radius= int(df_inner.iloc[i]['Cumulative_cases'])).add_to(map1)

pais_interes = ['CO', 'US', 'BR', 'IT', 'FR']
df_pais_interes = pd.DataFrame()

for i in pais_interes:
  df_pais_interes = df_pais_interes.append(
      df_inner[df_inner.Country_code ==  i])

print(df_pais_interes)

for i in range(0,len(df_pais_interes)):
  folium.Marker(location=[df_pais_interes.iloc[i]['lat'], df_pais_interes.iloc[i]['lng']], popup=df_pais_interes.iloc[i]['Country_code']).add_to(map1)

#print(df2[df2.Country_code=='US'])
#print(df_inner[df_inner.Country_code=='US'])

#print(df2[df2.Country_code=='CO'])
#print(df_inner[df_inner.Country_code=='CO'])
print(df_inner[df_inner.Country_code=='CO'].Cumulative_cases)
print(df_inner[df_inner.Country_code=='CO'].Cumulative_deaths)

map1.save('COVID-19_to_date_map.html')
map1
