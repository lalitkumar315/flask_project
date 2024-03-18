CREATE Procedure prcInsertJsonData
(@json VARCHAR(MAX) = '')
AS
BEGIN

INSERT INTO tblJsonData 
SELECT end_year, intensity, sector, topic, insight, url, region, start_year, impact, added, published, country, relevance, pestle, source, title, likelihood
	FROM OPENJSON(@json)
	WITH (
		end_year NVARCHAR(50) '$.end_year',
		intensity NVARCHAR(50) '$.intensity',
		sector NVARCHAR(50) '$.sector',
        topic NVARCHAR(50) '$.topic',
        insight NVARCHAR(150) '$.insight',
        url NVARCHAR(150) '$.url',
        region NVARCHAR(50) '$.region',
        start_year NVARCHAR(50) '$.start_year',
        impact NVARCHAR(50) '$.impact',
        added NVARCHAR(50) '$.added',
        published NVARCHAR(50) '$.published',
        country NVARCHAR(50) '$.country',
        relevance NVARCHAR(50) '$.relevance',
        pestle NVARCHAR(50) '$.pestle',
        source NVARCHAR(50) '$.source',
        title NVARCHAR(150) '$.title',
        likelihood NVARCHAR(50) '$.likelihood'
		);

END