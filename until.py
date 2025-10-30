import requests
from convertMarkdown import MarkItDownManager
md = MarkItDownManager()
BASE_URL = "http://localhost:8080/public/"
def fetch_and_extract_file(filename):
    url = BASE_URL + filename
    try:
        response = requests.get(url)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if any(filename.endswith(ext) for ext in [".pdf", ".pptx", ".docx",".txt",".html",".md"]):
            print(f"📄 Đang trích nội dung từ file: {filename}")
            result = md.convert_file(url)  
            return result
        else:
            return f"📎 File đính kèm: {filename} (không trích nội dung được)"

    except Exception as e:
        return f"❌ Lỗi khi đọc file {filename}: {e}"