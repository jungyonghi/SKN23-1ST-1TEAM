SELECT GENDER
	 , CNT, percent
FROM CAR C
JOIN GENDER_RANK G
ON C.carClassNbr = G.carClassNbr 
WHERE C.carClassNbr = %s