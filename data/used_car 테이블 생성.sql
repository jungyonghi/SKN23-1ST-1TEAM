-- usedcar.car definition

CREATE TABLE `car` (
  `brandNbr` int NOT NULL COMMENT '브랜드번호',
  `brandNm` varchar(100) NOT NULL COMMENT '브랜드명',
  `repCarClassNbr` int NOT NULL COMMENT '차종번호',
  `repCarClassNm` varchar(100) NOT NULL COMMENT '차종명',
  `carClassNbr` int NOT NULL COMMENT '세부차종번호',
  `carClassNm` varchar(100) NOT NULL COMMENT '세부차종명',
  `yearType` varchar(100) NOT NULL COMMENT '연식',
  `brandImage` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '브랜드이미지',
  PRIMARY KEY (`carClassNbr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='차종별 정보';


-- usedcar.grade definition

CREATE TABLE `grade` (
  `carGradeNbr` int NOT NULL COMMENT '등급번호',
  `carGradeNm` varchar(100) NOT NULL COMMENT '등급명',
  `carClassNbr` int NOT NULL COMMENT '차종상세명',
  `rn` varchar(100) NOT NULL COMMENT '등급순서',
  `fuel` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '연료',
  `fuelNm` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '연료명',
  `gradeFuelRate` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '등급연비',
  `fuelRateGrade` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '연비등급',
  `extShape` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '외형',
  `extShapeNm` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '외형명',
  `carSize` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '차급',
  `carClassRepImage` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '차량등급이미지',
  PRIMARY KEY (`carGradeNbr`),
  KEY `grade_car_FK` (`carClassNbr`),
  CONSTRAINT `grade_car_FK` FOREIGN KEY (`carClassNbr`) REFERENCES `car` (`carClassNbr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- usedcar.price definition

CREATE TABLE `price` (
  `priceNbr` int NOT NULL AUTO_INCREMENT COMMENT '가격번호',
  `carGradeNbr` int NOT NULL COMMENT '등급번호',
  `gradeSalePrice` int DEFAULT NULL COMMENT '현재신차가격',
  `gradeUsedCarPrice` int DEFAULT NULL COMMENT '현재중고가격',
  `grade1yearLaterPrice` int DEFAULT NULL COMMENT '1년후가격',
  `grade2yearLaterPrice` int DEFAULT NULL COMMENT '2년후가격',
  `grade3yearLaterPrice` int DEFAULT NULL COMMENT '3년후가격',
  `trvlDstnc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '거리',
  `carClassNbr` int DEFAULT NULL,
  PRIMARY KEY (`priceNbr`),
  KEY `price_grade_FK` (`carGradeNbr`),
  CONSTRAINT `price_grade_FK` FOREIGN KEY (`carGradeNbr`) REFERENCES `grade` (`carGradeNbr`)
) ENGINE=InnoDB AUTO_INCREMENT=81897 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- usedcar.age_rank definition

CREATE TABLE `age_rank` (
  `ageNbr` int NOT NULL AUTO_INCREMENT COMMENT '나이번호',
  `carClassNbr` int NOT NULL COMMENT '차량상세번호',
  `rn` int NOT NULL COMMENT '순서',
  `age` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '나이',
  `cnt` int DEFAULT NULL COMMENT '수',
  `percent` float DEFAULT NULL COMMENT '퍼샌트',
  PRIMARY KEY (`ageNbr`),
  KEY `age_rank_car_FK` (`carClassNbr`),
  CONSTRAINT `age_rank_car_FK` FOREIGN KEY (`carClassNbr`) REFERENCES `car` (`carClassNbr`)
) ENGINE=InnoDB AUTO_INCREMENT=12842 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- usedcar.dstnc_rank definition

CREATE TABLE `dstnc_rank` (
  `dstncNbr` int NOT NULL AUTO_INCREMENT COMMENT '나이번호',
  `carClassNbr` int NOT NULL COMMENT '차량상세번호',
  `trvlDstnc` int NOT NULL COMMENT '주행거리',
  `avgPrice` int DEFAULT NULL COMMENT '평균가격',
  `cnt` int DEFAULT NULL COMMENT '수',
  `percent` int DEFAULT NULL COMMENT '퍼샌트',
  PRIMARY KEY (`dstncNbr`),
  KEY `dstnc_rank_car_FK` (`carClassNbr`),
  CONSTRAINT `dstnc_rank_car_FK` FOREIGN KEY (`carClassNbr`) REFERENCES `car` (`carClassNbr`)
) ENGINE=InnoDB AUTO_INCREMENT=33379 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- usedcar.gender_rank definition

CREATE TABLE `gender_rank` (
  `genderNbr` int NOT NULL AUTO_INCREMENT COMMENT '성별번호',
  `carClassNbr` int NOT NULL COMMENT '차량상세번호',
  `rn` int NOT NULL COMMENT '순서',
  `gender` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '성별',
  `cnt` int DEFAULT NULL COMMENT '수',
  `percent` float DEFAULT NULL COMMENT '퍼샌트',
  PRIMARY KEY (`genderNbr`),
  KEY `gender_rank_car_FK` (`carClassNbr`),
  CONSTRAINT `gender_rank_car_FK` FOREIGN KEY (`carClassNbr`) REFERENCES `car` (`carClassNbr`)
) ENGINE=InnoDB AUTO_INCREMENT=7303 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- usedcar.region_rank definition

CREATE TABLE `region_rank` (
  `regionNbr` int NOT NULL AUTO_INCREMENT COMMENT '지역번호',
  `carClassNbr` int NOT NULL COMMENT '차량상세번호',
  `rn` int NOT NULL COMMENT '순서',
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '주소',
  `cnt` int DEFAULT NULL COMMENT '수',
  `percent` float DEFAULT NULL COMMENT '퍼샌트',
  PRIMARY KEY (`regionNbr`),
  KEY `region_rank_car_FK` (`carClassNbr`),
  CONSTRAINT `region_rank_car_FK` FOREIGN KEY (`carClassNbr`) REFERENCES `car` (`carClassNbr`)
) ENGINE=InnoDB AUTO_INCREMENT=12398 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

