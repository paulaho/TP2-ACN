# conjuntos (leídos de los datos)
set P := { read "cursos.dat" as "<1s>" };

set E := { read "estudiantes-en-comun.dat" as "<1s, 2s>"};

set D := { 1, 2, 3, 4, 5, 9, 10, 11, 12 }; #dias

set H := { 9, 12, 15, 18 }; #horarios

#se agrega para ej2
#defino nuevo conjunto T: trios incompatibles. ponerlos de un .dat nuevo --> lo hace creador_trios.py
set T := { read "trios.dat" as "<1s, 2s, 3s>" };

# parametros
param a[P] := read "cursos.dat" as "<1s> 2n"; 
#cantidad de aulas que neceista el parcial p
# cantidad está en la segunda columna y se indexa por parcial (que esta en la segunda columna)

var x[P * D * H] binary; #1 si tomo parcial p en horario h y dia d

# F obj
maximize TotalAsignados:
    sum <p> in P: sum <d> in D: sum <h> in H: x[p,d,h];

# restricciones
# R1: cantidad de aulas
subto Capacidad:
    forall <d> in D:
        forall <h> in H:
            sum <p> in P: a[p] * x[p,d,h] <= 75;

# R2: Incompatibilidad
subto Incompatibles:
    forall <p,q> in E:
        forall <d, h> in D * H:  # D * H son todas las combinaciones de dias y horarios. 
            x[p, d, h] + x[q, d, h] <= 1;

# R3: unicidad (asigno 1 fecha para cada parcial COMO MAX)
subto Unicidad:
    forall <p> in P:
        sum <d> in D: sum <h> in H: x[p,d,h] <= 1;

#agregado para ej2
#modificado ej3
#R4: No más de 1 parciales en 1 dia para cualquier estudiante
subto max1:
    forall <p,q> in E:
        forall <d> in D:
            sum <h> in H: x[p,d,h] + sum <h> in H: x[q,d,h] <= 1;
          

#ej 3 ideas
maximizar sumatoria para todo par de parciales (arista en G?) : cant de estudiantes que rinden los dos x distancia (en tiempo) entre los parciales

restar con un alfa la minimizacion de (#cat alumnos * penalizacion) --> combinar con un alpha la dos funciones objetivo
agregar alguna como restriccion
