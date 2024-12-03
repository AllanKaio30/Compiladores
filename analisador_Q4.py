import pandas as pd

# Carregar a tabela LL(1) exportada (tabela_ll1.xlsx)
table_path = "tabela_ll1.xlsx"  # Caminho do arquivo Excel gerado na Questão 3
table_df = pd.read_excel(table_path)

# Converter a tabela em um formato de dicionário para facilitar o acesso
ll1_table = {}

# Preencher o dicionário com as produções a partir da tabela
for row in range(len(table_df)):
    non_terminal = table_df["Não Terminal"][row]
    ll1_table[non_terminal] = {}
    for col in table_df.columns[1:]:
        production = table_df[col][row]
        if production:
            ll1_table[non_terminal][col] = production

# Exibir a tabela LL(1) carregada
print("Tabela LL(1) carregada:")
print(ll1_table)

# Definir o analisador descendente recursivo
class RecursiveParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0  # Aponta para o símbolo atual da entrada
        self.table = ll1_table

    def match(self, expected):
        """Verifica se o próximo token é o esperado"""
        if self.index < len(self.tokens) and self.tokens[self.index] == expected:
            self.index += 1  # Avança para o próximo token
            return True
        return False

    def parse(self):
        """Função inicial, correspondente ao símbolo inicial da gramática"""
        return self.S() and self.index == len(self.tokens)  # Cadeia válida se tudo foi consumido

    def error(self):
        """Se encontrar erro, lança uma exceção"""
        raise ValueError(f"Erro de sintaxe no token {self.tokens[self.index]} na posição {self.index}")

    # Função para a produção S → v [ A ]
    def S(self):
        if self.match("v"):  # S → v [ A ]
            if self.match("["):
                if self.A():
                    if self.match("]"):
                        return True
        self.error()  # Se algo deu errado

    # Função para a produção A → p | n | s | v | A : A
    def A(self):
        current_token = self.tokens[self.index]
        if current_token in self.table["A"]:
            production = self.table["A"][current_token]
            
            # Verifica as produções de A
            if production == "A → p":
                self.match("p")
                return True
            elif production == "A → n":
                self.match("n")
                return True
            elif production == "A → s":
                self.match("s")
                return True
            elif production == "A → v":
                self.match("v")
                return True
            elif production == "A → A : A":
                if self.A():
                    if self.match(":"):
                        return self.A()
            elif production == "A → ε":  # A → ε (não consome nenhum token)
                return True
        self.error()

# Testando com as cadeias fornecidas
tokens1 = ["v", "[", "v", "[", "p", ":", "p", "]", "]"]
tokens2 = ["v", "[", "p", ":", "s", "]"]

parser1 = RecursiveParser(tokens1)
parser2 = RecursiveParser(tokens2)

# Resultado
print("Tokens 1:", "Aceito" if parser1.parse() else "Rejeitado")
print("Tokens 2:", "Aceito" if parser2.parse() else "Rejeitado")
