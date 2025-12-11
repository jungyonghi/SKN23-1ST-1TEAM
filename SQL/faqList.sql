SELECT F.question as question
     , F.answer as answer
     , A.carClassNm as carClassNm
     , A.carClassNbr as carClassNbr
     , A.gradeUsedCarPrice
     , A.yearType as yearType
     , A.brandImage as brandImage
     , A.carClassRepImage as carClassRepImage
     , CONCAT(FORMAT(A.MINPRICE/10000,0),' ~ ',FORMAT(A.MAXPRICE/10000,0),' 만원') AS carPrice
FROM FAQ F
LEFT JOIN
(SELECT CONCAT(C.yearType, " ", C.carClassNm) AS carClassNm 
     , C.carClassNbr 
     , MIN(P.gradeUsedCarPrice) AS gradeUsedCarPrice  -- 집계 함수 사용
     , C.yearType
     , C.brandImage
     , MAX(G.carClassRepImage) AS carClassRepImage  -- 집계 함수 사용
     , MIN(P.gradeUsedCarPrice) AS minPrice
     , MAX(P.gradeUsedCarPrice) AS maxPrice
FROM CAR C
LEFT JOIN GRADE G ON C.carClassNbr = G.carClassNbr
LEFT JOIN PRICE P ON G.carGradeNbr = P.carGradeNbr
WHERE P.trvlDstnc = 50000
GROUP BY C.carClassNbr, C.yearType, C.carClassNm, C.brandImage) A
ON F.CARCLASSNBR = A.CARCLASSNBR
WHERE F.CARCLASSNBR IS NOT NULL