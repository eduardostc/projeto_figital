from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

@receiver(post_migrate)
def criar_superusuarios(sender, **kwargs):
    """Cria os grupos necessários e os superusuários automaticamente após migrações."""
    User = get_user_model()

    try:
        # Criar ou obter grupos
        grupo_exclusao, _ = Group.objects.get_or_create(name="Grupo de Exclusão")
        grupo_edicao, _ = Group.objects.get_or_create(name="Grupo de Edição")

        # Criar superusuário 'admin' se não existir
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'carlos.rodrigues@recife.pe.gov.br',
                'nome_completo': 'Carlos Eduardo',
                'telefone': '(81) 98717-2274',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('@Admin123')  # Define a senha corretamente
            admin_user.save()  # Salva as alterações
            admin_user.groups.add(grupo_exclusao, grupo_edicao)
            print("✅ Superusuário 'admin' criado e adicionado aos grupos!")

        # Criar superusuário 'joao' se não existir
        joao_user, created = User.objects.get_or_create(
            username='joao',  # Corrigido para evitar erro de duplicação
            defaults={
                'email': 'joaocarloscosta@recife.pe.gov.br',
                'nome_completo': 'João Carlos Costa',
                'telefone': '(81) 98765-0747',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            joao_user.set_password('112358')  # Define a senha corretamente
            joao_user.save()  # Salva as alterações
            joao_user.groups.add(grupo_exclusao, grupo_edicao)
            print("✅ Superusuário 'joao' criado e adicionado aos grupos!")

    except Exception as e:
        print(f"⚠️ Erro ao criar superusuários: {e}")





# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group

# @receiver(post_migrate)
# def criar_superusuarios(sender, **kwargs):
#     User = get_user_model()

#     try:
#         # Criar ou obter grupos
#         grupo_exclusao, _ = Group.objects.get_or_create(name="Grupo de Exclusão")
#         grupo_edicao, _ = Group.objects.get_or_create(name="Grupo de Edição")

#         # Criar superusuário 'admin' se não existir
#         if not User.objects.filter(username='admin').exists():
#             admin_user = User.objects.create_superuser(
#                 username='admin',
#                 email='carlos.rodrigues@recife.pe.gov.br',
#                 password='@Admin123',
#                 nome_completo='Carlos Eduardo',
#                 telefone='(81) 98717-2274'
#             )
#             admin_user.groups.add(grupo_exclusao, grupo_edicao)
#             print("✅ Superusuário 'admin' criado e adicionado aos grupos!")

#         # Criar superusuário 'joao' se não existir
#         if not User.objects.filter(username='joao').exists():
#             joao_user = User.objects.create_superuser(
#                 username='João',
#                 email='joaocarloscosta@recife.pe.gov.br',
#                 password='112358',
#                 nome_completo='João Carlos Costa',
#                 telefone='(81) 98765-0747'
#             )
#             joao_user.groups.add(grupo_exclusao, grupo_edicao)
#             print("✅ Superusuário 'admin' criado e adicionado aos grupos!")
        
#     except Exception as e:
#         print(f"⚠️ Erro ao criar superusuários: {e}")
