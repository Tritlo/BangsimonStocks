import wx
from stockInfo import stockInfo
from stockPlot import stockPlot

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

LABEL_MIN = "Min value: "
LABEL_MAX = "Max value: "
DEFAULT_TICKER = "GOOG"

class initialFrame(wx.Frame):
    """ The main frame of the application
    """
    title = "Bangsimon Stocks"
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        
        self.data = [5, 6, 9, 14]
        
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        
        self.textbox.SetValue(' '.join(map(str, self.data)))
        self.draw_figure()

    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        plot = wx.Menu()
        options = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close','Avg. Price']
        #Nennum ekki ad handlsa inn.
        M = map( (lambda x: self.Bind(wx.EVT_MENU,self.plot_handler,plot.AppendRadioItem(-1,x))),options)
        plot.AppendSeparator()
        m_sma = plot.AppendCheckItem(-1, "Simple Moving Average")
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(plot, "&Plot")
        self.SetMenuBar(self.menubar)
                                  
    def plot_handler(self,event):
        mIs = event.GetEventObject().GetMenuItems()
        for mI in mIs:
            if mI.GetKind() is 2:
                if mI.IsChecked():
                    label = mI.GetItemLabelText()
            if mI.GetKind() is 1:
                Ma = mI.IsChecked()
        stockPlot(self.panel.stockObj,label,MovingAvg = Ma)
             

    def create_main_panel(self):
        """ Creates the main panel with all the controls on it:
             * mpl canvas 
             * mpl navigation toolbar
             * Control panel for interaction
        """
        self.panel = wx.Panel(self)
        self.panel.stockObj = stockInfo("GOOG")
        
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        self.textbox = wx.TextCtrl(
            self.panel, 
            size=(200,-1),
            style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.textbox)
        
        self.drawbutton = wx.Button(self.panel, -1, "Draw!")
        self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton)

        self.cb_grid = wx.CheckBox(self.panel, -1, 
            "Show Grid",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)

        self.slider_label = wx.StaticText(self.panel, -1, 
            "Bar width (%): ")
        self.slider_width = wx.Slider(self.panel, -1, 
            value=20, 
            minValue=1,
            maxValue=100,
            style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider_width.SetTickFreq(10, 1)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_width, self.slider_width)

        # Create the navigation toolbar, tied to the canvas
        #
        self.toolbar = NavigationToolbar(self.canvas)
        
        #
        # Layout with box sizers
        #
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.vbox.AddSpacer(10)
        
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.hbox.Add(self.textbox, 0, border=3, flag=flags)
        self.hbox.Add(self.drawbutton, 0, border=3, flag=flags)
        self.hbox.Add(self.cb_grid, 0, border=3, flag=flags)
        self.hbox.AddSpacer(30)
        self.hbox.Add(self.slider_label, 0, flag=flags)
        self.hbox.Add(self.slider_width, 0, border=3, flag=flags)
        
        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
    
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
        """ Redraws the figure
        """
        str = self.textbox.GetValue()
        self.data = map(int, str.split())
        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()        
        self.axes.grid(self.cb_grid.IsChecked())
        
        self.axes.bar(
            left=x, 
            height=self.data, 
            width=self.slider_width.GetValue() / 100.0, 
            align='center', 
            alpha=0.44,
            picker=5)
        
        self.canvas.draw()
    
    def on_cb_grid(self, event):
        self.draw_figure()
    
    def on_slider_width(self, event):
        self.draw_figure()
    
    def on_draw_button(self, event):
        self.draw_figure()
    
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        dlg = wx.MessageDialog(
            self, 
            msg, 
            "Click!",
            wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal() 
        dlg.Destroy()        
    
    def on_text_enter(self, event):
        self.draw_figure()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
        
    def on_exit(self, event):
        self.Destroy()
        
    def on_about(self, event):
        msg = """ A demo using wxPython with matplotlib:
        
         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw!")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER, 
            self.on_flash_status_off, 
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)
    
    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')
  
class AnalystPanel(wx.Panel):

    stockObj = None
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1,style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # First button
        b = wx.Button(self, -1, "Get data", pos=(20, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClickGetData, b)
        
        b.SetDefault()
        b.SetSize(b.GetBestSize())
        b.SetToolTipString("Retrieves stock data.")
        
        # Second button
        b = wx.Button(self, -1, "Plot", pos=(20, 80))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, b)
        b.SetToolTipString("Plots stock data.")

        self.static_text1 = wx.StaticText(self, -1,"Data is from date: ",pos=(20, 120))
        self.static_text2 = wx.StaticText(self, -1,"Data is to date: ",pos=(20, 140))
        self.static_text3 = wx.StaticText(self, -1,"Company Ticker",pos=(120,20))

        # Text control
        self.text_ctrl1 = wx.TextCtrl(self, -1, DEFAULT_TICKER, pos=(250,20), size=(125,-1))

        self.text_ctrl1.SetToolTipString("Ticker of company")
        
    def OnClickGetData(self, event):
        # Stock info is kept as stockInfo object
        try:
            self.stockObj = stockInfo(self.text_ctrl1.GetValue())
            self.static_text1.SetLabel("Data is from date: " + str(self.stockObj.fromDate))
            self.static_text2.SetLabel("Data is to date: " + str(self.stockObj.toDate))
        except:
            self.stockObj = stockInfo(DEFAULT_TICKER)
            # Reset text control
            self.text_ctrl1.SetValue(DEFAULT_TICKER)
            self.static_text1.SetLabel("Data is from date: ")
            self.static_text2.SetLabel("Data is to date: ")

        # Create artificial stock data

    def OnClickPlot(self, event):
        if self.stockObj is not None:
            plotFrame = wx.Frame(None, title="Plot",size=(200,200))
            plotp = PlotPanel(plotFrame,self.stockObj)
        
            plotFrame.Show()

        

class PlotPanel(wx.Panel):
    stockObj = None
    ATTR= "Adj Close"
    fromDate = None
    toDate = None
    
    def __init__(self, parent, stockObj):
        wx.Panel.__init__(self, parent, -1,style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.stockObj = stockObj

        
        # select Attribute
        attr = ['Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume', 'Avg. Price']
        self.combo= wx.ComboBox(self,choices=attr, value="Adj Close",pos=(120,20))
        self.Bind(wx.EVT_COMBOBOX, self.OnCombo, self.combo)

        """#Virkar ekki 
        self.fromDatePicker = wx.DatePickerCtrl(self,dt = self.dateToWxDateTime(stockObj.fromDate),pos = ( 20,120))
        self.toDatePicker = wx.DatePickerCtrl(self,dt = self.dateToWxDateTime(stockObj.toDate), pos = (20, 140))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, self.fromDatePicker)
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, self.toDatePicker)
        """ 
        # Plot button
        b = wx.Button(self, -1, "Plot", pos=(20, 20))

        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, b)
        b.SetToolTipString("Plots stock data.")
        

    def OnCombo(self, event):
        self.ATTR = self.combo.GetValue()

    def OnClickPlot(self, event):
        stockPlot(self.stockObj,self.ATTR, self.fromDate, self.toDate)


    def dateToWxDateTime(self,date):
        pass
        
    def WxDateTimeToDate(self,datetime):
        pass

    
if __name__ == "__main__":
    app = wx.App(False)
    app.frame = initialFrame()
    app.frame.Show()
    app.MainLoop()
