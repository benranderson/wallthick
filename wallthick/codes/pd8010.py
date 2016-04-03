"""
PD 8010-2:2015
Pipeline Systems - Part 2: Subsea pipelines – Code of practice
"""

title = "PD 8010-2"
year = 2015

df_h = 0.72
df_e = 0.96

# (Table 2) Equivalent stress design factor
df_e = {'Temporary': 1.0,
        'Operational': 0.96}


def req_thickness(t, t_corr, f_tol):
    """Number [m], Number [m], Number [-] -> Number [m]
    Exrapolated from equation (4)
    Determine required wall thickness based on mechanical allowances"""
    try:
        return (t + t_corr) / (1 - f_tol)
    except ZeroDivisionError:
        print("Divide by zero. Check f_tol is in meters.")
        raise

if __name__ == "__main__":  # pragma: no cover
    pass
