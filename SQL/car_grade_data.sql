SELECT carGradeNbr, carClassNm, CONCAT(FORMAT(gradeUsedCarPrice/10000,0),' 만원') as gradeUsedCarPrice, 
       yearType, carGradeNm, CONCAT(FORMAT(MINPRICE/10000,0),' ~ ',FORMAT(MAXPRICE/10000,0),' 만원') AS carPrice, 
       brandImage, carClassRepImage
FROM
(SELECT G.carGradeNbr, 
        CONCAT(C.yearType, " ", C.carClassNm) AS carClassNm, 
        P.gradeUsedCarPrice, 
        C.yearType, 
        G.carGradeNm, 
        C.brandImage, 
        G.carClassRepImage,
        (SELECT MIN(P.gradeUsedCarPrice)
         FROM CAR C
         LEFT JOIN GRADE G ON C.carClassNbr = G.carClassNbr
         LEFT JOIN PRICE P ON G.carGradeNbr = P.carGradeNbr
         WHERE P.trvlDstnc = 50000 AND C.carClassNbr = %s
         GROUP BY C.carClassNbr) AS minPrice,
        (SELECT MAX(P.gradeUsedCarPrice)
         FROM CAR C
         LEFT JOIN GRADE G ON C.carClassNbr = G.carClassNbr
         LEFT JOIN PRICE P ON G.carGradeNbr = P.carGradeNbr
         WHERE P.trvlDstnc = 50000 AND C.carClassNbr = %s
         GROUP BY C.carClassNbr) AS maxPrice
 FROM CAR C
 LEFT JOIN GRADE G ON C.carClassNbr = G.carClassNbr
 LEFT JOIN PRICE P ON G.carGradeNbr = P.carGradeNbr
 WHERE P.trvlDstnc = 50000 AND C.carClassNbr = %s
 GROUP BY G.carGradeNbr, C.yearType, C.carClassNm, P.gradeUsedCarPrice, 
          G.carGradeNm, C.brandImage, G.carClassRepImage) AS a