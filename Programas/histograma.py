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
        self.sizer = wx.GridBagSizer(6, 6)

        # agrega boton para cargar matriz
        cargaButton = wx.Button(self.panel, label='Cargar matriz',
        size=(140, 80))
        cargaButton.Bind(wx.EVT_BUTTON, self.cargaMatriz)
        self.sizer.Add(cargaButton, pos=(0, 0), span=(0, 2),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        self.histograma = hist(self.panel, [1, 5, 8, 5, 10, 1, 1, 8, 3, 7],
        range(15))
        self.sizer.Add(self.histograma, pos=(1, 0),
            flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)

# carga la matriz y además reemplaza el histograma con los nuevos datos
    def cargaMatriz(self, event):
        fh = open("matriz.txt", "r")
        data = fh.readlines()

        listaSimple = list()
        for line in data:
            for num in line.split():
                listaSimple.append(int(num))

        self.histograma.replaceHist(listaSimple, range(256))
        self.panel.Refresh()


# clase de un panel con histograma dentro
class hist(wx.Panel):
    def __init__(self, parent, list1, list2):
        wx.Panel.__init__(self, parent, -1, size=(600, 600))

        self.bins = list2

        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_axes([0, 0, 1, 1])
        self.axes.hist(list1, self.bins)
        self.canvas = FigureCanvas(self, -1, self.figure)

    def replaceHist(self, list1, list2):
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.hist(list1, list2)
        self.canvas = FigureCanvas(self, -1, self.figure)


def main():
    app = wx.App()
    vp = ventanaHistograma(None, title='Histograma')
    vp.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
