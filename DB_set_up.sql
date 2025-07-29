/* CREATE DATABASE ZonaProp_db; */

USE ZonaProp_db;

CREATE TABLE IF NOT EXISTS Propiedades6 (
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
                            descripcion VARCHAR(51),
                            latitud FLOAT, -- nuevo
                            longitud FLOAT, -- nuevo
                            fecha_publicacion TIMESTAMP, -- Hay que convertir a timestamp
                            antiguedad_publicacion TEXT,
                            visitas_u30d INT, -- Hay que decidir que tipo tiene
                            superficie_total INT,
                            superficie_cubierta INT,
                            antiguedad TEXT,
                            disposicion TEXT,
                            orientacion TEXT,
                            luminosidad TEXT,
                            anunciante TEXT,
                            anunciante_premium_si_o_no BOOLEAN,
                            anunciante_tipo_de_id TEXT,
                            wpp_anunciante BIGINT,
                            url_anunciante TEXT,
                            property_type TEXT
                        );
/*
['stotal', 'scubierta', 'bano', 'cochera', 'dormitorio', 'toilete', 'antiguedad', 'disposicion', 'orientacion', 'luminosidad']

                    latitud FLOAT,                   ###agregada
                    longitud FLOAT,                  ###agregada

                    fecha_publicacion                ###agregada
                    antiguedad_publicacion           ###agregada
                    visitas_u30d                     ###agregada

                    superficie_total
                    superficie_cubierta
                    antiguedad
                    disposicion
                    orientacion
                    luminosidad

                    anunciante                       ###agregada
                    anunciante_premium_si_o_no       ###agregada
                    anunciante_tipo_de_id            ###agregada
                    wpp_anunciante                   ###agregada
                    url_anunciante                   ###agregada
*/
