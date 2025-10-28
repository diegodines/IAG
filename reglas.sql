/*
-- Query: SELECT * FROM sbc_python.rule
LIMIT 0, 1000

-- Date: 2025-10-28 19:23
*/
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (1,'IfSinDosPuntos','code','(?m)^\\s*if\\b[^\\r\\n:]*$',1,'Se detectó una línea \"if\" sin \":\" al final.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (2,'MsgIndent','message','indent',2,'El mensaje del intérprete indica un problema de indentación.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (3,'MsgTypeCatStrInt','message','can\'t concatenate str and int',3,'Concatenación entre str e int detectada en el mensaje.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (4,'MsgExpectedColon','message','expected \':\':',1,'El intérprete indica que falta \":\".',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (5,'ForSinDosPuntos','code','(?m)^\\s*for\\b[^\\r\\n:]*$',1,'Se detectó un \"for\" sin \":\" al final.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (6,'WhileSinDosPuntos','code','(?m)^\\s*while\\b[^\\r\\n:]*$',1,'Se detectó un \"while\" sin \":\" al final.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (7,'DefSinDosPuntos','code','(?m)^\\s*def\\b[^\\r\\n:]*$',1,'Se detectó un \"def\" sin \":\" al final.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (8,'ClassSinDosPuntos','code','(?m)^\\s*class\\b[^\\r\\n:]*$',1,'Se detectó un \"class\" sin \":\" al final.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (9,'MsgUnterminatedString','message','unterminated string literal|EOL while scanning string literal',1,'Cadena de texto sin cerrar (comillas faltantes).',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (10,'MsgIndentGroup','message','unexpected indent|expected an indented block|unindent does not match',2,'Problema de indentación detectado por el intérprete.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (11,'MsgNameError','message','name .+ is not defined',4,'Variable/Nombre usado sin estar definido.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (12,'MsgTypeConcatStrInt','message','can\'t concatenate str and int|can only concatenate str \\(not \".+\"\\) to str',3,'Concatenación entre str e int detectada.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (13,'MsgTypeUnsupportedOperand','message','unsupported operand type\\(s\\) for [^:]+:\\s*\'.+\'\\s+and\\s*\'.+\'',3,'Operandos de tipos incompatibles en una operación.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (14,'MsgTypeNotCallable','message','object is not callable',3,'Intento de llamar a algo que no es función (p.ej., variable con mismo nombre).',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (15,'MsgValueInvalidLiteralInt','message','invalid literal for int\\(\\) with base \\d+: .+',5,'Conversión a int() falló por formato inválido.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (16,'MsgZeroDivision','message','division by zero',6,'División por cero detectada.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (17,'MsgIndexOutOfRange','message','list index out of range',7,'Índice fuera de rango en lista.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (18,'MsgKeyError','message','KeyError:\\s*[\'\"].+[\'\"]',8,'Clave inexistente en diccionario.',1);
INSERT INTO `` (`id`,`name`,`kind`,`pattern_regex`,`conclusion_error_type_id`,`diag_text`,`priority`) VALUES (19,'MsgAttributeError','message','AttributeError:\\s*\'.+\': object has no attribute [\'\"].+[\'\"]',9,'Acceso a un atributo inexistente.',1);
