def get_at_content(dna, sig_figs=2):
    """
    Calcula el contenido AT de una secuencia de ADN,
    redondeando a un número específico de cifras decimales.
    Parámetros:
    dna (str): Secuencia de ADN (ej. 'ATGCGC')
    sig_figs (int, opcional): número de cifras decimales (por defecto = 2)
    Retorna:
    float: contenido AT redondeado
    """
    dna = dna.upper().strip()
    # Validaciones
    if len(dna) == 0:
        raise ValueError("La secuencia está vacía.")
    invalid = set(dna) - set("ATCG")
    if invalid:
        raise ValueError(f"Caracteres inválidos en la secuencia: {', '.join(sorted(invalid))}")
    a = dna.count("A")
    t = dna.count("T")
    at_content = (a + t) / len(dna)
    return round(at_content, sig_figs)

if __name__ == "__main__":
    assert get_at_content("ATGC", 1) == 0.5
    assert get_at_content("ATGCNNNNNN", 1) == 0.5
    
    # ejemplo de uso
    #dna_sequence = "ATGCGCATTAAGC"
    #at_content_value = get_at_content(dna_sequence, sig_figs=3)
    #print(f"El contenido AT de la secuencia es: {at_content_value}")
