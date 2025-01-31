from django.db import models

class CarregarArquivo(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('filename',)

    def __str__(self):
        return self.filename
