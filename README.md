### Descripción General

Este sistema experto analiza código Python y detecta errores comunes de **sintaxis** y **semántica**.  
Utiliza una **Base de Conocimiento en MySQL** que contiene reglas y tipos de error, junto con explicaciones y sugerencias educativas.

El motor (`expert_cli.py`) emplea un enfoque **de inferencia por clasificación**,  
reconociendo patrones de código o mensajes del intérprete, y genera un reporte con diagnósticos y soluciones

Características Principales

Detección automática de:
- `SyntaxError`, `IndentationError`, `TypeError`, `NameError`, `ZeroDivisionError`, `ValueError`, `KeyError`, etc.  
Múltiples errores en una sola ejecución.  
Motor de inferencia con ejecución controlada y análisis progresivo (*post-fix*).  
Base de conocimiento extensible mediante MySQL.  
Modo **debug** para desarrolladores.  
Compatible con Python 3.10 o superior.
 
 
 **** https://github.com/diegodines/IAG ****
REPOSITORIO, DONDE ENCONTRARA LOS SCRIPTS(INSERTS) SQL PARA LA BASE DE DATOS SIN ESTO NO TIENE BASE DE CONOCIMIENTOS, EJEMPLOS Y CODIGO MAIN. 
LA CONFIGURACION DE LA BASE DE DATOS SE REALIZA EN EL MISMO PROGRAMA

INSTALAR DEPENDENCIAS / Debe tener instalado conector mysql para python
pip install mysql-connector-python

//EN MYSQLWORKBENCH 
CREATE DATABASE sbc_python;
USE sbc_python;
SCRIPTS EN GITHUB SUBIDOS COMO INSERT


//USO
AQUI EDITAR DEPENDIENDO DE LA LOCALIDAD DE SUS ARCHIVOS
python C:\Users\Diego\Desktop\IAG\expert_cli.py C:\Users\Diego\Desktop\ejemplo.py 
O EJECUTAR DIRECTAMENTE (RECOMENDADO)
python expert_cli.py ejemplo.py



