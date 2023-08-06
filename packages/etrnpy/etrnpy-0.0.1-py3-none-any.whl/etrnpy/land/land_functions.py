import arcpy

class land_functions:

    @staticmethod
    def buffer_features(original_feature, new_feature, buffer_distance):
        arcpy.Buffer_analysis(original_feature, new_feature, buffer_distance)

    @staticmethod
    def clip_features(original_feature, path, new_feature):
        arcpy.Clip_analysis(original_feature, clip_feature, new_feature)

    @staticmethod
    def feature_class_to_feature_class(original_feature, path, new_feature, definition_query):
        arcpy.FeatureClassToFeatureClass_conversion(original_feature, path, new_feature, definition_query)

    
    @staticmethod
    def msgLog(msg):
        # print(msg)
        arcpy.AddMessage(msg)

    @staticmethod
    def errLog(msg):
        # print(msg)
        arcpy.AddError(msg)

    @staticmethod
    def remove_space (NameIN):
        NameIN = NameIN.replace(" ", "_")
        return NameIN

    @staticmethod
    def clean_name (NameIN):
        Remove = ["`", "~","!","@","#","$","%","^","&","*",".","(",")","+", "=", "[", "]", "{", "}", "\\", "|", ";", ":", "'", '"', "<", ".", ">", "/", "?","*","]"]
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
            NameIn = NameIn.replace('.', '_')
        if '__' in NameIn:
            NameIn = NameIn.replace('__', '_')
        return NameIn

    @staticmethod
    def get_count(source):

        """Returns the count of selected features or table rows"""

        result = arcpy.GetCount_management(source)
        count = int(result.getOutput(0))
        return count

    @staticmethod
    def get_query(GID):
        GIDS = ""
        for G in GID:
            GIDS += str(G) + "', '"
        where_clause  = "APN IN ('" + GIDS[:-3] + ")"
        return where_clause

    @staticmethod
    def get_query_MVP(GID):
        GIDS = ""
        for G in GID:
            GIDS += str(G) + "', '"
        where_clause  = "TRACTID IN ('" + GIDS[:-3] + ")"
        return where_clause

    @staticmethod
    def get_linename_query(line_name_list):
        line_names = ""
        for line_name in line_name_list:
            line_names += str(line_name) + "', '"
        where_clause  = "LINENAME IN ('" + line_names[:-3] + ")"
        return where_clause

    @staticmethod
    def get_linename_like_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ")"
        return where_clause

    @staticmethod
    def get_parcel_query(parcelNumber):
        if ',' in parcelNumber:
            parcelNumber = parcelNumber.replace(",", "', '")
        return parcelNumber

    @staticmethod
    def get_accessroute_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ") AND ACCESSTYPE IN (2, 3)"
        return where_clause

    @staticmethod
    def get_temp_accessroute_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ") AND ACCESSTYPE IN (2)"
        return where_clause

    @staticmethod
    def get_perm_accessroute_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ") AND ACCESSTYPE IN (3)"
        return where_clause

    @staticmethod
    def get_lod_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ") AND LODTYPE IN (1,2)"
        return where_clause

    @staticmethod
    def get_temp_lod_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ") AND LODTYPE IN (2)"
        return where_clause

    @staticmethod
    def get_perm_lod_query(line_name_list):
        queries = ["LINENAME LIKE '%{}%'".format(line_name) for line_name in line_name_list]
        query_string = " OR ".join(queries)
        where_clause  = "(" + query_string + ") AND LODTYPE IN (1)"
        return where_clause

    @staticmethod
    def get_queryName(name_list):
        names = ""
        for name in name_list:
            names += str(name) + "', '"
        where_clause  = "NAME IN ('" + names[:-3] + ")"
        return where_clause

    @staticmethod
    def refresh():
        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

    @staticmethod
    def get_domains(domain_name, workspace):

        print("Getting domains")
        domains = arcpy.da.ListDomains(workspace)
        coded_values = {}

        try:
            for domain in domains:
                if domain.name == domain_name:
                    coded_values = domain.codedValues

            if coded_values:
                coded_values[None] = None
                return coded_values
            else:
                errLog("Coded values is null")
                exit()

        except Exception as e:
            print ("Name not in the coded value for {}".format(domain_name))