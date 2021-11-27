--
-- Sample data to input into the project database for development and testing
--

-- DB name
USE dbproj;

-- Regions
INSERT INTO REGION (NAME) VALUES ('North Eastern');
INSERT INTO REGION (NAME) VALUES ('Atlantic');
INSERT INTO REGION (NAME) VALUES ('Western');
INSERT INTO REGION (NAME) VALUES ('Alaska');

-- Facilities (at least one per region)
INSERT INTO FACILITY (Adress, R_Name, Name) VALUES ('0018 Alivia Extensions, Lake Emmitt, PA, 43964', 'North Eastern', 'Lake Emmitt');

-- Species ( fish)
INSERT INTO SPECIES (is_recreational, is_aquatic, ITIS_NUMBER, taxonomic_group, Name) VALUES (0,1,161980,'Fish','Chinook Salmon');
INSERT INTO SPECIES (is_recreational, is_aquatic, ITIS_NUMBER, taxonomic_group, Name) VALUES (1,1,167680,'Fish','Striped Bass');
INSERT INTO SPECIES (is_recreational, is_aquatic, ITIS_NUMBER, taxonomic_group, Name) VALUES (1,1,167678,'Fish','White Perch');
INSERT INTO SPECIES (is_recreational, is_aquatic, ITIS_NUMBER, taxonomic_group, Name) VALUES (0,0,773512,'Amphibian','Wyoming Toad');

-- Distrobutions 
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2020-01-02',12345,'North Eastern',167680);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2020-02-01',23462,'North Eastern',167678);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2020-03-10',22334,'North Eastern',167680);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2020-08-21',13456,'Atlantic',167678);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2020-09-13',17245,'Atlantic',167680);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2021-05-01',29563,'Western',161980);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2021-05-01',2534,'Western',773512);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2021-05-01',28433,'Western',161980);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2021-05-11',47664,'Alaska',161980);
INSERT INTO DISTRIBUTION (Date, Count, Fname, ITIS) VALUES ('2021-10-23',53456,'Alaska',161980);

-- Hatched Distribution
INSERT INTO HATCHED_DISTRIBUTION (Average_length,life_stage,Average_weight,HID) VALUES ()

-- Released
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude, HID) VALUES ()