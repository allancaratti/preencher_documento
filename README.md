# 📄 Preenchedor de Documentos - Tahuna Engenharia - By: Allan Mauad - linkedin.com/in/allancaratti

Script em Python com interface gráfica em **Streamlit** para automação do preenchimento de documentação padrão da construtora.  
Permite selecionar modelos de documentos (carta de aviso prévio, carta de notificação por falta e contrato PJ), inserir dados específicos e gerar arquivos prontos para impressão e salvamento.

---

## 🚀 Funcionalidades
- Seleção de modelos de documentos pré-definidos.
- Interface gráfica amigável via **Streamlit**.
- Preenchimento automático de campos variáveis (nome, cargo, datas, CPF/CNPJ).
- Geração de arquivos `.docx` prontos para impressão.
- Download direto do documento gerado.
- Estrutura modular para adicionar novos modelos facilmente.

---

## 🧰 Requisitos
- Python 3.x  
- Bibliotecas:
  - streamlit  
  - docxtpl  
  - datetime  

---

## 📂 Estrutura do Script
1. Interface em Streamlit para seleção do tipo de documento.  
2. Exibição dinâmica dos campos necessários conforme o modelo escolhido.  
3. Preenchimento automático dos placeholders definidos nos arquivos `.docx`.  
4. Geração do documento final na pasta `saida/`.  
5. Opção de download direto pelo navegador.  

---

## ▶️ Uso
Clone o repositório:
```bash
git clone https://github.com/seu-usuario/preenchedor-documentos.git
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
Configure:
- Adicione seus modelos .docx na pasta modelos/.
- Certifique-se de que os placeholders ({{nome}}, {{cargo}}, etc.) estão definidos corretamente.
Execute:
```bash
streamlit run app.py
```
Acesse no navegador: 
```bash
http://localhost:8501
```
## 📑 Documentos Suportados
- Carta de Aviso Prévio
- Carta de Notificação por Falta
- Contrato PJ

## ⚠️ Notas
- Os modelos devem estar na pasta modelos/ com placeholders compatíveis.
- Os documentos gerados são salvos automaticamente na pasta saida/.
- É possível expandir para novos tipos de documentos adicionando entradas no dicionário de configuração.

## 👨‍💻 Autor
Desenvolvido por Allan Mauad
🔗 LinkedIn: linkedin.com/in/allancaratti 

## 📜 Licença
Este projeto está sob Licença Proprietária.
O uso, modificação ou distribuição sem autorização expressa do autor é proibido.
Veja o arquivo LICENSE.md para mais detalhes.
