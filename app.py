import csv
import os
import re
from collections import Counter

current_directory = os.path.dirname(__file__)    
csv_resultado = os.path.join(current_directory, 'dataout.csv')
csv_data = os.path.join(current_directory, 'datain.csv')
csv_exclude = os.path.join(current_directory, 'dataexclude.csv')

def read_csv(filename):
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            return [row[0] for row in csv.reader(file)]
    except FileNotFoundError:
        print(f"ERRO: O arquivo {filename} não foi encontrado.")
        return []

def write_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    # Leitura do arquivo exclude.csv
    print("Lendo arquivo de palavras excluídas...")
    exclude_words = set(read_csv(csv_exclude))

    # Leitura do arquivo data.csv
    print("Lendo arquivo de descrições...")
    descriptions = read_csv(csv_data)

    if not descriptions:
        print("Nenhuma descrição encontrada. Encerrando o script.")
        return

    # Contagem das palavras
    print("Contando as palavras nas descrições...")
    word_count = Counter()
    word_regex = re.compile(r'\b\w+\b')
    for idx, description in enumerate(descriptions, start=1):
        words = word_regex.findall(description.lower())
        word_count.update(word for word in words if word not in exclude_words)
        print(f"Progresso: {idx}/{len(descriptions)}", end='\r')

    print("\nContagem de palavras concluída.")

    # Ordenar as palavras por contagem decrescente
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # Escrita do resultado
    print("Escrevendo resultados no arquivo...")
    result_data = [['Word', 'Count']] + sorted_word_count
    write_csv(result_data, csv_resultado)
    print("Resultado escrito com sucesso!")

if __name__ == "__main__":
    main()