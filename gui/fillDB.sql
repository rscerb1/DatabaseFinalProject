--
-- Sample data to input into the project database for development and testing
--

-- DB name
USE dbproj;

-- Regions
INSERT INTO REGION (NAME) 
VALUES
    ('North Eastern'),
    ('Atlantic'),
    ('Western'),
    ('Alaska');

-- Facilities (at least one per region)
INSERT INTO FACILITY (Address, R_Name, Name)
VALUES
    ('0018 Alivia Extensions, Lake Emmitt, PA, 43964', 'North Eastern', 'Lake Emmitt'),
    ('334 Liberty Lane, Woodly, ME, 33442', 'North Eastern', 'Liberty'),
    ('2535 Washington Drive, Heinicke, MD, 59382', 'Atlantic', 'Heinicke'),
    ('642 Palm Street, San Diego, CA, 39583', 'Western', 'Yellow Beach'),
    ('2988 Snowy Road, Deep Creek, AK, 48482', 'Alaska', 'Eagle Peak'),
    ('593, Bear River, AK, 33445', 'Alaska', 'Bear River');

-- Species ( fish)
INSERT INTO SPECIES (is_recreational, is_aquatic, ITIS_NUMBER, taxonomic_group, Name) 
VALUES
    (0,1,161980,'Fish','Chinook Salmon'),
    (1,1,167680,'Fish','Striped Bass'),
    (1,1,167678,'Fish','White Perch'),
    (0,0,773512,'Amphibian','Wyoming Toad');


INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('2020-09-13',17245,'Heinicke',167680, 'Juvenile');
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('2021-05-01',29563,'Yellow Beach',161980, 'Juvenile');
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('2021-05-01',2534,'Yellow Beach',773512, 'Juvenile');
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('2021-05-01',28433,'Eagle Peak',161980, 'Egg');
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('2021-05-11',47664,'Eagle Peak',161980, 'Adult');
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS) VALUES ('2021-10-23',53456,'Bear River',161980, 'Adult');

--
-- Distrobutions
--
-- Released, Hatched, Tagged Distributions
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS, LifeStage) VALUES ('2020-01-02',12345,'Lake Emmitt',167680, 'Juvenile');
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude) VALUES (LAST_INSERT_ID(), 34.3425, 65.2352);
INSERT INTO HATCHED_DISTRIBUTION (Average_length,Average_weight) VALUES (3.34, .24);
UPDATE RELEASED SET HID = LAST_INSERT_ID();
INSERT INTO TAGGED_DISTRIBUTION (tag_type, percent_tagged, HID) VALUES ('anchor', 5, LAST_INSERT_ID());

INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS, LifeStage) VALUES ('2020-02-01',23462,'Lake Emmitt',167678, 'Juvenile');
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude) VALUES (LAST_INSERT_ID(), 35.5265, 62.5432);
INSERT INTO HATCHED_DISTRIBUTION (Average_length,Average_weight,HID) VALUES (4.74, .423, LAST_INSERT_ID());
INSERT INTO TAGGED_DISTRIBUTION (tag_type, percent_tagged, HID) VALUES ('PIT', 3, LAST_INSERT_ID());

-- Released, Hatched Distributions
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS, LifeStage) VALUES ('2020-03-10',22334,'Liberty',167680, 'Adult');
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude) VALUES (LAST_INSERT_ID(), 73.3753, 63.4986);
INSERT INTO HATCHED_DISTRIBUTION (Average_length,Average_weight,HID) VALUES (10.43, 3.245, LAST_INSERT_ID());

INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS, LifeStage) VALUES ('2020-08-21',13456,'Heinicke',167678, 'Adult');
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude) VALUES (LAST_INSERT_ID(), 44.0752, 25.6502);
INSERT INTO HATCHED_DISTRIBUTION (Average_length,Average_weight,HID) VALUES (5.13, 1.005, LAST_INSERT_ID());

-- Released Distributions
INSERT INTO DISTRIBUTION (Date, Count, Fname, S_ITIS, LifeStage) VALUES ('2020-09-13',17245,'Heinicke',167680, 'Egg');
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude) VALUES (LAST_INSERT_ID(), 43.5032, 26.0131);

-- Transfer Distribution

-- Released
INSERT INTO RELEASED (Distribution_ID, Latitude, Longitude, HID) VALUES ()
INSERT INTO HATCHED_DISTRIBUTION (Average_length,life_stage,Average_weight,HID) VALUES ()
