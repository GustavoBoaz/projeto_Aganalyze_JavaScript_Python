# 📊 Aganalyze - Dashboard de Análise de Atendimentos

Esta aplicação demonstra gráficos interativos de atendimentos por todo território brasileiro, desenvolvida com **Flask** e **Dash/Plotly** para visualização de dados de SLA e performance de atendimentos por regional e cliente.

## ✨ Funcionalidades

- 📈 **Visualização temporal**: Gráficos de fechamento mensal com filtros por mês e ano
- 🗺️ **Análise regional**: Dados segmentados por regional e cliente 
- 📊 **Gráficos polares**: Visualização de quantidade de chamados por mês
- 🎯 **Análise de SLA**: Comparação entre atendimentos dentro e fora do prazo
- 🌙 **Interface moderna**: Layout responsivo com tema dark

## 🛠️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8+** 
- **pip** (gerenciador de pacotes Python)
- **virtualenv** (para isolamento de dependências)

### Verificar versões:
```bash
python3 --version
pip --version
virtualenv --version
```

## 🚀 Instalação e Setup

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd projeto_Aganalyze_JavaScript_Python
```

### 2. Criar ambiente virtual
```bash
# Criar ambiente virtual
virtualenv env01

# Ou se preferir especificar a versão do Python:
virtualenv -p python3.8 env01
```

### 3. Ativar o ambiente virtual

**Linux/MacOS:**
```bash
source env01/bin/activate
```

**Windows:**
```bash
env01\Scripts\activate
```

> 💡 **Dica**: Você saberá que o ambiente está ativo quando ver `(env01)` no início da linha do terminal.

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar o ambiente
```bash
# Copiar arquivo de configuração de exemplo
cp instance/config.py.example instance/config.py

# Editar configurações se necessário (opcional)
nano instance/config.py
```

## ▶️ Como Executar

### Executar a aplicação:
```bash
python3 run.py
```

### Acessar a aplicação:
- **Página principal**: http://127.0.0.1:8050/
- **Dashboard**: http://127.0.0.1:8050/dashboard/

### Parar a aplicação:
Pressione `Ctrl + C` no terminal

### Desativar ambiente virtual:
```bash
deactivate
```

## 📁 Estrutura do Projeto

```
projeto_Aganalyze_JavaScript_Python/
├── analyze/                    # Módulo principal da aplicação
│   ├── __init__.py            # Factory da aplicação Flask
│   ├── dashboard.py           # Configuração dos dashboards Dash
│   ├── routes.py              # Rotas Flask
│   ├── data_csv/              # Dados CSV para os gráficos
│   ├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/             # Templates HTML
├── instance/                   # Configurações da instância
│   ├── config.py              # Configurações (não versionado)
│   └── config.py.example      # Exemplo de configuração
├── env01/                     # Ambiente virtual (não versionado)
├── requirements.txt           # Dependências Python
├── run.py                     # Arquivo principal para executar
└── README.md                  # Este arquivo
```

## 🔧 Dependências Principais

- **Flask 2.0+**: Framework web
- **Dash 2.0+**: Framework para dashboards interativos  
- **Plotly 5.0+**: Biblioteca de gráficos
- **Pandas 1.3+**: Manipulação de dados
- **Numpy 1.21+**: Computação numérica

## 🔄 Workflow de Desenvolvimento

### Para contribuir:

1. **Ativar ambiente virtual**:
   ```bash
   source env01/bin/activate
   ```

2. **Fazer suas modificações**

3. **Testar localmente**:
   ```bash
   python3 run.py
   ```

4. **Antes de commitar**:
   ```bash
   # Verificar se não há arquivos indesejados
   git status
   
   # Adicionar mudanças
   git add .
   git commit -m "Sua mensagem de commit"
   ```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
- Certifique-se de que o ambiente virtual está ativo
- Reinstale as dependências: `pip install -r requirements.txt`

### Erro: "Address already in use"
- A porta 8050 já está em uso
- Pare outros processos ou mude a porta no código

### Erro: "Permission denied"
- No Linux/MacOS, use `python3` em vez de `python`
- Verifique permissões de execução: `chmod +x run.py`

### Problemas com CSV
- Verifique se os arquivos em `analyze/data_csv/` existem
- Confirme que o formato dos dados está correto

## 📝 Notas Importantes

- ⚠️ **Sempre ative o ambiente virtual** antes de trabalhar no projeto
- 🔒 **Não commite** arquivos de configuração com dados sensíveis
- 📊 **Dados CSV** estão incluídos no repositório para demonstração
- 🌐 **Acesso externo**: Para permitir acesso de outras máquinas, modifique `run.py`

## 🤝 Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

Se tiver problemas ou dúvidas:
1. Verifique a seção **Troubleshooting** acima
2. Confirme que seguiu todos os passos de instalação
3. Abra uma issue no repositório com detalhes do erro

---

**Desenvolvido com ❤️ usando Flask + Dash + Plotly**
