import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simple_plot(xx, yy, title):
    plt.figure()
    plt.plot(xx, yy)
    plt.savefig(f"basic/{title}.png")

def simple_hist(xx, title):
    plt.figure()
    plt.hist(xx)
    plt.savefig(f"basic/{title}.png")

def simple_bar(xx, yy, title):
    plt.figure()
    plt.bar(xx, yy)
    plt.savefig(f"basic/{title}.png")

def get_data():
    names = ["invitation", "name", "amount", "bride", "groom", "who", "engaged", "cannot", "Merkel"]
    dtype = {
        "invitation": "str",
        "name": "str",
        "amount": "Float64",
        "bride": "Int64",
        "groom": "Int64",
        "who": "Int64",
        "engaged": "Int64",
        "cannot": "Int64",
        "Merkel": "Float64"
    }
    filename = "Hochzeit  - Wahl.csv"
    df = pd.read_csv(filename, names = names, header = 0, dtype = dtype)
    df["invitation"] = df.invitation.str.strip()
    df["bride_w"] = df.bride * df.amount
    df["groom_w"] = df.groom * df.amount
    df["who_w"] = df.who * df.amount
    return df

# prepare data
df = get_data()
# df = df[df.invitation == "Abend"]

# type of invitation
simple_hist(df.invitation, "invitation_type")
abend = df[df.invitation == "Abend"].amount.sum()
sekt = df[df.invitation == "Sekt"].amount.sum()
count = [abend, sekt]
labels = ["Abend", "Sekt"]
simple_bar(labels, count, "invitation_by_amount")

# number of guests
simple_hist(df.amount, "number_of_guests")

# belonging
noanswer = df[(df.bride == 0) & (df.groom == 0) & (df.who == 0)].amount.sum()
count = [df.bride_w.sum(), df.groom_w.sum(), df.who_w.sum(), noanswer]
labels = ["Bride", "Groom", "Who are you?", "No answer"]
simple_bar(labels, count, "belonging")
simple_hist(df.bride, "belonging_bride")
simple_hist(df.groom, "belonging_groom")
simple_hist(df.bride+df.groom, "belonging_both")
simple_hist(df.who, "belonging_who")

# participation
received = df.amount.sum()
missing = 3 # Acki, Sven, Nico
total = received + missing
count = [received , missing ]
labels = ["Erhalten (%)", "Fehlt (%)"]
simple_bar(labels, count, "participation")

# engaged?
simple_hist(df.engaged, "engaged")
ref = df.engaged
knew = df[ref == 1].amount.sum()
didnt = df[ref == 0].amount.sum()
count = [knew, didnt]
labels = ["Wusste ich", "Nicht"]
simple_bar(labels, count, "engaged_by_amount")

# cannot
simple_hist(df.cannot, "cannot")
ref = df.cannot
cannot = df[ref == 1].amount.count()
can = df[ref == 0].amount.sum()
count = [cannot, can]
labels = ["Kann nicht", "Kann"]
simple_bar(labels, count, "cannot_by_amount")

# Merkel
ref = df.Merkel
abs_no = df[ref < 0].amount.sum()
no = df[ref == 0].amount.sum()
undecided = df[(ref > 0) & (ref < 1)].amount.sum()
yes = df[ref == 1].amount.sum()
abs_yes = df[ref > 1].amount.sum()
count = [abs_no, no, undecided, yes, abs_yes]
print(f"count: {sum(count)}")
labels = ["Klar nein", "Nein", "Unentschieden", "Ja", "Klar ja"]
simple_bar(labels, count, "Merkel")
simple_hist(ref[ref < 10], "Merkel_hist")

print("success")
