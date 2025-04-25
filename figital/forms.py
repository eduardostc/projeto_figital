from django import forms
from .models import PrimeiroEscalao, RedeTransformacaoDigital, Usuario
from django.contrib.auth.forms import UserCreationForm

# Formulário de criação de usuários
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password1', 'password2']

class PrimeiroEscalaoForm(forms.ModelForm):
    class Meta:
        model = PrimeiroEscalao
        # fields = '__all__'
        fields = [
            'nome',
            'secretaria',
            'cargo',
            'email',
            'telefone',
            'problema_urgente',
        ]
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'form-control mask-telefone',
                'placeholder': '(00) 00000-0000'
            }),
            'problema_urgente': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder': ''}),
        }
        labels = {
            'nome' : 'Nome:',
            'secretaria' : 'Secretaria:',
            'cargo': 'Cargo ou Função:',
            'email': 'E-mail:',
            'telefone' : 'Whatsapp:',
            'cargo': 'Cargo ou Função:',
            'problema_urgente': 'Qual o principal problema em sua secretaria ou unidade que precisa ser atacado urgentemente?',
        }
    #metodo para remover os placeholder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = ''
    

class RedeTransformacaoDigitalForm(forms.ModelForm):
    class Meta:
        model = RedeTransformacaoDigital
        fields = [
            'nome',
            'secretaria',
            'cargo',
            'email',
            'telefone',
            'chefe_imediato',
            'problema_urgente',
        ]
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'form-control mask-telefone',
                'placeholder': '(00) 00000-0000'
            }),
            'chefe_imediato': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'problema_urgente': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
        labels = {
            'nome' : 'Nome:',
            'secretaria' : 'Secretaria:',
            'cargo': 'Cargo ou Função:',
            'email': 'E-mail:',
            'telefone' : 'Whatsapp:',
            'cargo': 'Cargo ou Função:',
            'chefe_imediato': 'Quem é o seu chefe imediato (nome, cargo, fone, email)?',
            'problema_urgente': 'Qual o principal problema em sua secretaria ou unidade que precisa ser atacado urgentemente?',
        }

    #metodo para remover os placeholder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = ''


