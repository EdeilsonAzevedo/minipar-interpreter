#!/usr/bin/env python3
import os
import subprocess
import sys


def clear_screen():
    """Limpa a tela do terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def find_examples():
    """Encontra todos os exemplos no diretório examples"""
    examples_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(examples_dir):
        print("Diretório de exemplos não encontrado!")
        sys.exit(1)

    examples = []
    for file in os.listdir(examples_dir):
        if file.endswith(".minipar"):
            examples.append(file)

    return sorted(examples)


def display_menu(examples):
    """Exibe o menu de exemplos"""
    clear_screen()
    print("=" * 50)
    print("INTERPRETADOR MINIPAR - EXEMPLOS DISPONÍVEIS")
    print("=" * 50)
    print()

    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")

    print()
    print("0. Sair")
    print("=" * 50)


def run_example(example_path):
    """Executa um exemplo usando o interpretador minipar"""
    try:
        print(f"\nExecutando: {example_path}\n")
        print("-" * 50)
        subprocess.run(["python", "-m", "minipar", example_path], check=True)
        print("-" * 50)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o exemplo: {e}")

    input("\nPressione Enter para continuar...")


def main():
    """Função principal do script"""
    examples = find_examples()

    if not examples:
        print("Nenhum exemplo (.minipar) encontrado no diretório 'examples'!")
        sys.exit(1)

    while True:
        display_menu(examples)

        try:
            choice = input("\nEscolha um exemplo para executar (0 para sair): ")
            if choice == "0":
                print("\nAté mais!")
                break

            example_idx = int(choice) - 1
            if 0 <= example_idx < len(examples):
                example_path = os.path.join("examples", examples[example_idx])
                run_example(example_path)
            else:
                print("\nOpção inválida!")
                input("Pressione Enter para continuar...")
        except ValueError:
            print("\nPor favor, digite um número válido!")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
