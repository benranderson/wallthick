def initial_calcs(a, b):
    c = a + b
    d = a - b

    return (c, d)


def main_calcs(init_results):
    (c, d) = init_results

    results = {}

    e = c*d
    f = c/d

    results["g"] = e
    results["f"] = f

    return results

init_results = initial_calcs(5, 6)

results = main_calcs(init_results)

print(results)
