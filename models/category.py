class Category:

    #Une liste qui contient toutes les catégories du site
    list_category = []

    #il faut ajouter une liste de livre aussi, mais comment ?
    def __init__(self, url, name):
        self.url = url
        self.name = name
        Category.list_category.append(self)

