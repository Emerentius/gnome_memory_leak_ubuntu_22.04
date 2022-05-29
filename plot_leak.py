import plotnine as p9
from plotnine import ggplot, aes, geom_line
import pandas as pd

data = pd.read_csv("./gnome-shell-memory-usage-kb.txt", parse_dates=[0])

# Find places where the data is interrupted because the PC was off
# so it can be marked.
data["time_to_next"] = (data["date"].shift(-1) - data["date"]).fillna(
    pd.Timedelta(seconds=60)
)
data["is_breakpoint"] = data["time_to_next"] > pd.Timedelta(5, unit="minutes")

plot: ggplot = (
    ggplot(
        data=data,
        mapping=aes(
            "date",
            "memory_usage_in_kB / 1024 / 1024",
            group=1,
            color="factor(is_breakpoint)",
        ),
    )
    + geom_line()
    + p9.ylab("Gnome Shell Memory Usage [GiB]")
    + p9.xlab("Date (Month-Day)")
    + p9.scale_y_continuous(breaks=list(range(0, 15)), minor_breaks=5)
    + p9.scale_x_date(date_breaks="1 day", date_labels="%m-%d")
    + p9.scale_color_manual(["black", "red"], labels=["Running", "Stand-By"])
    + p9.labs(color="PC State")
    + p9.theme(
        figure_size=(16, 8),
        axis_text_y=p9.element_text(size=16),
        axis_text_x=p9.element_text(size=12),
        legend_text=p9.element_text(size=12),
        text=p9.element_text(size=14),
    )
)

plot.save(filename="figure.png")
# fig = plot.draw(show=True)
