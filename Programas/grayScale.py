import wx


class ventanaGrayScale(wx.Frame):

    def __init__(self, parent, title):
        super(ventanaGrayScale, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)
        self.PhotoMaxSize = 600
        self.sizer = wx.GridBagSizer(6, 6)

        # AGREGA BOTON PARA ABRIR LA IMAGEN (SU EVENTO ESTÁ MAS ABAJO)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))
        imageButton = wx.Button(self.panel, label='Abrir imagen',
        size=(140, 80))
        imageButton.Bind(wx.EVT_BUTTON, self.onBrowse)
        self.sizer.Add(imageButton, pos=(0, 0), span=(0, 2),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        # AGREGA BOTON PARA CAMBIAR LA IMAGEN A SU ESCALA DE GRISES
        escalaButton = wx.Button(self.panel,
        label='Convertir a \nescala de grises',
        size=(140, 80))
        escalaButton.Bind(wx.EVT_BUTTON, self.convertir)
        self.sizer.Add(escalaButton, pos=(1, 0), span=(0, 2),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        # LUGAR DONDE DEBERIA IR LA IMAGEN
        img = wx.Image(600, 600)
        self.imgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
             wx.Bitmap(img), size=(600, 600))
        self.sizer.Add(self.imgCtrl, pos=(0, 2), span=(4, 2),
        flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=25)

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
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        self.img = self.img.Scale(NewW, NewH)

        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()

    def convertir(self, event):

        width = self.img.GetWidth()
        height = self.img.GetHeight()

        # Metodo de ponderaciones para transformar rgb a grayscale
        for i in range(width):
            for j in range(height):
                redW = round(self.img.GetRed(i, j) * 0.333, 0)
                greenW = round(self.img.GetGreen(i, j) * 0.333, 0)
                blueW = round(self.img.GetBlue(i, j) * 0.333, 0)
                x = redW + greenW + blueW

                self.img.SetRGB(i, j, x, x, x)
        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()


def main():
    app = wx.App()
    vp = ventanaGrayScale(None, title='Escala de grises')
    vp.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()