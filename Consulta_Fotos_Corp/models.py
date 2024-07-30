from django.db import models
from django.conf import settings

class Persona(models.Model):
    id_persona = models.IntegerField(db_column='ID_PERSONA', primary_key=True)
    paterno = models.CharField(db_column='PATERNO', max_length=100)
    materno = models.CharField(db_column='MATERNO', max_length=100, blank=True, null=True)
    nombre = models.CharField(db_column='NOMBRE', max_length=100)
    rfc = models.CharField(db_column='RFC', max_length=15)
    
    def __str__(self) -> str:
        return self.id_persona
    
    class Meta:
        managed = False
        db_table = 'PERSONA'
        
class Corporacion(models.Model):
    clave = models.IntegerField(db_column='CLAVE', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=100)  # Field name made lowercase.
    fecha_hora = models.DateField(db_column='FECHA_HORA')  # Field name made lowercase.
    status_corporacion = models.DecimalField(db_column='STATUS_CORPORACION', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.descripcion 

    class Meta:
        managed = False
        db_table = 'CORPORACION'
    
class Corporaciones(models.Model):
    id_corp = models.IntegerField(db_column='ID_CORP', primary_key=True)  # Field name made lowercase.
    cont_corp = models.DecimalField(db_column='CONT_CORP', max_digits=10, decimal_places=0)  # Field name made lowercase.
    id_persona = models.DecimalField(db_column='ID_PERSONA', max_digits=10, decimal_places=0)  # Field name made lowercase.
    corporacion = models.IntegerField('Corporacion', db_column='CORPORACION')
    
    situacion_snsp = models.IntegerField(models.DO_NOTHING, db_column='SITUACION_SNSP')
    status_snsp = models.IntegerField(models.DO_NOTHING, db_column='STATUS_SNSP')
    situacion_jal = models.IntegerField(models.DO_NOTHING, db_column='SITUACION_JAL')
    status_real = models.IntegerField(models.DO_NOTHING, db_column='STATUS_REAL')
    
    f_ing_depen = models.DateField(db_column='F_ING_DEPEN', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.id_corp
    
    class Meta:
        managed = False
        db_table = 'CORPORACIONES'

class CorporacionesMov(models.Model):
    id_mov = models.AutoField(db_column='ID_MOV', primary_key=True)  # Field name made lowercase.
    id_corp = models.DecimalField( max_digits=10, decimal_places=0, db_column='ID_CORP')  # Field name made lowercase.
    id_persona = models.DecimalField(db_column='ID_PERSONA', max_digits=10, decimal_places=0)  # Field name made lowercase.division = models.CharField(db_column='DIVISION', max_length=30, blank=True, null=True)  # Field name made lowercase.
    corporacion = models.DecimalField(db_column='CORPORACION', max_digits=10, decimal_places=0, blank=True,                    null=True)  # Field name made lowercase.
    
    situacion_snsp = models.DecimalField(db_column='SITUACION_SNSP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status_snsp = models.DecimalField(db_column='STATUS_SNSP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    situacion_jal = models.DecimalField(db_column='SITUACION_JAL', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status_jal = models.DecimalField(db_column='STATUS_JAL', max_digits=10, decimal_places=0, blank=True, null=True)
    
    id_doc_baja = models.DecimalField(db_column='ID_DOC_BAJA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fecha_baja = models.DateTimeField(db_column='FECHA_BAJA', blank=True, null=True)  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', blank=True, null=True)  # Field name made lowercase.
    fecha_horabis = models.DateTimeField(db_column='FECHA_HORABIS', blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.id_mov
    
    class Meta:
        managed = False
        db_table = 'CORPORACIONES_MOV'
        
class FichaFoto(models.Model):
    id_persona = models.IntegerField(db_column='ID_PERSONA', blank=False, null=False)
    id_corp = models.DecimalField( max_digits=10, decimal_places=0, db_column='ID_CORP')
    id_cat_doc = models.DecimalField( max_digits=10, decimal_places=0, db_column='ID_CATEGORIA_DOC')
    imagen = models.BinaryField(db_column = 'IMAGEN', blank = True)
    id_ficha = models.IntegerField( db_column = 'ID_FICHA_FOTOGRAF_EXT', blank = False, null = False)
    
    def __str__(self) -> str:
        return self.id_persona
    
    class Meta:
        managed = False
        db_table = 'FICHA_FOTOGRAFICA'
