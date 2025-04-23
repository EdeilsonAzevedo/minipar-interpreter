.PHONY: format lint check all

# Diretório raiz do código-fonte
SRC=.

# Formata o código com black e organiza os imports com isort
format:
	@echo "🔧 Formatando código com black e isort..."
	black $(SRC)
	isort $(SRC)

# Executa análise estática com flake8
lint:
	@echo "🔍 Rodando flake8..."
	flake8 $(SRC)

# Verifica se o código está formatado corretamente (sem modificar)
check:
	@echo "✅ Verificando formatação..."
	black --check $(SRC)
	isort --check-only $(SRC)
	flake8 $(SRC)

# Executa tudo: formatar, organizar imports e lint
all: format lint

compile:
	@python setup.py build

run-examples:
	python examples/run_examples.py