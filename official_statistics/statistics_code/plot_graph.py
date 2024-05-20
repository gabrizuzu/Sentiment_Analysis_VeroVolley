import matplotlib.pyplot as plt
import numpy as np

# -------------------- PLOT THE STATISTICS --------------------

def plot_season(xlabel, ylabel, title, data1, data2, data3, label1, label2, label3):
    seasons = ['Season 21-22', 'Season 22-23', 'Season 23-24']
    data1.smooth = True
     # Crea il grafico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Linee con marcatori e stili
    ax.plot(seasons, data1, color='#20519F', label=label1, marker='o', linestyle='-', linewidth=2, markersize=6)
    ax.plot(seasons, data2, color='#e14547', label=label2, marker='o', linestyle='-', linewidth=2, markersize=6)
    ax.plot(seasons, data3, color='#A8D9FD', label=label3, marker='o', linestyle='-', linewidth=2, markersize=6)

    # Etichette degli assi e titolo
    ax.set_xlabel(xlabel, fontweight='bold', fontsize=12)
    ax.set_ylabel(ylabel, fontweight='bold', fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold')

    # Griglia
    ax.grid(True, linestyle='--', alpha=0.6)

    # Legenda
    ax.legend(fontsize=10, loc='upper left')

    # Migliora la disposizione degli elementi
    plt.tight_layout()
    
    plt.show()


def plot_bar_chart_3data(xlabel, ylabel, title, data1, data2, data3, label1, label2, label3):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots()
    ax.plot(months, data1, color='#20519F', label=f'{label1}')
    ax.plot(months, data2, color='#e14547', label=f'{label2}')
    ax.plot(months, data3, color='#A8D9FD', label=f'{label3}')
    ax.set_xlabel(f'{xlabel}', fontweight='bold')
    ax.set_ylabel(f'{ylabel}', fontweight='bold')
    ax.set_title(f'{title}', fontsize=14, fontweight='bold')
    ax.legend()
    plt.show()
    
    # Crea il grafico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Linee con marcatori e stili
    ax.plot(months, data1, color='#20519F', label=label1, marker='o', linestyle='-', linewidth=2, markersize=6)
    ax.plot(months, data2, color='#e14547', label=label2, marker='o', linestyle='-', linewidth=2, markersize=6)
    ax.plot(months, data3, color='#A8D9FD', label=label3, marker='o', linestyle='-', linewidth=2, markersize=6)

    # Etichette degli assi e titolo
    ax.set_xlabel(xlabel, fontweight='bold', fontsize=12)
    ax.set_ylabel(ylabel, fontweight='bold', fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold')

    # Griglia
    ax.grid(True, linestyle='--', alpha=0.6)

    # Legenda
    ax.legend(fontsize=10, loc='upper left')

    # Migliora la disposizione degli elementi
    plt.tight_layout()
    
    x = np.arange(len(months))  # the label locations
    width = 0.18 # the width of the bars
    fig, ax = plt.subplots(figsize=(12,8))
    rects1 = ax.bar(x - width, data1, width, color='#20519F', label=f'{label1}')
    rects2 = ax.bar(x, data2, width, color='#e14547', label=f'{label2}')
    rects3 = ax.bar(x + width, data3, width, color='#A8D9FD', label=f'{label3}')
    
    # valori settati in scala logaritmica per una miglior presentazione dei dati
    # ax.set_yscale('log')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(f'{xlabel}', fontweight='bold')
    ax.set_ylabel(f'{ylabel}', fontweight='bold')
    ax.set_title(f'{title}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right')
    ax.legend()

    ax.bar_label(rects1, padding=5, fontsize=8, fontweight='bold')
    ax.bar_label(rects2, padding=5, fontsize=8, fontweight='bold')
    ax.bar_label(rects3, padding=5, fontsize=8, fontweight='bold')

    fig.tight_layout()
    #plt.savefig(f'{title}')
    plt.show()
    

def plot_bar_chart_2data(xlabel, ylabel, title, data1, data2, label1, label2):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = np.arange(len(months))  # the label locations
    width = 0.18  # the width of the bars

    fig, ax = plt.subplots(figsize=(12,8))
    rects1 = ax.bar(x - width/2, data1, width, color='#20519F', label=f'{label1}')
    rects2 = ax.bar(x + width/2, data2, width, color='#e14547', label=f'{label2}')
    
    # valori settati in scala logaritmica per una miglior presentazione dei dati
    #ax.set_yscale('log')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(f'{xlabel}', fontweight='bold')
    ax.set_ylabel(f'{ylabel}', fontweight='bold')
    ax.set_title(f'{title}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right')
    ax.legend()

    ax.bar_label(rects1, padding=5, fontsize=8, fontweight='bold')
    ax.bar_label(rects2, padding=5, fontsize=8, fontweight='bold')

    fig.tight_layout()
    plt.savefig(f'{title}')
    plt.show()