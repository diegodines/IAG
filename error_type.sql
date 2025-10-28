/*
-- Query: SELECT * FROM sbc_python.error_type
LIMIT 0, 1000

-- Date: 2025-10-28 19:24
*/
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (1,'SyntaxError','SINTAXIS',1,'El código no sigue las reglas del lenguaje.','Revisa \":\" al final de if/for/while/def/class, paréntesis y comillas.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (2,'IndentationError','SINTAXIS',1,'Indentación inválida o inconsistente.','Usa 4 espacios por nivel y no mezcles tabs con espacios.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (3,'TypeError','SEMANTICO',1,'Operación inválida entre tipos (str, int, etc.).','Convierte tipos con int(), float(), str() cuando corresponda.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (4,'NameError','SEMANTICO',1,'Se usa un nombre/variable que no fue definido.','Declara/asigna o importa el nombre antes de usarlo.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (5,'ValueError','SEMANTICO',2,'Un valor tiene formato inválido para la conversión.','Valida y sanitiza la entrada; maneja excepciones con try/except.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (6,'ZeroDivisionError','SEMANTICO',1,'Se intentó dividir por cero.','Valida el denominador antes de dividir.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (7,'IndexError','SEMANTICO',2,'Índice fuera de rango en una secuencia.','Verifica longitudes y rangos antes de indexar.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (8,'KeyError','SEMANTICO',2,'Clave inexistente en un diccionario.','Usa in/ get() con valor por defecto o valida la clave.');
INSERT INTO `` (`id`,`name`,`category`,`severity`,`explanation`,`suggestion`) VALUES (9,'AttributeError','SEMANTICO',2,'Se accedió a un atributo que no existe.','Verifica el tipo/atributos u ocupa getattr con default.');
