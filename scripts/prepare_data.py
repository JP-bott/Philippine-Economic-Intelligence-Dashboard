"""Validate versioned PSA observations and produce a deployable JSON snapshot.

Usage: python scripts/prepare_data.py
The workflow is intentionally offline: no credentials, scraping, or unverifiable updates.
"""
from __future__ import annotations
import csv, json, math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = {
    'grdp_growth': {'label':'Real GRDP growth','unit':'%','preferred':'higher','source':'grdp','periods':['2024','2025'],'caption':'Year-on-year growth at constant 2018 prices'},
    'inflation': {'label':'Annual average inflation','unit':'%','preferred':'neutral','source':'inflation','periods':['2025'],'caption':'All-income households; annual average year-on-year CPI change, 2018=100'},
    'unemployment': {'label':'Unemployment rate','unit':'%','preferred':'lower','source':'labor','periods':['2025-07'],'caption':'July 2025 preliminary labor force survey; not an annual average'},
    'poverty': {'label':'Poverty incidence among families','unit':'%','preferred':'lower','source':'poverty','periods':['2018','2021','2023'],'caption':'Full-year estimates from FIES; 2023 is latest in this snapshot'},
}
SOURCES = {
    'grdp': {'title':'PSA Regional Accounts of the Philippines, 2024 and 2025 releases','url':'https://psa.gov.ph/statistics/grdp','cadence':'Annual','updated':'2026-04-23','notes':'GRDP growth at constant 2018 prices. 2024 regional numbers from 2024 PSA release and official regional infographic; 2025 from 2025 PSA release/chart. Some 2024 values are not transcribed and are null.'},
    'inflation': {'title':'PSA 2025 Annual Average Regional Inflation, All-Income Households','url':'https://rsso08.psa.gov.ph/content/summary-inflation-report-consumer-price-index-all-income-households-2018-base-year-december','cadence':'Annual','updated':'2026-01-14','notes':'Annual average 2025 inflation, not December 2025 point inflation; based on 2018 CPI basket.'},
    'labor': {'title':'PSA July 2025 Labor Force Survey, Regional Employment Indicators','url':'https://psa.gov.ph/sites/default/files/infographics/July%202025%20LAbor%20Force%20Survey.pdf','cadence':'Monthly','updated':'2025-09-01','notes':'Preliminary July 2025 unemployment rates by region. These are month-specific, not annual statistics.'},
    'poverty': {'title':'PSA 2023 Full Year Official Poverty Statistics, Table 3','url':'https://psa.gov.ph/sites/default/files/phdsd/2023%20FY%20Official%20PovStat%20Publication%20Report_r2.pdf','cadence':'FIES survey waves','updated':'2024-08-15','notes':'Poverty incidence among families, not persons. 2018/2021 revised regional back-estimates include NIR; use the 2023 publication series.'},
    'geography': {'title':'PSA Philippine Standard Geographic Code, regions (18)','url':'https://psa.gov.ph/classification/psgc/regions','cadence':'Administrative updates','updated':'2025-07-31','notes':'NIR introduced in 2024; boundary geometry is from faeldon/philippines-json-maps low resolution. It is for regional overview and not a legal boundary reference.'},
}

def build():
    with (ROOT / 'data' / 'regions.csv').open(encoding='utf-8-sig', newline='') as f: regions=list(csv.DictReader(f))
    with (ROOT / 'data' / 'observations.csv').open(encoding='utf-8-sig', newline='') as f: obs=list(csv.DictReader(f))
    assert len(regions)==18, 'Expected 18 PSA regions'
    assert len(set(row['code'] for row in regions))==18
    assert len(set(row['psgc'] for row in regions))==18
    region_codes=set(r['code'] for r in regions)
    valid_keys=[]
    for row in obs:
        assert row['region'] in region_codes | {'PH'}, row
        assert row['metric'] in METRICS, row
        assert row['period'] in METRICS[row['metric']]['periods'], row
        assert row['source']==METRICS[row['metric']]['source'], row
        x=float(row['value']); assert math.isfinite(x)
        if row['metric']=='poverty':assert 0 <= x <= 100
        if row['metric']=='unemployment':assert 0 <= x <= 100
        valid_keys.append((row['region'],row['metric'],row['period']))
    duplicates=[k for k,v in Counter(valid_keys).items() if v>1]
    assert not duplicates, duplicates
    actual={f"{row['region']}|{row['metric']}|{row['period']}":float(row['value']) for row in obs}
    target={'regions':[{**r,'psgc':int(r['psgc'])} for r in regions],'metrics':METRICS,'sources':SOURCES,'values':actual,'revision':'2026-10-28','publisher':'Philippine Statistics Authority (PSA); dashboard compiled independently by John Paul Torres'}
    out=ROOT / 'public' / 'data' / 'snapshot.json'
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(target,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Validated',len(obs),'source observations,',len(regions),'regions ->',out.relative_to(ROOT))
    return target

if __name__=='__main__':build()
