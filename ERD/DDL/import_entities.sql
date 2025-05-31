CREATE TABLE Region (
  region_id INT UNSIGNED PRIMARY KEY,
  region_name VARCHAR(50),
  region_code VARCHAR(10),
  population INT UNSIGNED,
  area_km2 DECIMAL(6,2),
  green_ratio DECIMAL(5,2),
  road_extension INT UNSIGNED,
  road_coverage_ratio DECIMAL(5,2),
  num_administrative_dongs SMALLINT UNSIGNED,
  num_hospitals SMALLINT UNSIGNED,
  num_bus_stops INT UNSIGNED
);

CREATE TABLE RoadMaintenanceYearBudget (
  region_id INT UNSIGNED,
  year YEAR,
  total_budget INT UNSIGNED,
  PRIMARY KEY (region_id, year),
  FOREIGN KEY (region_id) REFERENCES Region(region_id)
);

CREATE TABLE RoadMaintenanceMonthBudget (
  region_id INT UNSIGNED,
  year YEAR,
  month TINYINT,
  monthly_budget INT,
  PRIMARY KEY (region_id, year, month),
  FOREIGN KEY (region_id, year) REFERENCES RoadMaintenanceYearBudget(region_id, year)
);


CREATE TABLE Road (
  road_id INT UNSIGNED PRIMARY KEY,
  road_name VARCHAR(100),
  road_type VARCHAR(20),
  region_id INT UNSIGNED,
  pavement_type VARCHAR(20),
  road_axis_code SMALLINT UNSIGNED,
  FOREIGN KEY (region_id) REFERENCES Region(region_id)
);


CREATE TABLE RoadTraffic (
  road_traffic_id INT UNSIGNED PRIMARY KEY,
  road_id INT UNSIGNED,
  site_code VARCHAR(10),
  direction VARCHAR(10),
  route_desc VARCHAR(100),
  date DATE,
  hour_00 SMALLINT UNSIGNED,
  hour_01 SMALLINT UNSIGNED,
  hour_02 SMALLINT UNSIGNED,
  hour_03 SMALLINT UNSIGNED,
  hour_04 SMALLINT UNSIGNED,
  hour_05 SMALLINT UNSIGNED,
  hour_06 SMALLINT UNSIGNED,
  hour_07 SMALLINT UNSIGNED,
  hour_08 SMALLINT UNSIGNED,
  hour_09 SMALLINT UNSIGNED,
  hour_10 SMALLINT UNSIGNED,
  hour_11 SMALLINT UNSIGNED,
  hour_12 SMALLINT UNSIGNED,
  hour_13 SMALLINT UNSIGNED,
  hour_14 SMALLINT UNSIGNED,
  hour_15 SMALLINT UNSIGNED,
  hour_16 SMALLINT UNSIGNED,
  hour_17 SMALLINT UNSIGNED,
  hour_18 SMALLINT UNSIGNED,
  hour_19 SMALLINT UNSIGNED,
  hour_20 SMALLINT UNSIGNED,
  hour_21 SMALLINT UNSIGNED,
  hour_22 SMALLINT UNSIGNED,
  hour_23 SMALLINT UNSIGNED,
  FOREIGN KEY (road_id) REFERENCES Road(road_id)
);

CREATE TABLE PotholeLocation (
  pothole_location_id INT UNSIGNED PRIMARY KEY,
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6),
  date DATE,
  road_id INT UNSIGNED,
  pothole_area DECIMAL(8,2),
  is_fixed BOOLEAN,
  fix_date DATE,
  FOREIGN KEY (road_id) REFERENCES Road(road_id)
);

CREATE TABLE SensorVehicle (
  vehicle_id VARCHAR(50) PRIMARY KEY,
  model_name VARCHAR(50),
  region_id INT UNSIGNED,
  in_service BOOLEAN,
  registered_at DATE,
  FOREIGN KEY (region_id) REFERENCES Region(region_id)
);

CREATE TABLE DetectionEvent (
  event_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  vehicle_id VARCHAR(20),
  pothole_location_id INT UNSIGNED,
  detected_at DATETIME,
  impact_score DECIMAL(5,2),
  vehicle_speed DECIMAL(5,2),
  confidence DECIMAL(5,2),
  UNIQUE (vehicle_id, pothole_location_id, detected_at),
  FOREIGN KEY (vehicle_id) REFERENCES SensorVehicle(vehicle_id),
  FOREIGN KEY (pothole_location_id) REFERENCES PotholeLocation(pothole_location_id)
);


CREATE TABLE Weather (
    weather_id INT UNSIGNED PRIMARY KEY,
    date DATE,
    station_region VARCHAR(20),
    avg_temperature DECIMAL(5,2),
    min_temperature DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    max_precip_10min DECIMAL(5,1),
    max_precip_1hr DECIMAL(5,1),
    precip_duration_hr DECIMAL(4,1),
    precipitation DECIMAL(6,1),
    humidity DECIMAL(5,2),
    vapor_pressure DECIMAL(5,2),
    snow_depth DECIMAL(5,1),
    cloud_amount_avg DECIMAL(4,1),
    subsoil_temp_10cm DECIMAL(5,2),
    avg_blow DECIMAL(5,2)
);


