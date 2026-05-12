import requests
import time
import re
import urllib.request, urllib.parse, urllib.error
import builtins
import http, ssl
from datetime import datetime
from io import BytesIO
import json
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


HEADERS = {"User-Agent": "PersonalResearch XYZ@gmail.com"}

def get_company_submissions(cik: str) -> dict:
    """Fetch all filing metadata for a company by CIK."""
    cik_padded = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def conv_time(tm):
  if int(tm[:2]) < datetime.now().month:
    tm_up = '2026-'+tm[:2]+'-'+tm[2:]
  else:
    tm_up = '2025-'+tm[:2]+'-'+tm[2:]
  return(tm_up)

def histograme(df):
  plt.figure(figsize=(10, 5))
  sns.histplot(data=df, x='delay', bins=70, kde=True)
  plt.title('Distribution of Filing Delays')
  plt.xlabel('Delay (Days)')
  plt.ylabel('Number of companies')
  plt.tight_layout()
  plt.show()
  
def scatterplot(df):
  plt.figure(figsize=(10, 6))
  sns.scatterplot(data=df, x='filer_category', y = 'delay', hue='filer_category', style= 'filer_category')
  plt.title('Distribution of Filing Delays')
  plt.xlabel('Filer Category)')
  plt.ylabel('Delay in days')
  plt.tight_layout()
  plt.show()


def filer_details(df):
  plt.figure(figsize=(10, 5))
  sns.histplot(data=df, x='delay', bins=80, kde=True)
  plt.title('Distribution of Filing Delays')
  plt.xlabel('Delay (Days)')
  plt.ylabel('Number of companies')
  plt.tight_layout()
  plt.show()

with open('c:\\Users\\Admin\\codes\\company_tickers_exchange.json', 'r', encoding = 'utf-8') as file:
    ps = json.loads(file.read())

fields = ps['fields']
cik_idx = fields.index('cik')

conn = sqlite3.connect('companydb.sqlite', timeout=5)
cur = conn.cursor() 
cur.executescript('''DROP TABLE IF EXISTS Company;


CREATE TABLE Company (
    id     INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT,
    cik    INTEGER UNIQUE,
    sic    INTEGER,
    report_type TEXT,
    report_date TEXT,
    fy_end TEXT,
    filer_category TEXT,
    delay INTEGER
);
''')
for entry_data in ps['data']:
  cik = str(entry_data[cik_idx])
  codata = get_company_submissions(cik)
  name = codata["name"]
  sic = codata["sic"]
  filer_category = codata["category"]
  fend = codata.get("fiscalYearEnd") 
  if fend:
    fy_end = conv_time(fend)
  else:
    fy_end = '0' # Assign '0' if fiscalYearEnd is None
  print(name)
  print(filer_category)
  print(fy_end)
  recent = codata["filings"]["recent"]
  # Recent filings as parallel arrays
  forms = recent["form"] # ["10-K", "10-Q", "8-K", ...]
  dates = recent["filingDate"]
  if "10-K" in forms:
    index_of_10k = forms.index("10-K")
    recent_date_10k = dates[index_of_10k]
    print(forms[index_of_10k])
    report_type = forms[index_of_10k]
    report_date = recent_date_10k
    print(recent_date_10k)
  else:
    print('10-K not found')
    report_type = '0'
    report_date = '0'
  cur.execute('''INSERT OR IGNORE INTO Company (name, cik, sic, report_type, report_date, fy_end, filer_category) VALUES ( ?, ?, ?, ?, ?, ?, ?)''', (name, cik, sic, report_type, report_date, fy_end, filer_category) )
  accessions = recent["accessionNumber"]
  time.sleep(0.1)
data = cur.fetchall()
conn.commit()

conn = sqlite3.connect('companydb.sqlite', timeout=5)
cur = conn.cursor()
cur.execute('''
DELETE FROM Company
WHERE report_date = '0';
''')
cur.execute('''
update Company
set filer_category = replace(filer_category, '<br>','');
''')
cur.execute('''
update Company
set delay = CASE
	when filer_category like 'Large%' then (julianday(report_date)- julianday(fy_end) - 60)
	when filer_category like 'Acceler%' then (julianday(report_date)- julianday(fy_end) - 75)
	when filer_category like 'Non-Acc%' then (julianday(report_date)- julianday(fy_end) - 90)
	when filer_category like 'Emerg%' then (julianday(report_date)- julianday(fy_end) - 90)
end;''')
cur.execute('''
DELETE FROM Company
WHERE filer_category = '';
''')
cur.execute('''
UPDATE Company
set filer_category = CASE
	WHEN filer_category like 'Large%' then 'Large accelerated filer'
	WHEN filer_category like 'Accel%' then 'Accelerated Filer'
	WHEN filer_category like 'Non%' then 'Non-Accelerated Filer'
	WHEN filer_category like 'Emerg%' then 'Emerging Growth'
End;
''')
cur.execute('''
delete from Company where filer_category is NULL''')
cur.execute('''
delete from Company where fy_end = 0''')
cur.execute('''SELECT * FROM Company''')
data = cur.fetchall()
conn.commit()

conn = sqlite3.connect("companydb.sqlite")
df = pd.read_sql_query("""
    SELECT name, sic, filer_category, delay
    FROM Company
    WHERE typeof(delay) = 'integer' AND delay > 0
""", conn)
conn.close()
histograme(df)
scatterplot(df)
print(df.head())

conn = sqlite3.connect("companydb.sqlite")
df = pd.read_sql_query("""
    SELECT count(filer_category) as totCo, filer_category
    FROM Company
    WHERE delay > 0
    group by filer_category
""", conn)
print(df.head()) 
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x='filer_category', y = 'totCo', palette='viridis')
plt.title('Number of Companies per Filer Category (Delay > 0)')
plt.xlabel('Filer Categories')
plt.ylabel('Number of companies')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
conn.close()

conn = sqlite3.connect("companydb.sqlite")

df = pd.read_sql_query("""
    SELECT filer_category, avg(delay) as avgdel
    FROM Company
    WHERE delay > 0
    group by filer_category
""", conn)
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x='filer_category', y = 'avgdel', palette='viridis')
plt.title('Average delay as per the filer category')
plt.xlabel('Filer Categories')
plt.ylabel('Average delay in days')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
conn.close()

conn = sqlite3.connect("companydb.sqlite")
df = pd.read_sql_query(f"""
    SELECT name, delay
    FROM Company
    WHERE delay > 0 and filer_category like 'Lar%'
""", conn)
filer_details(df)
conn.close()

conn = sqlite3.connect("companydb.sqlite")


df = pd.read_sql_query("""
    SELECT name, report_date, delay, filer_category
    FROM Company
    WHERE delay > 0 AND filer_category = 'Emerging Growth'
    ORDER BY report_date ASC
""", conn)

conn.close()

print(df.head())
print(f"Total records: {len(df)}")

# Calculate mean delay
mean_delay = df['delay'].mean()
std_delay  = df['delay'].std()
median_delay = df['delay'].median()

print(f"Mean Delay:   {mean_delay:.2f} days")
print(f"Std Dev:      {std_delay:.2f} days")
print(f"Median Delay: {median_delay:.2f} days")

# Calculate deviation of each record from mean
df['deviation_from_mean'] = df['delay'] - mean_delay
plt.figure(figsize=(12, 6))

# Distribution histogram
sns.histplot(
    data=df,
    x='delay',
    bins=20,
    kde=True,
    color='steelblue',
    alpha=0.6,
    label='Delay Distribution'
)

# Mean line
plt.axvline(
    x=mean_delay,
    color='red',
    linestyle='-',
    linewidth=2,
    label=f'Mean = {mean_delay:.1f} days'
)

# +1 and -1 std deviation lines
plt.axvline(
    x=mean_delay + std_delay,
    color='orange',
    linestyle='--',
    linewidth=1.5,
    label=f'+1 Std = {mean_delay + std_delay:.1f} days'
)
plt.axvline(
    x=mean_delay - std_delay,
    color='orange',
    linestyle='--',
    linewidth=1.5,
    label=f'-1 Std = {mean_delay - std_delay:.1f} days'
)

plt.title('Delay Distribution- Emerging Growth')
plt.xlabel('Delay (Days)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()