# notebook.py

class Notebook:
    def __init__(self, brand: str, page_count: int, cover_type: str, size: str):
        self.brand = brand
        self.page_count = page_count
        self.cover_type = cover_type  # e.g. "soft", "hard"
        self.size = size              # e.g. "A5", "A4"
        self.pages_written = 0
        self.notes = []

    def write(self, text: str):
        """Simulate writing text in the notebook."""
        if self.pages_written < self.page_count:
            self.notes.append(text)
            self.pages_written += 1
            print(f"Page {self.pages_written} written.")
        else:
            print("Notebook is full!")

    def tear_page(self, page_number: int):
        """Tear out a page if it exists."""
        if 0 < page_number <= len(self.notes):
            removed = self.notes.pop(page_number - 1)
            print(f"Tore out page {page_number}: '{removed[:20]}...'")
        else:
            print("Invalid page number.")

    def __str__(self):
        return f"{self.brand} Notebook ({self.size}, {self.cover_type} cover, {self.page_count} pages)"
