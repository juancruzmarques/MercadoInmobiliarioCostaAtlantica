SELECT
	*
FROM 
	Propiedades
WHERE
	precio != 'N/A' AND
  NOT precio REGEXP '^1+$' AND
  NOT metros_cuadrados REGEXP '^1+$'

AND
	localizacion != 'N/A'
AND
	metros_cuadrados != 'N/A'
AND
	ambientes != 'N/A'
ORDER BY 
	metros_cuadrados DESC