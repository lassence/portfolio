## Setup

```python
### Import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import lifetimes
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.plotting import plot_frequency_recency_matrix
from lifetimes.plotting import plot_probability_alive_matrix
from lifetimes.plotting import plot_period_transactions
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

import sklearn
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

### Set options
pd.set_option('display.max_columns', 40)
%matplotlib inline
sns.set();
```

## Data import and cleaning

```python
### Load file
df = pd.read_csv('./exclude/eshop_transaction.csv', dtype='object')

### Remove useless columsn
remove_cols = ['Currency', 'Lineitem sku', 'Lineitem requires shipping',
               'Lineitem taxable', 'Lineitem discount', 'Vendor']
df = df.drop(columns=remove_cols)

### Rename columns with standardized names
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

### Convert 'datetime' columns
for col in df.filter(regex='_at$', axis=1):
    df[col] = pd.to_datetime(df[col], utc=True)

### Convert 'float' columns
for col in ['subtotal', 'shipping', 'taxes', 'total', 'discount_amount',
            'lineitem_price', 'lineitem_compare_at_price', 'refunded_amount']:
    df[col] = df[col].astype('float')

### Convert 'int' columns
df['lineitem_quantity'] = df['lineitem_quantity'].astype('int')

### Clean order_id but keep as str
df['order_id'] = df['order_id'].str.replace('^#', '')

### Add and rename some columns
df['order_date'] = df['created_at'].dt.date.astype('datetime64[ns]')

### Anonymize data
df['client_id'] = df['client_id'].apply(lambda x: x[0:15])
```

## Exploration

### Summary

```python
%%capture
### Summary data (not printed for anonymity)
print(f"Period range: {df['order_date'].min():%Y-%m-%d} to {df['order_date'].max():%Y-%m-%d}\n"
      f"Unique clients: {df['client_id'].nunique()}\n"
      f"Orders: {df['order_id'].nunique()}\n"
      f"Total revenue: {df['total'].sum():,.0f} €\n"
      f"AOV: {df['total'].sum()/df['order_id'].nunique():.2f} €\n"
      f"Revenue per client: {df['total'].sum()/df['client_id'].nunique():.2f} €\n"
      f"Avg orders per client: {df['order_id'].nunique()/df['client_id'].nunique():.2f}\n"
      f"Total items sold: {df['lineitem_quantity'].sum()}\n"
      f"AIV: {df['total'].sum()/df['lineitem_quantity'].sum():.2f} €\n"
      f"Avg qty per order: {df['lineitem_quantity'].sum()/df['order_id'].nunique():.2f}"
)
```

### Evolution of main KPIs

```python
df_day = (
    df
    .groupby('order_date')
    .agg({'client_id': 'nunique', 'order_id': 'nunique', 'lineitem_name': 'nunique',
          'lineitem_quantity': 'sum', 'total': 'sum'})
    .rename(columns={'client_id': 'users', 'order_id': 'orders',
                     'lineitem_quantity': 'items_qty',
                     'lineitem_name': 'items'})
    .assign(total_cum=lambda x: x['total'].cumsum())
)
```

```python
df_week = (
    df
    .groupby([df['order_date'].dt.strftime("%Y%W")])
    .agg({'client_id': 'nunique', 'order_id': 'nunique', 'lineitem_name': 'nunique',
          'lineitem_quantity': 'sum', 'total': 'sum'})
    .rename(columns={'client_id': 'users', 'order_id': 'orders',
                     'lineitem_quantity': 'items_qty',
                     'lineitem_name': 'items', 'total': 'revenue'})
    .assign(revenue_cum=lambda x: x['revenue'].cumsum(),
            orders_cum=lambda x: x['orders'].cumsum(),
            items_qty_cum=lambda x: x['items_qty'].cumsum(),
            aov=lambda x: x['revenue']/x['orders'],
            aiv=lambda x: x['revenue']/x['items_qty'],
            aov_rolling=lambda x: x['aov'].rolling(4).mean(),
            aiv_rolling=lambda x: x['aiv'].rolling(4).mean(),
            aov_cum=lambda x: x['revenue_cum']/x['orders_cum'],
            aiv_cum=lambda x: x['revenue_cum']/x['items_qty_cum'])
)
```

```python
df_week.plot(y=['revenue', 'revenue_cum'], kind='area', subplots=True, figsize=(14,10),
             yticks=[0]);  # Y-axis masked for anonymity
```

![png](eshop_analysis_files/eshop_analysis_10_0.png)

```python
### Fit linear regression on cumulated revenue
fig, ax = plt.subplots(figsize=(14,6))
ax.set_xlim(0, 150)
labels = [d.strftime('%Y-%m') for d in pd.date_range(start='2017-06-21', periods=9, freq='20W')]
ax.set_xticklabels(labels)
ax.set_yticklabels([0]) # Y-axis masked for anonymity
sns.regplot(pd.DataFrame(list(range(len(df_week)))), y = df_week['revenue_cum'], marker=".");
```

![png](eshop_analysis_files/eshop_analysis_11_0.png)

```python
df_week.plot(y=['aov_rolling', 'aov_cum', 'aiv_rolling', 'aiv_cum'],
             kind='line', subplots=True, figsize=(14, 14),
             yticks=[0]);  # Y-axis masked for anonymity
```

![png](eshop_analysis_files/eshop_analysis_12_0.png)

### Products

```python
df_products = (
    df.loc[:, ['order_date', 'lineitem_name', 'lineitem_quantity', 'lineitem_price', 'total']]
    .rename(columns={'lineitem_quantity': 'qty', 'lineitem_price': 'price'})
    .assign(product=lambda x: (x['lineitem_name'].str.split(' - ')).apply(lambda x: x[0]),
            collection=lambda x: x['product'].str.split().apply(lambda x: x[0]))
    .groupby(['collection', 'product'], as_index=False)
    .agg({'qty': sum, 'price': 'mean', 'total': sum})
    .sort_values('qty', ascending=False)
    .loc[lambda x: x['qty'] >= 5]
    .reset_index(drop=True)
)
```

```python
fig, ax = plt.subplots(figsize=(14,6))
df_products.plot(x='product', y='qty', kind='bar', yticks=[0], ax=ax)
ax.set_xticklabels(list(range(0, 21)));
```

![png](eshop_analysis_files/eshop_analysis_15_0.png)

```python
### Evolution of revenue per products collection
df_collections = (
    df
    .assign(collection=lambda x: x['lineitem_name'].str.split().apply(lambda x: x[0]))
    .groupby(['collection', df['order_date'].dt.strftime("%Y%W")])
    .agg({'total': 'sum'})
    .rename(columns={'total': 'revenue'})
    .assign(revenue_cum=lambda x: x['revenue'].cumsum())
    .reset_index()
)
df_collections['revenue_cum'] = df_collections.groupby('collection')['revenue'].transform(pd.Series.cumsum)
```

```python
### Plot evolution of revenue per collection
(
    df_collections
    .pivot(index='order_date', columns='collection', values='revenue_cum')
    .fillna(method='ffill', axis=0)
    .plot(kind='area', figsize=(14,7), colormap='Set2_r', alpha=0.8,
          title="Cumulated revenue per collection",
          yticks=[0], legend=False)  # Masked for anonymity
)
```

![png](eshop_analysis_files/eshop_analysis_17_1.png)

### Zip codes

```python
df_zip = (
    df
    .assign(billing_dept=lambda x:
            df.apply(
                lambda x: (x['billing_country'] \
                           if x['billing_country'] != 'FR' \
                           else (x['billing_country'] + "_" + x['billing_zip'][1:3])),
                axis=1)
     )
    .groupby(['billing_country', 'billing_dept'], as_index=False)
    .agg({'client_id': 'nunique', 'order_id': 'nunique', 'total': 'sum', 'lineitem_quantity': 'sum'})
    .rename(columns={'client_id': 'clients', 'order_id': 'orders', 'total': 'revenue', 'lineitem_quantity': 'qty'})
    .sort_values('clients', ascending=False)
    .reset_index(drop=True)
    .assign(clients_pct=lambda x: x['clients']/x['clients'].sum(),
            revenue_pct=lambda x: x['revenue']/x['revenue'].sum())
)
```

```python
(
    df_zip
    .head(20)
    .sort_values('clients_pct', ascending=True)
    .plot(x='billing_dept', y=['clients_pct', 'revenue_pct'],
          kind='barh', figsize=(14,8))
)
```

![png](eshop_analysis_files/eshop_analysis_20_1.png)

### Best customers

```python
### Stats per client
df_clients = (
    df
    .groupby('client_id')
    .agg({'total': 'sum', 'order_id': 'nunique',
          'created_at': {'first': lambda x: x.min(),
                         'second': lambda x: (x.drop_duplicates().nsmallest(2).iloc[-1] if len(x.drop_duplicates()) > 1 else None),
                         'latest': 'max'},
          'lineitem_quantity': 'sum', 'lineitem_name': 'nunique',
          'billing_country': lambda x: x.dropna().unique()})
    .sort_values([('total','sum'), ('created_at', 'first')], ascending=[False, True])
    .reset_index()
)
df_clients.columns = ['client_id', 'revenue', 'orders',
                      'first_order', 'second_order', 'latest_order',
                      'items_qty', 'unique_items', 'country']
df_clients['aov'] = df_clients['revenue']/df_clients['orders']
df_clients['days_return'] = (df_clients['second_order']-df_clients['first_order']).dt.days
```

```python
%%capture
df_clients.head()
```

### New vs returning customers

```python
### Get new and returning client, by date
df_new_clients = (
    # First order date for each client => incremental deduplicated clients
    df_clients.groupby(df_clients['first_order'].dt.date).agg({'orders': 'count'})
    # Second order date => add returning client, substract a new client
    .merge(df_clients.groupby(df_clients['second_order'].dt.date).agg({'orders': 'count'}),
        how='outer', left_index=True, right_index=True)
    .fillna(0)
    .rename(columns={'orders_x': 'unique', 'orders_y': 'returning'})
    .assign(
        unique_cum=lambda x: x['unique'].cumsum(),
        returning_cum=lambda x: x['returning'].cumsum(),
        new_cum=lambda x: x['unique_cum']-x['returning_cum'],
        new_cum_pct=lambda x: x['new_cum']/x['unique_cum'],
        returning_cum_pct=lambda x: 1-x['new_cum_pct']
    )
)
```

```python
df_new_clients.plot(y=['returning_cum', 'new_cum'], kind='area', alpha=0.8, figsize=(14,6),
                    yticks=[0]);  # Y-axis masked for anonymity
```

![png](eshop_analysis_files/eshop_analysis_26_0.png)

```python
df_new_clients.plot(y=['returning_cum_pct', 'new_cum_pct'], kind='line', alpha=0.8, figsize=(14,6));
```

![png](eshop_analysis_files/eshop_analysis_27_0.png)

### Lag between 1st and 2nd purchase

```python
### Plot distribution of delay between 1st and 2nd purchase, for returning customers
fig, ax = plt.subplots(1, 1, figsize=(14, 6))
df_clients['days_return'].plot(kind='hist', bins=40, legend=None, alpha=0.5, ax=ax,
                               title="Delay between 1st and 2nd purchase")
ax.axvline(df_clients['days_return'].mean(), color='r');
print("Average delay: {:.1f} days".format(df_clients['days_return'].mean()))
```

    Average delay: 140.1 days

![png](eshop_analysis_files/eshop_analysis_29_1.png)

### Distribution of revenue and orders per client

```python
### Revenue per client
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
df_clients.plot(y='revenue', kind='hist', bins=50, xlim=(0,1000), alpha=0.5, yticks=[0], ax=ax)
ax.axvline(df_clients['revenue'].mean(), color='r')
```

![png](eshop_analysis_files/eshop_analysis_31_1.png)

```python
### Orders per client
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
df_clients.plot(y='orders', kind='hist', alpha=0.5, yticks=[0], ax=ax)
ax.axvline(df_clients['orders'].mean(), color='r')
```

![png](eshop_analysis_files/eshop_analysis_32_1.png)

```python
### Table of number of orders per client
(
    df_clients['orders']
    .value_counts()
    .sort_index()
    .to_frame()
    .assign(orders_pct=lambda x: x['orders']/x['orders'].sum(),
            orders_pct_cum=lambda x: x['orders_pct'].cumsum())
    .drop(columns={'orders': 'count'})  # Masked for anonymity
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>orders_pct</th>
      <th>orders_pct_cum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.708735</td>
      <td>0.708735</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.169734</td>
      <td>0.878469</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.059305</td>
      <td>0.937774</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.028046</td>
      <td>0.965819</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.014023</td>
      <td>0.979842</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.012562</td>
      <td>0.992404</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.003214</td>
      <td>0.995618</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.001753</td>
      <td>0.997371</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.000584</td>
      <td>0.997955</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.000584</td>
      <td>0.998539</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.000876</td>
      <td>0.999416</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0.000584</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>

```python
fig, ax = plt.subplots(1, 1, figsize=(12,6))
sns.boxplot(x=df_clients['orders'], y=df_clients['aov'],
            showfliers=False, ax=ax)
sns.pointplot(x=df_clients['orders'], y=df_clients['aov'],
              color='gold', ci=None, ax=ax)
ax.set_title("AOV by number of orders")
ax.set_yticklabels([0]);  # Y-axis masked for anonymity
```

![png](eshop_analysis_files/eshop_analysis_34_0.png)

### Orders per week day and hour of day

```python
### Sales stats per weekday and hour
df_weekday_hour = (
    df
    .groupby([df['created_at'].dt.weekday, df['created_at'].dt.hour])
    .agg({'total': 'sum', 'order_id': 'nunique'})
    .rename(columns={'total': 'revenue', 'order_id': 'orders'})
)

df_weekday_hour.index.names = ['weekday', 'hour']
```

```python
### Plot activity by hour and weekday
fig, ax = plt.subplots(2, 1, figsize=(12, 12))
sns.heatmap(df_weekday_hour['orders'].unstack(), ax=ax[0])
sns.lineplot(x='hour', y='orders', hue='weekday',
             data=df_weekday_hour.reset_index(),
             palette='Paired', ax=ax[1])

ax[0].set_yticklabels([0]);  # Y-axis masked for anonymity
ax[1].set_yticklabels([0]);  # Y-axis masked for anonymity
```

![png](eshop_analysis_files/eshop_analysis_37_0.png)

## Lifetime value

### Prepare data

```python
### Get list of transactions, with date, customer ID and monetary value
df_transactions = (
    df
    .groupby(['order_id'])
    .agg({'order_date': 'first', 'client_id': 'first', 'total': 'sum'})
)
```

```python
### Transform data to appropriate shape
df_rfm = summary_data_from_transaction_data(
    df_transactions, 'client_id', 'order_date',
    monetary_value_col = 'total',
    observation_period_end='2019-03-31'
)
df_rfm.head(7)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>frequency</th>
      <th>recency</th>
      <th>T</th>
      <th>monetary_value</th>
    </tr>
    <tr>
      <th>client_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0020c81355c2057</th>
      <td>1.0</td>
      <td>236.0</td>
      <td>619.0</td>
      <td>94.5</td>
    </tr>
    <tr>
      <th>003b1637ce45163</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>535.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>00444e8c950c199</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>226.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>0055eb3281238fa</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>163.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>006e783513f582e</th>
      <td>1.0</td>
      <td>103.0</td>
      <td>634.0</td>
      <td>53.0</td>
    </tr>
    <tr>
      <th>007062115a3cbd2</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>299.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>0085fabd8952f67</th>
      <td>2.0</td>
      <td>327.0</td>
      <td>439.0</td>
      <td>94.5</td>
    </tr>
  </tbody>
</table>
</div>

### Simple BG/NBD model

```python
### Fit BG/NBD model
bgf = BetaGeoFitter(penalizer_coef=0.0)
bgf.fit(df_rfm['frequency'], df_rfm['recency'], df_rfm['T'])
```

    <lifetimes.BetaGeoFitter: fitted with 3408 subjects, a: 0.83, alpha: 140.63, b: 3.55, r: 0.30>

```python
### Expected future purchases given frequency/recency
fig, ax = plt.subplots(1, 2, figsize=(8, 8))
ax = plot_frequency_recency_matrix(bgf, T=365)
ax.grid(False)
```

![png](eshop_analysis_files/eshop_analysis_44_0.png)

```python
### Probability of being alive given frequency/recency
fig, ax = plt.subplots(1, 2, figsize=(8, 8))
ax = plot_probability_alive_matrix(bgf)
ax.grid(False)
```

![png](eshop_analysis_files/eshop_analysis_45_0.png)

```python
### Predict expected purchase for every customer

# Number of periods (days) forward to predict the number of purchases
t = 365

# Create prediction dataframe
df_clv = df_rfm.copy()
df_clv['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(
    t, df_rfm['frequency'], df_rfm['recency'], df_rfm['T']
)
df_clv['proba_alive'] = bgf.conditional_probability_alive(
    frequency=df_rfm['frequency'],
    recency=df_rfm['recency'],
    T=df_rfm['T']
)
```

### Gamma-Gamma model

```python
### Keep only returning customers
df_rfm_return = df_rfm[df_rfm['frequency'] > 0]

### Check (absence of) correlation between frequency and monetary value
df_rfm_return[['frequency', 'monetary_value']].corr()
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>frequency</th>
      <th>monetary_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>frequency</th>
      <td>1.00000</td>
      <td>0.02488</td>
    </tr>
    <tr>
      <th>monetary_value</th>
      <td>0.02488</td>
      <td>1.00000</td>
    </tr>
  </tbody>
</table>
</div>

```python
### Fit Gamma-Gamme model
ggf = GammaGammaFitter()
ggf.fit(df_rfm_return['frequency'], df_rfm_return['monetary_value'])
```

    <lifetimes.GammaGammaFitter: fitted with 972 subjects, p: 15.67, q: 9.52, v: 44.74>

```python
### Predict expected value per transaction
df_clv['exp_avg_value'] = ggf.conditional_expected_average_profit(
    df_rfm['frequency'], df_rfm['monetary_value']
)

### Compare with actual average profit
df_clv['exp_avg_value'].mean(), df_rfm_return['monetary_value'].mean()
```

    (82.40351077543289, 82.45551248448625)

```python
### Predict residual Customer Lifetime Value
df_clv['clv'] = ggf.customer_lifetime_value(
    bgf, # predict the number of future transactions
    df_rfm['frequency'],
    df_rfm['recency'],
    df_rfm['T'],
    df_rfm['monetary_value'],
    time=12, # months
    discount_rate=0.01 # to be calculated for better estimation
)
```

```python
df_clv.head(10)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>frequency</th>
      <th>recency</th>
      <th>T</th>
      <th>monetary_value</th>
      <th>predicted_purchases</th>
      <th>proba_alive</th>
      <th>exp_avg_value</th>
      <th>clv</th>
    </tr>
    <tr>
      <th>client_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0020c81355c2057</th>
      <td>1.0</td>
      <td>236.0</td>
      <td>619.0</td>
      <td>94.5</td>
      <td>0.366296</td>
      <td>0.632351</td>
      <td>90.224048</td>
      <td>30.646868</td>
    </tr>
    <tr>
      <th>003b1637ce45163</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>535.0</td>
      <td>0.0</td>
      <td>0.153738</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>11.734557</td>
    </tr>
    <tr>
      <th>00444e8c950c199</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>226.0</td>
      <td>0.0</td>
      <td>0.271200</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>20.726374</td>
    </tr>
    <tr>
      <th>0055eb3281238fa</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>163.0</td>
      <td>0.0</td>
      <td>0.321570</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>24.588284</td>
    </tr>
    <tr>
      <th>006e783513f582e</th>
      <td>1.0</td>
      <td>103.0</td>
      <td>634.0</td>
      <td>53.0</td>
      <td>0.277238</td>
      <td>0.487392</td>
      <td>63.333827</td>
      <td>16.281799</td>
    </tr>
    <tr>
      <th>007062115a3cbd2</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>299.0</td>
      <td>0.0</td>
      <td>0.229641</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>17.542679</td>
    </tr>
    <tr>
      <th>0085fabd8952f67</th>
      <td>2.0</td>
      <td>327.0</td>
      <td>439.0</td>
      <td>94.5</td>
      <td>0.992625</td>
      <td>0.770313</td>
      <td>91.905301</td>
      <td>84.700322</td>
    </tr>
    <tr>
      <th>00ea24e5e4d8e23</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>531.0</td>
      <td>0.0</td>
      <td>0.154603</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>11.800679</td>
    </tr>
    <tr>
      <th>00eadbac352d329</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>533.0</td>
      <td>0.0</td>
      <td>0.154169</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>11.767525</td>
    </tr>
    <tr>
      <th>00fdec6d2a88918</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>621.0</td>
      <td>0.0</td>
      <td>0.137240</td>
      <td>1.000000</td>
      <td>82.353889</td>
      <td>10.473291</td>
    </tr>
  </tbody>
</table>
</div>

## RFM segmentation

```python
### Compute recency: number of days since last purchase
df_clients['recency'] = (
    df_clients
    .apply(
        lambda x: (df_clients['latest_order'].max() - x['latest_order']).days,
        axis=1)
)
```

```python
### Compute quantiles
df_clients['r'] = pd.qcut(df_clients['recency'], 4, labels=[3,2,1,0]).astype(int)
df_clients['f'] = pd.qcut(df_clients['orders'], 10, labels=False, duplicates='drop')
df_clients['m'] = pd.qcut(df_clients['revenue'], 4, labels=False)

### Aggregate RFM values with INVERSE value (bigger is better)
df_clients['rfm'] = df_clients['r'] * 100 + df_clients['f'] * 10 + df_clients['m']
```

```python
### Plot distribution
(
    df_clients['rfm']
    .value_counts()
    .sort_index()
    .to_frame()
    .plot(kind='bar', figsize=(10,6))
)
```

![png](eshop_analysis_files/eshop_analysis_56_1.png)

### K-means segmentation

```python
### Look at pairplot for RFM
sns.pairplot(df_clients[['revenue', 'orders', 'recency']], height=3.5)
```

![png](eshop_analysis_files/eshop_analysis_58_1.png)

```python
### Create clusters based on Recency, Frequency, Monetary value
kmeans = KMeans(n_clusters=3)
df_clients['rfm_cluster'] = kmeans.fit_predict(df_clients[['revenue', 'orders', 'recency']])
```

```python
### Plot results
fig, ax = plt.subplots(2, 2, figsize=(14,12))
sns.scatterplot(x='orders', y='revenue', hue='rfm_cluster', data=df_clients, palette='Paired', ax=ax[0,0])
sns.scatterplot(x='orders', y='recency', hue='rfm_cluster', data=df_clients, palette='Paired', ax=ax[0,1])
sns.scatterplot(x='recency', y='revenue', hue='rfm_cluster', data=df_clients, palette='Paired', ax=ax[1,0])
```

![png](eshop_analysis_files/eshop_analysis_60_1.png)
