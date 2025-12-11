SELECT repCarClassNbr, repCarClassNm
  FROM CAR
 WHERE brandNbr = %s
 GROUP BY repCarClassNbr, repCarClassNm