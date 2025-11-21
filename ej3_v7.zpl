# conjuntos (leídos de los datos)
set P := { read "cursos.dat" as "<1s>" };
set E := { read "estudiantes-en-comun.dat" as "<1s, 2s>"};
set D := { 1, 2, 3, 4, 5, 9, 10, 11, 12 }; #dias
set H := { 9, 12, 15, 18 }; #horarios
set T := { read "trios.dat" as "<1s, 2s, 3s>" };

# parametros
param a[P] := read "cursos.dat" as "<1s> 2n";
param w[E] := read "estudiantes-en-comun.dat" as "<1s,2s> 3n"; 

var x[P * D * H] binary;
var y[P * D] binary;

# Variables para medir si dos parciales están en el mismo día o días consecutivos
var mismo_dia[E * D] binary;      # 1 si p y q están en el mismo día d
var consecutivos[E] binary;       # 1 si p y q están en días consecutivos (cualquier par)

# Pesos: priorizar CANTIDAD de parciales programados
param M := 1000;  # Peso alto para cantidad

# Penalizaciones PROGRESIVAS según cantidad de estudiantes
param penalizacion_mismo_dia[<p,q> in E] := 
    if w[p,q] >= 100 then 500
    else if w[p,q] >= 50 then 200
    else if w[p,q] >= 20 then 50
    else 5 end end end;

param penalizacion_consecutivo[<p,q> in E] := 
    if w[p,q] >= 100 then 100
    else if w[p,q] >= 50 then 30
    else if w[p,q] >= 20 then 10
    else 1 end end end;

# Función objetivo: Maximizar parciales programados - penalizar días cercanos
maximize dispersion_inteligente:
    (M * sum <p,d,h> in P*D*H: x[p,d,h])
    - (sum <p,q> in E: 
        sum <d> in D: 
            penalizacion_mismo_dia[p,q] * mismo_dia[p,q,d])
    - (sum <p,q> in E: 
            penalizacion_consecutivo[p,q] * consecutivos[p,q]);

# Restricciones originales
subto Capacidad:
    forall <d,h> in D*H:
        sum <p> in P: a[p] * x[p,d,h] <= 75;

subto Incompatibles:
    forall <p,q> in E:
        forall <d,h> in D*H:
            x[p,d,h] + x[q,d,h] <= 1;

subto Unicidad:
    forall <p> in P:
        sum <d,h> in D*H: x[p,d,h] <= 1;

subto max2:
    forall <p,q,r> in T:
        forall <d> in D:
            sum <h> in H: (x[p,d,h] + x[q,d,h] + x[r,d,h]) <= 2;

# Definición de y
subto def_y_upper:
    forall <p,d> in P*D:
        y[p,d] >= sum <h> in H: x[p,d,h];

subto def_y_lower:
    forall <p,d> in P*D:
        y[p,d] <= sum <h> in H: x[p,d,h];

# Definición de mismo_dia: p y q ambos en día d
subto def_mismo_dia_1:
    forall <p,q> in E:
        forall <d> in D:
            mismo_dia[p,q,d] <= y[p,d];

subto def_mismo_dia_2:
    forall <p,q> in E:
        forall <d> in D:
            mismo_dia[p,q,d] <= y[q,d];

subto def_mismo_dia_3:
    forall <p,q> in E:
        forall <d> in D:
            mismo_dia[p,q,d] >= y[p,d] + y[q,d] - 1;

# Definición de consecutivos: p y q en días consecutivos
# Revisamos todos los pares de días válidos
subto def_consecutivos_1_2:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,1] + y[q,2] - 1;

subto def_consecutivos_2_3:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,2] + y[q,3] - 1;

subto def_consecutivos_3_4:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,3] + y[q,4] - 1;

subto def_consecutivos_4_5:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,4] + y[q,5] - 1;

subto def_consecutivos_9_10:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,9] + y[q,10] - 1;

subto def_consecutivos_10_11:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,10] + y[q,11] - 1;

subto def_consecutivos_11_12:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,11] + y[q,12] - 1;

# También en dirección inversa (q antes que p)
subto def_consecutivos_2_1:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,2] + y[q,1] - 1;

subto def_consecutivos_3_2:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,3] + y[q,2] - 1;

subto def_consecutivos_4_3:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,4] + y[q,3] - 1;

subto def_consecutivos_5_4:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,5] + y[q,4] - 1;

subto def_consecutivos_10_9:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,10] + y[q,9] - 1;

subto def_consecutivos_11_10:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,11] + y[q,10] - 1;

subto def_consecutivos_12_11:
    forall <p,q> in E:
        consecutivos[p,q] >= y[p,12] + y[q,11] - 1;

# Límite superior para consecutivos
subto def_consecutivos_upper:
    forall <p,q> in E:
        consecutivos[p,q] <= y[p,1] + y[p,2] + y[p,3] + y[p,4] + y[p,5] + 
                             y[p,9] + y[p,10] + y[p,11] + y[p,12] +
                             y[q,1] + y[q,2] + y[q,3] + y[q,4] + y[q,5] + 
                             y[q,9] + y[q,10] + y[q,11] + y[q,12];