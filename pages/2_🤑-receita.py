import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Home",
    page_icon="✅",
    layout="wide"
    )

# Função para adicionar uma nova receita
def add_category(df, category, description, value):
    # Verifica se a categoria já existe
    if category in df['Categoria'].values:
        st.error(f"A categoria '{category}' já existe.")
    # Verifica se a categoria é vazia
    elif category.strip() == "":
        st.error("O nome da categoria não pode estar vazio.")
    # Caso seja uma nova categoria válida
    else:
        # Cria uma nova linha
        new_row = pd.DataFrame({'Valor': [value], 'Categoria': [category], 'Descrição': [description]})
        # Adiciona a nova linha ao DataFrame existente sem remover as outras
        df = pd.concat([df, new_row], ignore_index=True)
        st.success(f"Categoria '{category}' adicionada com sucesso!")
    return df

# Função para remover categoria
def remove_category(df, category):
    # Remove a categoria escolhida do DataFrame
    df = df[df['Categoria'] != category]
    return df

# Função para carregar os dados do CSV
def load_data(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        # Retorna um DataFrame vazio se o arquivo não for encontrado
        return pd.DataFrame(columns=['Valor', 'Categoria', 'Descrição'])

# Função para salvar no CSV sobrescrevendo o conteúdo
def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Carregar os dados existentes
df_receitas = load_data('df_receitas.csv')

# Interface para adicionar nova receita
# st.subheader('Adicionar Nova Categoria de receita')
st.markdown("<h3 style='color: green;'>Adicionar Nova Categoria de receita</h3>", unsafe_allow_html=True)

with st.form(key='add_expense_form'):
    new_expense_category = st.text_input('Nome da Categoria de receita')
    new_expense_description = st.text_input('Descrição da receita')
    new_expense_value = st.number_input('Valor da receita', min_value=0.0, format='%f')
    submit_expense_button = st.form_submit_button('Adicionar Categoria de receita')

    if submit_expense_button:
        df_receitas = add_category(df_receitas, new_expense_category, new_expense_description, new_expense_value)
        save_to_csv(df_receitas, 'df_receitas.csv')  # Salva todas as receitas, inclusive a nova

# Interface para remover categoria de receita
# st.subheader('Remover Categoria de Receita')
st.markdown("<h3 style='color: red;'>Remover Categoria de Receita</h3>", unsafe_allow_html=True)

if not df_receitas.empty:
    remove_expense_category_select = st.selectbox('Selecione a Categoria para Remover', df_receitas['Categoria'].unique())
    if st.button('Remover Categoria de Receita'):
        df_receitas = remove_category(df_receitas, remove_expense_category_select)
        save_to_csv(df_receitas, 'df_receitas.csv')  # Salva as alterações no CSV
        st.success(f"Categoria '{remove_expense_category_select}' removida com sucesso!")
else:
    st.write("Nenhuma receita disponível para remover.")

