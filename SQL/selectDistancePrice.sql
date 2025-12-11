SELECT DR.cnt AS CNT # 거래건수
	 , DR.avgPrice  AS avgPrice # 평균가격
	 , DR.trvlDstnc AS trvlDstnc # 주행거리
FROM CAR C
JOIN DSTNC_RANK DR 
ON C.carClassNbr = DR.carClassNbr 
WHERE C.carClassNbr = %s
and DR.trvlDstnc is not null
ORDER BY DR.trvlDstnc 