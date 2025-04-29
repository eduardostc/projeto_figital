from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import PrimeiroEscalaoForm, RedeTransformacaoDigitalForm, UsuarioForm
from .models import PrimeiroEscalao, RedeTransformacaoDigital
from .forms import PrimeiroEscalaoForm


# Página inicial
def index(request):
    return render(request, 'figital/index.html')

#Metodos com acesso somente pra quem está autenticado
@login_required  # Opcional: protege a rota para usuários logados
def index_autenticado(request):
    return render(request, 'figital/index_autenticado.html')


#Metado para cadastrar os registro nos formulários
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


# Visualização dos registros - 1º Escalão (restrito)
@login_required
def visualizar_escalao(request):
    if str(request.user) != 'AnonymousUser':

        # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
        pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

        context = {
            'registros' : PrimeiroEscalao.objects.all(),  # Exibe todos os registros
            'pertence_grupo_exclusao': pertence_grupo_exclusao,  # Passa a variável ao template
        }    
        return render(request, 'figital/visualizar_escalao.html', context)
    else:
        return redirect('index')
    

# Visualização dos registros - Rede de Transformação Digital (restrito)
@login_required
def visualizar_transformacao(request):
    if str(request.user) != 'AnonymousUser':     

        # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
        pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

        context = {
            'registros' : RedeTransformacaoDigital.objects.all(),  # Exibe todos os registros
            'pertence_grupo_exclusao': pertence_grupo_exclusao,  # Passa a variável ao template
        }           
        return render(request, 'figital/visualizar_transformacao.html', context)
    else:
        return redirect('index')
    

#Metodo para exportar para excel
import csv
import datetime
from django.http import HttpResponse, HttpResponseForbidden
from .models import PrimeiroEscalao, RedeTransformacaoDigital

@login_required
def exportar_escalao_excel(request):
    # Configurando a resposta HTTP para um arquivo Excel
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="primeiro_escalao_{datetime.date.today()}.csv"'

    writer = csv.writer(response)
    # writer = csv.writer(response, delimiter=";")
    writer.writerow(['ID', 'Data da Publicação', 'Nome', 'Secretaria', 'Cargo', 'Email', 'Telefone', 'Problema Urgente'])

    registros = PrimeiroEscalao.objects.all()
    for registro in registros:
        print(registro)  # Exibir dados no terminal
        writer.writerow([registro.id, registro.data_publicacao, registro.nome, registro.secretaria, registro.cargo, registro.email, registro.telefone, registro.problema_urgente])

    return response


#metodo 3
# import csv
# import datetime
# from django.http import HttpResponse
# from .models import PrimeiroEscalao

# def exportar_escalao_excel(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="primeiro_escalao_{datetime.date.today()}.csv"'
#     response.write(u'\ufeff'.encode('utf8'))  # Evita problemas de codificação

#     writer = csv.writer(response, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

#     # Escrevendo cabeçalho
#     writer.writerow(['ID', 'Data da Publicação', 'Nome', 'Secretaria', 'Cargo', 'Email', 'Telefone', 'Problema Urgente'])

#     registros = PrimeiroEscalao.objects.all()

#     # 🔹 Adicionando print para depuração
#     for registro in registros:
#         print(f"Escrevendo no CSV: {registro.nome}, {registro.secretaria}, {registro.cargo}")
#         writer.writerow([
#             registro.id, 
#             registro.data_publicacao.strftime("%Y-%m-%d %H:%M:%S"), 
#             registro.nome, 
#             registro.secretaria, 
#             registro.cargo, 
#             registro.email, 
#             registro.telefone, 
#             registro.problema_urgente
#         ])

#     print("Resposta do CSV gerada com sucesso.")  # Confirmação final

#     return response


@login_required
def exportar_transformacao_excel(request):
    # Configurando a resposta HTTP para um arquivo Excel
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="rede_transformacao_{datetime.date.today()}.csv"'

    # writer = csv.writer(response)
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['ID', 'Data da Publicação', 'Nome', 'Secretaria', 'Cargo', 'Email', 'Telefone', 'Chefe Imediato', 'Problema Urgente'])

    registros = RedeTransformacaoDigital.objects.all()
    for registro in registros:
        writer.writerow([registro.id, registro.data_publicacao, registro.nome, registro.secretaria, registro.cargo, registro.email, registro.telefone, registro.chefe_imediato, registro.problema_urgente])

    return response

#Metodos para excluir os registros
@login_required
def excluir_registro_escalao(request, registro_id):
    """
    Exclui um registro específico, permitido apenas para membros do Grupo de Exclusão.
    """
    registro = get_object_or_404(PrimeiroEscalao, id=registro_id)

     # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
    pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

    if not pertence_grupo_exclusao:
        return HttpResponseForbidden("Você não tem permissão para excluir este atendimento.")

    if request.method == 'POST':
        #Excluir o registro
        registro.delete()
        messages.success(request, "Registro removido com sucesso.")

        next_url = request.GET.get('next', 'visualizar_escalao')
        return redirect(next_url)
    context = {
        'registro': registro,
        'pertence_grupo_exclusao': pertence_grupo_exclusao,
    }

    return render(request, 'figital/index.html',context)

@login_required
def excluir_registro_transformacao(request, registro_id):
    """
    Exclui um registro específico, permitido apenas para membros do Grupo de Exclusão.
    """
    registro = get_object_or_404(RedeTransformacaoDigital, id=registro_id)

     # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
    pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

    if not pertence_grupo_exclusao:
        return HttpResponseForbidden("Você não tem permissão para excluir este atendimento.")

    if request.method == 'POST':
        #Excluir o registro
        registro.delete()
        messages.success(request, "Registro removido com sucesso.")

        next_url = request.GET.get('next', 'visualizar_transformacao')
        return redirect(next_url)
    context = {
        'registro': registro,
        'pertence_grupo_exclusao': pertence_grupo_exclusao,
    }

    return render(request, 'figital/index.html',context)

#Metodos para editar os registros
@login_required
def editar_registro_escalao(request, registro_id):
    """
    Editar um registro específico, permitido apenas para membros do Grupo de Exclusão.
    """
    registro = get_object_or_404(PrimeiroEscalao, id=registro_id)

     # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
    pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

    if not pertence_grupo_exclusao:
        return HttpResponseForbidden("Você não tem permissão para editar este atendimento.")

    if request.method == 'POST':
        form = PrimeiroEscalaoForm(request.POST, instance=registro)  # Popula o formulário com os dados enviados
        if form.is_valid():
            form.save() #salva o formulário
            messages.success(request, "Registro atualizado com sucesso.")
            return redirect('visualizar_escalao') # Redireciona após salvar
    else:
        form = PrimeiroEscalaoForm(isinstance=registro) # Carrega o registro

    context = {
        'registro': registro,
        'pertence_grupo_exclusao': pertence_grupo_exclusao,
    }
    return render(request, 'figital/visualizar_escalao.html',context)


@login_required
def editar_registro_transformacao(request, registro_id):
    """
    Editar um registro específico, permitido apenas para membros do Grupo de Exclusão.
    """
    registro = get_object_or_404(RedeTransformacaoDigital, id=registro_id)

     # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
    pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

    if not pertence_grupo_exclusao:
        return HttpResponseForbidden("Você não tem permissão para editar este atendimento.")

    if request.method == 'POST':
        form = RedeTransformacaoDigitalForm(request.POST, instance=registro)  # Popula o formulário com os dados enviados
        if form.is_valid():
            form.save() #salva o formulário
            messages.success(request, "Registro atualizado com sucesso.")
            return redirect('visualizar_transformacao') # Redireciona após salvar
    else:
        form = RedeTransformacaoDigitalForm(isinstance=registro) # Carrega o registro

    context = {
        'registro': registro,
        'pertence_grupo_exclusao': pertence_grupo_exclusao,
    }
    return render(request, 'figital/visualizar_transformacao.html',context)