# Catálogos simples (criterios epistemológicos)
TIPOS_AMBIENTE = [
    "urbano", "suburbano", "rural", "costero",
    "serrano", "litoral", "forestal", "natural_protegido",
]
USOS_SUELO = ["residencial","agropecuario","forestal","industrial","turistico","conservacion","mixto"]
COBERTURA_RELIEVE = ["pradera/llanura","sierras/piedra","humedal/bañado","dunas/playa","ribera/costa","mosaico_mixto"]
INTERVENCION_HUMANA = ["baja","media","alta"]
CONECTIVIDAD_TERRITORIAL = ["baja","media","alta"]
VALOR_ECOCULTURAL = ["ninguno","local","departamental","nacional","snap"]

def escoger(opciones, valor, default=None):
    v = (valor or "").strip().lower()
    if v in opciones:
        return v
    return default if (default and default in opciones) else opciones[0]
