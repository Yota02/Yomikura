class Book:
    def __init__(self, id, title, series_id, file_path):
        self.id = id
        self.title = title
        self.series_id = series_id
        self.file_path = file_path
        self.series_name = None  # Optionnel, pour référence