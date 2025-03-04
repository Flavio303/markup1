import tkinter as tk
from tkinter import ttk, messagebox
import json
from fpdf import FPDF  # Para exportar para PDF

# Variáveis globais para armazenar os valores calculados
valor_mercadoria = 0.0
valor_servico = 0.0
proporcao_custos = 0.0


# Função para formatar CPF/CNPJ
def formatar_cpf_cnpj(event):
    widget = event.widget
    text = widget.get().replace(".", "").replace("-", "").replace("/", "")
    if len(text) <= 11:  # CPF
        if len(text) > 11:
            text = text[:11]
        if len(text) >= 3:
            text = text[:3] + "." + text[3:]
        if len(text) >= 7:
            text = text[:7] + "." + text[7:]
        if len(text) >= 11:
            text = text[:11] + "-" + text[11:]
    else:  # CNPJ
        if len(text) > 14:
            text = text[:14]
        if len(text) >= 2:
            text = text[:2] + "." + text[2:]
        if len(text) >= 6:
            text = text[:6] + "." + text[6:]
        if len(text) >= 10:
            text = text[:10] + "/" + text[10:]
        if len(text) >= 15:
            text = text[:15] + "-" + text[15:]

    widget.delete(0, tk.END)
    widget.insert(0, text)


# Função para formatar CEP
def formatar_cep(event):
    widget = event.widget
    text = widget.get().replace(".", "").replace("-", "")
    if len(text) > 8:
        text = text[:8]
    if len(text) >= 2:
        text = text[:2] + "." + text[2:]
    if len(text) >= 6:
        text = text[:6] + "-" + text[6:]

    widget.delete(0, tk.END)
    widget.insert(0, text)


# Função para formatar telefone fixo
def formatar_telefone(event):
    widget = event.widget
    text = widget.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if len(text) > 10:
        text = text[:10]
    if len(text) >= 2:
        text = "(" + text[:2] + ") " + text[2:]
    if len(text) >= 8:
        text = text[:9] + "-" + text[9:]

    widget.delete(0, tk.END)
    widget.insert(0, text)


# Função para formatar celular
def formatar_celular(event):
    widget = event.widget
    text = widget.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if len(text) > 11:
        text = text[:11]
    if len(text) >= 2:
        text = "(" + text[:2] + ") " + text[2:]
    if len(text) >= 8:
        text = text[:10] + "-" + text[10:]

    widget.delete(0, tk.END)
    widget.insert(0, text)


# Função para exibir tooltips
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# Funções para a Aba de Dados Cadastrais
def salvar_dados_cadastrais():
    dados = {
        "nome_razao_social": entry_nome.get(),
        "cpf_cnpj": entry_cpf_cnpj.get(),
        "endereco": entry_endereco.get(),
        "bairro": entry_bairro.get(),
        "cep": entry_cep.get(),
        "uf": entry_uf.get(),
        "pais": entry_pais.get(),
        "telefone": entry_telefone.get(),
        "celular": entry_celular.get(),
        "responsavel": entry_responsavel.get()
    }
    with open("dados_cadastrais.json", "w") as f:
        json.dump(dados, f)
    messagebox.showinfo("Sucesso", "Dados cadastrais salvos com sucesso!")


def carregar_dados_cadastrais():
    try:
        with open("dados_cadastrais.json", "r") as f:
            dados = json.load(f)
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados["nome_razao_social"])
        entry_cpf_cnpj.delete(0, tk.END)
        entry_cpf_cnpj.insert(0, dados["cpf_cnpj"])
        entry_endereco.delete(0, tk.END)
        entry_endereco.insert(0, dados["endereco"])
        entry_bairro.delete(0, tk.END)
        entry_bairro.insert(0, dados["bairro"])
        entry_cep.delete(0, tk.END)
        entry_cep.insert(0, dados["cep"])
        entry_uf.delete(0, tk.END)
        entry_uf.insert(0, dados["uf"])
        entry_pais.delete(0, tk.END)
        entry_pais.insert(0, dados["pais"])
        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, dados["telefone"])
        entry_celular.delete(0, tk.END)
        entry_celular.insert(0, dados["celular"])
        entry_responsavel.delete(0, tk.END)
        entry_responsavel.insert(0, dados["responsavel"])
        messagebox.showinfo("Sucesso", "Dados cadastrais carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum dado salvo encontrado.")


def limpar_dados_cadastrais():
    entry_nome.delete(0, tk.END)
    entry_cpf_cnpj.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_bairro.delete(0, tk.END)
    entry_cep.delete(0, tk.END)
    entry_uf.delete(0, tk.END)
    entry_pais.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_celular.delete(0, tk.END)
    entry_responsavel.delete(0, tk.END)


# Funções para a Aba de Dados Financeiros
def atualizar_totais_e_medias(*args):
    try:
        # Coletar dados de faturamento
        faturamento = [formatar_valor(entry[1].get()) or 0.0 for entry in faturamento_entries]

        # Coletar dados de custos e despesas fixas
        custos = [formatar_valor(entry[1].get()) or 0.0 for entry in custos_entries]

        # Calcular totais e médias
        total_faturamento = sum(faturamento)
        total_custos = sum(custos)
        media_faturamento = total_faturamento / len(faturamento) if len(faturamento) > 0 else 0
        media_custos = total_custos / len(custos) if len(custos) > 0 else 0

        # Calcular proporção
        proporcao = (media_custos / media_faturamento) * 100 if media_faturamento > 0 else 0

        # Exibir resultados
        label_total_faturamento.config(text=f"Total Faturamento: R$ {total_faturamento:,.2f}")
        label_media_faturamento.config(text=f"Média Faturamento: R$ {media_faturamento:,.2f}")
        label_total_custos.config(text=f"Total Custos e Despesas Fixas: R$ {total_custos:,.2f}")
        label_media_custos.config(text=f"Média Custos e Despesas Fixas: R$ {media_custos:,.2f}")
        label_proporcao.config(text=f"Proporção: {proporcao:.2f}%")

        # Armazenar a proporção para uso nas outras abas
        global proporcao_custos
        proporcao_custos = proporcao / 100  # Convertendo para decimal
    except ValueError:
        pass  # Ignorar erros de conversão durante a digitação


def limpar_dados_financeiros():
    for entry in faturamento_entries:
        entry[1].delete(0, tk.END)
    for entry in custos_entries:
        entry[1].delete(0, tk.END)
    label_total_faturamento.config(text="Total Faturamento: R$ 0,00")
    label_media_faturamento.config(text="Média Faturamento: R$ 0,00")
    label_total_custos.config(text="Total Custos e Despesas Fixas: R$ 0,00")
    label_media_custos.config(text="Média Custos e Despesas Fixas: R$ 0,00")
    label_proporcao.config(text="Proporção: 0,00%")


def salvar_dados_financeiros():
    dados = {
        "faturamento": [entry[1].get() for entry in faturamento_entries],
        "custos": [entry[1].get() for entry in custos_entries]
    }
    with open("dados_financeiros.json", "w") as f:
        json.dump(dados, f)
    messagebox.showinfo("Sucesso", "Dados financeiros salvos com sucesso!")


def carregar_dados_financeiros():
    try:
        with open("dados_financeiros.json", "r") as f:
            dados = json.load(f)
        for i, valor in enumerate(dados["faturamento"]):
            faturamento_entries[i][1].delete(0, tk.END)
            faturamento_entries[i][1].insert(0, valor)
        for i, valor in enumerate(dados["custos"]):
            custos_entries[i][1].delete(0, tk.END)
            custos_entries[i][1].insert(0, valor)
        messagebox.showinfo("Sucesso", "Dados financeiros carregados com sucesso!")
        atualizar_totais_e_medias()  # Atualizar totais e médias após carregar
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum dado salvo encontrado.")


# Funções para a Aba de Precificação de Mercadorias
def calcular_mercadorias():
    global valor_mercadoria
    try:
        mercadoria = formatar_valor(entry_mercadoria.get())
        embalagem = formatar_valor(entry_embalagem.get())
        frete = formatar_valor(entry_frete.get())
        impostos = formatar_percentual(entry_impostos.get())
        taxa_cartoes = formatar_percentual(entry_taxa_cartoes.get())
        margem_lucro = formatar_percentual(entry_margem_lucro.get())
        desconto = formatar_percentual(entry_desconto.get())

        if None in [mercadoria, embalagem, frete, impostos, taxa_cartoes, margem_lucro, desconto]:
            raise ValueError("Valores inválidos. Verifique os campos e tente novamente.")

        # Verificar se o desconto é maior que a margem de lucro
        if desconto > margem_lucro:
            raise ValueError("O desconto não pode ser maior que a margem de lucro.")

        # Usar a proporção dos custos e despesas fixas da aba de Dados Financeiros
        global proporcao_custos
        proporcao_custos = proporcao_custos if 'proporcao_custos' in globals() else 0.0

        # Ajustar a margem de lucro com o desconto
        margem_lucro_ajustada = margem_lucro - desconto

        # Calcular o preço de venda
        preco_venda = (mercadoria + embalagem + frete) / (
                1 - (impostos + taxa_cartoes + margem_lucro_ajustada + proporcao_custos)
        )

        # Atualizar o valor global da mercadoria
        valor_mercadoria = preco_venda

        # Calcular o ponto de equilíbrio (sem margem de lucro)
        ponto_equilibrio = (mercadoria + embalagem + frete) / (
                1 - (impostos + taxa_cartoes + proporcao_custos)
        )

        # Calcular valores detalhados
        impostos_valor = preco_venda * impostos
        taxa_cartoes_valor = preco_venda * taxa_cartoes
        custos_fixas_valor = preco_venda * proporcao_custos
        margem_lucro_valor = preco_venda * margem_lucro_ajustada

        # Exibir detalhamento
        memoria_calculo_mercadorias.config(state=tk.NORMAL)
        memoria_calculo_mercadorias.delete(1.0, tk.END)
        memoria_calculo_mercadorias.insert(tk.END, "\nDetalhamento:\n\n", "titulo")
        memoria_calculo_mercadorias.insert(tk.END, f"Preço de Venda Final: R$ {preco_venda:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Custo da Mercadoria Vendida: R$ {mercadoria:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Custo com Embalagem: R$ {embalagem:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Custo com Frete e Envio: R$ {frete:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Impostos Gerais: R$ {impostos_valor:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END,
                                           f"Taxas com Cartão de Crédito ou Débito: R$ {taxa_cartoes_valor:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Custos e Despesas Fixas Gerais: R$ {custos_fixas_valor:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Margem de Lucro: R$ {margem_lucro_valor:.2f}\n")
        memoria_calculo_mercadorias.insert(tk.END, f"Ponto de Equilíbrio: R$ {ponto_equilibrio:.2f}\n")
        memoria_calculo_mercadorias.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Erro", str(e))


def limpar_mercadorias():
    entry_mercadoria.delete(0, tk.END)
    entry_embalagem.delete(0, tk.END)
    entry_frete.delete(0, tk.END)
    entry_impostos.delete(0, tk.END)
    entry_taxa_cartoes.delete(0, tk.END)
    entry_margem_lucro.delete(0, tk.END)
    entry_desconto.delete(0, tk.END)
    memoria_calculo_mercadorias.config(state=tk.NORMAL)
    memoria_calculo_mercadorias.delete(1.0, tk.END)
    memoria_calculo_mercadorias.config(state=tk.DISABLED)


def salvar_dados_mercadorias():
    dados = {
        "mercadoria": entry_mercadoria.get(),
        "embalagem": entry_embalagem.get(),
        "frete": entry_frete.get(),
        "impostos": entry_impostos.get(),
        "taxa_cartoes": entry_taxa_cartoes.get(),
        "margem_lucro": entry_margem_lucro.get(),
        "desconto": entry_desconto.get()
    }
    with open("dados_mercadorias.json", "w") as f:
        json.dump(dados, f)
    messagebox.showinfo("Sucesso", "Dados de mercadorias salvos com sucesso!")


def carregar_dados_mercadorias():
    try:
        with open("dados_mercadorias.json", "r") as f:
            dados = json.load(f)
        entry_mercadoria.delete(0, tk.END)
        entry_mercadoria.insert(0, dados["mercadoria"])
        entry_embalagem.delete(0, tk.END)
        entry_embalagem.insert(0, dados["embalagem"])
        entry_frete.delete(0, tk.END)
        entry_frete.insert(0, dados["frete"])
        entry_impostos.delete(0, tk.END)
        entry_impostos.insert(0, dados["impostos"])
        entry_taxa_cartoes.delete(0, tk.END)
        entry_taxa_cartoes.insert(0, dados["taxa_cartoes"])
        entry_margem_lucro.delete(0, tk.END)
        entry_margem_lucro.insert(0, dados["margem_lucro"])
        entry_desconto.delete(0, tk.END)
        entry_desconto.insert(0, dados["desconto"])
        messagebox.showinfo("Sucesso", "Dados de mercadorias carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum dado salvo encontrado.")


# Funções para a Aba de Precificação de Serviços
def calcular_servicos():
    global valor_servico
    try:
        dias_uteis = int(entry_dias_uteis.get() or 0)
        sabados = int(entry_sabados.get() or 0)
        horas_dia_util = converter_para_horas(entry_horas_dia_util.get() or "00:00")
        horas_sabado = converter_para_horas(entry_horas_sabado.get() or "00:00")
        impostos = formatar_percentual(entry_impostos_servicos.get() or "0")
        taxas_cartoes = formatar_percentual(entry_taxas_cartoes.get() or "0")
        lucro = formatar_percentual(entry_lucro.get() or "0")
        desconto = formatar_percentual(entry_desconto_servicos.get() or "0")
        tempo_gasto = converter_para_horas(entry_tempo_gasto.get() or "00:00")

        if None in [dias_uteis, sabados, horas_dia_util, horas_sabado, impostos, taxas_cartoes, lucro, desconto,
                    tempo_gasto]:
            raise ValueError("Valores inválidos. Verifique os campos e tente novamente.")

        # Verificar se o desconto é maior que a margem de lucro
        if desconto > lucro:
            raise ValueError("O desconto não pode ser maior que a margem de lucro.")

        # Calcular horas efetivas no mês
        horas_efetivas = calcular_horas_efetivas(dias_uteis, sabados, horas_dia_util, horas_sabado)

        # Usar o valor fixo de R$ 500,00 como proporção dos custos e despesas fixas
        proporcao_custos = 500.00  # Valor fixo conforme o exemplo hipotético

        # Calcular custo por hora
        custo_por_hora = proporcao_custos / horas_efetivas if horas_efetivas > 0 else 0

        # Calcular custo do tempo gasto
        custo_tempo_gasto = custo_por_hora * tempo_gasto

        # Ajustar a margem de lucro com o desconto
        lucro_ajustado = lucro - desconto

        # Calcular markup
        markup = 1 - (impostos + taxas_cartoes + lucro_ajustado)

        # Calcular preço final do serviço
        preco_final = custo_tempo_gasto / markup if markup > 0 else 0

        # Atualizar o valor global do serviço
        valor_servico = preco_final

        # Calcular ponto de equilíbrio (sem margem de lucro)
        ponto_equilibrio = custo_tempo_gasto / (1 - (impostos + taxas_cartoes))

        # Calcular valores detalhados
        valor_impostos = preco_final * impostos
        valor_taxas_cartoes = preco_final * taxas_cartoes
        valor_lucro = preco_final * lucro_ajustado
        valor_custos_fixos = custo_tempo_gasto

        # Exibir demonstração
        memoria_calculo_servicos.config(state=tk.NORMAL)
        memoria_calculo_servicos.delete(1.0, tk.END)
        memoria_calculo_servicos.insert(tk.END, "\nDetalhamento:\n\n", "titulo_detalhamento:")
        memoria_calculo_servicos.insert(tk.END, f"Tempo Gasto: R$ {preco_final:.2f}\n")
        memoria_calculo_servicos.insert(tk.END, f"Custos e Despesas Fixas Gerais: R$ {valor_custos_fixos:.2f}\n")
        memoria_calculo_servicos.insert(tk.END, f"Impostos Gerais: R$ {valor_impostos:.2f}\n")
        memoria_calculo_servicos.insert(tk.END, f"Taxa de Cartões de Crédito e Débito: R$ {valor_taxas_cartoes:.2f}\n")
        memoria_calculo_servicos.insert(tk.END, f"Margem de Lucro: R$ {valor_lucro:.2f}\n")
        memoria_calculo_servicos.insert(tk.END, f"Ponto de Equilíbrio: R$ {ponto_equilibrio:.2f}\n")
        memoria_calculo_servicos.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Erro", str(e))


def limpar_servicos():
    entry_dias_uteis.delete(0, tk.END)
    entry_sabados.delete(0, tk.END)
    entry_horas_dia_util.delete(0, tk.END)
    entry_horas_sabado.delete(0, tk.END)
    entry_impostos_servicos.delete(0, tk.END)
    entry_taxas_cartoes.delete(0, tk.END)
    entry_lucro.delete(0, tk.END)
    entry_desconto_servicos.delete(0, tk.END)
    entry_tempo_gasto.delete(0, tk.END)
    memoria_calculo_servicos.config(state=tk.NORMAL)
    memoria_calculo_servicos.delete(1.0, tk.END)
    memoria_calculo_servicos.config(state=tk.DISABLED)


def salvar_dados_servicos():
    dados = {
        "dias_uteis": entry_dias_uteis.get(),
        "sabados": entry_sabados.get(),
        "horas_dia_util": entry_horas_dia_util.get(),
        "horas_sabado": entry_horas_sabado.get(),
        "impostos_servicos": entry_impostos_servicos.get(),
        "taxas_cartoes": entry_taxas_cartoes.get(),
        "lucro": entry_lucro.get(),
        "desconto_servicos": entry_desconto_servicos.get(),
        "tempo_gasto": entry_tempo_gasto.get()
    }
    with open("dados_servicos.json", "w") as f:
        json.dump(dados, f)
    messagebox.showinfo("Sucesso", "Dados de serviços salvos com sucesso!")


def carregar_dados_servicos():
    try:
        with open("dados_servicos.json", "r") as f:
            dados = json.load(f)
        entry_dias_uteis.delete(0, tk.END)
        entry_dias_uteis.insert(0, dados["dias_uteis"])
        entry_sabados.delete(0, tk.END)
        entry_sabados.insert(0, dados["sabados"])
        entry_horas_dia_util.delete(0, tk.END)
        entry_horas_dia_util.insert(0, dados["horas_dia_util"])
        entry_horas_sabado.delete(0, tk.END)
        entry_horas_sabado.insert(0, dados["horas_sabado"])
        entry_impostos_servicos.delete(0, tk.END)
        entry_impostos_servicos.insert(0, dados["impostos_servicos"])
        entry_taxas_cartoes.delete(0, tk.END)
        entry_taxas_cartoes.insert(0, dados["taxas_cartoes"])
        entry_lucro.delete(0, tk.END)
        entry_lucro.insert(0, dados["lucro"])
        entry_desconto_servicos.delete(0, tk.END)
        entry_desconto_servicos.insert(0, dados["desconto_servicos"])
        entry_tempo_gasto.delete(0, tk.END)
        entry_tempo_gasto.insert(0, dados["tempo_gasto"])
        messagebox.showinfo("Sucesso", "Dados de serviços carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum dado salvo encontrado.")


# Funções para a Aba de Orçamento
def adicionar_item_orcamento():
    global valor_mercadoria, valor_servico
    tipo_item = combo_tipo_item.get()
    quantidade = entry_quantidade.get()

    if not tipo_item or not quantidade:
        messagebox.showerror("Erro", "Selecione o tipo de item e informe a quantidade.")
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número.")
        return

    # Obter o valor unitário do tipo de item selecionado
    if tipo_item == "Mercadoria":
        valor_unitario = valor_mercadoria  # Valor da aba de formação de preço
    elif tipo_item == "Serviço":
        valor_unitario = valor_servico  # Valor da aba de formação de preço
    else:
        messagebox.showerror("Erro", "Tipo de item inválido.")
        return

    valor_total = quantidade * valor_unitario
    tabela_orcamento.insert("", "end",
                            values=(tipo_item, quantidade, f"R$ {valor_unitario:.2f}", f"R$ {valor_total:.2f}"))
    calcular_total_orcamento()


def remover_item_orcamento():
    selecionado = tabela_orcamento.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Nenhum item selecionado.")
        return
    for item in selecionado:
        tabela_orcamento.delete(item)
    calcular_total_orcamento()


def calcular_total_orcamento():
    total = 0
    for item in tabela_orcamento.get_children():
        valor_total = float(tabela_orcamento.item(item, "values")[3].replace("R$ ", "").replace(",", ""))
        total += valor_total
    label_total_orcamento.config(text=f"Total: R$ {total:.2f}")


def limpar_orcamento():
    entry_nome_cliente.delete(0, tk.END)
    entry_cpf_cnpj_cliente.delete(0, tk.END)
    entry_endereco_cliente.delete(0, tk.END)
    entry_telefone_cliente.delete(0, tk.END)
    entry_email_cliente.delete(0, tk.END)
    entry_prazo_entrega.delete(0, tk.END)
    entry_condicoes_pagamento.delete(0, tk.END)
    entry_observacoes_orcamento.delete(0, tk.END)
    for item in tabela_orcamento.get_children():
        tabela_orcamento.delete(item)
    label_total_orcamento.config(text="Total: R$ 0,00")


def salvar_dados_orcamento():
    dados = {
        "nome_cliente": entry_nome_cliente.get(),
        "cpf_cnpj_cliente": entry_cpf_cnpj_cliente.get(),
        "endereco_cliente": entry_endereco_cliente.get(),
        "telefone_cliente": entry_telefone_cliente.get(),
        "email_cliente": entry_email_cliente.get(),
        "prazo_entrega": entry_prazo_entrega.get(),
        "condicoes_pagamento": entry_condicoes_pagamento.get(),
        "observacoes": entry_observacoes_orcamento.get("1.0", tk.END).strip(),
        "itens": [tabela_orcamento.item(item, "values") for item in tabela_orcamento.get_children()]
    }
    with open("dados_orcamento.json", "w") as f:
        json.dump(dados, f)
    messagebox.showinfo("Sucesso", "Dados do orçamento salvos com sucesso!")


def carregar_dados_orcamento():
    try:
        with open("dados_orcamento.json", "r") as f:
            dados = json.load(f)
        entry_nome_cliente.delete(0, tk.END)
        entry_nome_cliente.insert(0, dados["nome_cliente"])
        entry_cpf_cnpj_cliente.delete(0, tk.END)
        entry_cpf_cnpj_cliente.insert(0, dados["cpf_cnpj_cliente"])
        entry_endereco_cliente.delete(0, tk.END)
        entry_endereco_cliente.insert(0, dados["endereco_cliente"])
        entry_telefone_cliente.delete(0, tk.END)
        entry_telefone_cliente.insert(0, dados["telefone_cliente"])
        entry_email_cliente.delete(0, tk.END)
        entry_email_cliente.insert(0, dados["email_cliente"])
        entry_prazo_entrega.delete(0, tk.END)
        entry_prazo_entrega.insert(0, dados["prazo_entrega"])
        entry_condicoes_pagamento.delete(0, tk.END)
        entry_condicoes_pagamento.insert(0, dados["condicoes_pagamento"])
        entry_observacoes_orcamento.delete("1.0", tk.END)
        entry_observacoes_orcamento.insert("1.0", dados["observacoes"])
        for item in tabela_orcamento.get_children():
            tabela_orcamento.delete(item)
        for item in dados["itens"]:
            tabela_orcamento.insert("", "end", values=item)
        calcular_total_orcamento()
        messagebox.showinfo("Sucesso", "Dados do orçamento carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum dado salvo encontrado.")


# Funções auxiliares
def formatar_valor(valor):
    if not valor.strip():
        return 0.0
    try:
        valor = valor.replace('.', '').replace(',', '.')
        return float(valor)
    except ValueError:
        return None


def formatar_percentual(percentual):
    if not percentual.strip():
        return 0.0
    try:
        percentual = percentual.replace('%', '').replace(',', '.')
        return float(percentual) / 100
    except ValueError:
        return None


def converter_para_horas(tempo):
    if not tempo.strip():
        return 0.0
    try:
        horas, minutos = map(int, tempo.split(':'))
        return horas + minutos / 60
    except ValueError:
        return None


def calcular_horas_efetivas(dias_uteis, sabados, horas_dia_util, horas_sabado):
    return (dias_uteis * horas_dia_util) + (sabados * horas_sabado)


# Exportar orçamento para PDF
def exportar_orcamento_pdf():
    nome_cliente = entry_nome_cliente.get()
    cpf_cnpj_cliente = entry_cpf_cnpj_cliente.get()
    endereco_cliente = entry_endereco_cliente.get()
    telefone_cliente = entry_telefone_cliente.get()
    email_cliente = entry_email_cliente.get()
    prazo_entrega = entry_prazo_entrega.get()
    condicoes_pagamento = entry_condicoes_pagamento.get()
    observacoes = entry_observacoes_orcamento.get("1.0", tk.END).strip()

    itens = []
    for item in tabela_orcamento.get_children():
        itens.append(tabela_orcamento.item(item, "values"))

    if not nome_cliente or not itens:
        messagebox.showerror("Erro", "Cliente e itens são obrigatórios.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Cabeçalho
    pdf.cell(200, 10, txt="Orçamento", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Cliente: {nome_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"CPF/CNPJ: {cpf_cnpj_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Endereço: {endereco_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Telefone: {telefone_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"E-mail: {email_cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Prazo de Entrega: {prazo_entrega}", ln=True)
    pdf.cell(200, 10, txt=f"Condições de Pagamento: {condicoes_pagamento}", ln=True)
    pdf.cell(200, 10, txt=f"Observações: {observacoes}", ln=True)

    # Detalhes do orçamento
    pdf.ln(10)
    pdf.cell(200, 10, txt="Itens do Orçamento:", ln=True)

    total = 0
    for item in itens:
        descricao = item[0]
        quantidade = item[1]
        valor = float(item[2].replace("R$ ", "").replace(",", ""))
        subtotal = quantidade * valor
        total += subtotal

        pdf.cell(200, 10, txt=f"{descricao} - Qtd: {quantidade} - Valor: R$ {valor:.2f} - Subtotal: R$ {subtotal:.2f}",
                 ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total do Orçamento: R$ {total:.2f}", ln=True)

    # Salvar o PDF
    pdf.output("orcamento.pdf")
    messagebox.showinfo("Sucesso", "Orçamento exportado para PDF com sucesso!")


def salvar_dados_mercadorias():
    dados = {
        "mercadoria": entry_mercadoria.get(),
        "embalagem": entry_embalagem.get(),
        "frete": entry_frete.get(),
        "impostos": entry_impostos.get(),
        "taxa_cartoes": entry_taxa_cartoes.get(),
        "margem_lucro": entry_margem_lucro.get(),
        "desconto": entry_desconto.get()
    }
    with open("dados_mercadorias.json", "w") as f:
        json.dump(dados, f)
    messagebox.showinfo("Sucesso", "Dados de mercadorias salvos com sucesso!")


def carregar_dados_mercadorias():
    try:
        with open("dados_mercadorias.json", "r") as f:
            dados = json.load(f)
        entry_mercadoria.delete(0, tk.END)
        entry_mercadoria.insert(0, dados["mercadoria"])
        entry_embalagem.delete(0, tk.END)
        entry_embalagem.insert(0, dados["embalagem"])
        entry_frete.delete(0, tk.END)
        entry_frete.insert(0, dados["frete"])
        entry_impostos.delete(0, tk.END)
        entry_impostos.insert(0, dados["impostos"])
        entry_taxa_cartoes.delete(0, tk.END)
        entry_taxa_cartoes.insert(0, dados["taxa_cartoes"])
        entry_margem_lucro.delete(0, tk.END)
        entry_margem_lucro.insert(0, dados["margem_lucro"])
        entry_desconto.delete(0, tk.END)
        entry_desconto.insert(0, dados["desconto"])
        messagebox.showinfo("Sucesso", "Dados de mercadorias carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showwarning("Aviso", "Nenhum dado salvo encontrado.")


# Criar a janela principal
root = tk.Tk()
root.title(
    "Programa para Precificação de Mercadorias e Serviços - Desenvolvido por Flávio Vinicius D`Agostino - Todos os Direitos Reservados - 2025")

# Centralizar a janela
largura_janela = 1000
altura_janela = 600
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela // 2) - (largura_janela // 2)
y = (altura_tela // 2) - (altura_janela // 2)
root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Configurar estilo
style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TEntry", font=("Arial", 10), padding=5)
style.configure("TNotebook", background="#f0f0f0")
style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=5)

# Criar abas
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Aba 0: Dados Cadastrais
aba0 = ttk.Frame(notebook)
notebook.add(aba0, text="Dados Cadastrais")

frame_cadastro = ttk.Frame(aba0, padding="10")
frame_cadastro.grid(column=0, row=0, sticky="nsew")

# Lista atualizada de campos cadastrais
campos_cadastro = [
    ("Nome / Razão Social", "entry_nome"),
    ("CPF/CNPJ", "entry_cpf_cnpj"),
    ("Endereço", "entry_endereco"),
    ("Bairro", "entry_bairro"),
    ("CEP", "entry_cep"),
    ("UF", "entry_uf"),
    ("País", "entry_pais"),
    ("Telefone", "entry_telefone"),
    ("Celular", "entry_celular"),
    ("Responsável", "entry_responsavel")
]

# Criar campos e aplicar formatação
for i, (label_text, entry_name) in enumerate(campos_cadastro):
    ttk.Label(frame_cadastro, text=label_text).grid(column=0, row=i, padx=10, pady=5, sticky=tk.W)
    entry = ttk.Entry(frame_cadastro, width=40)
    entry.grid(column=1, row=i, padx=10, pady=5)
    globals()[entry_name] = entry

    # Aplicar formatação específica para cada campo
    if entry_name == "entry_cpf_cnpj":
        entry.bind("<KeyRelease>", formatar_cpf_cnpj)
    elif entry_name == "entry_cep":
        entry.bind("<KeyRelease>", formatar_cep)
    elif entry_name == "entry_telefone":
        entry.bind("<KeyRelease>", formatar_telefone)
    elif entry_name == "entry_celular":
        entry.bind("<KeyRelease>", formatar_celular)

# Botões para Dados Cadastrais
button_frame_cadastro = ttk.Frame(frame_cadastro)
button_frame_cadastro.grid(column=0, row=len(campos_cadastro), columnspan=2, pady=10)

ttk.Button(button_frame_cadastro, text="Salvar", command=salvar_dados_cadastrais).grid(column=0, row=0, padx=5)
ttk.Button(button_frame_cadastro, text="Carregar", command=carregar_dados_cadastrais).grid(column=1, row=0, padx=5)
ttk.Button(button_frame_cadastro, text="Limpar", command=limpar_dados_cadastrais).grid(column=2, row=0, padx=5)

# Aba 1: Dados Financeiros
aba1 = ttk.Frame(notebook)
notebook.add(aba1, text="Dados Financeiros")

# Frame para Faturamento
frame_faturamento = ttk.LabelFrame(aba1, text="Faturamento", padding="10")
frame_faturamento.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

# Frame para Custos e Despesas Fixas
frame_custos = ttk.LabelFrame(aba1, text="Custos e Despesas Fixas", padding="10")
frame_custos.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

# Listas para armazenar os campos de entrada
faturamento_entries = []
custos_entries = []

# Nomes dos meses
meses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

# Adicionar campos de entrada para Faturamento
for i, mes in enumerate(meses):
    mes_label = ttk.Label(frame_faturamento, text=mes)
    mes_label.grid(column=0, row=i, padx=5, pady=5)
    valor_entry = ttk.Entry(frame_faturamento, width=15)
    valor_entry.grid(column=1, row=i, padx=5, pady=5)
    valor_entry.bind("<KeyRelease>", atualizar_totais_e_medias)  # Atualizar automaticamente
    faturamento_entries.append((mes_label, valor_entry))
    ToolTip(valor_entry, "Insira o valor do faturamento bruto para o mês correspondente.")

# Adicionar campos de entrada para Custos e Despesas Fixas
for i, mes in enumerate(meses):
    mes_label = ttk.Label(frame_custos, text=mes)
    mes_label.grid(column=0, row=i, padx=5, pady=5)
    valor_entry = ttk.Entry(frame_custos, width=15)
    valor_entry.grid(column=1, row=i, padx=5, pady=5)
    valor_entry.bind("<KeyRelease>", atualizar_totais_e_medias)  # Atualizar automaticamente
    custos_entries.append((mes_label, valor_entry))
    ToolTip(valor_entry, "Insira o valor total dos custos e despesas fixas para o mês correspondente.")

# Frame para resultados
frame_resultados = ttk.Frame(aba1, padding="10")
frame_resultados.grid(column=0, row=1, columnspan=2, pady=10)

# Labels para exibir resultados
label_total_faturamento = ttk.Label(frame_resultados, text="Total Faturamento: R$ 0,00")
label_total_faturamento.grid(column=0, row=0, padx=5, pady=5)
label_media_faturamento = ttk.Label(frame_resultados, text="Média Faturamento: R$ 0,00")
label_media_faturamento.grid(column=1, row=0, padx=5, pady=5)
label_total_custos = ttk.Label(frame_resultados, text="Total Custos e Despesas Fixas: R$ 0,00")
label_total_custos.grid(column=0, row=1, padx=5, pady=5)
label_media_custos = ttk.Label(frame_resultados, text="Média Custos e Despesas Fixas: R$ 0,00")
label_media_custos.grid(column=1, row=1, padx=5, pady=5)
label_proporcao = ttk.Label(frame_resultados, text="Proporção: 0,00%")
label_proporcao.grid(column=0, row=2, columnspan=2, pady=5)

# Botões para Dados Financeiros
button_frame_financeiro = ttk.Frame(frame_resultados)
button_frame_financeiro.grid(column=0, row=3, columnspan=2, pady=5)

ttk.Button(button_frame_financeiro, text="Limpar", command=limpar_dados_financeiros).grid(column=0, row=0, padx=5)
ttk.Button(button_frame_financeiro, text="Salvar", command=salvar_dados_financeiros).grid(column=1, row=0, padx=5)
ttk.Button(button_frame_financeiro, text="Carregar", command=carregar_dados_financeiros).grid(column=2, row=0, padx=5)

# Aba 2: Precificação de Mercadorias
aba2 = ttk.Frame(notebook)
notebook.add(aba2, text="Precificação de Mercadorias")

# Frame principal para Precificação de Mercadorias
frame_mercadorias = ttk.Frame(aba2, padding="10")
frame_mercadorias.grid(column=0, row=0, sticky="nsew")

# Campos de entrada para Precificação de Mercadorias
ttk.Label(frame_mercadorias, text="Mercadoria Adquirida (R$)").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
entry_mercadoria = ttk.Entry(frame_mercadorias)
entry_mercadoria.grid(column=1, row=0, padx=10, pady=5)
ToolTip(entry_mercadoria, "Insira o valor da mercadoria adquirida, sem impostos ou taxas.")

ttk.Label(frame_mercadorias, text="Custo com Embalagem (R$)").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
entry_embalagem = ttk.Entry(frame_mercadorias)
entry_embalagem.grid(column=1, row=1, padx=10, pady=5)
ToolTip(entry_embalagem, "Insira o custo com embalagem.")

ttk.Label(frame_mercadorias, text="Custo com Frete e Envio (R$)").grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
entry_frete = ttk.Entry(frame_mercadorias)
entry_frete.grid(column=1, row=2, padx=10, pady=5)
ToolTip(entry_frete, "Insira o custo com frete e envio.")

ttk.Label(frame_mercadorias, text="Impostos Gerais (%)").grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)
entry_impostos = ttk.Entry(frame_mercadorias)
entry_impostos.grid(column=1, row=3, padx=10, pady=5)
ToolTip(entry_impostos, "Insira a porcentagem de impostos gerais.")

ttk.Label(frame_mercadorias, text="Taxa de Cartões de Crédito e Débito (%)").grid(column=0, row=4, padx=10, pady=5,
                                                                                  sticky=tk.W)
entry_taxa_cartoes = ttk.Entry(frame_mercadorias)
entry_taxa_cartoes.grid(column=1, row=4, padx=10, pady=5)
ToolTip(entry_taxa_cartoes, "Insira a porcentagem de taxas de cartões de crédito e débito.")

ttk.Label(frame_mercadorias, text="Margem de Lucro (%)").grid(column=0, row=5, padx=10, pady=5, sticky=tk.W)
entry_margem_lucro = ttk.Entry(frame_mercadorias)
entry_margem_lucro.grid(column=1, row=5, padx=10, pady=5)
ToolTip(entry_margem_lucro, "Insira a porcentagem de margem de lucro desejada.")

ttk.Label(frame_mercadorias, text="Desconto (%)").grid(column=0, row=6, padx=10, pady=5, sticky=tk.W)
entry_desconto = ttk.Entry(frame_mercadorias)
entry_desconto.grid(column=1, row=6, padx=10, pady=5)
ToolTip(entry_desconto, "Insira a porcentagem de desconto, se aplicável.")

# Botões para Precificação de Mercadorias
button_frame_mercadorias = ttk.Frame(frame_mercadorias)
button_frame_mercadorias.grid(column=0, row=7, columnspan=2, pady=10)

ttk.Button(button_frame_mercadorias, text="Calcular", command=calcular_mercadorias).grid(column=0, row=0, padx=5)
ttk.Button(button_frame_mercadorias, text="Limpar", command=limpar_mercadorias).grid(column=1, row=0, padx=5)
ttk.Button(button_frame_mercadorias, text="Salvar", command=salvar_dados_mercadorias).grid(column=2, row=0, padx=5)
ttk.Button(button_frame_mercadorias, text="Carregar", command=carregar_dados_mercadorias).grid(column=3, row=0, padx=5)

# Memória de Cálculo para Precificação de Mercadorias
memoria_calculo_mercadorias = tk.Text(frame_mercadorias, width=80, height=14, state=tk.DISABLED, font=("Courier", 10))
memoria_calculo_mercadorias.grid(column=0, row=8, columnspan=2, padx=10, pady=5)

# Aba 3: Precificação de Serviços
aba3 = ttk.Frame(notebook)
notebook.add(aba3, text="Precificação de Serviços")

# Frame principal para Precificação de Serviços
frame_servicos = ttk.Frame(aba3, padding="10")
frame_servicos.grid(column=0, row=0, sticky="nsew")

# Campos de entrada para Precificação de Serviços
ttk.Label(frame_servicos, text="Dias Úteis no Mês").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
entry_dias_uteis = ttk.Entry(frame_servicos)
entry_dias_uteis.grid(column=1, row=0, padx=10, pady=5)
ToolTip(entry_dias_uteis, "Insira o número de dias úteis no mês.")

ttk.Label(frame_servicos, text="Sábados no Mês").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
entry_sabados = ttk.Entry(frame_servicos)
entry_sabados.grid(column=1, row=1, padx=10, pady=5)
ToolTip(entry_sabados, "Insira o número de sábados no mês.")

ttk.Label(frame_servicos, text="Horas por Dia Útil (HH:MM)").grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
entry_horas_dia_util = ttk.Entry(frame_servicos)
entry_horas_dia_util.grid(column=1, row=2, padx=10, pady=5)
ToolTip(entry_horas_dia_util, "Insira as horas trabalhadas por dia útil no formato HH:MM.")

ttk.Label(frame_servicos, text="Horas por Sábado (HH:MM)").grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)
entry_horas_sabado = ttk.Entry(frame_servicos)
entry_horas_sabado.grid(column=1, row=3, padx=10, pady=5)
ToolTip(entry_horas_sabado, "Insira as horas trabalhadas por sábado no formato HH:MM.")

ttk.Label(frame_servicos, text="Impostos Gerais (%)").grid(column=0, row=4, padx=10, pady=5, sticky=tk.W)
entry_impostos_servicos = ttk.Entry(frame_servicos)
entry_impostos_servicos.grid(column=1, row=4, padx=10, pady=5)
ToolTip(entry_impostos_servicos, "Insira a porcentagem de impostos gerais.")

ttk.Label(frame_servicos, text="Taxa de Cartões de Crédito e Débito (%)").grid(column=0, row=5, padx=10, pady=5,
                                                                               sticky=tk.W)
entry_taxas_cartoes = ttk.Entry(frame_servicos)
entry_taxas_cartoes.grid(column=1, row=5, padx=10, pady=5)
ToolTip(entry_taxas_cartoes, "Insira a porcentagem de taxas de cartões de crédito e débito.")

ttk.Label(frame_servicos, text="Margem de Lucro (%)").grid(column=0, row=6, padx=10, pady=5, sticky=tk.W)
entry_lucro = ttk.Entry(frame_servicos)
entry_lucro.grid(column=1, row=6, padx=10, pady=5)
ToolTip(entry_lucro, "Insira a porcentagem de margem de lucro desejada.")

ttk.Label(frame_servicos, text="Desconto (%)").grid(column=0, row=7, padx=10, pady=5, sticky=tk.W)
entry_desconto_servicos = ttk.Entry(frame_servicos)
entry_desconto_servicos.grid(column=1, row=7, padx=10, pady=5)
ToolTip(entry_desconto_servicos, "Insira a porcentagem de desconto, se aplicável.")

ttk.Label(frame_servicos, text="Tempo Gasto no Serviço (HH:MM)").grid(column=0, row=8, padx=10, pady=5, sticky=tk.W)
entry_tempo_gasto = ttk.Entry(frame_servicos)
entry_tempo_gasto.grid(column=1, row=8, padx=10, pady=5)
ToolTip(entry_tempo_gasto, "Insira o tempo gasto no serviço no formato HH:MM.")

# Botões para Precificação de Serviços
button_frame_servicos = ttk.Frame(frame_servicos)
button_frame_servicos.grid(column=0, row=9, columnspan=2, pady=10)

ttk.Button(button_frame_servicos, text="Calcular", command=calcular_servicos).grid(column=0, row=0, padx=5)
ttk.Button(button_frame_servicos, text="Limpar", command=limpar_servicos).grid(column=1, row=0, padx=5)
ttk.Button(button_frame_servicos, text="Salvar", command=salvar_dados_servicos).grid(column=2, row=0, padx=5)
ttk.Button(button_frame_servicos, text="Carregar", command=carregar_dados_servicos).grid(column=3, row=0, padx=5)

# Memória de Cálculo para Precificação de Serviços
memoria_calculo_servicos = tk.Text(frame_servicos, width=80, height=14, state=tk.DISABLED, font=("Courier", 10))
memoria_calculo_servicos.grid(column=0, row=10, columnspan=2, padx=10, pady=5)

# Aba 4: Orçamento
aba4 = ttk.Frame(notebook)
notebook.add(aba4, text="Orçamento")

# Frame principal para Orçamento
frame_orcamento = ttk.Frame(aba4, padding="10")
frame_orcamento.grid(column=0, row=0, sticky="nsew")

# Dividir a tela em duas colunas
coluna_esquerda = ttk.Frame(frame_orcamento)
coluna_esquerda.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

coluna_direita = ttk.Frame(frame_orcamento)
coluna_direita.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

# Dados do Cliente (Coluna Esquerda)
campos_cliente = [
    ("Nome do Cliente", "entry_nome_cliente"),
    ("CPF/CNPJ", "entry_cpf_cnpj_cliente"),
    ("Endereço", "entry_endereco_cliente"),
    ("Telefone", "entry_telefone_cliente"),
    ("E-mail", "entry_email_cliente"),
    ("Prazo de Entrega", "entry_prazo_entrega"),
    ("Condições de Pagamento", "entry_condicoes_pagamento"),
    ("Observações", "entry_observacoes_orcamento")
]

for i, (label_text, entry_name) in enumerate(campos_cliente):
    ttk.Label(coluna_esquerda, text=label_text).grid(column=0, row=i, padx=10, pady=5, sticky=tk.W)
    if label_text == "Observações":
        entry = tk.Text(coluna_esquerda, width=30, height=4)
    else:
        entry = ttk.Entry(coluna_esquerda, width=30)
    entry.grid(column=1, row=i, padx=10, pady=5)
    globals()[entry_name] = entry

# Seleção de Itens (Coluna Direita)
ttk.Label(coluna_direita, text="Tipo de Item").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
combo_tipo_item = ttk.Combobox(coluna_direita, width=27, values=["Mercadoria", "Serviço"])
combo_tipo_item.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(coluna_direita, text="Quantidade").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
entry_quantidade = ttk.Entry(coluna_direita, width=30)
entry_quantidade.grid(column=1, row=1, padx=10, pady=5)

# Botões para adicionar/remover itens
button_frame_itens = ttk.Frame(coluna_direita)
button_frame_itens.grid(column=0, row=2, columnspan=2, pady=10)

ttk.Button(button_frame_itens, text="Adicionar Item", command=adicionar_item_orcamento).grid(column=0, row=0, padx=5)
ttk.Button(button_frame_itens, text="Remover Item", command=remover_item_orcamento).grid(column=1, row=0, padx=5)

# Tabela de itens do orçamento
colunas = ("Tipo", "Quantidade", "Valor Unitário", "Valor Total")
tabela_orcamento = ttk.Treeview(coluna_direita, columns=colunas, show="headings", height=10)
for col in colunas:
    tabela_orcamento.heading(col, text=col)
tabela_orcamento.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

# Total do orçamento
label_total_orcamento = ttk.Label(coluna_direita, text="Total: R$ 0,00", font=("Arial", 12, "bold"))
label_total_orcamento.grid(column=0, row=4, columnspan=2, pady=10)

# Botões para Orçamento
button_frame_orcamento = ttk.Frame(coluna_direita)
button_frame_orcamento.grid(column=0, row=5, columnspan=2, pady=10)

ttk.Button(button_frame_orcamento, text="Salvar", command=salvar_dados_orcamento).grid(column=0, row=0, padx=5)
ttk.Button(button_frame_orcamento, text="Carregar", command=carregar_dados_orcamento).grid(column=1, row=0, padx=5)
ttk.Button(button_frame_orcamento, text="Limpar", command=limpar_orcamento).grid(column=2, row=0, padx=5)
ttk.Button(button_frame_orcamento, text="Exportar PDF", command=exportar_orcamento_pdf).grid(column=3, row=0, padx=5)

# Iniciar o loop principal da interface gráfica
root.mainloop()

