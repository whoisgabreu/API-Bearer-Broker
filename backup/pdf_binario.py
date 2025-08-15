from flask import Flask, request, jsonify
import os
import uuid
import base64
import subprocess
import platform

# Apenas importa docx2pdf se for Windows
if platform.system() == "Windows":
    from docx2pdf import convert as convert_docx2pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert/docx', methods=['POST'])
def convert_docx_base64_to_pdf():
    data = request.get_json()

    if not data or 'file_base64' not in data:
        return jsonify({"error": "Campo 'file_base64' não encontrado"}), 400

    try:
        file_data = base64.b64decode(data['file_base64'])
    except Exception as e:
        return jsonify({"error": "Base64 inválido", "details": str(e)}), 400

    docx_filename = f"{uuid.uuid4()}.docx"
    pdf_filename = docx_filename.replace(".docx", ".pdf")
    input_path = os.path.join(UPLOAD_FOLDER, docx_filename)
    output_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    try:
        # Salva o arquivo .docx
        with open(input_path, "wb") as f:
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
            pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

        return jsonify({"pdf_base64": pdf_b64})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Falha na conversão com LibreOffice", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Erro geral", "details": str(e)}), 500

    finally:
        # Limpa arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True)
