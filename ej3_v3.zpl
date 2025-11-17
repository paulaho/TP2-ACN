# conjuntos (leídos de los datos)
set P := { read "cursos.dat" as "<1s>" };
set E := { read "estudiantes-en-comun.dat" as "<1s, 2s>"};
set D := { 1, 2, 3, 4, 5, 9, 10, 11, 12 }; #dias
set H := { 9, 12, 15, 18 }; #horarios
set T := { read "trios.dat" as "<1s, 2s, 3s>" };

# parametros
param a[P] := read "cursos.dat" as "<1s> 2n";  #cantidad de aulas que neceista el parcial p
# cantidad está en la segunda columna y se indexa por parcial (que esta en la segunda columna)

param w[E] := read "estudiantes-en-comun.dat" as "<1s,2s> 3n"; 

var x[P * D * H] binary; #1 si tomo parcial p en horario h y dia d

#agregadas ej3
var y[P * D] binary; #1 si tomo el parcial p en dia d. Definicion en restriccion 5
var z[E * D * D] binary; #1 si tomo parcial p en dia d y parcial q en dia d' (correspondiente al segundo indice de día). pq es arista en E. definicion en restriccion 6

#penalizaciones para ej 3 CHEQUEAR
param K[D * D] := read "penalizaciones.dat" as "<1n, 2n> 3n"; #k(d1, d2) = penalizacion de poner p en d1 y q en d2 si pq estan en E.

param M := 100; #experimentar. peso para ponderar la f obj


# F obj: combinacion de maximizar parciales asignados y minimizar penalizaciones
maximize mixta:
    (M * (sum <p> in P: sum <d> in D: sum <h> in H: x[p,d,h])) #max programados
    - ( sum <p,q> in E: sum <d1> in D: sum <d2> in D: w[p,q] * K[d1,d2] * z[p,q,d1,d2] ); #penalizaciones


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
#R4: No más de 2 parciales en 1 dia para cualquier estudiante
subto max2:
    forall <p,q,r> in T:
        forall <d> in D:
            sum <h> in H: x[p,d,h] + sum <h> in H: x[q,d,h] + sum <h> in H: x[r,d,h] <= 2;

#agregado ej3
#R5: Definicion de variable y
subto def_y:
    forall <p> in P:
        forall <d> in D:
            sum <h> in H: x[p,d,h] = y[p,d]

#R6: Definicion de variable z. necesito que z = 1 si y solo si y[p,d1] = 1 Y y[q,d2] = 1
subto def_z:
    forall <p,q> in E:
        forall <d1> in D:
            forall <d2> in D:
                z[p,q,d1,d2] <= y[p,d1]

subto def_z2:
    forall <p,q> in E:
        forall <d1> in D:
            forall <d2> in D:
                z[p,q,d1,d2] <= y[q,d2]

subto def_z3:
    forall <p,q> in E:
        forall <d1> in D:
            forall <d2> in D:
                z[p,q,d1,d2] >= y[p,d1] + y[q,d2] - 1


    