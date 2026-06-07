import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Load data ---
df = pd.read_csv("Popolazione_residente.csv", sep=None, engine="python")

# Drop the summary row ("Totale") and the "100 e oltre" label row
df = df[~df["Età"].isin(["Totale", "100 e oltre"])].copy()
df["Età"] = pd.to_numeric(df["Età"])
df = df.sort_values("Età")

ages   = df["Età"].values
males  = df["Totale maschi"].values
females = df["Totale femmine"].values

# --- Population Pyramid ---
fig, axes = plt.subplots(1, 2, figsize=(16, 9))
fig.patch.set_facecolor("#0f1117")

# ── Left: stacked area chart ──────────────────────────────────────────────────
ax1 = axes[0]
ax1.set_facecolor("#0f1117")

ax1.fill_betweenx(ages, 0, males,   color="#4C9BE8", alpha=0.85, label="Maschi")
ax1.fill_betweenx(ages, 0, females, color="#E8734C", alpha=0.85, label="Femmine")
ax1.plot(males,   ages, color="#4C9BE8", lw=1.5)
ax1.plot(females, ages, color="#E8734C", lw=1.5)

ax1.set_xlabel("Popolazione", color="white", fontsize=11)
ax1.set_ylabel("Età", color="white", fontsize=11)
ax1.set_title("Popolazione per età e genere\n(distribuzione)", color="white", fontsize=13, pad=12)
ax1.tick_params(colors="white")
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
for spine in ax1.spines.values():
    spine.set_edgecolor("#444")
ax1.legend(facecolor="#1a1d27", labelcolor="white", framealpha=0.9)
ax1.grid(axis="x", color="#333", linestyle="--", linewidth=0.5)

# ── Right: population pyramid ─────────────────────────────────────────────────
ax2 = axes[1]
ax2.set_facecolor("#0f1117")

ax2.barh(ages, -males,   height=0.85, color="#4C9BE8", alpha=0.9, label="Maschi")
ax2.barh(ages,  females, height=0.85, color="#E8734C", alpha=0.9, label="Femmine")

max_val = max(males.max(), females.max())
ax2.set_xlim(-max_val * 1.05, max_val * 1.05)
ax2.set_xlabel("Popolazione", color="white", fontsize=11)
ax2.set_title("Piramide demografica", color="white", fontsize=13, pad=12)
ax2.tick_params(colors="white")
ax2.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(abs(x)):,}")
)
# Midline labels
ax2.axvline(0, color="white", linewidth=0.8, alpha=0.4)
ax2.text(-max_val * 0.55, 95, "Maschi",   color="#4C9BE8", fontsize=10, ha="center")
ax2.text( max_val * 0.55, 95, "Femmine",  color="#E8734C", fontsize=10, ha="center")
for spine in ax2.spines.values():
    spine.set_edgecolor("#444")
ax2.grid(axis="x", color="#333", linestyle="--", linewidth=0.5)

# ── Shared title ──────────────────────────────────────────────────────────────
fig.suptitle("Popolazione Residente — distribuzione per età e sesso",
             color="white", fontsize=15, fontweight="bold", y=0.97)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("popolazione_plot.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Plot saved to: popolazione_plot.png")
plt.show()