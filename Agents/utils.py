def print_stream(stream):
    for s in stream:
        m = s["messages"][-1]
        if isinstance(m, tuple):
            print(m)
        else:
            m.pretty_print()
