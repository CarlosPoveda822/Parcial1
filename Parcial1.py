import json
import os

class Article:
    def __init__(self, name, category, cost):
        self.name = name
        self.category = category
        self.cost = cost

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "cost": self.cost
        }

    @staticmethod
    def from_dict(data):
        return Article(data['name'], data['category'], data['cost'])

class BudgetRegistry:
    def __init__(self, filename='budget_registry.json'):
        self.filename = filename
        self.articles = self.load_articles()

    def load_articles(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return [Article.from_dict(article) for article in json.load(f)]
        return []

    def save_articles(self):
        with open(self.filename, 'w') as f:
            json.dump([article.to_dict() for article in self.articles], f)

    def add_article(self, name, category, cost):
        self.articles.append(Article(name, category, cost))
        self.save_articles()

    def find_article(self, name):
        for article in self.articles:
            if article.name == name:
                return article
        return None

    def edit_article(self, old_name, new_name, new_category, new_cost):
        article = self.find_article(old_name)
        if article:
            article.name = new_name
            article.category = new_category
            article.cost = new_cost
            self.save_articles()
            return True
        return False

    def delete_article(self, name):
        article = self.find_article(name)
        if article:
            self.articles.remove(article)
            self.save_articles()
            return True
        return False

def main():
    registry = BudgetRegistry()

    while True:
        print("\nMenu:")
        print("1. Registrar artículo")
        print("2. Buscar artículo")
        print("3. Editar artículo")
        print("4. Eliminar artículo")
        print("5. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            name = input("Nombre del artículo: ")
            category = input("Categoría del artículo: ")
            cost = float(input("Costo del artículo: "))
            registry.add_article(name, category, cost)
            print("Artículo registrado con éxito.")
        elif choice == '2':
            name = input("Nombre del artículo a buscar: ")
            article = registry.find_article(name)
            if article:
                print(f"Nombre: {article.name}, Categoría: {article.category}, Costo: {article.cost}")
            else:
                print("Artículo no encontrado.")
        elif choice == '3':
            old_name = input("Nombre del artículo a editar: ")
            new_name = input("Nuevo nombre del artículo: ")
            new_category = input("Nueva categoría del artículo: ")
            new_cost = float(input("Nuevo costo del artículo: "))
            if registry.edit_article(old_name, new_name, new_category, new_cost):
                print("Artículo editado con éxito.")
            else:
                print("Artículo no encontrado.")
        elif choice == '4':
            name = input("Nombre del artículo a eliminar: ")
            if registry.delete_article(name):
                print("Artículo eliminado con éxito.")
            else:
                print("Artículo no encontrado.")
        elif choice == '5':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
