SELECT AGE, AR.cnt AS CNT, AR.percent AS percent  # 거래건수
FROM CAR C
JOIN AGE_RANK AR
ON C.carClassNbr = AR.carClassNbr 
WHERE AGE IN ('20대','30대','40대','50대','60대')
AND C.carClassNbr = %s
ORDER BY AGE
