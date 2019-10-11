import wx
import wx.lib.scrolledpanel
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import numpy as np
import math
import serial
import sys
import conexion

class controlRobot(wx.Frame):
    def __init__(self, parent, title):
        super(controlRobot, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 6)

        # crea menu de abrir imagen
        self.menuBar = wx.MenuBar()
        self.Menu = wx.Menu()
        self.fileItem = self.Menu.Append(1, 'Conexión')
        self.Bind(wx.EVT_MENU, self.onBrowse, self.fileItem)
        self.SetMenuBar(self.menuBar)        

        self.photoTxt = ''

        # boton de ROI
        roiButton = wx.Button(self.panel, label='ROI',
        size=(140, 80))
        roiButton.Bind(wx.EVT_BUTTON, self.regionOfInterest)
        self.sizer.Add(roiButton, pos=(0, 0), span=(2, 0),
        flag=wx.BOTTOM | wx.TOP | wx.LEFT, border=25)

        # textos que muestran las coordenadas usadas para ROI
        self.textoCoordenadas = wx.StaticText(self.panel, label='(X, Y) = ')
        self.sizer.Add(self.textoCoordenadas, pos=(2, 0),
        flag = wx.TOP | wx.LEFT, border=25)
        self.punto1 = (0, 0)
        self.punto2 = (-1, -1)
        self.estadoPunto1 = False  # indica si ya se eligio una coordenada o no en el punto1
        self.estadoPunto2 = False  # indica si ya se eligio una coordenada o no en el punto2
        self.punto1Text = wx.StaticText(self.panel, label='P1 = ')
        self.punto2Text = wx.StaticText(self.panel, label='P2 = ')
        self.sizer.Add(self.punto1Text, pos=(0, 1), flag = wx.TOP, border=30)
        self.sizer.Add(self.punto2Text, pos=(1, 1), flag=wx.TOP, border=30)

        # texto y cuadrado (panel) que cambia de color
        st1 = wx.StaticText(self.panel, label='Color: ')
        self.sizer.Add(st1, pos=(3, 0), flag=wx.TOP | wx.LEFT, border=25)
        self.colorPanel = wx.Panel(self.panel, size=(60, 60),
        style=wx.BORDER_SUNKEN)
        self.sizer.Add(self.colorPanel, pos=(3, 1),
          flag=wx.TOP | wx.LEFT, border=10)

        # textos que indican valor rgb
        self.st2 = wx.StaticText(self.panel, label='Valores Color')
        self.sizer.Add(self.st2, pos=(4, 0), flag=wx.LEFT, border=25)
        self.st3 = wx.StaticText(self.panel, label='.')
        self.sizer.Add(self.st3, pos=(5, 0),
        flag=wx.LEFT | wx.BOTTOM, border=25)

        # botón para volver a la imagen original
        originalButton = wx.Button(self.panel, label='Volver a original',
        size=(140, 80))
        originalButton.Bind(wx.EVT_BUTTON, self.volverOriginal)
        self.sizer.Add(originalButton, pos=(6, 0), span=(0, 0),
        flag=wx.BOTTOM | wx.TOP | wx.LEFT, border=25)

        # label de umbralización manual
        self.umbralizarLabel = wx.StaticText(self.panel, label='Intensidad de umbralización: ')
        self.sizer.Add(self.umbralizarLabel, pos=(7, 0), flag=wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.TOP | wx.LEFT, border=25)

        # cuadro de texto para umbralizar manualmente
        self.textoUmbralizar = wx.TextCtrl(self.panel, size=(40, 20), style=wx.TE_RIGHT)
        self.sizer.Add(self.textoUmbralizar, pos=(7, 1), span=(0, 0),
        flag=wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.TOP, border=25)

        # botón para umbralizar manualmente
        self.umbralizarButton = wx.Button(self.panel, label='Umbralizar',
        size=(80, 40))
        self.umbralizarButton.Bind(wx.EVT_BUTTON, self.umbralizarManual)
        self.sizer.Add(self.umbralizarButton, pos=(8, 0), span=(0, 0),
        flag=wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.BOTTOM | wx.LEFT, border=25)

        # se esconden los últimos 3 controles creados
        self.umbralizarLabel.Hide()
        self.umbralizarButton.Hide()
        self.textoUmbralizar.Hide()

        # panel donde deberia ir la imagen
        self.panelDeImagen = wx.lib.scrolledpanel.ScrolledPanel(self.panel , -1,
        size=(600, 600), style=wx.SIMPLE_BORDER)
        self.panelDeImagen.SetBackgroundColour('#FFFFFF')
        self.sizer.Add(self.panelDeImagen, pos=(0, 2), span=(9, 1),
        flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=25)

        # sizer dentro del panel de la imagen
        vbox = wx.BoxSizer(wx.VERTICAL)
        img = wx.Image(600, 600)
        self.imgCtrl = wx.StaticBitmap(self.panelDeImagen, wx.ID_ANY,
        wx.Bitmap(img), size=(600, 600))
        vbox.Add(self.imgCtrl, 0, flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT
        , border=25)
        self.imgCtrl.Bind(wx.EVT_MOTION, self.mouseOnPicture)
        self.imgCtrl.Bind(wx.EVT_LEFT_DOWN, self.clickIzquierdo)
        self.panelDeImagen.SetSizer(vbox)
        self.panelDeImagen.SetupScrolling()

        # integra el sizer y el panel
        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def onBrowse():
        print("no hago nada")


def main():
    app = wx.App()
    vp = controlRobot(None, title='Python Scorbot')
    vp.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()



