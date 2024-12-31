--CREATE DATABASE ZonaProp_db;

--USE ZonaProp_db;

CREATE TABLE IF NOT EXISTS Propiedades(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            precio FLOAT,
                            moneda_expensas VARCHAR(255),
                            expensas FLOAT,
                            nombre TEXT,
                            fotos INT,
                            localizacion TEXT,
                            metros_cuadrados INT,
                            ambientes INT,
                            dormitorios INT,
                            baños INT,
                            cocheras INT,
                            link TEXT,
                            id_zonaprop INT,
                            ultima_actualizacion TIMESTAMP,
                            descripcion VARCHAR(51)
                        );
