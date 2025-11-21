import re
from collections import defaultdict

# Leer los datos de estudiantes en común
estudiantes_comun = {}
with open('estudiantes-en-comun.dat', 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            p1, p2, cant = parts[0], parts[1], int(parts[2])
            estudiantes_comun[(p1, p2)] = cant
            estudiantes_comun[(p2, p1)] = cant  # simetría

# Leer la solución: ¿qué parcial está en qué día?
parcial_dia = {}
with open('solucion.sol', 'r') as f:
    for line in f:
        # Buscar líneas como: y$P0#1    1
        match = re.match(r'y\$([^#]+)#(\d+)\s+1', line)
        if match:
            parcial = match.group(1)
            dia = int(match.group(2))
            parcial_dia[parcial] = dia

print(f"Total de parciales programados: {len(parcial_dia)}")
print(f"Días usados: {sorted(set(parcial_dia.values()))}\n")

# Análisis 1: Estudiantes que rinden 2+ parciales el mismo día
estudiantes_mismo_dia = 0
estudiantes_mismo_dia_detalle = defaultdict(int)

for (p1, p2), cant_estudiantes in estudiantes_comun.items():
    if p1 in parcial_dia and p2 in parcial_dia:
        if parcial_dia[p1] == parcial_dia[p2]:
            estudiantes_mismo_dia += cant_estudiantes
            diff = 0
            estudiantes_mismo_dia_detalle[diff] += cant_estudiantes

print(f"📊 ESTUDIANTES CON PARCIALES EL MISMO DÍA:")
print(f"   Total: {estudiantes_mismo_dia} estudiantes")
print()

# Análisis 2: Distribución de estudiantes según diferencia de días
distribucion = defaultdict(int)

for (p1, p2), cant_estudiantes in estudiantes_comun.items():
    if p1 in parcial_dia and p2 in parcial_dia:
        diff_dias = abs(parcial_dia[p1] - parcial_dia[p2])
        distribucion[diff_dias] += cant_estudiantes

print(f"📊 DISTRIBUCIÓN DE ESTUDIANTES POR DIFERENCIA DE DÍAS:")
print(f"   {'Diferencia':<12} {'Estudiantes':>12} {'%':>8}")
print(f"   {'-'*12} {'-'*12} {'-'*8}")

total_estudiantes_pares = sum(distribucion.values())
for diff in sorted(distribucion.keys()):
    cant = distribucion[diff]
    porcentaje = (cant / total_estudiantes_pares) * 100
    print(f"   {diff} días      {cant:>12,}   {porcentaje:>7.2f}%")

print(f"\n   {'TOTAL':<12} {total_estudiantes_pares:>12,}  {100.00:>7.2f}%")

# Análisis 3: Estudiantes con diferencia <= 2 días
estudiantes_cerca = sum(distribucion[d] for d in [0, 1, 2] if d in distribucion)
estudiantes_lejos = sum(distribucion[d] for d in distribucion if d > 2)

print(f"\n📊 RESUMEN:")
print(f"   Mismo día (0):           {distribucion[0]:>12,} estudiantes  ({(distribucion[0]/total_estudiantes_pares)*100:>6.2f}%)")
print(f"   Días consecutivos (1):   {distribucion.get(1, 0):>12,} estudiantes  ({(distribucion.get(1,0)/total_estudiantes_pares)*100:>6.2f}%)")
print(f"   2 días de diferencia:    {distribucion.get(2, 0):>12,} estudiantes  ({(distribucion.get(2,0)/total_estudiantes_pares)*100:>6.2f}%)")
print(f"   ─────────────────────────────────────────────────")
print(f"   Total ≤ 2 días:          {estudiantes_cerca:>12,} estudiantes  ({(estudiantes_cerca/total_estudiantes_pares)*100:>6.2f}%)")
print(f"   Total > 2 días:          {estudiantes_lejos:>12,} estudiantes  ({(estudiantes_lejos/total_estudiantes_pares)*100:>6.2f}%)")

# Análisis 4: Casos críticos (muchos estudiantes muy cerca)
print(f"\n⚠️  CASOS CRÍTICOS (≥50 estudiantes en días muy cercanos):")
criticos = []
for (p1, p2), cant_estudiantes in estudiantes_comun.items():
    if cant_estudiantes >= 50 and p1 in parcial_dia and p2 in parcial_dia:
        diff = abs(parcial_dia[p1] - parcial_dia[p2])
        if diff <= 2:
            criticos.append((p1, p2, cant_estudiantes, diff))

criticos.sort(key=lambda x: (x[3], -x[2]))

if criticos:
    print(f"   {'Parcial 1':<12} {'Parcial 2':<12} {'Estudiantes':>12} {'Diferencia':>12}")
    print(f"   {'-'*12} {'-'*12} {'-'*12} {'-'*12}")
    for p1, p2, cant, diff in criticos[:20]:  # Top 20
        print(f"   {p1:<12} {p2:<12} {cant:>12}   {diff:>10} días")
else:
    print(f"   ✅ No hay casos críticos!")

# Análisis 5: Distribución por día
print(f"\n📅 PARCIALES POR DÍA:")
parciales_por_dia = defaultdict(int)
for parcial, dia in parcial_dia.items():
    parciales_por_dia[dia] += 1

for dia in sorted(parciales_por_dia.keys()):
    print(f"   Día {dia:>2}: {parciales_por_dia[dia]:>3} parciales")