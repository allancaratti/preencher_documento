# 📄 Preenchedor de Documentos - Tahuna Engenharia - By: Allan Mauad - linkedin.com/in/allancaratti

Script em Python com interface gráfica em **Streamlit** para automação do preenchimento de documentação padrão da construtora.
Permite selecionar modelos de documentos, inserir dados específicos e gerar arquivos prontos para impressão e salvamento.


---

## 🚀 Funcionalidades
- Seleção de modelos de documentos pré-definidos.
- Interface gráfica amigável via **Streamlit**.
- Preenchimento automático de campos variáveis (nome, cargo, datas, CPF, valores).
- Geração de arquivos `.docx` prontos para impressão.
- Download direto do documento gerado.
- Estrutura modular para adicionar novos modelos facilmente.
- Formatação automática de CPF.
- Cálculo automático de valores e extenso (diária, gratificação, rescisão).
- Registro de log com histórico dos documentos gerados.
- Processamento em lote via planilha (Excel/CSV) exclusivo para o modelo Acordo de Banco de Horas.


---

## 🧰 Requisitos
- Python 3.x
- Bibliotecas:
- streamlit
- docxtpl
- datetime
- num2words
- pandas 

---

## 📂 Estrutura do Script
- Interface em Streamlit para seleção do tipo de documento.
- Exibição dinâmica dos campos necessários conforme o modelo escolhido.
- Preenchimento automático dos placeholders definidos nos arquivos `.docx`.
- Geração do documento final na pasta `saida/`.
- Opção de download direto pelo navegador.
- Registro de log em `saida/log.txt`.
- Módulo de geração em lote para Banco de Horas via planilha.


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
- Carta de Aviso Prévio Indenizado
- Carta de Notificação por Falta CLT
- Carta de Notificação por Falta PJ
- Contrato PJ
- Rescisão de Contrato PJ
- Recibo de Gratificação
- Acordo de Banco de Horas (com opção de geração em lote via planilha)

## ⚠️ Notas
- Os modelos devem estar na pasta `modelos/` com placeholders compatíveis.
- Os documentos gerados são salvos automaticamente na pasta `saida/`.
- O log de geração é salvo em `saida/log.txt`.
- O recurso de geração em lote está disponível apenas para Acordo de Banco de Horas.
- É possível expandir para novos tipos de documentos adicionando entradas no dicionário de configuração.




## 👨‍💻 Autor
Desenvolvido por Allan Mauad
🔗 LinkedIn: linkedin.com/in/allancaratti 

## 📜 Licença
Este projeto está sob Licença Proprietária.
O uso, modificação ou distribuição sem autorização expressa do autor é proibido.
Veja o arquivo LICENSE.md para mais detalhes.
