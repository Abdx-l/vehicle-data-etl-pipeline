CREATE TABLE IF NOT EXISTS dim_vehicle(vin varchar(17) PRIMARY KEY);
CREATE TABLE IF NOT EXISTS fact_sensor_readings(
 vin varchar(17) REFERENCES dim_vehicle(vin),timestamp timestamptz NOT NULL,
 speed double precision CHECK(speed BETWEEN 0 AND 300),
 battery_temperature double precision CHECK(battery_temperature BETWEEN -50 AND 100),
 PRIMARY KEY(vin,timestamp)
) PARTITION BY RANGE(timestamp);
CREATE TABLE IF NOT EXISTS readings_default PARTITION OF fact_sensor_readings DEFAULT;
CREATE TABLE IF NOT EXISTS quarantine(id bigserial PRIMARY KEY,payload jsonb NOT NULL,reason text NOT NULL);
