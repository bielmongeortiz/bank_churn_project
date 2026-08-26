-- Q1: Which customer profiles have the highest churn risk rate based on geneder?
use [BankChurn];

WITH 
    MainTable AS (
        SELECT 
            [Gender],
            COUNT(*) AS TotalCustomers,
            SUM(CAST([Churned] AS INT)) AS TotalChurn
        FROM [dbo].[demographic]
        GROUP BY Gender
    )

SELECT *, 
	FORMAT((TotalChurn * 100 / TotalCustomers), 'N2') + '%' AS ChurnRate
FROM MainTable