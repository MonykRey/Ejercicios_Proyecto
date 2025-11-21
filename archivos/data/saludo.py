import argparse #por default la libreria utiliza el help para documentar los argumentos

#1 Create the parser
parser = argparse.ArgumentParser(description="Saluda a una persona por su nombre.") 

# 2 Definir los argumentos --argumento opcionales
parser.add_argument("nombre", type=str, help="El nombre de la persona a saludar")

#ahora con apellido
parser.add_argument("--apellido", type=str, help="El apellido de la persona a saludar", default="")

#edad
parser.add_argument("--edad", type=int, help="La edad de la persona", default=0) #Type especifica el tipo de dato, si es str, int, float, etc.
# default especifica un valor por defecto en caso de que el usuario no lo proporcione
#3 leer /Procesar los argumentos dado por el usuario
args = parser.parse_args()

#4 Usar el argumento
print(f"Hola, {args.nombre} {args.apellido} tiene {args.edad} años!")

#en los argumentos opcionales se usa -- antes del nombre del argumento, además no imporyta el orden en que se colocan y se pueden omitir si tienen un valor por defecto
