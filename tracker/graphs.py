import matplotlib.pyplot as plt
from collections import defaultdict

class Grahps:

    def create_pie(self,data:defaultdict):
        names,point = list(data[1].keys()),list(data[1].values())
        wedges, texts, autotexts = plt.pie(
            point,
            labels=None,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"width": 0.45},
            textprops={
                "fontsize": 9,
                "fontweight": "bold"
            }
        )
        plt.legend(
            wedges,
            names,
            title="Категории",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        
        plt.axis("equal")
        plt.show()
    
    def create_line(self, data):
        plt.figure(figsize=(12, 6))

        for name, values in data[0].items():
            x = range(1, len(values) + 1)
    
            plt.plot(
                x,
                values,
                marker="o",
                linewidth=2.5,
                markersize=7,
                label=name
            )
        
        ax = plt.gca()

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        

        plt.title(
            "Динамика",
            fontsize=18,
            fontweight="bold",
            pad=20
        )

        plt.xlabel("Транзакция", fontsize=12)
        plt.ylabel("Сумма (₽)", fontsize=12)

        plt.grid(color="lightgray", linestyle="--", linewidth=0.7, alpha=0.5)

        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        plt.legend(
            title="Категории",
            fontsize=10,
            title_fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True,
            loc="upper left"
        )

        plt.tight_layout()
        plt.show()