# mkh-plagiary-checker

Plugiary checker for MKH contest


### How to run

Full check: 

`sh check_all.sh`

Concrete check:

`sh check.sh 12 11` // new_file older_file 


### Report format:

```
-----------------------------------------
Finding haiku started 2019-04-01T15:07:17.170984
Haiku File=11.csv (NEW)
Origin File=10.csv (OLD)
-----------------------------------------
-----------------------------------------
!!! PLAGIARY DETECTED !!! haiku#=31 old#=822
OLD: ['04.04.2018 12:47:06', 'vasya@yandex.ru', 'Vasya Pupkin', 
NEW: ['11.02.2019 13:58:07', 'pupkin@yandex.ru',
-----------------------------------------
...
-----------------------------------------
Haiku processed=1735
Origin processed=2823
Total check count=4896170
Found 7
Execution time 31.092 (ms)

-----------------------------------------
Finding haiku started 2019-04-01T15:08:35.764208
Haiku File=11.csv (NEW)
Origin File=8.csv (OLD)
-----------------------------------------
...

```

### Format csv

FIELD_NAMES = ['в три строки', 'в одну строку', 'место', 'жанр', 'имя', 'почта', 'город', 'страна']
