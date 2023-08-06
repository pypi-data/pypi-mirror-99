class Flatten:

    def flatten(elements):
    results = []
    
    while elements:
        # Remove the last element from the list
        e = elements.pop() 
        print(e)
        # Check if elemt is a list
        if isinstance(e, list):
            # if is alist extend the element to current list.
            elements.extend(e) 
        elif isinstance(e, int):
            # if not list then add it to the flat list.
            results.append(e) 
        else:
            raise Exception("Only integers or list are pemited")
    
    return results[::-1]





