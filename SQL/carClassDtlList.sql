-- 연식
SELECT carClassNbr,  concat(yearType ," ", carClassNm) AS carClassNm
  FROM CAR
 WHERE repCarClassNbr = %s
 GROUP BY carClassNbr
 order by carClassNm DESC
