# models/administracion.py
class CopiaSeguridad:
    def __init__(self, id_copia=None, fecha_hora=None, tipo='Manual', ubicacion=None, tamano=None, generado_por=None):
        self.id = id_copia
        self.fechaHora = fecha_hora 
        self.tipo = tipo  # 'Manual' o 'Automática' 
        self.ubicacion = ubicacion 
        self.tamaño = tamano
        self.generadoPor = generado_por


class Reporte:
    def __init__(self, id_reporte=None, generado_por=None, tipo=None, fecha_inicio=None, fecha_fin=None, formato=None, fecha_generacion=None, archivo=None):
        self.id = id_reporte
        self.generadoPor = generado_por 
        self.tipo = tipo  # Ej. 1=Pacientes Activos, 2=Citas por Periodo 
        self.fechaInicio = fecha_inicio
        self.fechaFin = fecha_fin 
        self.formato = formato  # 'PDF', 'Excel' 
        self.fechaGeneracion = fecha_generacion
        self.archivo = archivo 
