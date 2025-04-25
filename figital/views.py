from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import PrimeiroEscalaoForm, RedeTransformacaoDigitalForm, UsuarioForm
from .models import PrimeiroEscalao, RedeTransformacaoDigital
from .forms import PrimeiroEscalaoForm

# Página inicial
def index(request):
    return render(request, 'figital/index.html')

# Cadastro no 1º Escalão (sem autenticação)
def primeiro_escalao(request):
    if str(request.method) == "POST":
        form = PrimeiroEscalaoForm(request.POST)

        if form.is_valid():
            form.save()  # Agora qualquer usuário pode salvar
            messages.success(request, 'Formulário enviado com sucesso!')
            form = PrimeiroEscalaoForm() # ao invés de return redirect('index')
        else:
            messages.error(request, 'Erro ao enviar o Formulário.')
    else:
        form = PrimeiroEscalaoForm()
    context = {
        'form' : form
    }
    return render(request, 'figital/form_escalao.html', context)


# Cadastro na Rede de Transformação Digital (sem autenticação)
def rede_transformacao(request):
    if str(request.method) == "POST":
        form = RedeTransformacaoDigitalForm(request.POST)

        if form.is_valid():
            form.save()  # Agora qualquer usuário pode salvar
            messages.success(request, 'Formulário enviado com sucesso!')
            form = RedeTransformacaoDigitalForm()
        else:
            messages.error(request, 'Erro ao enviar o Formulário.')
    else:
        form = RedeTransformacaoDigitalForm()
    context = {
        'form' : form
    }
    return render(request, 'figital/form_transformacao.html', context)


# Tela de Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Melhor usar .get() para evitar erros
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index_autenticado') 
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
    return render(request, 'figital/login.html')


#Metodos com acesso somente pra quem está autenticado

# views.py
@login_required  # Opcional: protege a rota para usuários logados
def index_autenticado(request):
    return render(request, 'figital/index_autenticado.html')

# Visualização dos registros - 1º Escalão (restrito)
@login_required
def visualizar_escalao(request):
    if str(request.user) != 'AnonymousUser':    
        context = {
            'registros' : PrimeiroEscalao.objects.all()  # Exibe todos os registros
        }    
        return render(request, 'figital/visualizar_escalao.html', context)
    else:
        return redirect('index')
    

# Visualização dos registros - Rede de Transformação Digital (restrito)
@login_required
def visualizar_transformacao(request):
    if str(request.user) != 'AnonymousUser':     
        context = {
        'registros' : RedeTransformacaoDigital.objects.all()  # Exibe todos os registros
        }           
        return render(request, 'figital/visualizar_transformacao.html', context)
    else:
        return redirect('index')

import csv
import datetime
from django.http import HttpResponse
from .models import PrimeiroEscalao

def exportar_escalao_excel(request):
    # Configurando a resposta HTTP para um arquivo Excel
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="primeiro_escalao_{datetime.date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Data da Publicação', 'Nome', 'Secretaria', 'Cargo', 'Email', 'Telefone', 'Problema Urgente'])

    registros = PrimeiroEscalao.objects.all()
    for registro in registros:
        writer.writerow([registro.id, registro.data_publicacao, registro.nome, registro.secretaria, registro.cargo, registro.email, registro.telefone, registro.problema_urgente])

    return response

import csv
import datetime
from django.http import HttpResponse
from .models import RedeTransformacaoDigital

def exportar_transformacao_excel(request):
    # Configurando a resposta HTTP para um arquivo Excel
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="rede_transformacao_{datetime.date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Data da Publicação', 'Nome', 'Secretaria', 'Cargo', 'Email', 'Telefone', 'Chefe Imediato', 'Problema Urgente'])

    registros = RedeTransformacaoDigital.objects.all()
    for registro in registros:
        writer.writerow([registro.id, registro.data_publicacao, registro.nome, registro.secretaria, registro.cargo, registro.email, registro.telefone, registro.chefe_imediato, registro.problema_urgente])

    return response


    