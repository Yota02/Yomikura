import os
import shutil
from typing import List, Optional

class FileHandler:
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def get_unassigned_books(self):
        """Récupère uniquement les fichiers PDF non assignés"""
        try:
            unassigned = []
            for file in os.listdir(self.base_path):
                if file.lower().endswith('.pdf'):
                    unassigned.append(file)
            print(f"PDFs trouvés : {unassigned}")  # Pour le débogage
            return unassigned
        except Exception as e:
            print(f"Erreur lors de la recherche des PDFs : {e}")
            return []

    def get_books_in_series(self, series_name):
        """Récupère uniquement les fichiers PDF dans une série"""
        series_path = os.path.join(self.base_path, series_name)
        try:
            if os.path.exists(series_path):
                return [f for f in os.listdir(series_path) if f.lower().endswith('.pdf')]
            return []
        except Exception as e:
            print(f"Erreur lors de la lecture de la série {series_name}: {e}")
            return []

    def move_book_to_series(self, book_name: str, series_name: str) -> bool:
        """Déplace un livre dans le dossier d'une série"""
        try:
            source = os.path.join(self.base_path, book_name)
            target = os.path.join(self.base_path, series_name, book_name)
            if os.path.exists(source):
                shutil.move(source, target)
                return True
            return False
        except Exception:
            return False

    def create_series_folder(self, series_name: str) -> str:
        """Crée un dossier pour une série"""
        series_path = os.path.join(self.base_path, series_name)
        os.makedirs(series_path, exist_ok=True)
        return series_path

    def save_book(self, series_name: str, book_file, filename: str) -> Optional[str]:
        """Sauvegarde un livre dans le dossier de sa série"""
        try:
            series_path = self.create_series_folder(series_name)
            file_path = os.path.join(series_path, filename)
            book_file.save(file_path)
            return file_path
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier : {e}")
            return None

    def get_series_list(self) -> List[str]:
        """Récupère la liste des séries"""
        try:
            return [d for d in os.listdir(self.base_path) 
                   if os.path.isdir(os.path.join(self.base_path, d))]
        except Exception:
            return []

    def delete_book(self, series_name: str, filename: str) -> bool:
        """Supprime un livre"""
        try:
            file_path = os.path.join(self.base_path, series_name, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    def delete_series(self, series_name: str) -> bool:
        """Supprime une série et tous ses livres"""
        try:
            series_path = os.path.join(self.base_path, series_name)
            if os.path.exists(series_path):
                shutil.rmtree(series_path)
                return True
            return False
        except Exception:
            return False

    def rename_series(self, old_name: str, new_name: str) -> bool:
        """Renomme une série"""
        try:
            old_path = os.path.join(self.base_path, old_name)
            new_path = os.path.join(self.base_path, new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                return True
            return False
        except Exception:
            return False