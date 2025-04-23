import os
import glob
import re
import PyPDF2
import calendar

# Caminho da pasta onde estão os PDFs
nfs_directory = r""

def find_pdf_files_in_2025(directory):
    """Encontra todos os PDFs dentro de diretórios que contenham '2025' no caminho."""
    pdf_pattern = os.path.join(directory, "**", "2025", "**", "*.pdf")
    return glob.glob(pdf_pattern, recursive=True)

def extract_nfs_info(pdf_path):
    """Extrai 'Valor Líquido da NFS-e' e 'Data e Hora da emissão da DPS' de um PDF."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            if not text.strip():
                print(f"[Aviso] Sem texto extraído de: {pdf_path}")
                return None, None

            # Buscar valor
            value_patterns = [
                r"Valor\s+L[ií]quido.*?R\$[\s]*([\d.,]+)",
                r"Valor\s+da\s+Nota.*?R\$[\s]*([\d.,]+)",
                r"Valor\s+Total.*?R\$[\s]*([\d.,]+)"
            ]
            value = None
            for pattern in value_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    value = match.group(1).strip()
                    break

            # Buscar data de emissão da DPS
            emissao_match = re.search(
                r"[\s:]*[\r\n]*\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})",
                text,
                re.IGNORECASE
            )
            emissao_dps = emissao_match.group(1) if emissao_match else None

            return value, emissao_dps

    except Exception as e:
        print(f"[Erro] {pdf_path}: {str(e)}")
        return None, None

# Execução principal
if __name__ == "__main__":
    print(f"🔍 Buscando PDFs em: {nfs_directory}")

    pdf_files = find_pdf_files_in_2025(nfs_directory)

    if not pdf_files:
        print("⚠️ Nenhum PDF encontrado nas pastas de 2025.")
        exit()

    print(f"📄 {len(pdf_files)} arquivos PDF encontrados. Extraindo valores...\n")

    resultados = []
    total = 0

    for file_path in pdf_files:
        valor, emissao_dps = extract_nfs_info(file_path)
        if valor:
            nome = os.path.normpath(file_path).split(os.sep)[-3]

            # Extrair mês da emissão da DPS
            mes_emissao = ""
            if emissao_dps:
                try:
                    dia, mes, ano = emissao_dps.split()[0].split("/")
                    mes_extenso = calendar.month_name[int(mes)].capitalize()
                    mes_emissao = f"{mes_extenso}/{ano}"
                except Exception as e:
                    mes_emissao = "Mês inválido"
            else:
                mes_emissao = "Data não encontrada"

            resultados.append((nome, valor, mes_emissao))

            try:
                valor_float = float(valor.replace(".", "").replace(",", "."))
                total += valor_float
            except ValueError:
                print(f"⚠️ Erro ao converter valor '{valor}' em {nome}")

    if resultados:
        print("🧾 Valores extraídos:")
        for nome, valor, mes_emissao in resultados:
            print(f"{nome}: {mes_emissao} - R$ {valor}")
        print(f"\n💰 Valor total: R$ {total:.2f}")
    else:
        print("⚠️ Nenhum valor encontrado nos PDFs.")
