# Disclosure_Calculator

# SEC 10-K Filing Delay Analysis by Filer Category (CY 2025) - Learning project

> **10% of all SEC filers delayed their 10-K submissions in CY 2025 — but the nature of those delays tells very different stories depending on who's filing.**

---

## Key Findings

### Delay Rates by Filer Category

| Filer Category | Total Filers | Delayed | Delay Rate | On-Time Rate |
|---|---|---|---|---|
| Large Accelerated | 2,000 | 121 | **6.05%** | 93.95% |
| Accelerated | 685 | 35 | **5.11%** | 94.89% |
| Non-Accelerated | 1,989 | 283 | **14.23%** | 85.77% |
| Emerging Growth | 558 | 84 | **15.05%** | 84.95% |
| **Total** | **5,232** | **523** | **10.00%** | **90.00%** |

### Delay Statistics (Among Delayed Filers Only)

| Filer Category | Mean Delay | Median Delay | Std Dev | Distribution Shape |
|---|---|---|---|---|
| Large Accelerated | 5.40 days | 1.00 day | 25.97 | Right-skewed (outlier-driven) |
| Accelerated | 16.97 days | 9.00 days | 30.11 | Right-skewed (outlier-driven) |
| Non-Accelerated | 14.29 days | 15.00 days | 14.50 | Near-symmetric (structural) |
| Emerging Growth | 13.46 days | 15.00 days | 18.05 | Near-symmetric (structural) |

**Weighted average delay across all delayed filers: ~12.3 days**

---

## Inferences

### 1. Smaller filers delay more — and more frequently
Non-Accelerated and Emerging Growth companies delayed at roughly **2.5× the rate** of larger filers (14–15% vs. 5–6%). This likely reflects fewer dedicated compliance resources, smaller legal/finance teams, and less mature reporting infrastructure.

### 2. Large filers delay rarely — but outliers dominate when they do
For Large Accelerated Filers, the **median delay is just 1 day** while the mean is 5.40 days, with a standard deviation of 25.97. This extreme divergence signals that the *typical* large filer is barely late, but a small number of severe outliers (potentially involving restatements, auditor changes, or material events) pull the mean sharply upward.

### 3. Smaller filers face structural, not incidental, delays
Non-Accelerated Filers show a **mean of 14.29 days and median of 15.00 days** — nearly identical. This near-symmetric distribution with a contained standard deviation of 14.50 suggests delays in this category are evenly distributed and driven by systemic capacity constraints, not isolated incidents.

### 4. A hidden compliance gap exists in mid-size filers
Accelerated Filers have a low delay *rate* (5.11%), but their mean delay among those who do slip is the **highest of all categories at 16.97 days** — exceeding even Non-Accelerated filers. This may point to a specific cohort of mid-size companies with complex operations but without the full compliance infrastructure of large filers.

### 5. The headline 90% compliance rate masks structural inequality
The overall 90% on-time rate is heavily weighted by the large number of Large Accelerated Filers (2,000) who comply at 94%. Assessed purely on the Non-Accelerated and Emerging Growth universe, the compliance picture is materially worse — fewer than 85% file on time.

---

## Methodology

**Data Source:** SEC EDGAR / USACC public filing database, CY 2025
**Sample:** 5,232 10-K filings across four filer categories (~10% of total filings)
**Delay Definition:** Calendar days between SEC filing deadline and actual filing date
**Tools:** Python (data extraction & visualisation) · SQLite (delay analysis & aggregation)

> ⚠️ **Caveat:** This analysis does not account for intentional delays formally notified to the SEC via **10-K NT (Notification of Late Filing)**. Companies that filed a 10-K NT are still counted as delayed in this dataset. Findings therefore reflect raw filing timelines rather than strictly penalisable non-compliance — actual non-compliance rates may be lower than reported here.

---

## Filer Category Reference (SEC Definitions)

| Category | Criteria |
|---|---|
| Large Accelerated Filer | Public float ≥ $700M |
| Accelerated Filer | Public float $75M–$700M |
| Non-Accelerated Filer | Public float < $75M (and not SRC/EGC) |
| Emerging Growth Company | IPO after Dec 8, 2011; revenue < $1.235B |

---

## Why This Matters

Timely disclosure is a cornerstone of market transparency. Delays — even short ones — can disadvantage investors, signal operational stress, or reflect governance gaps. Understanding *which* companies delay, *by how much*, and *in what pattern* provides a data-driven foundation for regulatory prioritisation and compliance benchmarking.



---

## License

MIT License — see `LICENSE` for details.
