from django.db import models

class CarregarArquivo(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('file_name',)

    def __str__(self):
        return self.filename
