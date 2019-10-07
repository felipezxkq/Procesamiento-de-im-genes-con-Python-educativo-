import wx
import wx.lib.scrolledpanel
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import numpy as np
import math


class procesamientoImagenes(wx.Frame):

    def __init__(self, parent, title):
        super(procesamientoImagenes, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

        self.esBlancoNegro = True

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(6, 6)

        # crea menu de abrir imagen
        self.menuBar = wx.MenuBar()
        self.Menu = wx.Menu()
        self.fileItem = self.Menu.Append(wx.ID_OPEN, '&Abrir imagen')
        self.Bind(wx.EVT_MENU, self.onBrowse, self.fileItem)
        self.SetMenuBar(self.menuBar)

        # crea menu de escala de grises
        self.menuGrises = wx.Menu()
        self.menuGrises.Append(2, 'Metodo ponderado')
        self.menuGrises.Append(3, 'Metodo luminosity')

        wx.EVT_MENU(self, 2, self.convertir)
        wx.EVT_MENU(self, 3, self.convertirLuminosity)

        # menu de histogramas
        self.menuHistogramas = wx.Menu()
        self.menuHistogramas.Append(4, 'Histograma de RED')
        self.menuHistogramas.Append(5, 'Histograma de GREEN')
        self.menuHistogramas.Append(6, 'Histograma de BLUE')
        wx.EVT_MENU(self, 4, self.mostrarHistogramaRojo)
        wx.EVT_MENU(self, 5, self.mostrarHistogramaVerde)
        wx.EVT_MENU(self, 6, self.mostrarHistogramaAzul)

        # menu de ecualizacion
        self.menuEcualizacion = wx.Menu()
        self.menuEcualizacion.Append(7, 'Ecualizar')
        wx.EVT_MENU(self, 7, self.ecualizar)

        # menu de umbralizacion
        self.menuUmbralizacion = wx.Menu()
        self.menuUmbralizacion.Append(8, 'Umbralizar automático')
        self.menuUmbralizacion.Append(9, 'Umbralizar manual')
        wx.EVT_MENU(self, 8, self.umbralizar)
        wx.EVT_MENU(self, 9, self.mostrarumbralizarManual)

        self.menuBar.Append(self.Menu, '&Imagen')
        self.menuBar.Append(self.menuGrises, '&Escala de grises')
        self.menuBar.Append(self.menuHistogramas, '&Histogramas')
        self.menuBar.Append(self.menuEcualizacion, '&Ecualizacion')
        self.menuBar.Append(self.menuUmbralizacion, '&Umbralizacion')

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

    # metodo usado en el boton de abrir imagen
    def onBrowse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard,
                                style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt = dialog.GetPath()
        dialog.Destroy()
        self.onView()

    # metodo usado para mostrar la imagen
    def onView(self):
        filepath = self.photoTxt
        self.img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        # estados de punto 1 y 2 usados en ROI
        self.estadoPunto1 = False
        self.estadoPunto2 = False

        self.imgOriginal = self.img.Copy()

        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()

        # revisa si la imagen esta en escala de grises
        r = 0
        g = 0
        b = 0
        width = self.img.GetWidth()
        height = self.img.GetHeight()
        for i in range(width):
            for j in range(height):
                r = self.img.GetRed(i, j)
                g = self.img.GetGreen(i, j)
                b = self.img.GetBlue(i, j)
                if(r != b or r != g):
                    self.esBlancoNegro = False
                    break

        # obtiene ancho y alto de la imagen inmediatamente (para usarlas despues)
        self.width = self.img.GetWidth()
        self.height = self.img.GetHeight()

    # convierte a escala de grises con una ponderacion normal
    def convertir(self, event):
        for i in range(self.width):
            for j in range(self.height):
                redW = round(self.imgOriginal.GetRed(i, j) * 0.333, 0)
                greenW = round(self.imgOriginal.GetGreen(i, j) * 0.333, 0)
                blueW = round(self.imgOriginal.GetBlue(i, j) * 0.333, 0)
                x = int(redW + greenW + blueW)

                self.img.SetRGB(i, j, x, x, x)

        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()
        self.esBlancoNegro = True

    # convierte a gris usando la ponderacion "luminosity"
    def convertirLuminosity(self, event):
        for i in range(self.width):
            for j in range(self.height):
                redW = round(self.imgOriginal.GetRed(i, j) * 0.21, 0)
                greenW = round(self.imgOriginal.GetGreen(i, j) * 0.72, 0)
                blueW = round(self.imgOriginal.GetBlue(i, j) * 0.07, 0)
                x = int(redW + greenW + blueW)

                self.img.SetRGB(i, j, x, x, x)
        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()
        self.esBlancoNegro = True

    def mouseOnPicture(self, event):
        x, y = event.GetPosition()

        # pone los valores RGB en texto
        self.st3.SetLabel("R: " + str(self.img.GetRed(x, y)) + ", G: " +
        str(self.img.GetGreen(x, y)) + ", B: " + str(self.img.GetBlue(x, y)))

        # muestra las coordenadas
        self.textoCoordenadas.SetLabel("(X, Y) = ("+str(x)+", "+str(y)+")")

        # pinta un cuadrado (panel) con el valor rgb
        self.colorPanel.SetBackgroundColour(wx.Colour(self.img.GetRed(x, y),
        self.img.GetGreen(x, y), self.img.GetBlue(x, y)))
        self.colorPanel.Refresh()

    def clickIzquierdo(self, event):
        x, y = event.GetPosition()

        # si es que ninguno de los puntos hay coordenadas, entonces llena coordenadas en el punto1
        if not self.estadoPunto1 and not self.estadoPunto2:
            self.punto1Text.SetLabel("P1 = "+"("+str(x)+", "+str(y)+")")
            self.punto1 = x, y
            self.estadoPunto1 = True
        elif self.estadoPunto1 and not self.estadoPunto2:  # si solo hay coordenadas en el punto1
            self.punto2Text.SetLabel("P2 = "+"("+str(x)+", "+str(y)+")")
            self.punto2 = x, y
            self.estadoPunto2 = True

    # metodo del boton de ROI
    def regionOfInterest(self, event):
        # que los dos puntos esten definidos
        if self.estadoPunto1 and self.estadoPunto2:
            self.img = self.img.GetSubImage(wx.Rect(topLeft = self.punto1, bottomRight = self.punto2))
            self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
            self.panel.Refresh()
            self.estadoPunto1 = False
            self.estadoPunto2 = False
            self.width = self.img.GetWidth()
            self.height = self.img.GetHeight()

    # metodo del boton de volver a imagen original
    def volverOriginal(self, event):
        self.img = self.imgOriginal
        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()
        self.estadoPunto1 = False
        self.estadoPunto2 = False
        self.width = self.img.GetWidth()
        self.height = self.img.GetHeight()

    # Funciones usadas para hacer los histogramas
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

    def mostrarHistogramaRojo(self, event):
        self.histo = Histograma(self, self.getRedValues(), list(range(256)),
        'crimson')
        self.histo.Show()

    def mostrarHistogramaVerde(self, event):
        self.histo = Histograma(self, self.getGreenValues(),
        list(range(256)), 'green')
        self.histo.Show()

    def mostrarHistogramaAzul(self, event):
        self.histo = Histograma(self, self.getBlueValues(),
        list(range(256)), 'blue')
        self.histo.Show()

    def ecualizar(self, event):
        if self.esBlancoNegro:
            intensidades_desordenadas = self.getBlueValues()
            intensidades_ordenadas = np.zeros(256, dtype=int)  # crea una lista con 255 índices con valor 0
            for i in range(len(intensidades_desordenadas)):
                intensidades_ordenadas[intensidades_desordenadas[i]] += 1  # suma 1 por cada píxel con este valor

            intensidades_acumuladas = intensidades_ordenadas.copy()
            for i in np.arange(1, 256):
                intensidades_acumuladas[i] = intensidades_acumuladas[i - 1] + intensidades_acumuladas[i]

            pixeles = self.width * self.height  # cantidad total de pixeles

            for i in range(self.width):
                for j in range(self.height):
                    intensidad = self.img.GetRed(i, j)  # obtiene la intensidad en red en el punto (i, j) de la imagen
                    nueva_intesidad = math.floor(intensidades_acumuladas[intensidad] * 255.0 / pixeles)
                    self.img.SetRGB(i, j, int(nueva_intesidad), int(nueva_intesidad), int(nueva_intesidad))  # convierte el punto a la intensidad que se obtuvo en b

            self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
            self.panel.Refresh()
        else:
            # con blue
            intensidades_desordenadas_blue = self.getBlueValues()
            intensidades_ordenadas_blue = np.zeros(256, dtype=int)
            for i in range(len(intensidades_desordenadas_blue)):
                intensidades_ordenadas_blue[intensidades_desordenadas_blue[i]] += 1
            intensidadesAcumB = intensidades_ordenadas_blue.copy()
            for i in np.arange(1, 256):
                intensidadesAcumB[i] = intensidadesAcumB[i - 1] + intensidadesAcumB[i]

            # con red
            intensidadesDesR = self.getRedValues()
            intensidadesOrdR = np.zeros(256, dtype=int)
            for i in range(len(intensidadesDesR)):
                intensidadesOrdR[intensidadesDesR[i]] += 1
            intensidadesAcumR = intensidadesOrdR.copy()
            for i in np.arange(1, 256):
                intensidadesAcumR[i] = intensidadesAcumR[i - 1] + intensidadesAcumR[i]

            # con green
            intensidadesDesG = self.getGreenValues()
            intensidadesOrdG = np.zeros(256, dtype=int)
            for i in range(len(intensidadesDesG)):
                intensidadesOrdG[intensidadesDesG[i]] += 1
            intensidadesAcumG = intensidadesOrdG.copy()
            for i in np.arange(1, 256):
                intensidadesAcumG[i] = intensidadesAcumG[i - 1] + intensidadesAcumG[i]

            pixeles = self.width * self.height

            for i in range(self.width):
                for j in range(self.height):
                    xR = self.img.GetRed(i, j)
                    yR = math.floor(intensidadesAcumR[xR] * 255.0 / pixeles)
                    xG = self.img.GetGreen(i, j)
                    yG = math.floor(intensidadesAcumG[xG] * 255.0 / pixeles)
                    xB = self.img.GetBlue(i, j)
                    yB = math.floor(intensidadesAcumB[xB] * 255.0 / pixeles)
                    self.img.SetRGB(i, j, int(yR), int(yG), int(yB))

            self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
            self.panel.Refresh()

    def umbralizar(self, event):
        if self.esBlancoNegro:
            intensidadesDes = self.getGreenValues()
            intensidadesOrd = np.zeros(256, dtype=int)
            for i in range(len(intensidadesDes)):
                intensidadesOrd[intensidadesDes[i]] += 1

            umbral = 0
            largo = len(intensidadesOrd)
            areaBajoCurva = 0
            pixelesTotales = self.width * self.height

            for i in range(largo):
                areaBajoCurva += intensidadesOrd[i] * i
            umbral = areaBajoCurva / pixelesTotales

            flag = True
            while flag:
                pixelsBackground = 0
                totalPixelsBG = 0
                pixelsForeground = 0
                totalPixelsFG = 0

                for i in range(int(umbral)):
                    pixelsBackground += i * intensidadesOrd[i]
                    totalPixelsBG += intensidadesOrd[i]
                pixelsForeground = areaBajoCurva - pixelsBackground
                totalPixelsFG = pixelesTotales - totalPixelsBG

                t = pixelsBackground / totalPixelsBG
                t = t + pixelsForeground / totalPixelsFG
                t = t / 2

                if umbral == t:
                    flag = False
                else:
                    umbral = t

            for i in range(self.width):
                for j in range(self.height):
                    if self.img.GetRed(i, j) < umbral:
                        self.img.SetRGB(i, j, 0, 0, 0)
                    else:
                        self.img.SetRGB(i, j, 255, 255, 255)

        else: # para una imagen en colores, red primero
            intensidadesDes = self.getRedValues()
            intensidadesOrd = np.zeros(256, dtype=int)
            for i in range(len(intensidadesDes)):
                intensidadesOrd[intensidadesDes[i]] += 1

            umbralRed = 0
            largo = len(intensidadesOrd)
            areaBajoCurva = 0
            pixelesTotales = self.width * self.height

            for i in range(largo):
                areaBajoCurva += intensidadesOrd[i] * i
            umbralRed = areaBajoCurva / pixelesTotales

            flag = True
            while flag:
                pixelsBackground = 0
                totalPixelsBG = 0
                pixelsForeground = 0
                totalPixelsFG = 0

                for i in range(int(umbralRed)):
                    pixelsBackground += i * intensidadesOrd[i]
                    totalPixelsBG += intensidadesOrd[i]
                pixelsForeground = areaBajoCurva - pixelsBackground
                totalPixelsFG = pixelesTotales - totalPixelsBG

                t = pixelsBackground / totalPixelsBG
                t = t + pixelsForeground / totalPixelsFG
                t = t / 2

                if umbralRed == t:
                    flag = False
                else:
                    umbralRed = t

            # green
            intensidadesDes = self.getGreenValues()
            intensidadesOrd = np.zeros(256, dtype=int)
            for i in range(len(intensidadesDes)):
                intensidadesOrd[intensidadesDes[i]] += 1

            umbralGreen = 0
            largo = len(intensidadesOrd)
            areaBajoCurva = 0
            pixelesTotales = self.width * self.height

            for i in range(largo):
                areaBajoCurva += intensidadesOrd[i] * i
            umbralGreen = areaBajoCurva / pixelesTotales

            flag = True
            while flag:
                pixelsBackground = 0
                totalPixelsBG = 0
                pixelsForeground = 0
                totalPixelsFG = 0

                for i in range(int(umbralGreen)):
                    pixelsBackground += i * intensidadesOrd[i]
                    totalPixelsBG += intensidadesOrd[i]
                pixelsForeground = areaBajoCurva - pixelsBackground
                totalPixelsFG = pixelesTotales - totalPixelsBG

                t = pixelsBackground / totalPixelsBG
                t = t + pixelsForeground / totalPixelsFG
                t = t / 2

                if umbralGreen == t:
                    flag = False
                else:
                    umbralGreen = t

            # BLUE
            intensidadesDes = self.getBlueValues()
            intensidadesOrd = np.zeros(256, dtype=int)
            for i in range(len(intensidadesDes)):
                intensidadesOrd[intensidadesDes[i]] += 1

            umbralBlue = 0
            largo = len(intensidadesOrd)
            areaBajoCurva = 0
            pixelesTotales = self.width * self.height

            for i in range(largo):
                areaBajoCurva += intensidadesOrd[i] * i
            umbralBlue = areaBajoCurva / pixelesTotales

            flag = True
            while flag:
                pixelsBackground = 0
                totalPixelsBG = 0
                pixelsForeground = 0
                totalPixelsFG = 0

                for i in range(int(umbralBlue)):
                    pixelsBackground += i * intensidadesOrd[i]
                    totalPixelsBG += intensidadesOrd[i]
                pixelsForeground = areaBajoCurva - pixelsBackground
                totalPixelsFG = pixelesTotales - totalPixelsBG

                t = pixelsBackground / totalPixelsBG
                t = t + pixelsForeground / totalPixelsFG
                t = t / 2

                if umbralBlue == t:
                    flag = False
                else:
                    umbralBlue = t


            for i in range(self.width):
                for j in range(self.height):
                    r = 0
                    g = 0
                    b = 0
                    if self.img.GetRed(i, j) > umbralRed:
                        r = 255
                    if self.img.GetGreen(i, j) > umbralGreen:
                        g = 255
                    if self.img.GetBlue(i, j) > umbralBlue:
                        b = 255
                    self.img.SetRGB(i, j, r, g, b)

        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()

    def umbralizarManual(self, event):
        umbral = (int)(self.textoUmbralizar.GetValue())
        for i in range(self.width):
                for j in range(self.height):
                    if self.img.GetRed(i, j) < umbral:
                        self.img.SetRGB(i, j, 0, 0, 0)
                    else:
                        self.img.SetRGB(i, j, 255, 255, 255)
        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()

    def mostrarumbralizarManual(self, event):
        self.umbralizarLabel.Show()
        self.umbralizarButton.Show()
        self.textoUmbralizar.Show()



class Histograma(wx.Frame):
    def __init__(self, parent, list1, list2, colorH):
        wx.Frame.__init__(self, None, size=(600, 550), title='Histograma')
        self.parent = parent

        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.hist(list1, list2, color=colorH)
        self.canvas = FigureCanvas(self, -1, self.figure)



def main():
    app = wx.App()
    vp = procesamientoImagenes(None, title='Procesamiento de imagenes')
    vp.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()