#Solutions for Test tasks:
## Level 1 
### Prerequisites
* Python 3.7 or greater
### Files definitions:

- [src-data](src-data) - Path with source data needed to be processed.
- [processed_data](processed_data) - Path with output processed data.
- user_id.png - User image file, for example, 1001.png. Could be several for different users in source data path.
- user_id.csv - User info file, for example, 1001.csv. Could be several for different users in source data path.

User csv file contains next columns:

1. first_name - User first name
2. last_name - User last name
3. birthts - User birthdate timestamp in milliseconds UTC

Test csv and img files could be found in the [src-data](src-data) folder

**For example:**

```text
first_name, last_name, birthts
Ivan, Ivanov, 946674000000
```

### Data processing description

1. Read csv file in format user_id.csv from [src-data](src-data) folder
2. Match images in forman user_id.png for each user from [src-data](src-data) folder
3. Combine data from CSV and image path
4. Update [processed_data/output.csv](processed_data/output.csv) CSV file and add new data. Important we can update data for previously processed
   user. In output CSV and DB we should not duplicate records. Output CSV file format: user_id, first_name,
   last_name, birthts, img_path

## Solution:
#### Prerequisites
* pandas~=1.3.3


[task1.py](task1.py) is an implementation of the task, which works with demo data from [src-data](src-data) 
folder and puts a resulting data into [processed_data/output.csv](processed_data/output.csv) CSV file. Here is the code of python script:
```python
import os
import pandas as pd

res_df = pd.DataFrame()
for filename in sorted(os.listdir('src-data')):
    if filename.endswith('.csv'):
        user_id = filename[:-4]
        df = pd.read_csv(os.path.join("src-data", filename))
        df.insert(0, 'user_id', user_id)
        df['img_path'] = f'src-data/{user_id}.jpg'
        df = df.set_index('user_id')
        res_df = res_df.append(df)

res_df.to_csv("processed_data/output.csv")
```

1. Create resulting dataframe, which will include all dataframes from csv files
2. Iterate over *.csv filenames and extract user_id
3. Read csv file as a dataframe
4. Add columns `user_id` and `img_path` to the dataframe of csv file
5. Append df from csv file to the resulting dataframe
6. Write resulting dataframe into [processed_data/output.csv](processed_data/output.csv) CSV file

### SQL
1. Rewrite this SQL without subquery:
```sql
SELECT id
FROM users
WHERE id NOT IN (
	SELECT user_id
	FROM departments
	WHERE department_id = 1
);
```

**Solution:**
```sql
SELECT id
FROM users
LEFT JOIN departments ON departments.user_id = users.id 
   WHERE departments.department_id IS NULL OR departments.department_id != 1;
```

2. Write an SQL query to find all duplicate lastnames in a table named **user**
```text
+----+-----------+-----------
| id | firstname | lastname |
+----+-----------+-----------
| 1  | Ivan      | Sidorov  |
| 2  | Alexandr  | Ivanov   |
| 3  | Petr      | Petrov   |
| 4  | Stepan    | Ivanov   |
+----+-----------+----------+
```
**Solution:**
```sql
SELECT id, firstname, lastname
FROM users
GROUP BY lastname
HAVING COUNT(lastname) > 1
```
3. Write a SQL query to get a username from the **user** table with the second highest salary from **salary** tables. Show the username and it's salary in the result.
```sql
+---------+--------+
| user_id | salary |
+----+--------+----+
| 1       | 1000   |
| 2       | 1100   |
| 3       | 900    |
| 4       | 1200   |
+---------+--------+
```
```sql
+---------+--------+
| id | username    |
+----+--------+----+
| 1  | Alex       |
| 2  | Maria      |
| 3  | Bob        |
| 4  | Sean       |
+---------+-------+
```

**Solution:**
```sql
SELECT user.username, salary.salary
FROM user
INNER JOIN salary ON salary.user_id = user.id
ORDER BY salary.salary DESC 
LIMIT 1 1
```

### Algorithms and Data Structures
1. Optimise execution time of this Python code snippet:
```python
def count_connections(list1: list, list2: list) -> int:
  count = 0
  
  for i in list1:
    for j in list2:
      if i == j:
        count += 1
  
  return count
```
**Solution:**<br>
Use dictionary to count an occurrence of numbers in the first list. For each 
element of second list which we have in a dictionary add number of its occurrence(in the first list) to the answer. The complexity of the solution is O(len(list1) + len(list2)) compared to original O(len(list1) * len(list2)) or basically O(n) vs O(n^2)
```python
def count_connections(list1: list, list2: list) -> int:
    ddict = {}
    count = 0
    for i in list1:
        if i not in ddict:
            ddict[i] = 0
        ddict[i] += 1

    for i in list2:
        if i in ddict:
            count += ddict[i]
    return count

```


2. Given a string `s`, find the length of the longest substring without repeating characters.
   Analyze your solution and please provide Space and Time complexities.

**Solution:**<br>
We keep the track of last occurrence of the character in a dictionary `seq`. 
After meeting a character belonging to the subsequence, we move _"start pointer"_ 
to the last position of the character and assign the value of `seq` to the current position. <br>
Time complexity - O(n), n - length of a string. <br>
Space complexity - O(k), where k - maximum number of distinct characters in `s`


```python
def longest_subs(s: str): 
    seq = {}
    max_len = 0
    start = 0
    for end in range(len(s)):
        if s[end] in seq:
            start = seq[s[end]] + 1
        seq[s[end]] = end
        max_len = max(max_len, end - start + 1)
    return max_len
```

**Example**
```python
s = "abcabcbb"
print(longest_subs(s))      # Output: 3
```


3. Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

**Solution:**<br>
We simply write a binary search, which Time complexity is O(log n).


```python
def bin_search(arr: list, value: int):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == value:
            return mid
        elif arr[mid] < value:
            left = mid + 1
        else:
            right = mid - 1
    return left
```

**Example:**
```python
nums = [1, 3, 5, 6]
target = 5
print(bin_search(nums, target))     # Output: 2
```

### Linux Shell
1. List processes listening on ports 80 and 443:
```commandline
   lsof -i :80; lsof -i :443 
```

2. List process environment variables by given PID:
```commandline
   cat /proc/WRITE_PID_HERE/environ
```
3. Launch a python program `my_program.py` through CLI in the background:
```commandline
   python my_program.py &
```
Console will print its PID (e.g. [1] 38924). To close it after some period of time:
```commandline
   kill PID
```
PID is process ID of `my_program.py` running in the background (e.g if PID = 38924, command would be `kill 38924`)