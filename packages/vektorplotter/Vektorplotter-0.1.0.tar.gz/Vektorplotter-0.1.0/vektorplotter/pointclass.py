from listclass import ObjectLists
from colorAssignclass import ColorAssign
from nameAssignclass import NameAssign


class Point:
    __idTag = "poi"
    __idCount = 0

    def __init__(self, x=0, y=0, z=0, name=None, color=None, show=True, append=False):
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)
        self.show = show
        Point.__idCount += 1
        self.__id = str(self.__idTag+str(self.__idCount))
        if name is None:
            self.__name = NameAssign.getNewName()
        else:
            self.__name = name
        if color is None:
            self.__color = ColorAssign.getNewColor()
        else:
            self.__color = color
        if append:
            ObjectLists.appendObjDict({str(self.__id): self})
            ObjectLists.appendPoiList(self)


    def __del__(self):
        ColorAssign.removeColor(self.__color)
        NameAssign.removeName(self.__name)
        try:
            ObjectLists.removeFromPoiList(self)
            ObjectLists.removeFromObjDict(str(self.__id))
        except ValueError:
            pass

    def __str__(self):
        """Str method for testing purposes.
        Uses given Point instance, returns string."""
        return "("+str(self.__x)+"; "+str(self.__y)+"; "+str(self.__z)+")"

    def getX(self):
        """The get method for the x-komponent.
        Returns x as float."""
        return float(self.__x)

    def getY(self):
        """The get method for the y-komponent.
        Returns y as float."""
        return float(self.__y)

    def getZ(self):
        """The get method for the z-komponent.
        Returns z as float."""
        return float(self.__z)

    def getName(self):
        """The get method for the name.
        Returns name as string."""
        return str(self.__name)

    def getID(self):
        """The get method for the ID.
        Returns ID as string."""
        return str(self.__id)

    def getColor(self):
        """The get method for the color.
        Returns color as tuple of format:
        (Red, Green, Blue).
        Valuerange = 0 to 256"""
        return self.__color

    def setX(self, x=0):
        """The set method for the x-komponent.
        Takes x as float."""
        self.__x = float(x)

    def setY(self, y=0):
        """The set method for the y-komponent.
        Takes y as float."""
        self.__y = float(y)

    def setZ(self, z=0):
        """The set method for the z-komponent.
        Takes z as float."""
        self.__z = float(z)

    def setName(self, name):
        """The set method for the name.
        Takes name as string."""
        self.__name = str(name)

    def setColor(self, color):
        """The set method for the colour.
        Takes colour as tuple of format:
        (Red, Green, Blue).
        Valuerange = 0 to 256"""
        self.__color = color

    x = property(getX, setX)
    y = property(getY, setY)
    z = property(getZ, setZ)
    name = property(getName, setName)
