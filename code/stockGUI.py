import wx
import os
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
        
        self.draw_figure()

    def create_menu(self):
        """Creates the menubar"""
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_new = menu_file.Append(-1, "&New ticker\tCtrl-N", "Choose new ticker to track")
        self.Bind(wx.EVT_MENU, self.on_new, m_new)
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        plot = wx.Menu()
        options = ['Adj Close','Open' ,'High', 'Low', 'Close', 'Volume','Avg. Price']
        #Nennum ekki ad handlsa inn.
        M = map( (lambda x: self.Bind(wx.EVT_MENU,self.plot_handler,plot.AppendRadioItem(-1,x))),options)
        plot.AppendSeparator()
        self.Bind(wx.EVT_MENU,self.plot_handler,plot.AppendCheckItem(-1, "Simple Moving Average"))
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(plot, "&Plot")
        self.SetMenuBar(self.menubar)

    def on_new(self, event):
        prompt = wx.TextEntryDialog(self, "Enter new ticker", "New ticker",self.panel.stockObj.ticker)
        prompt.ShowModal() 
        try:
            self.panel.stockObj = stockInfo(prompt.GetValue())
            self.draw_figure()
        except ValueError:
            msg = wx.MessageDialog(self, "Invalid Ticker", "Error", wx.OK|wx.ICON_ERROR)
            msg.ShowModal()
            self.on_new(None)
                                  
    def plot_handler(self,event):
        """Handles the changing of the plot"""
        mIs = event.GetEventObject().GetMenuItems()
        for mI in mIs:
            #find what is selected
            if mI.GetKind() is 2:
                if mI.IsChecked():
                    self.panel.currentAttr = mI.GetItemLabelText()
            # find whether sMA is on.
            if mI.GetKind() is 1:
                self.panel.MovingAvg = mI.IsChecked()
        self.draw_figure()
             

    def create_main_panel(self):
        """ Creates the main panel with all the controls on it:
             * mpl canvas 
             * mpl navigation toolbar
             * Control panel for interaction
        """
        self.panel = wx.Panel(self)
        self.panel.stockObj = stockInfo(DEFAULT_TICKER)

        #Setjum default value-in
        self.panel.currentAttr = "Adj Close"
        self.panel.fromDate = self.panel.stockObj.fromDate
        self.panel.toDate = self.panel.stockObj.toDate
        self.panel.MovingAvg = False
        self.panel.MovingAvgN = 110

        #Plottum i byrjun.
        self.fig = stockPlot(self.panel.stockObj,"Adj Close",MovingAvg = True)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        

        self.slider_label = wx.StaticText(self.panel, -1, 
            "Moving Average N: ")
        self.slider_width = wx.Slider(self.panel, -1, 
            value=110, 
            minValue=20,
            maxValue=200,
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
        self.hbox.AddSpacer(30)
        self.hbox.Add(self.slider_label, 0, flag=flags)
        self.hbox.Add(self.slider_width, 0, border=3, flag=flags)
        
        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
    
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
        self.fig.clear()
        self.fig = stockPlot(self.panel.stockObj,self.panel.currentAttr,self.panel.fromDate, self.panel.toDate, self.panel.MovingAvg, self.panel.MovingAvgN)
        self.canvas.draw()
        pass
    
    def on_cb_grid(self, event):
        self.draw_figure()
    
    def on_slider_width(self, event):
        self.panel.MovingAvgN = self.slider_width.GetValue()
        self.draw_figure()
    
    def on_draw_button(self, event):
        self.textbox.GetValue()
        try:
            self.panel.stockObj = stockInfo(self.textbox.GetValue())
            self.draw_figure()
        except ValueError:
            print "Invalid Ticker"
    
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
        pass

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
