from markitdown import MarkItDown

class MarkItDownManager:
    def __init__(self, enable_plugins=False):
        """
        Khởi tạo MarkItDown
        :param enable_plugins: Bật/tắt plugin khi convert
        """
        self.md = MarkItDown(enable_plugins=enable_plugins)

    def convert_file(self, file_path):
        """
        Chuyển file (Excel, PDF, Word, ...) sang text
        :param file_path: đường dẫn file
        :return: text nội dung của file
        """
        result = self.md.convert(file_path)
        return result.text_content