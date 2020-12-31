from .cart import Cart

# register in settings TEMPLATES list in OPTIONS dictionary
def cart(request):
    return {'cart': Cart(request)}

