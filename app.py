import streamlit as st
from docxtpl import DocxTemplate
import datetime
import os
from num2words import num2words

# Definir fonte global via CSS
st.markdown(
    """
    <style>
    * {
        font-family: 'PublicSans';
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para gerar documento
def gerar_documento(modelo, contexto):
    doc = DocxTemplate(f"modelos/{modelo}.docx")
    doc.render(contexto)
    nome_base = f"{modelo}_{contexto['nome']}_{datetime.date.today()}"
    caminho_docx = f"saida/{nome_base}.docx"
    doc.save(caminho_docx)
    return caminho_docx

# Função para formatar CPF
def formatar_cpf(cpf_num):
    return f"{cpf_num[:3]}.{cpf_num[3:6]}.{cpf_num[6:9]}-{cpf_num[9:]}"

# Interface
col1, col2 = st.columns([1, 4])
with col1:
    st.image(os.path.join(os.path.dirname(__file__), "image", "logo.png"), width=100)
with col2:
    st.title("Gerador de Documentos")
    st.markdown("### Tahuna Enhenharia")
    st.markdown("Desenvolvido por: [Allan Mauad](https://www.linkedin.com/in/allancaratti/)")

# Documentos
documentos = {
    "Carta de Aviso Prévio": ["nome", "cargo", "data_ass", "data_inicio_aviso"],
    "Carta de Notificação por Falta CLT": ["nome", "cargo", "data_falta"],
    "Carta de Notificação por Falta PJ": ["nome", "data_falta"],
    "Contrato PJ": ["nome", "nacionalidade", "cargo", "rg", "cpf", "valor_diaria", "data_inicio"]
}

# Labels
labels = {
    "data_ass": "Data de assinatura do Contrato *",
    "data_inicio_aviso": "Data de início do aviso prévio *",
    "data_falta": "Data da falta *",
    "nome": "Nome *",
    "cargo": "Cargo *",
    "data_inicio": "Data de início do contrato *",
    "nacionalidade": "Nacionalidade *",
    "rg": "RG *",
    "cpf": "CPF *",
    "valor_diaria": "Valor da diária (R$) *"
}

opcao = st.selectbox("Escolha o documento:", list(documentos.keys()))

# Campos
campos = documentos[opcao]
valores = {}

st.subheader("Preencha os dados:")
for campo in campos:
    label = labels.get(campo, campo.capitalize())
    if campo == "valor_diaria":
        valores[campo] = st.number_input(label, min_value=0.0, step=0.01, format="%.2f")
    elif campo == "cpf":
        cpf_input = st.text_input(label, max_chars=11, help="Digite apenas números (11 dígitos)")
        if cpf_input.isdigit() and len(cpf_input) == 11:
            valores[campo] = formatar_cpf(cpf_input)  # já salva formatado
            st.info(f"CPF formatado: {valores[campo]}")
        else:
            valores[campo] = ""
    elif "data" in campo.lower():
        valores[campo] = st.date_input(label)
    else:
        valores[campo] = st.text_input(label)

# Aviso prévio
if opcao == "Carta de Aviso Prévio":
    if valores["data_inicio_aviso"]:
        valores["data_fim_aviso"] = valores["data_inicio_aviso"] + datetime.timedelta(days=30)
    else:
        valores["data_fim_aviso"] = None
    escolha = st.selectbox("Escolha a alternativa de redução de jornada:",
                           ["Redução de 2 horas diárias", "Redução de 7 dias corridos"])
    valores["opcao1"] = "X" if escolha == "Redução de 2 horas diárias" else " "
    valores["opcao2"] = "X" if escolha == "Redução de 7 dias corridos" else " "

# Contrato PJ
if opcao == "Contrato PJ":
    alojamento_check = st.checkbox("Deseja incluir alojamento?")
    if alojamento_check:
        valores["alojamento"] = "Fornecer alojamento durante o período de vigência deste Contrato."
        valores["refeicao1"] = ""
        valores["refeicao2"] = "Café da manhã, almoço e jantar"
    else:
        valores["alojamento"] = ""
        valores["refeicao1"] = "Almoço"
        valores["refeicao2"] = ""
    if valores["valor_diaria"] and valores["valor_diaria"] > 0:
        reais = int(valores["valor_diaria"])
        centavos = int(round((valores["valor_diaria"] - reais) * 100))
        valores["valor_diaria"] = f"R$ {valores['valor_diaria']:,.2f}".replace(".", ",")
        if centavos > 0:
            valores["valor_diaria_extenso"] = (
                f"{num2words(reais, lang='pt_BR')} reais e {num2words(centavos, lang='pt_BR')} centavos"
            )
        else:
            valores["valor_diaria_extenso"] = f"{num2words(reais, lang='pt_BR')} reais"
    else:
        valores["valor_diaria_extenso"] = ""

# Botão de gerar
if st.button("Gerar Documento"):
    opcionais = ["alojamento", "refeicao1", "refeicao2"]
    faltando = [labels[k] for k in valores if k not in opcionais and not valores[k]]

    if not faltando:
        for k, v in valores.items():
            if isinstance(v, datetime.date):
                valores[k] = v.strftime("%d/%m/%Y")
        valores["Data_assinatura"] = datetime.date.today().strftime("%d/%m/%Y")

        caminho_docx = gerar_documento(opcao.replace(" ", "_").lower(), valores)
        st.success("Documento gerado com sucesso!")

        with open(caminho_docx, "rb") as f:
            st.download_button("⬇️ Baixar DOCX", f, file_name=os.path.basename(caminho_docx))
    else:
        st.error("Por favor, preencha todos os campos obrigatórios (marcados com *).")
        st.warning("Campos faltando: " + ", ".join(faltando))

        # Destacar os campos faltando
        for campo in campos:
            if labels.get(campo) in faltando:
                st.markdown(
                    f"<div style='background-color:#ffcccc;padding:5px;'>⚠️ {labels[campo]} é obrigatório.</div>",
                    unsafe_allow_html=True
                )