SELECT c.id, c.emailsubscribed_raw
	, LEFT(c.emailsubscribed_raw,5) AS emailsubscribed_left
	, CASE 
		WHEN LOWER(c.emailsubscribed_raw) = 'y' THEN 'Yes'
		WHEN LOWER(c.emailsubscribed_raw) LIKE '%yes%' THEN 'Yes'
		WHEN LOWER(c.emailsubscribed_raw) = 'n' THEN 'No'
		WHEN LOWER(c.emailsubscribed_raw) LIKE '%no%' THEN 'No'
		WHEN LOWER(c.emailsubscribed_raw) LIKE '%mail%' THEN 'Yes'
		WHEN LOWER(c.emailsubscribed_raw) LIKE '%text%' THEN 'No'
		ELSE 'No'
	END
	AS emailsubscribed_out	
FROM test.contact_types c
