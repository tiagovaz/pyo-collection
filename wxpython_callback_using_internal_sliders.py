#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.SetMinSize((300,150))
        self.panel = MyPanel(self)

class MyPanel(wx.Panel):
    def __init__(self, parent, id=-1, pos=(25,25), size=(500,400)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)
        self.slide = wx.Slider(self, minValue=20, maxValue=1000, value=500, 
                            size=(250,-1), style=wx.SL_LABELS)
        self.slide.Bind(wx.EVT_ENTER_WINDOW, self.enter_window)
        self.slide.Bind(wx.EVT_LEAVE_WINDOW, self.leave_window)
        self.slide.Bind(wx.EVT_SLIDER, self.onSlider)
        box.Add(self.slide, 0, wx.EXPAND | wx.ALL, 5)
    
        box.AddSpacer(50)
        self.slide2 = ControlSlider(self, 0.001, 1, log=True, outFunction=self.onSlider2)
        box.Add(self.slide2, 0, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(box)

    def onSlider2(self, value):
        print value

    def onSlider(self, evt):
        a.freq = evt.GetInt()

    def enter_window(self, evt):
        print "enter window..."
        sl = evt.GetEventObject()
        print sl.GetValue()

    def leave_window(self, evt):
        print "leave window..."
        sl = evt.GetEventObject()
        print sl.GetValue()

s = Server().boot().start()

a = Sine(freq=500, mul=0.2).out()

app = wx.PySimpleApp()
mainFrame = MyFrame(None, title='Simple App', pos=(100,100), size=(500,300))
mainFrame.Show()
app.MainLoop()
