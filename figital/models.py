from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Gerenciador de usuário personalizado
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        username = extra_fields.get('username', email)  
        extra_fields.setdefault('username', username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser precisa ter is_superuser=True')
        
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser precisa ter is_staff=True')
        
        return self._create_user(email, password, **extra_fields)

# Modelo de usuário personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# Classe Base para Formulários
class BaseFormulario(models.Model):    
    nome = models.CharField(max_length=200)
    secretaria = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=15) 
    problema_urgente = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome  # Retornando o nome como representação do objeto

# Modelo para 1º Escalão
class PrimeiroEscalao(BaseFormulario):
    def __str__(self):
        return f"1º Escalão - {self.nome}"  # Adiciona contexto ao nome

# Modelo para Rede de Transformação Digital
class RedeTransformacaoDigital(BaseFormulario):
    chefe_imediato = models.TextField()

    def __str__(self):
        return f"Rede de Transformação Digital - {self.nome}"  # Adiciona contexto ao nome

