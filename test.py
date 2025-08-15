import numpy as np
import pandas as pd

'''
U: maximum limit of new payment term to be extended
L: minimum limit of new payment term to be extended
from the dataframe it extracts 3 columns
Vendor count, Total amount, and current_payment_terms
'''
df = pd.DataFrame({
    "Current Payment Terms":[0,7,15,21,30],
    "Total Purchase Value  July 25 against the Vendors (INR)":[189716.86,662088.96,4632135.34,543024.38,3103392.91],
    "Vendors":[2,4,20,5,13]
})

amount = df["Total Purchase Value  July 25 against the Vendors (INR)"].abs().to_numpy(float)
vendors = df["Vendors"].to_numpy(float)
U = 60.0
L = 30

target_avg = 44  # <-- user input
K = target_avg * vendors.sum()

ratio = amount / vendors
order = np.argsort(-ratio)

x = np.full(len(df), L)
need = K - (vendors * x).sum()

for i in order:
    cap = (U - x[i]) * vendors[i]
    take = min(cap, need)
    x[i] += take / vendors[i]
    need -= take
    if need <= 1e-9:
        break

df["Target Payment Term"] = x
df["Improvement in Cash Inventory (CF) on Improvement  of WAPT"] = df["Target Payment Term"] * amount