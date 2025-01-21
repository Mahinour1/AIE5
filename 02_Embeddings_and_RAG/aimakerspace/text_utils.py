import os
from typing import List
from pypdf import PdfReader


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.endswith(".txt"):
                self.load_file()
            elif self.path.endswith(".pdf"):
                self.load_pdf()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a supported file type."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_pdf(self):
        """Extract text from PDF file."""
        reader = PdfReader(self.path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        self.documents.append(text.strip())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith((".txt", ".pdf")):  # Support both .txt and .pdf
                    file_path = os.path.join(root, file)
                    if file.endswith(".txt"):
                        with open(file_path, "r", encoding=self.encoding) as f:
                            self.documents.append(f.read())
                    else:  # PDF file
                        reader = PdfReader(file_path)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        self.documents.append(text.strip())

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
