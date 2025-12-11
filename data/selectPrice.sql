SELECT G.carGradeNbr AS carGradeNbr
	 , G.carGradeNm  AS carGradeNm
	 , P.gradeSalePrice AS gradeSalePrice # 현재가
	 , P.grade1yearLaterPrice AS grade1yearLaterPrice # 1년후
	 , P.grade2yearLaterPrice AS grade2yearLaterPrice # 2년후
	 , P.grade3yearLaterPrice AS grade3yearLaterPrice # 3년후
	 , p.trvlDstnc 
FROM CAR C
JOIN GRADE G
ON C.carClassNbr = G.carClassNbr 
JOIN PRICE P
ON G.carGradeNbr = P.carGradeNbr 
WHERE C.carClassNbr = %s
