SELECT 
	address
	 , cnt
	 , percent
FROM CAR C
JOIN REGION_RANK RR 
ON C.carClassNbr = RR.carClassNbr 
WHERE C.carClassNbr = %s