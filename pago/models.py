from django.db import models

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey('inscripcion.Inscripcion', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    referencia = models.CharField(max_length=100)
    enlace_recibido_pdf = models.URLField(max_length=200)

    def __str__(self):
        return f"Pago {self.id_pago} - Inscripción: {self.id_inscripcion} - Fecha: {self.fecha} - Monto: {self.monto} - Referencia: {self.referencia} - Enlace PDF: {self.enlace_recibido_pdf}"
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['fecha']
