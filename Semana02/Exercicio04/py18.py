global_var = 1

def outer_func():
    enclosing_var = 2
    
    def inner_func():
        local_var = 3
        print("local_var:", local_var)  # imprime 3
        print("enclosing_var:", enclosing_var)  # imprime 2
        print("global_var:", global_var)  # imprime 1
    
    inner_func()

outer_func()