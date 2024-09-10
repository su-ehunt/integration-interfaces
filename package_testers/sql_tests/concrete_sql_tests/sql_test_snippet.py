sql =''' EXEC sp_executesql N'
    -- Create a temporary table
    CREATE TABLE #TempTable (
        ID INT,
        Name NVARCHAR(50)
    );

    -- Insert 3 rows into the temporary table
    INSERT INTO #TempTable (ID, Name)
    VALUES 
        (1, ''Alice''),
        (2, ''Bob''),
        (3, ''Charlie'');
    
    -- Select the 3 rows from the temporary table
    SELECT *
    FROM #TempTable;

    -- Drop the temporary table
    DROP TABLE #TempTable;
';
'''