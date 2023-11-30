import csv

# Escribir datos a un archivo CSV
with open('archivo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'nombre', 'edad'])
    writer.writerow([1, 'Juan', 25])
    writer.writerow([2, 'María', 30])

# Leer datos desde un archivo CSV
with open('mi_archivo.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar la primera fila (encabezados)
    print("Usuarios:")
    for row in reader:
        print(row)
