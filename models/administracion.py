# models/administracion.py
class CopiaSeguridad:
    def __init__(self, id_copia=None, fecha_hora=None, tipo='Manual', ubicacion=None, tamano=None, generado_por=None):
        self.id = id_copia
        self.fechaHora = fecha_hora [cite: 137]
        self.tipo = tipo  # 'Manual' o 'Automática' [cite: 135, 148]
        self.ubicacion = ubicacion [cite: 138]
        self.tamaño = tamano
        self.generadoPor = generado_por


class Reporte:
    def __init__(self, id_reporte=None, generado_por=None, tipo=None, fecha_inicio=None, fecha_fin=None, formato=None, fecha_generacion=None, archivo=None):
        self.id = id_reporte
        self.generadoPor = generado_por [cite: 148]
        self.tipo = tipo  # Ej. 1=Pacientes Activos, 2=Citas por Periodo [cite: 148]
        self.fechaInicio = fecha_inicio [cite: 56]
        self.fechaFin = fecha_fin [cite: 56]
        self.formato = formato  # 'PDF', 'Excel' [cite: 59, 113]
        self.fechaGeneracion = fecha_generacion
        self.archivo = archivo [cite: 60]
