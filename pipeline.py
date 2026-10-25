import argparse,json,os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine,text
def validate(frame):
 required={"vin","timestamp","speed","battery_temperature"}
 if not required.issubset(frame.columns):raise ValueError("missing columns: "+str(required-set(frame.columns)))
 f=frame.copy();f["timestamp"]=pd.to_datetime(f.timestamp,utc=True,errors="coerce")
 for c in ("speed","battery_temperature"):f[c]=pd.to_numeric(f[c],errors="coerce")
 reasons=pd.Series("",index=f.index)
 for condition,reason in [(f.vin.isna()|~f.vin.astype(str).str.fullmatch(r"[A-HJ-NPR-Z0-9]{17}"),"VIN"),(f.timestamp.isna(),"TIMESTAMP"),(~f.speed.between(0,300),"SPEED"),(~f.battery_temperature.between(-50,100),"TEMPERATURE")]:
  reasons= reasons.mask(condition,reasons+"|"+reason)
 bad=f[reasons!=""].copy();bad["reason"]=reasons[reasons!=""].str.lstrip("|")
 good=f[reasons==""].drop_duplicates(["vin","timestamp"],keep="last")
 return good,bad
def load(engine,good,bad):
 with engine.begin() as conn:
  for row in good.to_dict("records"):
   conn.execute(text("INSERT INTO dim_vehicle(vin) VALUES(:vin) ON CONFLICT DO NOTHING"),row)
   conn.execute(text("""INSERT INTO fact_sensor_readings(vin,timestamp,speed,battery_temperature)
    VALUES(:vin,:timestamp,:speed,:battery_temperature)
    ON CONFLICT(vin,timestamp) DO UPDATE SET speed=EXCLUDED.speed,battery_temperature=EXCLUDED.battery_temperature"""),row)
  for row in bad.to_dict("records"):
   conn.execute(text("INSERT INTO quarantine(payload,reason) VALUES(CAST(:payload AS jsonb),:reason)"),{"payload":json.dumps(row,default=str),"reason":row["reason"]})
def process(source,archive,database=None):
 good,bad=validate(pd.read_csv(source));good.to_parquet(archive,index=False)
 bad.to_json(str(Path(archive).with_suffix(".quarantine.json")),orient="records",date_format="iso")
 if database:load(create_engine(database),good,bad)
 return {"accepted":len(good),"quarantined":len(bad)}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("source");p.add_argument("--archive",default="archive.parquet");a=p.parse_args();print(process(a.source,a.archive,os.getenv("DATABASE_URL")))
