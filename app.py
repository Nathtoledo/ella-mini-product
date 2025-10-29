import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from db import (
    init_db,
    criar_cliente,
    salvar_documento,
    listar_clientes_pendentes,
    get_cliente,
    listar_documentos_cliente,
    atualizar_status_cliente,
)
from email_utils import enviar_email


# carregar variáveis de ambiente (.env)
load_dotenv()
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", os.getenv("ADMIN_PASSWORD"))
SENDER_EMAIL = st.secrets.get("SENDER_EMAIL", os.getenv("SENDER_EMAIL"))
SENDER_EMAIL_APP_PASSWORD = st.secrets.get("SENDER_EMAIL_APP_PASSWORD", os.getenv("SENDER_EMAIL_APP_PASSWORD"))

# garantir que o banco/tabelas existem
init_db()

st.set_page_config(page_title="Onboarding de Cliente", page_icon="🧾")


#FRONT =============
# ================================
# THEME / BRANDING ELLA
# ================================

E_NEGRO = "#0F2A25"     # texto verde-escuro elegante
E_BG_PAGE = "#002F2A"   # fundo geral verde petróleo
E_BG_CARD = "#F8F6F1"   # fundo dos cards/bege claro
E_BORDER = "#0F2A25"    # borda sutil
E_ACCENT = "#F8F6F1"    # cor clara usada em botões de contorno

# injetar CSS custom
st.markdown(
    f"""
    <style>
    /* importar fontes elegantes do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Playfair+Display:wght@500;600&display=swap');

    /* ======== página inteira ======== */
    .main {{
        background-color: {E_BG_PAGE} !important;
    }}
    body {{
        background-color: {E_BG_PAGE} !important;
    }}

    /* ======== sidebar ======== */
    section[data-testid="stSidebar"] > div {{
        background-color: {E_BG_PAGE} !important;
        border-right: 1px solid rgba(248,246,241,0.18);
    }}
    section[data-testid="stSidebar"] * {{
        color: {E_BG_CARD} !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 16px;
    }}

    /* labels dos inputs, textos normais */
    label, .stMarkdown p, .stMarkdown li, .stTextInput label, .stFileUploader label {{
        color: {E_NEGRO} !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 18px !important;
        line-height: 1.4em !important;
        letter-spacing: 0.02em !important;
    }}

    /* título principal de cada página */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: {E_NEGRO} !important;
        font-family: "Playfair Display", "Cormorant Garamond", serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        line-height: 1.2em !important;
    }}
    h1 {{
        font-size: 40px !important;
    }}
    h2 {{
        font-size: 30px !important;
    }}
    h3 {{
        font-size: 24px !important;
    }}

    /* caixinhas estilo card */
    .ella-card {{
        background-color: {E_NEGRO};
        color: {E_NEGRO};
        border: 1px solid {E_BORDER};
        border-radius: 2px;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        font-family: "Cormorant Garamond", serif !important;
        max-width: 640px;
        margin-bottom: 1rem;
    }}
    .ella-card-title {{
        font-family: "Playfair Display", serif !important;
        font-size: 28px;
        color: {E_NEGRO};
        border-bottom: 1px solid {E_BORDER};
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 500;
        text-align: center;
        letter-spacing: 0.02em;
        line-height: 1.25em;
    }}
    .ella-card-text {{
        font-size: 20px;
        line-height: 1.5em;
        text-align: justify;
        color: {E_NEGRO};
        letter-spacing: 0.02em;
    }}

    /* inputs */
    input[type="text"], input[type="email"], textarea, div[data-baseweb="input"] > input {{
        background-color: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(248,246,241,0.4) !important;
        color: {E_NEGRO} !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 18px !important;
    }}
    input::placeholder {{
        color: rgba(248,246,241,0.5) !important;
    }}

    /* uploader */
    div[data-testid="stFileUploader"] > div {{
        background-color: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(248,246,241,0.4) !important;
        color: {E_NEGRO} !important;
        font-family: "Cormorant Garamond", serif !important;
    }}
    div[data-testid="stFileUploader"] * {{
        color: {E_NEGRO} !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 16px !important;
    }}

    /* botões */
    .stButton button {{
        background-color: transparent !important;
        border-radius: 4px !important;
        border: 1px solid {E_NEGRO} !important;
        color: {E_NEGRO} !important;
        font-family: "Playfair Display", serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        padding: 0.6rem 1.1rem !important;
    }}
    .stButton button:hover {{
        background-color: rgba(248,246,241,0.08) !important;
        border-color: {E_ACCENT} !important;
        color: {E_NEGRO} !important;
    }}

    /* mensagens de status (success / info / warning) */
    div.stAlert {{
        border-radius: 2px !important;
        border: 1px solid {E_BORDER} !important;
        font-family: "Cormorant Garamond", serif !important;
        font-size: 18px !important;
        letter-spacing: 0.02em !important;
    }}
    div.stAlert > div[role="alert"] {{
        color: {E_NEGRO} !important;
    }}
    div.stAlert[data-baseweb="notification"] {{
        background-color: {E_NEGRO} !important;
    }}

    /* ======== selectbox (filtro) ======== */
    div[data-baseweb="select"] > div {{
        background-color: white !important;
        border: 1px solid rgba(248,246,241,0.4) !important;
        color: {E_NEGRO} !important;  /* cor do texto do campo */
        font-family: "Cormorant Garamond", serif !important;
        font-size: 18px !important;
    }}

    div[data-baseweb="select"] * {{
        color: {E_NEGRO} !important; /* cor do texto das opções */
        font-family: "Cormorant Garamond", serif !important;
        font-size: 18px !important;
    }}

    ul[role="listbox"] li {{
        color: {E_NEGRO} !important; /* texto das opções */
        background-color: {E_BG_CARD} !important; /* fundo da listinha */
    }}

    ul[role="listbox"] li:hover {{
        background-color: rgba(0,47,42,0.08) !important; /* leve destaque ao passar o mouse */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar para escolher modo
modo = st.sidebar.selectbox("Escolha o modo", ["Cliente", "Admin"])

if modo == "Cliente":
    st.title("Cadastro de Cliente")

    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo")
        cpf = st.text_input("CPF")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")

        st.markdown("**Envio de Documentos**")
        rg_file = st.file_uploader("RG (frente ou PDF)", type=["pdf", "png", "jpg", "jpeg"])
        cnh_file = st.file_uploader("CNH", type=["pdf", "png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Enviar cadastro")

    if submitted:
        if not nome or not cpf or not email:
            st.error("Por favor, preencha pelo menos Nome, CPF e E-mail.")
        else:
            # 1. criar cliente no banco
            id_cliente = criar_cliente(nome, cpf, email, telefone)

            # 2. criar pasta uploads/<cliente_id>
            pasta_cliente = os.path.join("uploads", f"cliente_{id_cliente}")
            os.makedirs(pasta_cliente, exist_ok=True)

            def salvar_arquivo_local(file_obj, tipo_documento):
                if file_obj is None:
                    return
                timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
                nome_interno = f"{timestamp}_{tipo_documento}_{file_obj.name}"
                caminho_final = os.path.join(pasta_cliente, nome_interno)

                # salvar fisicamente o arquivo
                with open(caminho_final, "wb") as f:
                    f.write(file_obj.getvalue())

                # registrar no banco
                salvar_documento(
                    id_cliente=id_cliente,
                    tipo_documento=tipo_documento,
                    caminho_arquivo=caminho_final,
                )

            salvar_arquivo_local(rg_file, "RG")
            salvar_arquivo_local(cnh_file, "CNH")

            st.success(f"Cadastro enviado com sucesso! Seu protocolo interno é #{id_cliente}")
            st.info("Nossa equipe vai analisar seus documentos e você receberá um e-mail com o resultado.")

elif modo == "Admin":
    st.title("Painel Interno / Compliance 🔐")

    senha = st.text_input("Senha de acesso interno", type="password")

    if senha != ADMIN_PASSWORD:
        st.warning("Insira a senha correta para visualizar os cadastros pendentes.")
        st.stop()

    st.success("Acesso liberado ✅")

    # Listar clientes pendentes
    pendentes = listar_clientes_pendentes()
    if not pendentes:
        st.info("Nenhum cliente pendente no momento.")
    else:
        st.subheader("Clientes pendentes de análise")
        # montar um select pra escolher quem analisar
        opcoes = {f"#{c['id_cliente']} - {c['nome']} ({c['cpf']})": c["id_cliente"] for c in pendentes}
        escolha_label = st.selectbox("Selecione um cliente", list(opcoes.keys()))
        id_escolhido = opcoes[escolha_label]

        dados_cliente = get_cliente(id_escolhido)
        docs_cliente = listar_documentos_cliente(id_escolhido)

        st.markdown("### Dados do cliente")
        st.write({
            "id_cliente": dados_cliente["id_cliente"],
            "nome": dados_cliente["nome"],
            "cpf": dados_cliente["cpf"],
            "email": dados_cliente["email"],
            "telefone": dados_cliente["telefone"],
            "status": dados_cliente["status"],
            "criado_em": dados_cliente["created_at"],
        })

        st.markdown("### Documentos enviados")
        for doc in docs_cliente:
            st.write(f"- {doc['tipo_documento']} ({doc['uploaded_at']})")
            caminho = doc["caminho_arquivo"]

            # botão de download do arquivo
            try:
                with open(caminho, "rb") as f:
                    st.download_button(
                        label=f"Baixar {doc['tipo_documento']}",
                        data=f,
                        file_name=os.path.basename(caminho),
                        mime=None,
                        key=f"download_{doc['id_documento']}",
                    )
            except FileNotFoundError:
                st.error(f"Arquivo não encontrado: {caminho}")

        st.markdown("### Decisão de Compliance")

        novo_status = st.selectbox(
            "Resultado da análise",
            ["APROVADO", "REPROVADO"]
        )

        comentario_interno = st.text_area(
            "Comentário interno (visível SOMENTE para nossa equipe, pode ir no e-mail do reprovado)",
            ""
        )

        if st.button("Finalizar análise e notificar cliente"):
            # atualizar status no banco
            atualizar_status_cliente(
                id_cliente=id_escolhido,
                novo_status=novo_status,
                comentario_interno=comentario_interno
            )

            # mandar e-mail pro cliente
            enviar_email(
                destinatario=dados_cliente["email"],
                status=novo_status,
                comentario=comentario_interno
            )

            st.success("Status atualizado e e-mail enviado ✅")