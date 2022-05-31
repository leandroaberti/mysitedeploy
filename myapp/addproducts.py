from myapp.models import Product

#create an object
product = Product(name="iPhone", price=90.00, description="This is a iPhone")

product.save()


product2 = Product(name="iPad", price=1200.00, description="This is an iPad")
