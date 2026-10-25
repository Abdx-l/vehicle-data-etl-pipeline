import pandas as pd
from pipeline import validate
def test_quarantine_and_duplicates():
 f=pd.DataFrame([["1HGCM82633A004352","2026-01-01",20,30],["1HGCM82633A004352","2026-01-01",25,30],["bad","x",-1,200]],columns=["vin","timestamp","speed","battery_temperature"])
 good,bad=validate(f);assert len(good)==1 and good.iloc[0].speed==25;assert len(bad)==1;assert "VIN" in bad.iloc[0].reason
