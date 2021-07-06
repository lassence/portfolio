# Rolling average in SQL

To compute rolling averages in SQL (typically over the last N periods), the basic syntax is `AVG(metric) OVER (ORDER BY dimension ROWS N-1 PRECEDING)`, with variations depending on the window over which you want to calculate the average.

```python
%%bigquery
# Get Google Analytics sample data for July 2017
WITH sub1 AS (
      SELECT PARSE_DATE("%Y%m%d", date) AS day,
             SUM(totals.visits) AS sessions
        FROM `bigquery-public-data.google_analytics_sample.ga_sessions_201707*` 
    GROUP BY day
    ORDER BY day
       LIMIT 10
)

SELECT day,
       sessions,
       # Rolling average over 3 days, including current day
       AVG(sessions) OVER (ORDER BY day ROWS 2 PRECEDING) AS sessions_3d,
       # Rolling average over the last 3 days, excluding current day
       AVG(sessions) OVER (ORDER BY day ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS sessions_last_3d,
       # Cumulative moving average over full preceding period
       AVG(sessions) OVER (ORDER BY day ROWS UNBOUNDED PRECEDING) AS sessions_avg_ctd
  FROM sub1
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>day</th>
      <th>sessions</th>
      <th>sessions_3d</th>
      <th>sessions_last_3d</th>
      <th>sessions_avg_ctd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-01</td>
      <td>2048</td>
      <td>2048.000000</td>
      <td>NaN</td>
      <td>2048.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-07-02</td>
      <td>1895</td>
      <td>1971.500000</td>
      <td>2048.000000</td>
      <td>1971.500000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-03</td>
      <td>2046</td>
      <td>1996.333333</td>
      <td>1971.500000</td>
      <td>1996.333333</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-07-04</td>
      <td>1938</td>
      <td>1959.666667</td>
      <td>1996.333333</td>
      <td>1981.750000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-07-05</td>
      <td>2885</td>
      <td>2289.666667</td>
      <td>1959.666667</td>
      <td>2162.400000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-07-06</td>
      <td>2658</td>
      <td>2493.666667</td>
      <td>2289.666667</td>
      <td>2245.000000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-07-07</td>
      <td>2450</td>
      <td>2664.333333</td>
      <td>2493.666667</td>
      <td>2274.285714</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-07-08</td>
      <td>1859</td>
      <td>2322.333333</td>
      <td>2664.333333</td>
      <td>2222.375000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-07-09</td>
      <td>1921</td>
      <td>2076.666667</td>
      <td>2322.333333</td>
      <td>2188.888889</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-07-10</td>
      <td>2769</td>
      <td>2183.000000</td>
      <td>2076.666667</td>
      <td>2246.900000</td>
    </tr>
  </tbody>
</table>
</div>

