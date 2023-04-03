from os import path

import plotly.graph_objs as go
from plotly.subplots import make_subplots


class Chart:
    default_color = "#ddd"
    default_data_color = "#ddd"
    default_plot_color = "#222"
    default_background_color = "rgba(0,0,0,0)"
    default_font = "sans-serif"
    is_pdf = False

    def __init__(self, is_pdf):
        self.data = None
        self.fig = None
        self.is_pdf = is_pdf
        if self.is_pdf:
            self.default_font = "serif"
            self.default_color = "#222"
            self.default_data_color = "#222"
            self.default_plot_color = "#ddd"

    def set_data(self, data):
        self.data = data
        return self

    def get_svg(self, path):

        if self.fig is None:
            raise ValueError("No fig generated")
        self.fig.write_image(path)
        return self

    def md(self, file, out_format="<img src='{path}' alt='{alt}'>", alt="Chart"):
        if self.is_pdf:
            out_file = path.join("../build/", file)
        else:
            out_file = path.join("../out/", file)
        self.get_svg(out_file)
        return out_format.format(path=file, alt=alt)

    def line(
        self,
        color=None,
        plot_color=None,
        data_color=None,
        background_color=None,
        title="",
        annotations=[],
        x_title="",
        y_title="",
    ):
        if self.data is None:
            raise ValueError("No data provided")

        if color is None:
            color = self.default_color
        if plot_color is None:
            plot_color = self.default_plot_color
        if data_color is None:
            data_color = self.default_data_color
        if background_color is None:
            background_color = self.default_background_color

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.data["x"],
                y=self.data["y"],
                mode="lines+markers",
                name="",
                marker=dict(color=data_color, size=8),
                line=dict(width=1),
                showlegend=False,
            )
        )
        fig.update_layout(
            xaxis=dict(
                title=x_title,
                showgrid=False,
                tickmode="array",
                type="linear",
                autorange=True,
                tickvals=self.data["x"],
                tickfont=dict(size=10),
                ticks="outside",
            ),
            yaxis=dict(
                title=y_title,
                showgrid=False,
                tickmode="array",
                type="linear",
                tickfont=dict(size=10),
                ticks="outside",
            ),
            margin=dict(r=20),
            annotations=annotations,
            title=title,
            font=dict(family=self.default_font, color=color),
            plot_bgcolor=plot_color,
            paper_bgcolor=background_color,
        )
        self.fig = fig
        return self

    def scatter(

        self,
        color=None,
        plot_color=None,
        data_color=None,
        background_color=None,
        title="",
        annotations=[],
        x_title="",
        y_title="",
    ):
        if self.data is None:
            raise ValueError("No data provided")

        if color is None:
            color = self.default_color
        if plot_color is None:
            plot_color = self.default_plot_color
        if data_color is None:
            data_color = self.default_data_color
        if background_color is None:
            background_color = self.default_background_color
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.data["x"],
                y=self.data["y"],
                mode="markers",
                marker=dict(color=data_color),
                hoverinfo="text",
            )
        )

        fig.update_layout(
            xaxis=dict(
                title=x_title,
                showgrid=False,
                tickmode="array",
                tickvals=self.data["x"],
                tickfont=dict(size=10),
                ticks="outside",
                automargin=True,
            ),
            yaxis=dict(
                title=y_title,
                showgrid=False,
                tickmode="array",
                tickvals=self.data["y"],
                tickfont=dict(size=10),
                ticks="outside",
                automargin=True,
            ),
            margin=dict(r=20),
            annotations=annotations,
            title=title,
            font=dict(family=self.default_font, color=color),
            plot_bgcolor=plot_color,
            paper_bgcolor=background_color,
        )
        self.fig = fig
        return self

    def bar(

        self,
        color=None,
        plot_color=None,
        data_color=None,
        background_color=None,
        title="",
        annotations=[],
        x_title="",
        y_title="",
    ):
        if self.data is None:
            raise ValueError("No data provided")
        if color is None:
            color = self.default_color
        if plot_color is None:
            plot_color = self.default_plot_color
        if data_color is None:
            data_color = self.default_data_color
        if background_color is None:
            background_color = self.default_background_color


        fig = make_subplots(rows=1, cols=1)

        fig.add_trace(
            go.Bar(
                x=self.data["x"],
                y=self.data["y"],
                marker_color=data_color,
            ),
            row=1,
            col=1,
        )

        fig.update_layout(
            xaxis=dict(
                title=x_title,
                tickmode="array",
                tickvals=self.data["x"],
                tickfont=dict(size=10),
                automargin=True,
            ),
            yaxis=dict(
                title=y_title,
                showgrid=False,
                automargin=True,
            ),
            annotations=annotations,
            title=title,
            font=dict(family=self.default_font, color=color),
            plot_bgcolor=plot_color,
            paper_bgcolor=background_color,
        )
        self.fig = fig
        return self

    def spark(
        self,
        data_color=None,
        background_color=None,
        start_dot=False,
        end_dot=True,
        height=30,
        width=100,
    ):
        if self.data is None:
            raise ValueError("No data provided")
        if data_color is None:
            data_color = self.default_data_color
        if background_color is None:
            background_color = self.default_background_color
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.data["x"],
                y=self.data["y"],
                line=dict(color=data_color, width=1),
                mode="lines",
            )
        )
        if start_dot:
            fig.add_trace(
                go.Scatter(
                    x=[self.data["x"][0]],
                    y=[self.data["y"][0]],
                    mode="markers",
                    marker=dict(size=4, color="steelblue"),
                )
            )
        if end_dot:
            fig.add_trace(
                go.Scatter(
                    x=[self.data["x"][-1]],
                    y=[self.data["y"][-1]],
                    mode="markers",
                    marker=dict(size=4, color="tomato"),
                )
            )
        fig.update_layout(
            showlegend=False,
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
            ),
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            margin=dict(t=0, l=0, r=0, b=0),
            height=height,
            width=width,
        )
        self.fig = fig
        return self


if __name__ == "__main__":

    import random

    def line():
        data = {}
        data["y"] = [random.randint(0, 3) for _ in range(11)]
        data["x"] = list(range(1967, 1978))
        linechart = Chart(False)
        linechart.set_data(data)
        linechart.line(
            title="Test Line",
            x_title="years",
            y_title="Randint",
            background_color="#000",
        )
        linechart.get_svg("linechart.svg")

    def scatter():
        data = {}
        data["y"] = [random.randint(100, 300) for _ in range(11)]
        data["x"] = [random.randint(1, 64) for _ in range(11)]
        plot = Chart(False)
        plot.set_data(data)
        plot.scatter(
            title="Test Line",
            x_title="years",
            y_title="Randint",
            background_color="#000",
        )
        plot.get_svg("scatterplot.svg")

    def bar():
        data = {}
        data["y"] = [random.randint(100, 300) for _ in range(11)]
        data["x"] = [random.randint(1, 64) for _ in range(11)]
        plot = Chart(False)
        plot.set_data(data)
        plot.bar(
            title="Test Line",
            x_title="years",
            y_title="Randint",
            background_color="#000",
        )
        plot.get_svg("barchart.svg")

    def spark():
        data = {}
        data["y"] = [random.randint(0, 10) for _ in range(100)]
        data["x"] = list(range(0, 100))
        Chart(False).set_data(data).spark(
            background_color="#000", start_dot=True, width=300
        ).md("spark.svg")

    spark()
