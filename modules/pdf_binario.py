# modules/pdf_binario.py
import os
import uuid
import base64
import subprocess
import platform

# Apenas importa docx2pdf se for Windows
if platform.system() == "Windows":
    from docx2pdf import convert as convert_docx2pdf

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_docx_base64_to_pdf(file_base64: str) -> str:
    """
    Converte um arquivo DOCX (base64) para PDF (base64).
    Retorna o PDF codificado em base64.
    """
    try:
        file_data = base64.b64decode(file_base64)
    except Exception as e:
        raise ValueError(f"Base64 inválido: {e}")

    docx_filename = f"{uuid.uuid4()}.docx"
    pdf_filename = docx_filename.replace(".docx", ".pdf")
    input_path = os.path.join(UPLOAD_FOLDER, docx_filename)
    output_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    try:
        # Salva o arquivo .docx
        with open(input_path, "wb") as f:
            print("Salvando arquivo DOCX linha 33")
            f.write(file_data)

        system_type = platform.system()

        if system_type == "Windows":
            # Usa docx2pdf no Windows
            convert_docx2pdf(input_path, UPLOAD_FOLDER)
        else:
            # Usa libreoffice no Linux/macOS
            subprocess.run([
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                input_path,
                "--outdir", UPLOAD_FOLDER
            ], check=True)

        # Lê o PDF e retorna como base64
        with open(output_path, "rb") as f:
            print("Lendo arquivo PDF linha 53")

            pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

        return pdf_b64

    finally:
        # Limpa arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
