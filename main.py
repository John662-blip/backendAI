from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
from modelGen import QwenManager16bit
from until import fetch_and_extract_file
from modelSbert import SBertVectorizer

app = Flask(__name__)
CORS(app)  


# modelgen = QwenManager16bit() # Chừng có GPU mở ra 
modelsbert = SBertVectorizer() # Chừng có GPU mở ra 




@app.route('/', methods=['GET'])
def home():
    return "Flask API is running!"


@app.route('/summary_mail_100', methods=['POST'])
def receive_json():
    data = request.get_json()
    subject = data.get("subject", "(Không có tiêu đề)")
    content = data.get("content", "")
    mailTo = data.get("mailTo", "")
    nameTo = data.get("nameTo", "")
    mailFrom = data.get("mailFrom", "")
    nameFrom = data.get("nameFrom", "")
    attach_files = data.get("attach_Files", [])
    formatted_mail = f"""
        ==========  THÔNG TIN EMAIL NHẬN ĐƯỢC ==========
        Từ       : {nameFrom} <{mailFrom}>
        Gửi đến  : {nameTo} <{mailTo}>
        Chủ đề   : {subject}
        --------------------------------------------------
         Nội dung:
        {content}
        --------------------------------------------------
         File đính kèm:
        """
    if attach_files:
        for filen in attach_files:
            extracted = fetch_and_extract_file(file.get('storagePath'))
            formatted_mail += f"  • {file.get('fileName')}\n"
            if "không trích nội dung" not in extracted and "Lỗi" not in extracted:
                formatted_mail += "     Nội dung trích xuất:\n"
                formatted_mail += "    ---------------------------------\n"
                formatted_mail += "\n"+extracted
                formatted_mail += "\n    ---------------------------------\n"
            else:
                formatted_mail += f"    ⚠ {extracted}\n"
    else:
        formatted_mail += "  • Không có file đính kèm\n"

    formatted_mail += "=================================================="
    print(formatted_mail)
    summary = ""
    # summary = modelgen.summary_mail_100(formatted_mail) # chừng có gpu mở ra 
    print(summary)

    return jsonify({"ok": True, "message": "thành công","summary":f"{summary}"}), 200


@app.route('/mail_to_vector', methods=['POST'])
def mail_to_vec():
    data = request.get_json()
    subject = data.get("subject", "(Không có tiêu đề)")
    content = data.get("content", "")
    mailTo = data.get("mailTo", "")
    nameTo = data.get("nameTo", "")
    mailFrom = data.get("mailFrom", "")
    nameFrom = data.get("nameFrom", "")
    attach_files = data.get("attach_Files", [])
    formatted_mail = f"""
        ==========  THÔNG TIN EMAIL NHẬN ĐƯỢC ==========
        Từ       : {nameFrom} <{mailFrom}>
        Từ       : {nameFrom} <{mailFrom}>
        Gửi đến  : {nameTo} <{mailTo}>
        Gửi đến  : {nameTo} <{mailTo}>
        Chủ đề   : {subject}
        Chủ đề   : {subject}
        Chủ đề   : {subject}
        Chủ đề   : {subject}
        Chủ đề   : {subject}
        Chủ đề   : {subject}
        --------------------------------------------------
         Nội dung:
        {content}
        --------------------------------------------------
         File đính kèm:
        """
    if attach_files:
        for file in attach_files:
            extracted = fetch_and_extract_file(file.get('storagePath'))
            formatted_mail += f"  • {file.get('fileName')}\n"
            if "không trích nội dung" not in extracted and "Lỗi" not in extracted:
                formatted_mail += "     Nội dung trích xuất:\n"
                formatted_mail += "    ---------------------------------\n"
                formatted_mail += "\n"+extracted
                formatted_mail += "\n    ---------------------------------\n"
            else:
                formatted_mail += f"    ⚠ {extracted}\n"
    else:
        formatted_mail += "  • Không có file đính kèm\n"

    formatted_mail += "=================================================="
    print(formatted_mail)
    vector = modelsbert.to_vector(formatted_mail)

    return jsonify({"ok": True, "message": "thành công","vector":f"{vector}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
