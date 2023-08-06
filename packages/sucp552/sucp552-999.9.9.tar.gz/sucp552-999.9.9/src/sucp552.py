def say_hello(name=None):
    if name is None:
        return "This is the evil package!!!!"
    else:
        return f"You have been dooped, {name}!"
