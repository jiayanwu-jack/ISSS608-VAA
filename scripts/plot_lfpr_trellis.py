from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    r"E:\Documents\OneDrive - Singapore Management University\03 Visual Analytics and Applications\Timed Assignment\res_LFPR_2_sex_age.csv"
)
OUTPUT_DIR = ROOT / "images" / "timed-assignment"
PNG_OUT = OUTPUT_DIR / "lfpr_trellis_line_chart_2016_2025.png"
HTML_OUT = OUTPUT_DIR / "lfpr_trellis_line_chart_2016_2025.html"

AGE_ORDER = [
    "15-19",
    "20-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60-64",
    "65-69",
    "70-74",
    "75 & Over",
]

TOKENS = {
    "surface": "#FCFCFD",
    "panel": "#FFFFFF",
    "ink": "#1F2430",
    "muted": "#6F768A",
    "grid": "#E6E8F0",
    "axis": "#D7DBE7",
}

PALETTE = {
    "male": "#5477C4",
    "female": "#F0986E",
}


def add_header(fig, title, subtitle):
    fig.text(
        0.06,
        0.975,
        title,
        ha="left",
        va="top",
        fontsize=19,
        fontweight="bold",
        color=TOKENS["ink"],
    )
    fig.text(
        0.06,
        0.943,
        subtitle,
        ha="left",
        va="top",
        fontsize=10.5,
        color=TOKENS["muted"],
    )


def main():
    df = pd.read_csv(SOURCE)
    df["year_num"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[
        df["year_num"].between(2016, 2025)
        & df["age"].isin(AGE_ORDER)
        & df["sex"].isin(["male", "female"])
    ].copy()
    df["year_num"] = df["year_num"].astype(int)
    df["age"] = pd.Categorical(df["age"], categories=AGE_ORDER, ordered=True)
    df = df.sort_values(["age", "sex", "year_num"])

    sns.set_theme(
        style="whitegrid",
        rc={
            "figure.facecolor": TOKENS["surface"],
            "axes.facecolor": TOKENS["panel"],
            "axes.edgecolor": TOKENS["axis"],
            "axes.labelcolor": TOKENS["ink"],
            "xtick.color": TOKENS["muted"],
            "ytick.color": TOKENS["muted"],
            "grid.color": TOKENS["grid"],
            "font.family": ["Segoe UI", "DejaVu Sans", "Arial", "sans-serif"],
        },
    )

    fig, axes = plt.subplots(5, 3, figsize=(15, 14), sharex=True, sharey=True)
    axes = axes.ravel()

    for ax, age in zip(axes, AGE_ORDER):
        panel = df[df["age"] == age]
        for sex in ["male", "female"]:
            series = panel[panel["sex"] == sex]
            ax.plot(
                series["year_num"],
                series["resident_labour_force_participation_rate"],
                label=sex.capitalize(),
                color=PALETTE[sex],
                linewidth=2.1,
                marker="o" if sex == "male" else "s",
                markersize=3.6,
                markerfacecolor=PALETTE[sex],
                markeredgewidth=0,
                linestyle="-" if sex == "male" else "--",
            )

        ax.set_title(age, loc="left", fontsize=11.5, fontweight="bold", color=TOKENS["ink"])
        ax.set_ylim(0, 100)
        ax.set_xlim(2016, 2025)
        ax.set_xticks(range(2016, 2026, 3))
        ax.yaxis.set_major_locator(mticker.MultipleLocator(25))
        ax.grid(True, axis="y", linestyle=(0, (1, 3)), linewidth=0.8)
        ax.grid(False, axis="x")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(TOKENS["axis"])
        ax.spines["bottom"].set_color(TOKENS["axis"])
        ax.tick_params(labelsize=8.5)

    for ax in axes[len(AGE_ORDER) :]:
        ax.axis("off")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper left",
        bbox_to_anchor=(0.058, 0.914),
        ncol=2,
        frameon=False,
        fontsize=10,
    )
    fig.supxlabel("Year", x=0.52, y=0.035, fontsize=11, color=TOKENS["ink"])
    fig.supylabel("LFPR (%)", x=0.02, y=0.5, fontsize=11, color=TOKENS["ink"])
    add_header(
        fig,
        "Resident LFPR by sex and age group",
        "Singapore residents, 2016-2025; small multiples use a fixed 0-100% y-axis and exclude the overlapping 70 & Over aggregate.",
    )
    fig.text(
        0.06,
        0.018,
        "Source: res_LFPR_2_sex_age.csv",
        ha="left",
        va="bottom",
        fontsize=8.5,
        color=TOKENS["muted"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(rect=(0.045, 0.055, 0.99, 0.895), h_pad=1.3, w_pad=1.0)
    fig.savefig(PNG_OUT, dpi=180, bbox_inches="tight")
    plt.close(fig)

    HTML_OUT.write_text(
        f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Resident LFPR by sex and age group</title>
  <style>
    body {{
      margin: 0;
      background: {TOKENS['surface']};
      color: {TOKENS['ink']};
      font-family: Aptos, Segoe UI, Arial, sans-serif;
    }}
    main {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
  <main>
    <img src=\"{PNG_OUT.name}\" alt=\"Small multiples line chart of Singapore resident LFPR by sex and age group, 2016 to 2025\">
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )

    print(PNG_OUT)
    print(HTML_OUT)


if __name__ == "__main__":
    main()
