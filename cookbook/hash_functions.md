# Assign users to experiment groups with hash functions

In the case of statistical experiments, some hash functions that produce integers can be used for easily **pseudo-randomly** and **deterministically** assign users to groups.

The process works as follows:
1. Hash a unique identifier of each user, for example their UID --> it will generate a large integer
2. Optionally get the absolute value of the hash, because it can be negative
3. Apply a modulo to the integer, corresponding to the number of experimentation groups that you want

## Hash in Python

⚠️ **Warning**: in Python, using the built-in `hash()` function will produce different outputs across sessions if you don't explicitly specify the same hash seed value every time.

```python
# Set hash seed
%env PYTHONHASHSEED=0
```

    env: PYTHONHASHSEED=0

```python
# Import libraries
import pandas as pd

# Sample dataframe of UIDs
df = pd.DataFrame({'uid':[
    'd4212ed3-4399-4f5b-87ab-faec4f6558f8',
    'a9780c08-9714-4da2-a53c-6102d5f47cf7',
    '26c6853f-cae9-4a06-849d-7df46d744e5a',
    'efc1583b-946a-449f-a811-87d241e57bc4',
    '60d568e2-052b-4ca3-83da-34ee00ef5c6b'
]})
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>uid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>d4212ed3-4399-4f5b-87ab-faec4f6558f8</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a9780c08-9714-4da2-a53c-6102d5f47cf7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>26c6853f-cae9-4a06-849d-7df46d744e5a</td>
    </tr>
    <tr>
      <th>3</th>
      <td>efc1583b-946a-449f-a811-87d241e57bc4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>60d568e2-052b-4ca3-83da-34ee00ef5c6b</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Step 1a: compute hash value for each user UID
df['uid_hash'] = df['uid'].apply(hash)
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>uid</th>
      <th>uid_hash</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>d4212ed3-4399-4f5b-87ab-faec4f6558f8</td>
      <td>8654918514890274169</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a9780c08-9714-4da2-a53c-6102d5f47cf7</td>
      <td>1340609583511541598</td>
    </tr>
    <tr>
      <th>2</th>
      <td>26c6853f-cae9-4a06-849d-7df46d744e5a</td>
      <td>-1679195277781215170</td>
    </tr>
    <tr>
      <th>3</th>
      <td>efc1583b-946a-449f-a811-87d241e57bc4</td>
      <td>-2786820932382908882</td>
    </tr>
    <tr>
      <th>4</th>
      <td>60d568e2-052b-4ca3-83da-34ee00ef5c6b</td>
      <td>3180348019046944236</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Step 1b: get the absolute value of the hash
df['abs_hash'] = df['uid_hash'].apply(abs)
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>uid</th>
      <th>uid_hash</th>
      <th>abs_hash</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>d4212ed3-4399-4f5b-87ab-faec4f6558f8</td>
      <td>8654918514890274169</td>
      <td>8654918514890274169</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a9780c08-9714-4da2-a53c-6102d5f47cf7</td>
      <td>1340609583511541598</td>
      <td>1340609583511541598</td>
    </tr>
    <tr>
      <th>2</th>
      <td>26c6853f-cae9-4a06-849d-7df46d744e5a</td>
      <td>-1679195277781215170</td>
      <td>1679195277781215170</td>
    </tr>
    <tr>
      <th>3</th>
      <td>efc1583b-946a-449f-a811-87d241e57bc4</td>
      <td>-2786820932382908882</td>
      <td>2786820932382908882</td>
    </tr>
    <tr>
      <th>4</th>
      <td>60d568e2-052b-4ca3-83da-34ee00ef5c6b</td>
      <td>3180348019046944236</td>
      <td>3180348019046944236</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Step 3: apply a modulo, to reduce each hash
# In this example, we want 5 groups
groups = 5
df['user_group'] = df['abs_hash'].apply(lambda x: x % groups)
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>uid</th>
      <th>uid_hash</th>
      <th>abs_hash</th>
      <th>user_group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>d4212ed3-4399-4f5b-87ab-faec4f6558f8</td>
      <td>8654918514890274169</td>
      <td>8654918514890274169</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a9780c08-9714-4da2-a53c-6102d5f47cf7</td>
      <td>1340609583511541598</td>
      <td>1340609583511541598</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>26c6853f-cae9-4a06-849d-7df46d744e5a</td>
      <td>-1679195277781215170</td>
      <td>1679195277781215170</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>efc1583b-946a-449f-a811-87d241e57bc4</td>
      <td>-2786820932382908882</td>
      <td>2786820932382908882</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>60d568e2-052b-4ca3-83da-34ee00ef5c6b</td>
      <td>3180348019046944236</td>
      <td>3180348019046944236</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

## Hash in Redshift

Redshift provides several [hash functions](https://docs.aws.amazon.com/redshift/latest/dg/hash-functions.html), with one algorithm named [FNV](https://docs.aws.amazon.com/redshift/latest/dg/r_FNV_HASH.html) outputing integers with `FNV_HASH()`.

```sql
-- Redshift hash with FNV_HASH() function
SELECT
    uid,
    FNV_HASH(uid) AS uid_hash,
    ABS(FNV_HASH(uid)) AS abs_hash,
    MOD(ABS(FNV_HASH(uid)), 5) AS user_group
FROM users
```

| uid                                  | uid_hash             | abs_hash            | user_group |
|--------------------------------------|----------------------|---------------------|------------|
| e5bc5b34-7591-440b-afe5-abd09ce9e7fc | 3227803941034506429  | 3227803941034506429 | 4          |
| 45537e99-fb26-4f91-bc05-54609a1aaea4 | -5122133721459384104 | 5122133721459384104 | 4          |
| dd654604-c782-4bb7-b8b1-f4d29544901d | -6617981390633479988 | 6617981390633479988 | 3          |
| cdd58d6c-cc32-4d08-9bc2-5dbd9794a850 | -8431386626058726789 | 8431386626058726789 | 4          |
| 312fa481-ade1-4049-a0a2-1f8fd8127038 | -6575192304779364999 | 6575192304779364999 | 4          |
| 92a78700-1776-4bdd-9a30-3f1e2a5215ad | -3502909049117672277 | 3502909049117672277 | 2          |
| ff9bf307-46ed-4eaa-8768-56d9bd243638 | -3896326129685120733 | 3896326129685120733 | 3          |
| df0feb24-46fb-4413-a6dd-bc720a8404e0 | -1574156297740572233 | 1574156297740572233 | 3          |
| c88e885f-7e07-4164-bbef-8b3e06b01c03 | -2193445785569549438 | 2193445785569549438 | 3          |
| e6840bd5-a7f8-4bca-b3c4-dd0d063bd805 | 7232213398192042271  | 7232213398192042271 | 1          |

## Hash in Biguery

BigQuery provides a [deterministic fingerprinting](https://cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions) based on the FarmHash library with the `FARM_FINGERPRINT()` function

```sql
-- BigQuery provides FARM_FINGERPRINT() for hash
SELECT
    uid,
    FARM_FINGERPRINT(uid) AS uid_hash,
    ABS(FARM_FINGERPRINT(uid)) AS abs_hash,
    MOD(ABS(FARM_FINGERPRINT(uid)), 5) AS user_group
FROM users
```

| uid                                  | uid_hash             | abs_hash            | user_group |
|--------------------------------------|----------------------|---------------------|------------|
| e5bc5b34-7591-440b-afe5-abd09ce9e7fc | -7787564224466934590 | 7787564224466934590 | 0          |
| 45537e99-fb26-4f91-bc05-54609a1aaea4 | 5608318025082862745  | 5608318025082862745 | 0          |
| dd654604-c782-4bb7-b8b1-f4d29544901d | 5934209085968642182  | 5934209085968642182 | 2          |
| cdd58d6c-cc32-4d08-9bc2-5dbd9794a850 | -616326417315919032  | 616326417315919032  | 2          |
| 312fa481-ade1-4049-a0a2-1f8fd8127038 | 8906102320423035382  | 8906102320423035382 | 2          |
| 92a78700-1776-4bdd-9a30-3f1e2a5215ad | -6944503593848300382 | 6944503593848300382 | 2          |
| ff9bf307-46ed-4eaa-8768-56d9bd243638 | 941176159813038931   | 941176159813038931  | 1          |
| df0feb24-46fb-4413-a6dd-bc720a8404e0 | -7011198657730055701 | 7011198657730055701 | 1          |
| c88e885f-7e07-4164-bbef-8b3e06b01c03 | -7735882866151441807 | 7735882866151441807 | 2          |
| e6840bd5-a7f8-4bca-b3c4-dd0d063bd805 | 7843601242992569940  | 7843601242992569940 | 0          |
