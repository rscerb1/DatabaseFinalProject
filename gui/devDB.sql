-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema dbproj
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dbproj
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dbproj` DEFAULT CHARACTER SET latin1 ;
USE `dbproj` ;

-- -----------------------------------------------------
-- Table `dbproj`.`REGION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`REGION` (
  `Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`FACILITY`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`FACILITY` (
  `Address` VARCHAR(200) NULL DEFAULT NULL,
  `R_Name` VARCHAR(45) NULL DEFAULT NULL,
  `Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Name`),
  INDEX `R_Name_idx` (`R_Name` ASC) VISIBLE,
  CONSTRAINT `R_Name`
    FOREIGN KEY (`R_Name`)
    REFERENCES `dbproj`.`REGION` (`Name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`SPECIES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`SPECIES` (
  `is_recreational` TINYINT NULL DEFAULT NULL,
  `is_aquatic` TINYINT NULL DEFAULT NULL,
  `ITIS_NUMBER` INT NOT NULL,
  `taxonomic_group` VARCHAR(45) NULL DEFAULT NULL,
  `Name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ITIS_NUMBER`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`DISTRIBUTION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`DISTRIBUTION` (
  `Date` DATE NOT NULL,
  `Count` INT NULL DEFAULT NULL,
  `Fname` VARCHAR(45) NOT NULL,
  `Distribution_ID` INT NOT NULL AUTO_INCREMENT,
  `S_ITIS` INT NOT NULL,
  PRIMARY KEY (`Distribution_ID`),
  INDEX `S_ITIS_idx` (`S_ITIS` ASC) VISIBLE,
  INDEX `FNAME_idx` (`Fname` ASC) VISIBLE,
  CONSTRAINT `FNAME`
    FOREIGN KEY (`Fname`)
    REFERENCES `dbproj`.`FACILITY` (`Name`),
  CONSTRAINT `S_ITIS`
    FOREIGN KEY (`S_ITIS`)
    REFERENCES `dbproj`.`SPECIES` (`ITIS_NUMBER`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`HATCHED_DISTRIBUTION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`HATCHED_DISTRIBUTION` (
  `Average_length` DECIMAL(8,6) NULL DEFAULT NULL,
  `Average_weight` DECIMAL(8,6) NULL DEFAULT NULL,
  `HID` INT NOT NULL AUTO_INCREMENT,
  `life_stage` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`HID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`RELEASED`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`RELEASED` (
  `Distribution_ID` INT NOT NULL,
  `Latitude` DECIMAL(8,6) NULL DEFAULT NULL,
  `Longitude` DECIMAL(9,6) NULL DEFAULT NULL,
  `HID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`Distribution_ID`),
  INDEX `HID_idx` (`HID` ASC) VISIBLE,
  CONSTRAINT `DISTRIBUTION_ID`
    FOREIGN KEY (`Distribution_ID`)
    REFERENCES `dbproj`.`DISTRIBUTION` (`Distribution_ID`),
  CONSTRAINT `HID`
    FOREIGN KEY (`HID`)
    REFERENCES `dbproj`.`HATCHED_DISTRIBUTION` (`HID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`TAGGED_DISTRIBUTION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`TAGGED_DISTRIBUTION` (
  `tag_type` VARCHAR(45) NOT NULL,
  `percent_tagged` INT NOT NULL,
  `HID` INT NOT NULL,
  PRIMARY KEY (`HID`),
  INDEX `fk_TAGGED_DISTRIBUTION_HATCHED_DISTRIBUTION1_idx` (`HID` ASC) VISIBLE,
  CONSTRAINT `fk_TAGGED_DISTRIBUTION_HATCHED_DISTRIBUTION1`
    FOREIGN KEY (`HID`)
    REFERENCES `dbproj`.`HATCHED_DISTRIBUTION` (`HID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `dbproj`.`TRANSFER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dbproj`.`TRANSFER` (
  `Distribution_ID` INT NOT NULL,
  `F_Name` VARCHAR(45) NULL DEFAULT NULL,
  `HID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`Distribution_ID`),
  INDEX `fk_TRANSFER_DISTRIBUTION1_idx` (`Distribution_ID` ASC) VISIBLE,
  INDEX `fk_TRANSFER_HATCHED_DISTRIBUTION1_idx` (`HID` ASC) VISIBLE,
  INDEX `fk_TRANSFER_FACILITY1_idx` (`F_Name` ASC) VISIBLE,
  CONSTRAINT `fk_TRANSFER_DISTRIBUTION1`
    FOREIGN KEY (`Distribution_ID`)
    REFERENCES `dbproj`.`DISTRIBUTION` (`Distribution_ID`),
  CONSTRAINT `fk_TRANSFER_HATCHED_DISTRIBUTION1`
    FOREIGN KEY (`HID`)
    REFERENCES `dbproj`.`HATCHED_DISTRIBUTION` (`HID`),
  CONSTRAINT `fk_TRANSFER_FACILITY1`
    FOREIGN KEY (`F_Name`)
    REFERENCES `dbproj`.`FACILITY` (`Name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;