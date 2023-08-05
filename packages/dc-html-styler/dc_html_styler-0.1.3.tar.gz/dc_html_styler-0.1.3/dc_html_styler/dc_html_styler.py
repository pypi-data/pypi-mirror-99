import pandas as pd
import pandas.io.formats.style
import numpy as np
import jinja2
import numpy as np

class dcstyler(pd.io.formats.style.Styler):
    '''
    Expansion of the pandas.io.formats.style.Styler class.

    Attributes

    '''
    def __init__(self, data):
        self.titles = []
        self.empty_rows = []
        self.background_color = 'white'
        self.border = ''
        super(dcstyler,self).__init__(data)


    def dc_table(self,
                 font_family='sans-serif',
                 font_size='1em',
                 font_weight = '400',
                 font_color = 'black',
                 background_color='#FFFFFF',
                 border='2px solid black',
                 border_cols = None,
                 border_rows = '1px solid black',
                 text_align='center',
                 valign='bottom',
                 height='1.25em',
                 extra=None):
        '''
        Provides the basic setup of the table. All the attributes will be added to the <style> </style> part of the
        html-code.
        All the settings will apply to all cells, unless overwritten later by other methods.
        :param font_family: Font of all cels in table unless else is specified later
        :param font_size: Font size in em (em allows for resizing, per default 1em = 16px.)
        :param font_weight: Values in 100, 200, ..., 900 determining thickness. 400 is normal, 700 is bold.
        :param font_color: Color of the font. Standard is white.
        :param background_color: background color in hex or using html keywords (e.g. 'black' for #000000)
        :param border: The border around the entire table. Not between inner cells.
        :param border_cols: Borders between columns in table.
        :param border_rows: Borders between rows in table.
        :param text_align: Horizontal alignment (left,right,center)
        :param valign: Vertical alignment (bottom, middle, top, baseline)
        :param height: Height of cells
        :param extra: List of extra property,value pairs e.g. [("font-weight", '900')]
        :return: pandas.style-object with added table style
        '''
        styles = [{"selector": '', "props": [
            ("border-collapse", 'collapse'),
            ('font-family', f'{font_family}'),
            ('font-size', f'{font_size}'),
            ('font-weight', f'{font_weight}'),
            ('font-color', f'{font_color}'),
            ("background-color", f'{background_color}'),
            ("border", f'{border}'),
            ("text-align", f'{text_align}'),
            ("valign", f'{valign}'),
            ("height", f'{height}')
            ]},
            #    {"selector": 'td', "props":[
            #("white-space",'nowrap')]}
            ]

        self.background_color = background_color
        self.border = border
        if self.table_styles:
            self.table_styles.extend(styles)
        else:
            self.set_table_styles(styles)
        if extra is not None:
            extra = [{"selector": '', "props": extra}]
            self.table_styles.extend(extra)

        if border_cols:
            styles = [{"selector": 'td', "props": [
                ("border-left", f'{border_cols}'),
                ("border_right", f'{border_cols}')]}]
            self.table_styles.extend(styles)

        if border_rows:
            styles = [{"selector": 'td', "props": [
                ("border-top", f'{border_rows}'),
                ("border_bottom", f'{border_rows}')]}]
            self.table_styles.extend(styles)

    def dc_headers(self,
            font_family='sans-serif',
            font_size='1em',
            font_weight='bold',
            font_color = '#FFFFFF',
            background_color='#005187',
            border_side = '',
            border_bottom='2px solid black',
            text_align='center',
            valign='bottom',
            height='1.25em',
            width = '90px',
            extra=None
    ):
        '''
            Provides the header settings of the table. All the attributes will be added to the <th> </th> parts of the html-
            code. The attributes applies to ALL headers.
            :param font_family: Font of headers
            :param font_size: Font size in pixels
            :param font_weight: Values in 100, 200, ..., 900 determining thickness. 400 is normal, 700 is bold.
            :param font_color: Color of the font. Standard is white.
            :param background_color: background color in hex or using html keywords. Standard is DC-blue
            :param border_side: Border between header columns.
            :param border_bottom: The border below the header cells.
            :param text_align: Horizontal alignment (left,right,center)
            :param valign: Vertical alignment (bottom, middle, top, baseline)
            :param height: Height of cells
            :param width: Width of cells. Functions as a minimal width. If column name is longer, cell will be longer.
            :param extra: List of extra property,value pairs e.g. [("font-weight", '900')]
            :return: pandas.style-object with added table style
            '''
        if not background_color:
            background_color = self.background_color
        styles = [{"selector": 'th', "props": [
            ('font-family', f'{font_family}'),
            ('font-size', f'{font_size}'),
            ('font-weight', f'{font_weight}'),
            ('color', f'{font_color}'),
            ("background-color", f'{background_color}'),
            ("border-bottom", f'{border_bottom}'),
            ("border-right", f'{border_side}'),
            ("text-align", f'{text_align}'),
            ("valign", f'{valign}'),
            ("height", f'{height}'),
            ("width",f'{width}')]},
            {"selector": '', "props": [("border", f'{self.border}')]}]
        if self.table_styles:
            self.table_styles.extend(styles)
        else:
            self.set_table_styles(styles)
        if extra is not None:
            extra = [{"selector": '', "props": extra}]
            self.table_styles.extend(extra)

    def dc_peak(self,
                linetype='1px solid black',
                add_line=True,
                color_nonpeak=None,
                color_peak='#a3c0d2',
                rows=[8, 20, 24],
                subsetline=None,
                subsetbackground=None):
        '''
        Function to add borders between peak and non-peak hours. Inserts a border above row 8,20,24 by default.
        :param linetype: string describing the border inserted to seperate peak hours from non-peak.
        :param add_line: Boolean. True if a line should be added, otherwise False.
        :param color_nonpeak: string background color for non peak cells in hex or using html keywords.
        :param color_peak: string background color for peak cells in hex or using html keywords.
        :param rows: list of length 3 of rows defining 'boundary' between peak and non peak.
        :param subsetline: IndexSlice A valid indexer to limit where to add border line. If none applies to whole table.
        :param subsetbackground: IndexSlice A valid indexer to limit where to add background color
        :return: pandas.style-object with added borders
        '''
        if not color_nonpeak:
            color_nonpeak = self.background_color

        # Draws the border between peak and non-peak.
        if add_line == True:
            def _bordergiver(s):
                '''Helper function adding top and bottom borders to relevant cells'''
                return [f'border-bottom: {linetype}' if s.name + 1 in rows else '' for val in s]
            self.apply(_bordergiver, axis=1, subset=subsetline)


        # Applies backgrounds to cells.
        def _colorgiver(s):
            '''Helper function adding background colors to relevant cells'''
            return [f'background-color: {color_nonpeak}' if (
                    # if row 0-8 or row 20-24
                    (s.name in range(rows[0])) or (s.name in range(rows[1], rows[2])))
                    # if row 8-20
                    else f'background-color: {color_peak}' if s.name in range(rows[0], rows[1]) else None for val in
                    s]
        self.apply(_colorgiver, axis=1, subset=subsetbackground)

    def dc_sign(self,
                color_neg='#e8b3ae',
                color_pos='#bcf0a1',
                subset=None):
        '''
        Function to highlight negative an positive values by changing the background color.
        :param color_neg: String. Background color of cells containing negative values.
        :param color_pos: String. Background color of cells containing positive values.
        :param subset: IndexSlice. A valid indexer to limit where to add background color.
        :return: pandas.style-object with added colors
        '''
        def _colorgiver(val):
            background = color_pos if val >= 0 else color_neg if val < 0 else ''
            return f'background-color:{background}'
        self.applymap(_colorgiver, subset=subset)

    def dc_row_divider(self,
                          linetype='3px solid red',
                          color_above=None,
                          color_below=None,
                          row = 12,
                          subsetline=None,
                          subsetbackground=None
                          ):
        '''
        Adds a border beneath the specified row. Allows for custom coloring above and below the row.
        :param linetype: String. Description of the line. 'thicknes type color'.
        :param color_above: String. Hex or html keyword.
        :param color_below: String. Hex or html keyword.
        :param row: Integer. The row number.
        :param subsetline: IndexSlice A valid indexer to limit where to add the line.
        :param subsetbackground: IndexSlice A valid indexer to limit where to add background colors.
        :return: pandas.style-object.
        '''
        def _bordergiver(s):
            return [f'border-bottom: {linetype}' if s.name + 1 == row else '' for val in s]

        self.apply(_bordergiver, axis=1, subset=subsetline)
        if color_above or color_below: #Only color background if at least one color is given.
            if not color_above:
                color_above = self.background_color
            if not color_below:
                color_below = self.background_color

            def _colorgiver(s):
                return [f'background-color: {color_above}' if (
                    (s.name in range(row)))
                        else f'background-color: {color_below}' for val in s]
            self.apply(_colorgiver, axis=1, subset=subsetbackground)

    def dc_col_divider(self,
                       linetype='3px solid red',
                       color_left=None,
                       color_right=None,
                       col=4,
                       subsetline=None,
                       subsetbackground=None
                       ):
        '''
        Adds a border to the right of the specified column. Allows for custom coloring on either side.
        :param linetype: String. Description of the line. 'thicknes type color'.
        :param color_above: String. Hex or html keyword.
        :param color_below: String. Hex or html keyword.
        :param col: Integer. The column number.
        :param subsetline: IndexSlice A valid indexer to limit where to add the line.
        :param subsetbackground: IndexSlice A valid indexer to limit where to add background colors.
        :return: pandas.style-object.
        '''

        colname = self.data.columns[col-1]
        def _bordergiver(s):
            return [f'border-right: {linetype}' if s.name == colname else '' for val in s.index]

        self.apply(_bordergiver, subset=subsetline)
        if color_left or color_right:  # Only color background if at least one color is given.
            if not color_left:
                color_left = self.background_color
            if not color_right:
                color_right = self.background_color

            def _colorgiver(s):
                print(s.name)
                return [f'background-color: {color_left}' if (
                    (s.name in self.data.columns[:col]))
                        else f'background-color: {color_right}' for val in s.index]

            self.apply(_colorgiver, axis=0, subset=subsetbackground)

    def dc_heatmap(self, colors=['#e8b3ae', '#f5d5d3', '#f7f5f5','#e4f7da','#bcf0a1'], subset = None):
        '''
        Colors cells using a heatmap specified by the hex-values in colors using matplotlib's LinearSegmentedColormap.
        The standard colors goes from a light red for low values to a light green for high values with white colors in
        between.
        :param colors: List. A list of hex values for the colors.
        :param subset: IndexSlice. A valid indexer to limit where to add background colors.
        :return: pandas.style-object.
        '''
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list(
            name='test',
            colors=colors
        )
        cmap.set_bad('white', alpha=0)
        self.background_gradient(cmap=cmap, subset=subset)

    def dc_even_uneven(self,
                even_color=None,
                uneven_color='#D3D3D3',
                subset=None):
        '''
        Function to add borders between peak and non-peak hours. Inserts a border above row 8,20,24 by default.
        :param even_color: string background color for peak in hex or using html keywords.
        :param uneven_color: string background color for NON-peak in hex or using html keywords.
        :param subset: IndexSlice A valid indexer to limit where to add border line.
        :return: pandas.style-object with added borders.
        '''
        if even_color == None:
            even_color = self.background_color
        def _colorgiver(s):
            return [f'background-color: {uneven_color}' if s.name % 2 == 0
                    else f'background-color: {even_color}'for val in s]

        self.apply(_colorgiver, axis=1, subset=subset)

    def dc_add_title(self,
                     title='My table',
                     font_size='1.8em',
                     font_weight='700',
                     font_color='black',
                     background_color='None',
                     border='2px solid black',
                     text_align='center',
                     valign='bottom'):
        '''
        Adds a title to the table. A row which is merged across all columns will be added on top of the table with the
        title. Several titles can be added, with the title added last on top.
        :param title: String. The title.
        :param font_size: String. Size of the title font.
        :param font_weight: String. String value in '100', '200', ..., '900'. 400 is normal text, 700 is bold.
        :param font_color: String. Color of the text. Hex value or html keyword.
        :param background_color: String. Background color. If not specified, table background is used.
        Hex value or html keyword.
        :param border: String. 'thickness type color'. Border around the title-row.
        :param text_align: String. Horizontal alignment of the text.
        :param valign: String. Vertical alignment of the text.
        :return: Appends a html-sting to the style-list of titles.
        '''
        if background_color == None:
            background_color = self.background_color
        colspan = self.data.shape[1]
        self.titles.append(f'''<thead><tr>
                <td style="border: {border}; background-color: {background_color}; font-size:{font_size}; 
                font-weight:{font_weight}; color:{font_color}; text-align:{text_align}"
                colspan={colspan} valign={valign}>
                    <b><color="#000000">{title}</font></b></td>
                </tr>''')

    def dc_make_col_int(self, col_list=None):
        '''
        Makes the columns in col_list into type Int64. This is a integer type which allows np.NaN-values.
        :param col_list: List. List of column names.
        :return: Converts columns to integers.
        '''
        cols = self.data.columns
        if col_list==None:
            col_list = cols
        for col in col_list:
            if type(col) == int:
                self.data[cols[col]] = self.data[cols[col]].astype('Int64')
            else:
                self.data[col] = self.data[col].astype('Int64')

    def render(self, **kwargs):
        '''
        This is a rewritten version of the original pandas.io.format.style.Styler method called render. This version
        allows adding titles.
        :param kwargs:
        :return: Returns a html-string.
        '''
        # Taken from documentation found at:
        # https://github.com/pandas-dev/pandas/blob/v1.2.3/pandas/io/formats/style.py#L581-L628
        self._compute()
        d = self._translate()
        trimmed = [x for x in d["cellstyle"] if any(any(y) for y in x["props"])]
        d["cellstyle"] = trimmed
        d.update(kwargs)

        # Written to allow for own titles:
        normal_output = self.template.render(**d)
        normal_output = normal_output.replace('>nan</td>','></td>')
        if (len(self.titles) == 0): # If no titles have been added
            return normal_output
        else:
            new_output = normal_output
            before_titles, after_titles = new_output.split('<thead>')
            new_output = before_titles + '<thead>' + '\n'.join(self.titles) + after_titles
            return new_output

