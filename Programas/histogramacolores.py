import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class ventanaHistograma(wx.Frame):

    def __init__(self, parent, title):
        super(ventanaHistograma, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)
        self.PhotoMaxSizeH = 450   # horizontal
        self.PhotoMaxSizeV = 300   # vertical
        self.sizer = wx.GridBagSizer(7, 7)

        # AGREGA BOTON PARA ABRIR LA IMAGEN (SU EVENTO ESTA MAS ABAJO)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))
        imageButton = wx.Button(self.panel, label='Abrir imagen',
        size=(140, 80))
        imageButton.Bind(wx.EVT_BUTTON, self.onBrowse)
        self.sizer.Add(imageButton, pos=(0, 0), span=(1, 1),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=40)

        # BOTON PARA OBTENER HISTOGRAMA DE ROJO
        RedButton = wx.Button(self.panel, label='Histograma de RED',
        size=(140, 50))
        RedButton.Bind(wx.EVT_BUTTON, self.reemplazaRed)
        self.sizer.Add(RedButton, pos=(1, 0), span=(1, 1),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        # BOTON PARA OBTENER HISTOGRAMA DE VERDE
        GreenButton = wx.Button(self.panel, label='Histograma de GREEN',
        size=(140, 50))
        GreenButton.Bind(wx.EVT_BUTTON, self.reemplazaGreen)
        self.sizer.Add(GreenButton, pos=(2, 0), span=(1, 1),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        # BOTON PARA OBTENER HISTOGRAMA DE AZUL
        BlueButton = wx.Button(self.panel, label='Histograma de BLUE',
        size=(140, 50))
        BlueButton.Bind(wx.EVT_BUTTON, self.reemplazaBlue)
        self.sizer.Add(BlueButton, pos=(3, 0), span=(1, 1),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        # LUGAR DONDE DEBERIA IR LA IMAGEN
        self.img = wx.Image(450, 300)
        self.imgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
             wx.Bitmap(self.img), size=(450, 300))
        self.sizer.Add(self.imgCtrl, pos=(0, 1), span=(0, 0),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=20)

        # HISTOGRAMA CON VALORES DE EJEMPLO
        self.histograma = hist(self.panel, [1, 5, 8, 5, 10, 1, 1, 8, 3, 7],
        range(15))
        self.sizer.Add(self.histograma, pos=(1, 1), span=(3, 0),
            flag=wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def onBrowse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard,
                                style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()

    def onView(self):
        filepath = self.photoTxt.GetValue()
        self.img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        # ESCALA LA IMAGEN MANTENIENDO SUS PROPORCIONES
        W = self.img.GetWidth()
        H = self.img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSizeH
            NewH = self.PhotoMaxSizeH * H / W
        else:
            NewH = self.PhotoMaxSizeV
            NewW = self.PhotoMaxSizeV * W / H
        self.img = self.img.Scale(NewW, NewH)

        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()

    def getRedValues(self):
        lista = []
        for i in range(self.img.GetWidth()):
            for j in range(self.img.GetHeight()):
                lista.append(self.img.GetRed(i, j))
        return lista

    def getGreenValues(self):
        lista = []
        for i in range(self.img.GetWidth()):
            for j in range(self.img.GetHeight()):
                lista.append(self.img.GetGreen(i, j))
        return lista

    def getBlueValues(self):
        lista = []
        for i in range(self.img.GetWidth()):
            for j in range(self.img.GetHeight()):
                lista.append(self.img.GetBlue(i, j))
        return lista

    def reemplazaRed(self, event):
        self.histograma.replaceHist(self.getRedValues(), range(256), 'crimson')

    def reemplazaGreen(self, event):
        self.histograma.replaceHist(self.getGreenValues(), range(256), 'green')

    def reemplazaBlue(self, event):
        self.histograma.replaceHist(self.getBlueValues(), range(256), 'blue')


# clase de un panel con histograma dentro
class hist(wx.Panel):
    def __init__(self, parent, list1, list2):
        wx.Panel.__init__(self, parent, -1, size=(600, 600))

        self.bins = list2

        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.hist(list1, self.bins)
        self.canvas = FigureCanvas(self, -1, self.figure)

    def replaceHist(self, list1, list2, colorH):
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.hist(list1, list2, color=colorH)
        self.canvas = FigureCanvas(self, -1, self.figure)


def main():
    app = wx.App()
    vp = ventanaHistograma(None, title='Histograma')
    vp.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()