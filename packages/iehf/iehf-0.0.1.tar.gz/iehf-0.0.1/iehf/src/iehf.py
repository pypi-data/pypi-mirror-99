import numpy as np
import inflect
from scipy.stats import iqr


class PandasTransformFuncs:
    @staticmethod
    def calc_mean(x):
        return np.mean(x)

    @staticmethod
    def calc_iqr(x):
        return iqr(x)

    @staticmethod
    def calc_median(x):
        return np.median(x)

    @staticmethod
    def calc_iqr_score(x):
        return (x-np.median(x))/iqr(x)

    @staticmethod
    def calc_row_count(x):
        return len(x)


class HumanReadableTextFormatting:
    @staticmethod
    def format_col(x, method):
        if method == 'dollar':
            return f'${round(x):,}'
        if method == 'percent':
            return f'{round(x*1000)/10}%'
        if method == 'inflect':
            return inflect.engine().number_to_words(x)
    
    @staticmethod
    def html_text_augment(x, methods):
        tags = {
            'bold': 'b',
            'italics': 'i'
        }
        
        for m in methods:
            x  = f"<{tags[m]}>{x}</{tags[m]}>"
        return x

    @staticmethod
    def add_br_to_title(x, n = 2):
        words = x.split()

        out = ''
        for idx, w in enumerate(words):
            if idx > 0 and idx % 2 == 1:
                out += f'{w}<br>'
            else:
                out += f'{w} '
        out = ''.join(out).strip() 
        return out



def decimal_2_percent(x, n_decimals=0):
    return round(x*10**(n_decimals+2))/10**(n_decimals)


def distlr_fig_formatting(fig):
    fig = format_fig_layout(fig)
    fig.for_each_trace(
        lambda trace: UpdateTraceClass(trace).update_parent()
    )

    return fig

def format_fig_layout(fig):

    fig.update_layout(
                width = 282, showlegend=False,
                margin=dict(l=5, r=5, t=50, b=5),
                paper_bgcolor= '#FFFFFF',
                plot_bgcolor= '#FFFFFF',
                font_family = "'Roboto' sans-serif",
        )
        
    fig.update_annotations(font_size=12)
    fig.update_yaxes(
        showgrid = True,
        gridcolor = '#C8CDD5',
        gridwidth = 0.01,
        showline = True,
        linewidth = 1,
        linecolor = '#C8CDD5'
    )

    fig.update_xaxes(
        showline = True,
        linewidth = 1,
        linecolor = '#C8CDD5',
        tickfont_size = 10
    )

    return fig

class UpdateTraceClass():
    def __init__(self, trace):
        self.trace = trace
        self.theme = [
             '#0071EB',
             '#001A70',
             '#838D9C',
             '#05152D'
        ]
           
    def update_parent(self):
        if self.trace.type == 'bar':
           self.update_bar()
        
    def update_bar(self):
        self._update_bar_xlabels()

        update_dict = {}
        update_dict.update(self._update_bar_color())
        update_dict.update(self._update_bar_width())
        update_dict.update(self._update_bar_text())        
        self.trace.update(update_dict)
        
        
    def _update_bar_color(self):
        n_colors = len(self.theme)
        color_array = [self.theme[idx%n_colors] for idx,c in enumerate(self.trace.x)]
        return {'marker_color': color_array}
    
    def _update_bar_width(self):
        n_bars = len(self.trace.x)
        width = 1/(n_bars)
        return {'width':0.5}

    def _update_bar_text(self):
        return {'outsidetextfont': {'size': 10}}
    
    def _update_bar_xlabels(self):
        self.trace.x = [HumanReadableTextFormatting.add_br_to_title(label) for label in self.trace.x]
