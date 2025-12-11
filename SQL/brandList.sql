SELECT brandNbr, brandNm
  FROM CAR
 GROUP BY brandNbr, brandNm
 ORDER BY FIELD(brandNbr, 5177, 212, 108, 3981, 2121, 904, 1193) DESC, brandNbr ASC
 
