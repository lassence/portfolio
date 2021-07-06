# Revenue modeling for client X

This is an analysis to estimate revenue of online generated Leads, and use as proxy values for Google Ads campaigns, to enable advanced automated bidding strategies.

_For privacy reasons, only the code is publicly accessible, not the output of the notebook. Please contact me for more detail about this project._

## Context

For Google Ads (formerly named Adwords), one way to try to enhance performance is to activate [automated bidding](https://support.google.com/google-ads/answer/2979071). Indeed, as SEA campaigns have increased in granularity over the years, they have equivalently grown in complexity, to the point where manual campaign management becomes too difficult. Automated bidding strategies are powered by Machine Learning algorithms and can handle such complexity better than humans, with the promise of better performance.

Several automated strategies are available in Google Ads, from maximising *Impression Share* to optimising *Return On Ad Spend* (ROAS). For client X, as the ultimate goal of SEA campaigns is to generate subscriptions to their service, we are interested in the subset of Google Ads bidding strategies that are focused on *conversions*. 

However, on client X websites, user can only go as far as pre-subscription, also called *leads*. The actual outcome (granted/rejected + revenue) will not be tracked on the website, and will not be available in Google Ads for campaigns optimisation. Even though it is technically possible to import this information into Google Ads, this is not an option for client X due to legal and privacy constraints. 

Thus, our goal is to maximise the actual *revenue* generated by Google Ads, while reporting performance only as far as *leads* in the platform.

## Objective of the analysis

For the Google Ads client X campaigns in France, the current conversion funnel can be schematised as:   
`Impressions -> Clicks -> Leads -> Conversion & Revenue`

The tracking in Google Ads goes only up to *Lead* and does not include any data about actual *Conversions* and associated *Revenue*.

Our goal is to provide Google Ads with an estimation of the expected revenue for every Lead, so that bidding can be optimised on revenue (*Target ROAS* strategy) and not only on Leads (*Target CPA* strategy). This estimated value can then be injected in the Google Ads [tracking tag](https://support.google.com/google-ads/answer/6095947) implemented on the website, thus reporting a dummy revenue value to the Google Ads algorithms for each Lead. 

In this analysis, we try to identify the most significant dimension(s) (Product, Device, Date, etc.) to predict an average Revenue per Lead.

While our estimations will by definition never be perfectly accurate, the business decision criterion should be **whether the performance gains of switching to a ROAS bidding strategy based on approximate revenue will outweigh Manual or Target CPA strategies based only on Leads**.

## Pre-requisites

1. A dataset that includes Google Ads performance reporting joined with the associated Conversions and Revenue (from internal sources) for the **last 12 months**, in order to have enough volume and relatively fresh data. The dimensions and metrics of the dataset are detailed in a later section.   

2. Only include **non-brand campaigns** data. Brand campaigns usually appear later in the conversion funnel, and have very different performance, that should be considered separately from generic campaigns.  

3. Each campaign with a Target ROAS strategy should generate at least **15 Leads over a 30 days period** (50 Leads recommended), in order for the algorithm to have enough data.   

4. We have focused on **Google** Search campaigns, which usually represent most of the Search spends. However the same principle could theoretically be applied to other search engines, once this strategy has been successfully applied to Google campaigns.  

## Documentation and resources

The [Google Ads Help website](https://support.google.com/google-ads/) provides detailed and up-to-date information, and is a privileged source of information.

Specifically, the links below provide useful information for this analysis:
- [About automated bidding](https://support.google.com/google-ads/answer/2979071)  
- [Smart Bidding contextual signals](https://support.google.com/google-ads/answer/7065882)
- [About Target CPA bidding](https://support.google.com/google-ads/answer/6268632)
- [About Target ROAS bidding](https://support.google.com/google-ads/answer/6268637)
- [About transactions value](https://support.google.com/google-ads/answer/3419241)
- [Track transaction-specific value](https://support.google.com/google-ads/answer/6095947)

## Setup and data loading

```python
### Standard libraries
import pandas as pd
import numpy as np

### Machine Learning libraries
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

### Graph setup
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
sns.set();
```

```python
### Load data
df = pd.read_csv('../data/raw_dataset.csv', low_memory=False)

### Look at columns and number of rows
df.info(verbose=False)
```

## Data preparation

```python
clean_df = (
    df
    # Filter out rows with zero impressions, except if they have a cost or a Lead
    .loc[lambda x: (x['Impressions'] > 0) | (x['Cost'] > 0) | (x['Leads'] > 0)]
    .assign(Cost=lambda x: x['Cost']/1000000,
            Date=lambda x: pd.to_datetime(x['Day']),
            CampaignNetwork=lambda x: x['Campaign'].str.extract(r'^([A-Z]+)_'),
            CampaignBrand=lambda x: x['Campaign'].str.contains(r'_Marque_'),
            CampaignMobile=lambda x: x['Campaign'].str.contains(r'_Mobile'),
            Campaign=lambda x: x['Campaign'].apply(lambda y: str(hash(y))),   # Anonymize campaign names
            KwUniqueID=(df['Ad group ID'].astype(str) + df['Keyword ID'].astype(str)),
            Week=lambda x: x['Date'].dt.isocalendar().week,
            WeekDay=lambda x: x['Date'].dt.weekday,
            MonthDay=lambda x: x['Date'].dt.day)
    .loc[:, ['CampaignNetwork', 'CampaignBrand', 'CampaignMobile', 'Campaign', 'Adgroup', 
             'Keyword', 'KwUniqueID', 'Week', 'MonthDay', 'WeekDay', 'Date', 'Cost', 
             'Impressions', 'Clicks', 'Leads', 'Convs', 'Revenue', 'Product']]
    # Zero Leads generated by brand campaigns and GDN campaigns ==> filter them out
    .loc[lambda x: (x['CampaignBrand'] == False) & (x['CampaignNetwork'] == 'SEA')]
    .sort_values(by=['Date', 'Campaign', 'Adgroup', 'Keyword'])
    .reset_index(drop=True)
)
```

```python
clean_df.info(verbose=False)
```

This transformed dataset leaves us with a smaller table, with 185K rows and 18 columns, that we can now use for further analysis.

## Data exploration

### Metrics evolution by day

```python
### Aggregate at day level
daily_df = (
    clean_df
    .loc[:, 'Date':]
    .groupby(['Date'])
    .sum()
    .assign(LeadRate=lambda x: x['Leads']/x['Clicks'],  # Leads/Clicks
            ConvRate=lambda x: x['Convs']/x['Leads'],   # Convs/Leads
            RevLead=lambda x: x['Revenue']/x['Leads'])  # Revenue/Leads
)
```

```python
### Plot key metrics by day
daily_df.plot(y=['Cost', 'Leads', 'Convs', 'Revenue'], subplots=True, sharex=False, figsize=(14,14));
```

```python
### Check absence of correlation between Leads/Clicks and Convs/Convs
sns.pairplot(daily_df[['ConvRate', 'LeadRate']])
print("Correlation coefficient between LeadRate and ConvRate: {:.4f}".format(daily_df['ConvRate'].corr(daily_df['LeadRate'])))
```

```python
### Look at summary metrics
daily_df.agg(['sum', 'mean', 'median', 'std', 'min', 'max'])
```

As we can see above, while Adwords-related data is available from DD/MM/YYYY up to DD/MM/YYYY, we only have **conversion data up to MM YYYY**, e.g. about x months of data.  

Specifically on conversion data, we have **x Leads, y Convs and z€ revenue**. The overall "Conversion Rate" (`ConvRate` = `Convs`/`Leads`) is x%, and the average Revenue per Lead (`RevLead` = `Revenue`/`Leads`) is x€.

```python
### Remove all data after DD/MM, as there is no conversion
clean_df = clean_df.loc[lambda x: x['Date'] <= '2018-08-01', :]
```

### Distribution of production metrics

We will be interested in the dispersion of `ConvRate` and `RevLead` metrics, so let's have a look at their overall distribution:

```python
### Look at distribution of final conversions
fig, ax = plt.subplots(2, 1, figsize=(12, 8))

sns.histplot(daily_df['ConvRate'].dropna(), ax=ax[0])
ax[0].axvline(daily_df['ConvRate'].mean(), color='r')

sns.histplot(daily_df['RevLead'].dropna(), color='g', ax=ax[1])
ax[1].axvline(daily_df['RevLead'].mean(), color='r');
```

### Conversions by campaigns, adgroups and keywords

One important aspect for conversions estimations is how granular we can go down the Adwords structure, which is correlated to how many conversions we have at Campaign/Adgroup/Keyword level. Let's have a look at conversions volumes by level.

```python
adwords_structure_df = (
    clean_df
    .groupby(['Campaign', 'Adgroup', 'Keyword', 'KwUniqueID'])
    .agg(sum)
    .loc[:, 'Cost':'Revenue']
    .sort_values('Convs', ascending=False)
    .reset_index()
)
```

```python
fig, ax = plt.subplots(1, 1, figsize=(14, 6))
n = 30
pd.concat([
(
    adwords_structure_df
    .groupby('Campaign').sum()
    .sort_values('Convs', ascending=False)
    .reset_index()
    .loc[:n, ['Convs']]
    .rename(columns={'Convs': 'Top Campaign Convs'})
),
(
    adwords_structure_df
    .groupby(['Campaign', 'Adgroup']).sum()
    .sort_values('Convs', ascending=False)
    .reset_index()
    .loc[:n, ['Convs']]
    .rename(columns={'Convs': 'Top Adgroup Convs'})
),
(
    adwords_structure_df
    .groupby(['Campaign', 'Adgroup', 'Keyword']).sum()
    .sort_values('Convs', ascending=False)
    .reset_index()
    .loc[:n, ['Convs']]
    .rename(columns={'Convs': 'Top Keyword Convs'})
)
], axis=1).plot(kind='bar', ax=ax)
ax.axhline(10, color='gray', linestyle='--');
```

If we define the **minimum number of Convs at 10** to calculate meaningful, statistically significant metrics, we will be limited by our dataset to the top 16 Campaigns, after which the number of observed Convs drops below 10.

## Estimate features importances with 'dummy' models

Several dimensions may intuitively be analysed, to look at how they affect average Revenue per Lead: day of month, day of week, device, campaign. We choose to not go more granular than Campaign (i.e. not at Adgroup or Keyword level), as there would be too many values, and consequently too small volumes, as seen in the graph above.

However, to have a hint at which dimensions may be the most "discriminant" in explaining the Revenue per Lead, we can mimic a simple Machine Learning model for rows with exactly 1 Lead. While the model will be very simple and not exploitable for actual prediction, it may guide us to the prominent dimensions.

### Prepare data

```python
### Keep only rows with Leads == 1, to mimic non-aggregated data
model_df = (
    clean_df
    .loc[lambda x: x['Leads'] == 1, :]
    .assign(Converted=lambda x: (x['Convs'] > 0).astype('int'),
            CampaignDummy=clean_df['Campaign'].astype('category').cat.codes,
            CampaignMobile=clean_df['CampaignMobile'].astype('int'))
    .loc[:, ['Campaign', 'CampaignDummy', 'CampaignMobile', 'WeekDay', 'MonthDay', 'Converted', 'Revenue']]
    .reset_index(drop=True)
)
```

```python
### Split into features and target datasets
np.random.seed(2222)
X = model_df.iloc[:, 1:-2]
y = model_df.iloc[:, -1]

### Split into training and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
```

### Helper function

```python
### Utility function for fitting model and displaying features importance
def show_features(model):
    
    # Fit model
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)
    
    # Features importance
    feature_importance = model.feature_importances_
    sorted_idx = np.argsort(feature_importance)

    # Plot features
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, X.columns[sorted_idx])
    title = 'R²: ' + str(round(model.score(X_test, y_test), 4))
    plt.title(title);
```

### Gradient Boosting

```python
np.random.seed(2222)
show_features(GradientBoostingRegressor())
```

### Random Forest

```python
np.random.seed(2222)
show_features(RandomForestRegressor(n_estimators=100))
```

### Insights from the features importance estimation

Both the Gradient Boosting and Random Forest classify `MonthDay` and `CampaignDummy` as the two most significant dimensions in estimating if a Lead will lead to a Conversion. Also, `CampaignMobile` seems to be a poorly discriminant feature.

The following remarks can be made:  
1. Based on the current Adwords structure, **`Campaigns` include several pieces of information**:  
    1. *Device*: according to the current design, Mobile and Desktop/Tablets campaigns are separated. Thus, `Campaign` and `CampaignMobile` are strongly intercorrelated.  
    2. *Product*: thematic-related campaigns, e.g. `XXXX`, probably induce a higher probability of converting on a specific product.  
    3. *Quality of the `Leads`*: it might be that very specific queries (`xxxx`) come from more engaged users than from more generic keywords (e.g. `xxxx`)  

2. `MonthDay` seem to be a relevant feature, but it includes **31 different values, which may be too granular** combined with one or more other dimensions, and lead to small `Convs` volumes.

## Conversion KPIs broken down by dimensions

We can now dive deeper in the 4 dimensions (`Campaign`, `MonthDay`, `WeekDay`, `CampaignMobile`) and look at their distribution. We are especially interested in dimensions that have values with low dispersion.

Dispersion can be calculated with the following criteria:
- Standard Deviation
- Coefficient of Variation = Standard Deviation / Mean
- Interquartile Range

```python
### Helper function for plotting production KPIs by different dimensions
def graph_dist(dimension, graph_data=None, style='violin'):
    
    if graph_data is None:
        graph_data = (
            clean_df
            .groupby([dimension, 'Date'], as_index=False)
            .agg(sum)
            .assign(ConvRate=lambda x: x['Convs']/x['Leads'])
            .assign(RevLead=lambda x: x['Revenue']/x['Leads'])
        )
        
    if style == 'violin':
        g = sns.violinplot(x=dimension, y='ConvRate', data=graph_data, cut=0, color='b', ax=ax[0])
        g = sns.violinplot(x=dimension, y='RevLead', data=graph_data, cut=0, color='g', ax=ax[1])
    else:
        g = sns.boxplot(x=dimension, y='ConvRate', data=graph_data, width=0.3, showfliers=False, color='b', ax=ax[0])
        g = sns.boxplot(x=dimension, y='RevLead', data=graph_data, width=0.3, showfliers=False, color='g', ax=ax[1])        
    
    return g
```

```python
### Function to extract main dispersion metrics for a given dimension
def summary_dim(dimension):
    
    df = (
        clean_df
        .assign(ConvRate=lambda x: x['Convs']/x['Leads'])
        .assign(RevLead=lambda x: x['Revenue']/x['Leads'])
        .loc[:, [dimension, 'Leads', 'Convs', 'Revenue', 'ConvRate', 'RevLead']]
        .groupby(dimension, as_index=True)
        .agg({'Leads': 'sum', 'Convs': 'sum', 'Revenue': 'sum', 
              'ConvRate': ['mean', 'std'], 
              'RevLead' : ['mean', 'std']
             })
    )
    df['ConvRate', 'coeff_var'] = df['ConvRate', 'std']/df['ConvRate', 'mean']
    df['RevLead', 'coeff_var'] = df['RevLead', 'std']/df['RevLead', 'mean']
    for col in [0, 1, 2]:
        df.iloc[:, col] = df.iloc[:, col].astype(int)
    for col in [3, 4]:
        df.iloc[:, col] = df.iloc[:, col].round(4)
    for col in [5, 6, 7, 8]:
        df.iloc[:, col] = df.iloc[:, col].round(2)
        
    return df.iloc[:, [0,1,2,3,4,7,5,6,8]]
```

### By device

```python
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
graph_dist('CampaignMobile');
```

```python
summary_dim('CampaignMobile')
```

### By day of week

```python
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
graph_dist('WeekDay');
```

```python
summary_dim('WeekDay')
```

### By day of month

```python
fig, ax = plt.subplots(2, 1, figsize=(14, 12))
graph_dist('MonthDay', style='box');
```

```python
summary_dim('MonthDay').head(10)
```

### By top campaign

```python
### Group by week, to have enough data by campaign
top_campaigns_df = (
    clean_df
    .groupby('Campaign', as_index=False)
    .sum()
    .sort_values('Convs', ascending=False)
    .head(15)
    .reset_index(drop=True)
)
graph_df = (
    clean_df
    .loc[clean_df['Campaign'].isin(top_campaigns_df['Campaign'])]
    .groupby(['Campaign', 'Week'], as_index=False)
    .agg(sum)
    .assign(ConvRate=lambda x: x['Convs']/x['Leads'])
    .assign(RevLead=lambda x: x['Revenue']/x['Leads'])
)
fig, ax = plt.subplots(2, 1, figsize=(14, 12))
graph_dist('Campaign', graph_data=graph_df, style='box')
[label.set_rotation(90) for axe in ax for label in axe.get_xticklabels()]
plt.setp(ax[0].get_xticklabels(), visible=False);
```

## Crossing dimensions

```python
def cross_dim(dimensions):

    graph_df = (
        clean_df
        .groupby(dimensions)
        .agg({'Leads': ['sum', 'mean', 'std']})
    )
    graph_df.columns = graph_df.columns.get_level_values(1)
    graph_df['coeff_var'] = graph_df['std']/graph_df['mean']

    g = sns.heatmap(graph_df['sum'].unstack(), annot=True, fmt='.0f', cmap='rocket', ax=ax[0])
    g = sns.heatmap(graph_df['coeff_var'].unstack(), annot=True, fmt='.3f', cmap="Greens_r", ax=ax[1])
    return g
```

### Weekday x Device

```python
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
cross_dim(['WeekDay', 'CampaignMobile']);
```

### Monthday x Mobile

```python
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
cross_dim(['MonthDay', 'CampaignMobile']);
```

### Monthday x Weekday

```python
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
cross_dim(['MonthDay', 'WeekDay']);
```

### Clustering by cross-dimensions

```python
graph_df = (
    clean_df
    .groupby(['MonthDay', 'CampaignMobile'])
    .agg(sum)
    .loc[:, ['Leads', 'Convs', 'Revenue']]
    .assign(RevLead=lambda x: x['Revenue']/x['Leads'])
)
sns.clustermap(graph_df['RevLead'].unstack());
```

## Clustering days of month by similarity

```python
fig, ax = plt.subplots(2, 1, figsize=(14, 14))

### Prepare data
graph_df = (
    clean_df
    .groupby('MonthDay')
    .agg(sum)
    .loc[:, ['Leads', 'Convs', 'Revenue']]
    .assign(RevLead=lambda x: x['Revenue']/x['Leads'])
    .reset_index()
)

### Dendogram for clustering
Z = linkage(graph_df[['RevLead']], 'single')
dendrogram(Z, labels=range(1, 32), color_threshold=10,
           leaf_rotation=0, leaf_font_size=12, ax=ax[0]);

### Compute clusters
days_clusters = (pd.DataFrame(
    fcluster(Z, 5, criterion='maxclust'), 
    index=list(range(1,32)), 
    columns=['MonthDayCluster'])
).merge(
    graph_df, how='left', 
    left_index=True, right_on='MonthDay'
)

### Plot of days sorted by RevLead
sns.barplot(data=days_clusters, x='MonthDay', y='RevLead', hue='MonthDayCluster', 
            order=days_clusters.sort_values('RevLead', ascending=False)['MonthDay'], 
            dodge=False, ax=ax[1]);
```

```python
graph_df = (
     clean_df
    .groupby(['MonthDay', 'Date'], as_index=False)
    .agg(sum)
    .assign(ConvRate=lambda x: x['Convs']/x['Leads'],
            RevLead=lambda x: x['Revenue']/x['Leads'])
    .merge(days_clusters[['MonthDay', 'MonthDayCluster']], how='left', on='MonthDay')
)

fig, ax = plt.subplots(1, 2, figsize=(14,6))
sns.boxplot(x='MonthDayCluster', y='RevLead', data=graph_df, showfliers=False, ax=ax[0])
sns.pointplot(x='MonthDayCluster', y='RevLead', color='gold', data=graph_df, ax=ax[0])
sns.barplot(data=days_clusters.groupby('MonthDayCluster', as_index=False).sum(), 
            x='MonthDayCluster', y='Convs');
```

```python
final_df = (
    clean_df
    .merge(days_clusters[['MonthDay', 'MonthDayCluster']], on='MonthDay')
    .groupby(['MonthDayCluster', 'Campaign'])
    .sum()
    .loc[:, 'Leads':]
    .reset_index()
)

### Group campaigns that have less Convs than a threshold
threshold = 7
final_df['CampaignGroup'] = (
    final_df
    .apply(lambda x: x['Campaign'] if x['Convs'] >= threshold else 'Other campaigns', axis=1)
)

### Final grouping
final_df = (
    final_df
    .groupby(['MonthDayCluster', 'CampaignGroup'])
    .agg('sum')
    .assign(RevLead=lambda x: x['Revenue']/x['Leads'],
            ConvRate=lambda x: x['Convs']/x['Leads'])
)

### Plot number of Convs per cluster
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
sns.heatmap(final_df['Convs'].unstack().transpose(), annot=True, fmt='.0f', cmap='rocket');
```

### Smart bidding minimum conversions

Beyond statistical significance of Revenue per Leads, we must take into account the [minimum 
volume of conversions](https://support.google.com/google-ads/answer/6268637?hl=en) that Adwords requires to activate Smart Bidding, e.g. **~15 Leads over the last 30 days.**

## Volatility of dimensions

```python
(
    clean_df
    .groupby(['Week'])
    .agg('sum')
    .reset_index()
    .loc[:, ['Week', 'Cost', 'Leads', 'Convs', 'Revenue']]
    .assign(ConvRate=lambda x: x['Convs']/x['Leads'],
            RevLead=lambda x: x['Revenue']/x['Leads'])
).plot(x='Week', y=['Convs', 'RevLead'], subplots='True', figsize=(14,10));
```

```python
graph_df = (
    clean_df
    .groupby(['Campaign', 'Week'])
    .agg('sum')
    .reset_index()
    .loc[lambda x: x['Campaign'].isin(top_campaigns_df.loc[:5, 'Campaign']), 
         ['Campaign', 'Week', 'Cost', 'Leads', 'Convs', 'Revenue']]
    .assign(ConvRate=lambda x: x['Convs']/x['Leads'],
            RevLead=lambda x: x['Revenue']/x['Leads'])
)

fig, ax = plt.subplots(2, 1, figsize=(14, 12))
sns.pointplot(data=graph_df, x='Week', y='RevLead', hue='Campaign', markers='', legend=False, ax=ax[0])
sns.pointplot(data=graph_df, x='Week', y='ConvRate',  hue='Campaign', markers='', legend=False, ax=ax[1]);
```