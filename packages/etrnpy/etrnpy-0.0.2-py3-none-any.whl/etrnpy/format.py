import arcpy

class Format:

    @staticmethod
    def clean_name (NameIN):
        Remove = ["`", "~","!","@","#","$","%","^","&","*",".","(",")","-","+", "=", "[", "]", "{", "}", "\\", "|", ";", ":", "'", '"', "<", ",", ">", "/", "?","*","]"]
        NameIN = NameIN.replace(" ", "_")
        NameIN = NameIN.replace("__", "_")
        for x in Remove:
            if x in NameIN:
                NameIN = NameIN.replace(x, "")
        return NameIN

    @staticmethod
    def format_name(NameIn):
        if '&' in NameIn:
            NameIn = NameIn.replace("&", "and")
        if 'And' in NameIn:
            NameIn = NameIn.replace('And', 'and')
        if '.' in NameIn:
            NameIn = NameIn.replace('.', '')
        return NameIn

    @staticmethod
    def remove_space (NameIN):
        NameIN = NameIN.replace(" ", "_")
        return NameIN