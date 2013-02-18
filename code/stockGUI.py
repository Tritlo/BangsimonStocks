import wx
import warnings
import os
import matplotlib
import wx.lib.hyperlink as hl
import wx.lib.scrolledpanel
import wx.lib.calendar as cal
matplotlib.use('WXAgg')

from stockInfo import stockInfo
from stockPlot import stockPlot
from stockUtil import *
from stockAnalysis import Beta, BuyOrSell
from datetime import timedelta,date,datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

DEFAULT_TICKER = "GOOG"
DEFAULT_PERIOD = 52

class initialFrame(wx.Frame):
    """ The main frame of the application
    """
    title = "Bangsimon Stocks"
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.create_menu()
        self.create_status_bar()
        print "Fetching initial data"
        self.create_main_panel()
        
        print "Plotting initial data"
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
        options = ['Adj Close','Open' ,'High', 'Low', 'Close', 'Avg. Price']
        #Nennum ekki ad handsla inn.
        M = map( (lambda x: self.Bind(wx.EVT_MENU,self.plot_handler,
                                      plot.AppendRadioItem(-1,x))),options)
        plot.AppendSeparator()
        self.Bind(wx.EVT_MENU,self.plot_handler,plot.AppendCheckItem(-1, "Simple Moving Average"))
        self.Bind(wx.EVT_MENU,self.plot_handler,plot.AppendCheckItem(-1, "Volume"))


        dates = wx.Menu()
        self.Bind(wx.EVT_MENU,self.changeFromDate,dates.Append(-1, "Change From Date"))
        self.Bind(wx.EVT_MENU,self.changeToDate,dates.Append(-1, "Change To Date"))

        self.menubar.SetMenus([(menu_file,"&File"),(plot, "&Plot"),(dates,"&Dates")])
        self.SetMenuBar(self.menubar)
        

            

    def create_main_panel(self):
        """ Creates the main panel and everything"""
        self.panel = wx.Panel(self)
        self.panel.stockObj = stockInfo(DEFAULT_TICKER)
        
        #Setjum default value-in
        self.panel.currentAttr = "Adj Close"
        td = self.panel.stockObj.toDate - timedelta(weeks=DEFAULT_PERIOD)
        if self.panel.stockObj.validDate(td):
            self.panel.fromDate = td
        else:
            self.panel.fromDate = self.panel.stockObj.fromDate
            
        self.panel.toDate = self.panel.stockObj.toDate
        self.panel.MovingAvg = False
        self.panel.Volume = False
        self.panel.MovingAvgN = 20
        self.panel.Beta = Beta(self.panel.stockObj,self.panel.fromDate, self.panel.toDate)
        
        #Plottum i byrjun.
        self.fig = matplotlib.pyplot.gcf()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.slider_label = wx.StaticText(self.panel, -1, 
            "Moving Average N: ")
        self.slider_width = wx.Slider(self.panel, -1, 
            value=20, 
            minValue=20,
            maxValue=200,
            style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider_width.SetTickFreq(10, 1)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_width, self.slider_width)
        self.Bind(wx.EVT_COMMAND_SCROLL_CHANGED, self.on_slider_width, self.slider_width)

        #Toolbar of chart
        self.toolbar = NavigationToolbar(self.canvas)
        self.SetToolBar(self.toolbar)
        
        # Layout
        
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
        self.RssPanel = wx.lib.scrolledpanel.ScrolledPanel(self.panel)
        self.RssPanel.SetMinSize((-1,100))
        self.RssPanel.SetSizer(self.RssBox)
        self.updateRSS()
        
        self.RssBox.Fit(self.RssPanel)
        self.RssPanel.SetupScrolling()
        self.vbox.Add(self.RssPanel,1, flag= wx.EXPAND)
        self.panel.SetSizer(self.vbox)
        
        self.vbox.Fit(self)
        
        self.updateCurrentData()

    def updateRSS(self):
        """Fetches news for the graph"""
        self.RssBox.Clear()
        rss = self.panel.stockObj.getRSS()
        self.hyperlinks = map( (lambda p:hl.HyperLinkCtrl(self.RssPanel,wx.ID_ANY,label=str(p[0]),URL = str(p[1]))),rss)
        for i in self.hyperlinks:
            self.RssBox.Add(i,0,flag= wx.EXPAND)
        self.RssBox.Layout()
        
    def create_status_bar(self):
        """Creates the statusbar"""
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
        """Plots the graph"""
        self.flash_status_message("Plotting...")
        self.fig.clear()
        self.fig.subplots_adjust(top=0.82)
        self.fig = stockPlot(self.panel.stockObj,self.panel.currentAttr,
                                 self.panel.fromDate, self.panel.toDate,
                                 self.panel.MovingAvg, self.panel.MovingAvgN,
                                 self.panel.Volume)
        self.plotInformation()
        self.canvas.draw()
        self.flash_status_message("Plotting...Done")

    def plotInformation(self):
        """Prints additional data on graph"""
        self.updateCurrentData()
        self.fig.suptitle(self.panel.currentData['name'],fontsize="16",fontweight="bold")
        
        Cd = lambda c : str(self.panel.currentData[c])
        
        currentDataString1 = "Price: %s, Market Cap %s\n\
52 week high/low: %s/%s,\n\
Beta of period: %s" % (Cd('price'), Cd('market_cap'), Cd('52_week_high'), Cd('52_week_low'), str(self.panel.Beta))
        
        currentDataString2 = "Short ratio:%s, 50 MAvg: %s\n\
Earnings per share: %s\n\
Data indicates you should %s" % (Cd('short_ratio'), Cd('50day_moving_avg'), Cd('earnings_per_share'), self.panel.BuyOrSell)
        
        self.fig.text(0.13, 0.965,"Current:\n" + currentDataString1,
                  horizontalalignment='left',
                  verticalalignment='top',
                  multialignment='center',
                  transform = self.fig.axes[0].transAxes)
        
        self.fig.text(0.87, 0.965,"Current:\n" + currentDataString2,
                  horizontalalignment='right',
                  verticalalignment='top',
                  multialignment='center',
                  transform = self.fig.axes[0].transAxes)
        
    def updateCurrentData(self):
        """Fetches current data from yahoo"""
        self.panel.currentData = self.panel.stockObj.getCurrent()
        if BuyOrSell(self.panel.stockObj) == 1:
            self.panel.BuyOrSell = "buy"
        else:
            self.panel.BuyOrSell = "sell"
        
    def on_slider_width(self, event):
        """Handles the changing of the slider"""
        self.panel.MovingAvgN = self.slider_width.GetValue()
        self.draw_figure()
    
    def on_new(self, event):
        """Handles creating new tickers"""
        prompt = wx.TextEntryDialog(self, "Enter new ticker", "New ticker",self.panel.stockObj.ticker)
        prompt.ShowModal() 
        try:
            self.flash_status_message("Fetching data...")
            self.panel.stockObj = stockInfo(prompt.GetValue())
            self.flash_status_message("Fetching data...Done")
            if not (self.panel.stockObj.validDate(self.panel.fromDate) and self.panel.stockObj.validDate(self.panel.toDate)):
                td = self.panel.stockObj.toDate - timedelta(weeks=DEFAULT_PERIOD)
                if self.panel.stockObj.validDate(td):
                    self.panel.fromDate = td
                else:
                    self.panel.fromDate = self.panel.stockObj.fromDate
                self.panel.toDate = self.panel.stockObj.toDate
                
            self.panel.Beta = Beta(self.panel.stockObj,self.panel.fromDate, self.panel.toDate)
            self.updateCurrentData()
            self.updateRSS()
            self.draw_figure()
        except ValueError:
            msg = wx.MessageDialog(self, "Invalid Ticker", "Error", wx.OK|wx.ICON_ERROR)
            msg.ShowModal()
            self.on_new()
                                  
    def plot_handler(self,event):
        """Handles the changing of the plot"""
        mIs = event.GetEventObject().GetMenuItems()
        for mI in mIs:
            label = mI.GetItemLabelText()
            if mI.GetKind() is 2:
                if mI.IsChecked():
                    self.panel.currentAttr = label 
            # find whether sMA is on.
            if mI.GetKind() is 1:
                if label == "Simple Moving Average":
                    self.panel.MovingAvg = mI.IsChecked()
                if label == "Volume":
                    self.panel.Volume = mI.IsChecked()
                    
        self.updateCurrentData()
        self.draw_figure()

    def on_save_plot(self, event):
        """Handles the saving of the plot"""
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
        """Exits program"""
        self.timeroff.Stop()
        self.Destroy()
        quit()

    def changeFromDate(self,event):
        """Changes the from date of the graph"""
        day,month,year = self.panel.fromDate.day,self.panel.fromDate.month,self.panel.fromDate.year
        dlg = cal.CalenDlg(self.panel,month,day,year)
        dlg.y_spin.SetRange(self.panel.stockObj.fromDate.year,self.panel.stockObj.toDate.year)
        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            r = dlg.result
            r = r[3] + " " + r[2] + " " + r[1]
            resDate = datetime.strptime(r,"%Y %B %d").date()
        else:
            return

        
        if self.panel.stockObj.validDate(resDate):
            self.panel.fromDate = resDate
            self.panel.Beta = Beta(self.panel.stockObj,self.panel.fromDate, self.panel.toDate)
            self.draw_figure()
        else:
            msg = wx.MessageDialog(self, "Invalid Date, date must be within range %s to %s" % (self.panel.stockObj.fromDate,self.panel.stockObj.toDate), "Error", wx.OK|wx.ICON_ERROR)
            msg.ShowModal()
            self.changeFromDate(None)
             
    def changeToDate(self,event):
        """Changes the to date of the graph"""
        day,month,year = self.panel.toDate.day,self.panel.toDate.month,self.panel.toDate.year
        dlg = cal.CalenDlg(self.panel,month,day,year)
        dlg.y_spin.SetRange(self.panel.stockObj.fromDate.year,self.panel.stockObj.toDate.year)
        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            r = dlg.result
            r = r[3] + " " + r[2] + " " + r[1]
            resDate = datetime.strptime(r,"%Y %B %d").date()
        else:
            return
            
        if self.panel.stockObj.validDate(resDate):
            self.panel.toDate = resDate
            self.panel.Beta = Beta(self.panel.stockObj,self.panel.fromDate, self.panel.toDate)
            self.draw_figure()
        else:
            msg = wx.MessageDialog(self, "Invalid Date, date must be within range %s to %s" % (self.panel.stockObj.fromDate,self.panel.stockObj.toDate), "Error", wx.OK|wx.ICON_ERROR)
            msg.ShowModal()
            self.changeToDate(None)
        
    def flash_status_message(self, msg, flash_len_ms=1500):
        """Flashes status message on status bar"""
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
