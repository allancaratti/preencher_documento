import streamlit as st
from docxtpl import DocxTemplate
import datetime
import os
from num2words import num2words
import pandas as pd  # Adicionado para suporte a planilhas

# Definir fonte global via CSS
st.markdown(
    """
    <style>
    * { font-family: 'PublicSans'; }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para gerar documento
def gerar_documento(modelo, contexto):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_modelo = os.path.join(base_dir, "modelos", f"{modelo}.docx")

    if not os.path.exists(caminho_modelo):
        st.error(f"Modelo não encontrado: {caminho_modelo}")
        return None

    doc = DocxTemplate(caminho_modelo)
    doc.render(contexto)

    nome_base = f"{modelo}_{contexto['nome']}_{datetime.date.today()}"
    caminho_saida = os.path.join(base_dir, "saida", f"{nome_base}.docx")

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    doc.save(caminho_saida)

    # Registrar log
    registrar_log(modelo, contexto['nome'], caminho_saida)

    return caminho_saida

# Função para registrar log
def registrar_log(modelo, nome, caminho_saida):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, "saida", "log.txt")
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.datetime.now():%d/%m/%Y %H:%M:%S} - {modelo}.docx - {nome} - {caminho_saida}\n")

# Função para formatar CPF
def formatar_cpf(cpf_num):
    cpf_limpo = ''.join(filter(str.isdigit, str(cpf_num))).zfill(11)
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

# Documentos e mapeamento
documentos = {
    "Carta de Aviso Prévio": {"campos": ["nome", "cargo", "data_ass", "data_inicio_aviso"], "arquivo": "carta_de_aviso_previo"},
    "Carta de Aviso Prévio Indenizado": {"campos": ["nome", "cargo", "data_ass", "data_fim"], "arquivo": "aviso_previo_indenizado"},
    "Carta de Notificação por Falta CLT": {"campos": ["nome", "cargo", "data_falta"], "arquivo": "carta_de_notificacao_por_falta_clt"},
    "Carta de Notificação por Falta PJ": {"campos": ["nome", "data_falta"], "arquivo": "carta_de_notificacao_por_falta_pj"},
    "Contrato PJ": {"campos": ["nome", "nacionalidade", "cargo", "rg", "cpf", "valor_diaria", "data_inicio"], "arquivo": "contrato_pj"},
    "Rescisão de Contrato PJ": {"campos": ["nome", "nacionalidade", "cargo", "rg", "cpf", "valor_diaria", "data_fim", "dias_trbalhado"], "arquivo": "recisao_pj"},
    "Recibo de Gratificação": {"campos": ["nome", "nacionalidade", "cargo", "rg", "cpf", "valor_recibo", "motivo_recibo"], "arquivo": "recibo"},
    "Acordo de Banco de Horas": {"campos": ["nome", "cpf"], "arquivo": "banco_horas"},
}

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
    "valor_diaria": "Valor da diária (R$) *",
    "valor_recibo": "Valor da gratificação (R$) *",
    "motivo_recibo": "Motivo da gratificação *",
    "data_fim": "Data de desligamento *",
    "dias_trbalhado": "Quantidade de dias trabalhados *",
    "valor_total": "Valor total da rescisão (R$)",
    "valor_total_extenso": "Valor total por extenso"
}

# Interface
col1, col2 = st.columns([1, 4])
with col1:
    st.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "image", "logo.png"), width=100)
with col2:
    st.title("Gerador de Documentos")
    st.markdown("### Tahuna Engenharia")
    st.markdown("Desenvolvido por: [Allan Mauad](https://www.linkedin.com/in/allancaratti/)")

# --- NOVO BLOCO: PROCESSAMENTO EM LOTE ---
st.sidebar.header("Configurações de Lote")
lote_ativado = st.sidebar.checkbox("Ativar preenchimento via Planilha")

if lote_ativado:
    st.subheader("📦 Gerar Banco de Horas em Lote")
    st.info("A planilha deve conter as colunas: nome, cpf, rg")
    arquivo_lote = st.file_uploader("Selecione o arquivo Excel ou CSV", type=["xlsx", "csv"])
    
    if arquivo_lote:
        try:
            df = pd.read_csv(arquivo_lote) if arquivo_lote.name.endswith('.csv') else pd.read_excel(arquivo_lote)
            st.dataframe(df.head())
            
            if st.button("🚀 Iniciar Geração em Massa"):
                cont = 0
                for _, row in df.iterrows():
                    contexto_lote = {
                        "nome": str(row["nome"]),
                        "cpf": formatar_cpf(row["cpf"]),
                        "Data_assinatura": datetime.date.today().strftime("%d/%m/%Y")
                    }
                    gerar_documento("banco_horas", contexto_lote)
                    cont += 1
                st.success(f"Finalizado! {cont} documentos de Banco de Horas gerados na pasta 'saida'.")
        except Exception as e:
            st.error(f"Erro ao processar planilha: {e}")
    st.markdown("---")
# --- FIM DO BLOCO DE LOTE ---

# Dropdown (Manual)
base_dir = os.path.dirname(os.path.abspath(__file__))
opcoes_menu = []
for nome, dados in documentos.items():
    caminho_modelo = os.path.join(base_dir, "modelos", f"{dados['arquivo']}.docx")
    if os.path.exists(caminho_modelo):
        opcoes_menu.append(f"✅ {nome}")
    else:
        opcoes_menu.append(f"❌ {nome}")

opcao_com_icone = st.selectbox("Escolha o documento para preenchimento manual:", opcoes_menu)
opcao = opcao_com_icone.replace("✅ ", "").replace("❌ ", "")
campos = documentos[opcao]["campos"]
valores = {}

st.subheader("Preencha os dados:")
for campo in campos:
    label = labels.get(campo, campo.capitalize())
    if campo in ["valor_diaria", "valor_recibo"]:
        valor = st.number_input(label, min_value=0.0, step=0.01, format="%.2f")
        if valor > 0:
            reais = int(valor)
            centavos = int(round((valor - reais) * 100))
            valores[campo] = f"R$ {valor:,.2f}".replace(".", ",")
            if centavos > 0:
                valores[f"{campo}_extenso"] = f"{num2words(reais, lang='pt_BR')} reais e {num2words(centavos, lang='pt_BR')} centavos"
            else:
                valores[f"{campo}_extenso"] = f"{num2words(reais, lang='pt_BR')} reais"
        else:
            valores[campo] = ""
            valores[f"{campo}_extenso"] = ""
    elif campo == "cpf":
        cpf_input = st.text_input(label, max_chars=11, help="Digite apenas números (11 dígitos)")
        if cpf_input.isdigit() and len(cpf_input) == 11:
            valores[campo] = formatar_cpf(cpf_input)
            st.info(f"CPF formatado: {valores[campo]}")
        else:
            valores[campo] = ""
    elif "data" in campo.lower():
        valores[campo] = st.date_input(label)
    else:
        valores[campo] = st.text_input(label)

# Regras de negócio específicas (Aviso Prévio, PJ, etc) permanecem inalteradas
if opcao == "Carta de Aviso Prévio":
    if valores["data_inicio_aviso"]:
        valores["data_fim_aviso"] = valores["data_inicio_aviso"] + datetime.timedelta(days=30)
    else:
        valores["data_fim_aviso"] = None
    escolha = st.selectbox("Escolha a alternativa de redução de jornada:", ["Redução de 2 horas diárias", "Redução de 7 dias corridos"])
    valores["opcao1"] = "X" if escolha == "Redução de 2 horas diárias" else " "
    valores["opcao2"] = "X" if escolha == "Redução de 7 dias corridos" else " "

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

if opcao == "Rescisão de Contrato PJ":
    if valores.get("valor_diaria") and valores.get("dias_trbalhado"):
        try:
            valor_diaria_num = float(str(valores["valor_diaria"]).replace("R$", "").replace(",", "."))
            dias = int(valores["dias_trbalhado"])
            total = valor_diaria_num * dias
            valores["valor_total"] = f"R$ {total:,.2f}".replace(".", ",")
            reais = int(total)
            centavos = int(round((total - reais) * 100))
            if centavos > 0:
                valores["valor_total_extenso"] = f"{num2words(reais, lang='pt_BR')} reais e {num2words(centavos, lang='pt_BR')} centavos"
            else:
                valores["valor_total_extenso"] = f"{num2words(reais, lang='pt_BR')} reais"
        except Exception as e:
            st.error(f"Erro ao calcular valor total: {e}")
            valores["valor_total"] = ""
            valores["valor_total_extenso"] = ""

# Botão de gerar (Manual)
if st.button("Gerar Documento Individual"):
    opcionais = ["alojamento", "refeicao1", "refeicao2"]
    faltando = [labels[k] for k in valores if k not in opcionais and not valores[k]]

    if not faltando:
        for k, v in valores.items():
            if isinstance(v, datetime.date):
                valores[k] = v.strftime("%d/%m/%Y")
        valores["Data_assinatura"] = datetime.date.today().strftime("%d/%m/%Y")

        arquivo_modelo = documentos[opcao]["arquivo"]
        caminho_docx = gerar_documento(arquivo_modelo, valores)
        
        if caminho_docx:
            st.success("Documento gerado com sucesso!")
            with open(caminho_docx, "rb") as f:
                st.download_button(
                    f"⬇️ Baixar {os.path.basename(caminho_docx)}",
                    f,
                    file_name=os.path.basename(caminho_docx)
                )
    else:
        st.error("Por favor, preencha todos os campos obrigatórios (marcados com *).")