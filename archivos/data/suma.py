import argparse

def parse_arguments():
    #Configura y parsea los argumentos de línea de comandos.
    parser = argparse.ArgumentParser(description='Suma dos números.') #descripción del programa
    parser.add_argument('-n1', '--numero1', type=float, required=True, help='Primer número a sumar')
    parser.add_argument('-n2', '--numero2',type=float, required=True, help='Segundo número a sumar')
    return parser.parse_args()

def main(): #Función principal del programa    
    args = parse_arguments() #Parsea los argumentos de línea de comandos
    resultado = args.numero1 + args.numero2 #Suma los dos números proporcionados
    print(f"La suma de {args.numero1} y {args.numero2} es: {resultado}") #Muestra el resultado de la suma

if __name__ == "__main__": #Ejecuta la función principal si el script es ejecutado directamente
    main()

    #requiered sirve para hacer obligatorio el argumento, si no se proporciona, el programa mostrará un mensaje de error y terminará la ejecución
    #verbose sirve para mostrar más detalles durante la ejecución del programa, útil para depuración
    #action='store_true' convierte el argumento en un booleano, si se proporciona el argumento, su valor será True, de lo contrario será False
    # choises limita las opciones que el usuario puede proporcionar para un argumento específico, por ejemplo solo
    # puede elegir entre un conjunto predefinido de valores
    #nargs sirve para capturar una cantidad variable de argumentos posicionales, almacenándolos en una lista

    #mutables: los valores pueden cambiarse después de la creación del objeto
    #inmutables: los valores no pueden cambiarse después de la creación del objeto