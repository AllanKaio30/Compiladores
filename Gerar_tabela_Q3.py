import pandas as pd
import matplotlib.pyplot as plt

# Dados da tabela
data = {
    "Não Terminal": ["S", "A", "A", "A", "A", "A"],
    "v": ["S → v [ A ]", "A → v", "", "", "", ""],
    "[": ["", "", "", "", "", ""],
    "p": ["", "A → p", "", "", "", ""],
    "n": ["", "", "A → n", "", "", ""],
    "s": ["", "", "", "A → s", "", ""],
    ":": ["", "", "", "", "A → A : A", ""],
    "]": ["", "", "", "", "", "ε"],
    "$": ["", "", "", "", "", ""],
}

# Criar DataFrame
table = pd.DataFrame(data)

# Função para verificar conflitos na tabela LL(1)
def check_ll1_table(table):
    # Dicionário para armazenar os conflitos
    conflicts = []
    
    # Iterar pelas células da tabela (excluindo a coluna "Não Terminal")
    for i in range(len(table)):
        for j in range(1, len(table.columns)):
            non_terminal = table.iloc[i]["Não Terminal"]
            terminal = table.columns[j]
            production = table.iloc[i][terminal]
            
            if production:  # Verifica se há produção nesta célula
                # Verifica se já existe uma produção para o mesmo par (não terminal, terminal)
                if (non_terminal, terminal) in conflicts:
                    print(f"Conflito encontrado: {non_terminal} para {terminal}")
                    return False
                # Marca o par (não terminal, terminal) como já processado
                conflicts.append((non_terminal, terminal))
    
    return True  # Se não houver conflitos

# Verificar se a tabela é LL(1)
is_ll1 = check_ll1_table(table)
if is_ll1:
    print("A tabela é LL(1).")
else:
    print("A tabela não é LL(1).")

# Exportar para Excel
excel_path = "tabela_ll1.xlsx"
table.to_excel(excel_path, index=False)
print(f"Tabela exportada para Excel: {excel_path}")

# Criar tabela usando matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=table.values, colLabels=table.columns, loc='center')

# Exportar para PDF
pdf_path = "tabela_ll1.pdf"
plt.savefig(pdf_path, bbox_inches='tight')
print(f"Tabela exportada para PDF: {pdf_path}")
