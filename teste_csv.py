import csv

# 🔹 Criando um arquivo CSV manualmente e garantindo que os dados sejam gravados corretamente
with open("teste_escalao.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")

    # Cabeçalho
    writer.writerow(["ID", "Nome", "Secretaria", "Cargo", "Email", "Telefone"])
    
    # Registros de exemplo (simulando os dados do banco)
    dados = [
        [1, "Carlos Eduardo Rodrigues dos Santos", "Sect", "Administrativa", "eduardostc@hotmail.com", "(81) 9874-6549"],
        [2, "João Silva", "Financeiro", "Gerente", "joao.silva@email.com", "(81) 9234-5678"]
    ]

    for linha in dados:
        writer.writerow(linha)
        file.flush()  # 🔹 Força a gravação dos dados no arquivo

print("Arquivo CSV gerado com sucesso.")
