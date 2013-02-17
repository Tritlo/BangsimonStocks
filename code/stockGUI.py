import wx
import os
import matplotlib
import wx.lib.hyperlink as hl
import wx.lib.scrolledpanel
matplotlib.use('WXAgg')

from stockInfo import stockInfo
from stockPlot import stockPlot
from stockUtil import *
from stockAnalysis import Beta

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

DEFAULT_TICKER = "GOOG"

class initialFrame(wx.Frame):
    """ The main frame of the application
    """
    title = "Bangsimon Stocks"
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        
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
        #Nennum ekki ad handsla inn.
        M = map( (lambda x: self.Bind(wx.EVT_MENU,self.plot_handler,
                                      plot.AppendRadioItem(-1,x))),options)
        plot.AppendSeparator()
        self.Bind(wx.EVT_MENU,self.plot_handler,plot.AppendCheckItem(-1, "Simple Moving Average"))

        self.menubar.SetMenus([(menu_file,"&File"),(plot, "&Plot")])
        #self.menubar.Append(menu_file, )
        #self.menubar.Append
        self.SetMenuBar(self.menubar)

             

    def create_main_panel(self):
        """ Creates the main panel with all the controls on it:
             * mpl canvas 
             * mpl navigation toolbar
             * Control panel for interaction
        """
        self.panel = wx.Panel(self)
        self.panel.stockObj = stockInfo(DEFAULT_TICKER)

        
        #Plottum i byrjun.
        self.fig = stockPlot(self.panel.stockObj,"Adj Close")
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        
        #Setjum default value-in
        self.panel.currentAttr = "Adj Close"
        self.panel.fromDate = self.panel.stockObj.fromDate
        self.panel.toDate = self.panel.stockObj.toDate
        self.panel.MovingAvg = False
        self.panel.MovingAvgN = 110
        self.panel.Beta = Beta(self.panel.stockObj,self.panel.fromDate, self.panel.toDate)
        

        self.slider_label = wx.StaticText(self.panel, -1, 
            "Moving Average N: ")
        self.slider_width = wx.Slider(self.panel, -1, 
            value=110, 
            minValue=20,
            maxValue=200,
            style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider_width.SetTickFreq(10, 1)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_width, self.slider_width)
        self.Bind(wx.EVT_COMMAND_SCROLL_CHANGED, self.on_slider_width, self.slider_width)

        # Create the navigation toolbar, tied to the canvas
        #
        self.toolbar = NavigationToolbar(self.canvas)
        self.SetToolBar(self.toolbar)
        
        #
        # Layout with box sizers
        #
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 0, wx.LEFT | wx.TOP | wx.EXPAND)
        
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.hbox.AddSpacer(30)
        self.hbox.Add(self.slider_label, 0, flag=flags)
        self.hbox.Add(self.slider_width, 1, border=3, flag=flags |wx.EXPAND)
        
        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP| wx.EXPAND)

        self.vbox.AddSpacer(10)
        self.RssBox = wx.BoxSizer(wx.VERTICAL)
        
        self.RssPanel = wx.lib.scrolledpanel.ScrolledPanel(self.panel,size = wx.Size(-1, 150))
        
        self.RssPanel.SetSizer(self.RssBox)
        self.updateRSS()
        self.RssBox.Fit(self.RssPanel)
        self.RssPanel.SetupScrolling()
        
        self.vbox.Add(self.RssPanel,0, flag= wx.EXPAND)
        
        self.panel.SetSizer(self.vbox)
        
        self.vbox.Fit(self)
        
        self.updateCurrentData()

    def updateRSS(self):
        rss = self.panel.stockObj.getRSS()
        self.RssBox.Clear()
        self.hyperlinks = map( (lambda p:hl.HyperLinkCtrl(self.RssPanel,wx.ID_ANY,label=str(p[0]),URL = str(p[1]))),rss)
        for i in self.hyperlinks:
            self.RssBox.Add(i,0,flag= wx.EXPAND)
            
    
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
        self.flash_status_message("Plotting...")
        self.fig.clear()
        self.fig = stockPlot(self.panel.stockObj,self.panel.currentAttr,
                                 self.panel.fromDate, self.panel.toDate,
                                 self.panel.MovingAvg, self.panel.MovingAvgN)
        self.plotInformation()
        self.flash_status_message("Plotting...Done")
        self.canvas.draw()

    def plotInformation(self):
        self.updateCurrentData()
        self.fig.suptitle(self.panel.currentData['name'])
        self.fig.text(0.13, 0.89,"Beta: " + str(self.panel.Beta),
                  horizontalalignment='left',
                  verticalalignment='top',
                  transform = self.fig.axes[0].transAxes)
        
        Cd = lambda c : str(self.panel.currentData[c])
        currentDataString = "Price: %s, Market Cap %s\n\
52 week high/low: %s/%s,\n\
Short ratio:%s, 50 MAvg: %s\n\
Earnings per share: %s" % (Cd('price'), Cd('market_cap'), Cd('52_week_high'), Cd('52_week_low'), Cd('short_ratio'), Cd('50day_moving_avg'), Cd('earnings_per_share'))
        self.fig.text(0.98, 1,"Current data:\n" + currentDataString,
                  horizontalalignment='right',
                  verticalalignment='top',
                  multialignment='center',
                  transform = self.fig.axes[0].transAxes)
        
        
        
    def updateCurrentData(self):
        self.panel.currentData = self.panel.stockObj.getCurrent()
        
    def on_slider_width(self, event):
        self.panel.MovingAvgN = self.slider_width.GetValue()
        self.draw_figure()
    
    def on_new(self, event):
        prompt = wx.TextEntryDialog(self, "Enter new ticker", "New ticker",self.panel.stockObj.ticker)
        prompt.ShowModal() 
        try:
            self.panel.stockObj = stockInfo(prompt.GetValue())
            self.panel.fromDate = self.panel.stockObj.fromDate
            self.panel.toDate = self.panel.stockObj.toDate
            self.panel.Beta = Beta(self.panel.stockObj,self.panel.fromDate, self.panel.toDate)
            self.updateCurrentData()
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
                
        self.updateCurrentData()
        self.draw_figure()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png|PS (*.ps)|*.ps|JPG (*.jpg)|*.jpg"
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile= self.panel.stockObj.ticker+"plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.fig.get_dpi())
            self.flash_status_message("Saved to %s" % path)
        
    def on_exit(self, event):
        self.timeroff.Stop()
        #self.Close()
        self.Destroy()
        quit()
        
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
  

    
if __name__ == "__main__":
    app = wx.App(False)
    app.frame = initialFrame()
    app.frame.Show()
    app.MainLoop()
