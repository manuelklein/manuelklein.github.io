import matplotlib.pyplot as plt
import pandas as pd

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

def check_none(mylist):
    check = False
    try:
        if not mylist:
            check = True
    except:
        pass
    try:
        if len(mylist) == 0:
            check = True
    except:
        pass
    return check

def add_arrays(lists):
    rseries = pd.Series(lists[0])
    rseries *= 0
    for mylist in lists:
        if check_none(mylist):
            continue
        myseries = pd.Series(mylist)
        myseries.fillna(0, inplace = True)
        rseries = rseries.add(myseries)
    return rseries

def normalize_counts(yyy, yytotal):
    scale = sum(yytotal) / 100
    for j, yy in enumerate(yyy):
        for i, _ in enumerate(yy):
            yy[i] /= scale
        yyy[j] = yy
    for i, _ in enumerate(yytotal):
        yytotal[i] /= scale
    return yyy, yytotal

def calculate_bottom(i, yyy):
    bottom = [0 for y in yyy[i]]
    if i > 0:
        bottom = add_arrays(yyy[:i])
    return bottom

def advanced_bar(
        xx, 
        yyy, 
        labels = [None],
        name = "default", 
        title = "",
        xlabel = "",
        ylabel = "",
        width = .8,
        edgecolor = 'white',
        linewidth = 2.5,
        fontsize = 12,
        loclegend = 'best',
        color = ['C0', 'C1', 'C2', 'C3'],
        hatch = ['', '', '', '']
    ):
    # print(title)
    plt.figure()
    yytotal = add_arrays(yyy)
    yyy, yytotal = normalize_counts(yyy, yytotal)
    for i, yy in enumerate(yyy):
        bottom = calculate_bottom(i, yyy)
        plt.bar(
            xx,
            yy,
            # color = colors[i],
            bottom = bottom,
            label = labels[i],
            width = width,
            color = color[i],
            edgecolor = edgecolor,
            linewidth = linewidth/2,
            hatch = hatch[i]
            )
        if i > 0:
            plt.legend(loc=loclegend)
    format_axes(xx, yytotal, linewidth, fontsize)
    plt.savefig(f"plots/{name}.png", transparent=True)

def format_axes(xx, yytotal, linewidth, fontsize):
    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['bottom'].set_linewidth(linewidth)
    # ax.xaxis.label.set_color('white')
    ax.tick_params(
        axis='x', 
        colors='white', 
        width=linewidth, 
        labelsize = fontsize, 
        bottom = False
        )
    for tick in ax.get_xticklabels():
        tick.set_fontweight('bold')
    offset = max(yytotal) * 0.05
    for i, y in enumerate(yytotal):
        ax.text(xx[i], y + offset, f"{y:.1f}%", ha="center", 
                color = 'white', 
                fontweight = 'bold', 
                fontsize = fontsize
                )


def plot_groupsize(df):
    """ Plot histogram of group size of invited guests.
    """
    xx = df.amount.unique()
    xx = sorted(xx)
    yy = list()
    for x in xx:
        y = df[df.amount == x].amount.count()
        yy.append(y)
    advanced_bar(
        xx,
        [yy],
        name = "Gruppengroesse", 
        title = "Wähler pro Stimmzettel",
        xlabel = "Anzahl Personen",
        ylabel = "Häufigkeit",
        width = .45
    )

def get_count_partei(df):
    noanswer = df[(df.bride == 0) & (df.groom == 0) & (df.who == 0)].amount.sum()
    count = [df.bride_w.sum(), df.groom_w.sum(), df.who_w.sum(), noanswer]
    return count

def plot_partei(df):
    """ Plot to which party the guests belong:
        - Braut
        - Bräutigam
        - Wer seid ihr?
        - Keine Antwort
    Stacked by invitation type:
        - Abend
        - Sekt
    """
    count_abend = get_count_partei(df[df.invitation == "Abend"])
    count_sekt = get_count_partei(df[df.invitation == "Sekt"])
    labels = ["Braut", "Bräutigam", "Wer\nseid ihr?", "Keine\nAntwort"]
    advanced_bar(
        xx = labels,
        yyy = [count_abend, count_sekt],
        labels = ["Trauung und abendliche Feier", "Nur zur Trauung eingeladen"],
        name = "Parteianhaenger",
        title = "Parteizugehörigkeit",
        ylabel = "Anzahl",
        fontsize = 12,
        color = [['C1', 'C0', 'C2', 'C3'], ['C1', 'C0', 'C2', 'C3']],
        hatch = ['', '////']
    )

def plot_wahlbeteiligung(df):
    """ Plot voter turnout in percent.
        Stacked by response (cannot participate).
    """
    received = df.amount.sum()
    missing = 3 # Acki, Sven, Nico
    total = received + missing
    count_can = df[df.cannot == 0].amount.sum()
    count_cannot = df[df.cannot == 1].amount.count()
    scale = total * 100
    xx = [count_can, count_cannot, missing] / scale
    labels = ["Ja", "Nein", "Keine\nAntwort"]
    colors = ['#8e7d64', '#555555', '#d8c3a5']
    explode = [0, 0.5, 0.5]
    plt.clf()
    _, _, autotexts = plt.pie(
        xx,
        labels = labels,
        explode = explode,
        # shadow = True,
        autopct='%1.f%%',
        pctdistance=0.8,
        startangle=10,
        # colors = colors,
        textprops={'color':'white', 'weight':'bold', 'fontsize':12},
        wedgeprops={"edgecolor":"white",'linewidth': 2, 'linestyle': 'solid', 'antialiased': True}
        )
    plt.setp(autotexts, **{'color':'white', 'weight':'bold', 'fontsize':12})
    plt.savefig(f"plots/Wahlbeteiligung.png", transparent=True)

def get_count_verlobung(df):
    ref = df.engaged
    knew = df[ref == 1].amount.sum()
    didnt = df[ref == 0].amount.sum()
    count = [knew, didnt]
    return count

def plot_verlobung(df):
    """ Plot bar chart if people knew about engagement:
        - Knew it
        - Didn't know
        Stacked by party:
        - Braut
        - Bräutigam
        - Wer seid ihr?
        - Keine Antwort
    """
    count_bride = get_count_verlobung(df[df.bride == 1])
    count_groom = get_count_verlobung(df[df.groom == 1])
    count_who = get_count_verlobung(df[df.who == 1])
    # count_no = get_count_verlobung(df[(df.bride == 0) & (df.groom == 0) & (df.who == 0)])
    xx = ["Ich wusste es.", "Ich wusste es nicht."]
    yyy = [count_bride, count_groom, count_who] #, count_no]
    labels = ["Partei der Braut", "Partei des Bräutigams", "Wer seid ihr?"] #, "Keine Antwort"]
    advanced_bar(
        xx = xx,
        yyy = yyy,
        labels = labels,
        name = "Verlobung",
        title = "Ich wusste noch gar nicht, dass ihr verlobt seid.",
        ylabel = "Anzahl",
        loclegend='center right',
        color = ['C1', 'C0', 'C2', 'C3']
    )

def plot_merkel(df):
    """ Plot bar chart: "Ich wünsche mir Angela Merkel zurück."
        - Klar nein
        - Nein
        - Unentschieden
        - Ja
        - Klar ja
        No stacking for privacy reasons.
    """
    ref = df.Merkel
    abs_no = df[ref < 0].amount.sum()
    no = df[ref == 0].amount.sum()
    undecided = df[(ref > 0) & (ref < 1)].amount.sum()
    yes = df[ref == 1].amount.sum()
    abs_yes = df[ref > 1].amount.sum()
    count = [abs_no, no, undecided, yes, abs_yes]
    labels = ["Klar nein", "Nein", "Unsicher", "Ja", "Klar ja"]
    advanced_bar(
        xx = labels, 
        yyy = [count], 
        name = "Merkel", 
        title = "Ich wünsche mir Angela Merkel zurück.",
        ylabel = "Anzahl"
    )

# prepare data
data = get_data()
plot_partei(data)
plot_wahlbeteiligung(data)
plot_groupsize(data)
plot_verlobung(data)
plot_merkel(data)
# Wortwolke Merkel
