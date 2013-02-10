import wx

class finnsi(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Bangsimon',size=(800,600))
        panel=wx.Panel(self)


        status=self.CreateStatusBar()
        menubar=wx.MenuBar()
        first=wx.Menu()
        save=wx.Menu()
        third=wx.Menu()
        plot=wx.Menu()
        first.Append(wx.NewId(),"New Window","This opens a new window" )
        first.Append(wx.NewId(),"Open","Opens saved graphs and data" )
        
        menubar.Append(first,"File")
        menubar.Append(third,"Actions")
        save.Append(wx.NewId(),"Graph","This will save the graph" )
        save.Append(wx.NewId(),"Data","This will save the data" )
        plot.Append(wx.NewId(),"Simple Moving Average","Plots Simple Moving Average" )
        plot.Append(wx.NewId(),"Beta","Plot Beta" )
        third.Append(wx.NewId(),"News","Shows the news" )

        first.AppendMenu(wx.NewId(), 'Save', save)
        third.AppendMenu(wx.NewId(), 'Plot', plot)
        
        self.SetMenuBar(menubar)
        #self.Bind(wx.EVT_MENU


if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=finnsi(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
        
