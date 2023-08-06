import arcpy

class Additions:

    @staticmethod
    def add_cartopac_fields(workspace,target):
        AddField_Text(workspace, target, "EVENTID", "38", "EventID", "#")
        AddField_Date(os.path.join(workspace, target), "GPS_DATE", "#")
        AddField_Text(workspace, target, "GPS_COLLECTOR", "25", "GPS COLLECTOR", "#")
        AddField_Double(target, "GPS_AVGPPHACC", "#")

    @staticmethod
    def add_cartopac_fields_two(workspace,target):
        AddField_Text(workspace, target, "EVENTID", "38", "EventID", "#"),
        AddField_Date(os.path.join(workspace, target), "GPS_DATE", "#"),
        AddField_Double(target, "GPS_AVGPPHACC", "#")

    @staticmethod
    def add_coded_value_to_domain(domain_name, new_value, new_description):
        log("Add Coded Value To Domain:  " + workspace + "/" + domain_name + ", " + new_description + "(" + new_value + ")")
        arcpy.AddCodedValueToDomain_management(workspace,domain_name,new_value,new_description)

    @staticmethod
    def add_coded_value_domain(workspace, domain_name, comments, type):
        log("Add Coded Value Domain:  Adding coded value domain " + domain_name + "...")
        arcpy.CreateDomain_management(workspace, domain_name, comments, type, "CODED", "DEFAULT", "DEFAULT")

    @staticmethod
    def add_EAM_fields(dataset_and_feature_class):
        AddField_Text(dataset_and_feature_class, "EAM_DESCRIPTION", "50", "EAM Description", "")
        AddField_Text(dataset_and_feature_class, "EAM_AREA", "50", "EAM Area", "")
        AddField_Text(dataset_and_feature_class, "EAM_LOCATION", "50", "EAM Location", "")
        AddField_Date(dataset_and_feature_class, "EAM_TAKEN", "EAM Taken")

    @staticmethod
    def add_field_date(workspace, dataset_and_feature_class, field_name, alias):   
        log("AddField_Date:" + workspace + "/" + dataset_and_feature_class + ":  " + field_name)
        #arcpy.AddField_management(workspace + "/" + dataset_and_feature_class, field_name,"DATE","#","#","#",alias, "NULLABLE","NON_REQUIRED","#")
        arcpy.AddField_management(dataset_and_feature_class, field_name,"DATE","#","#","#",alias, "NULLABLE","NON_REQUIRED","#")
    
    @staticmethod
    def add_field_double(workspace, target, field_name, alias):
        log("AddField_Double:" + target + ":" + field_name)
        arcpy.AddField_management (workspace + "/" + target, field_name, "DOUBLE", "", "", "", alias)

    @staticmethod
    def add_field_long(workspace,dataset_and_feature_class, field_name, length, domain, alias):
        try:
            log("AddField_Long(" + length + "):" + workspace + "/" + dataset_and_feature_class + ":  " + field_name + "(" + domain + ")")
            arcpy.AddField_management(workspace + "/" + dataset_and_feature_class, field_name,"LONG", length,"#","#",alias,"NULLABLE","NON_REQUIRED", domain)
        except Exception as e:
            ExceptHandle(e)
 
    @staticmethod
    def add_field_short(dataset_and_feature_class, field_name, length, domain, alias):
        try:
            log("AddField_Short(" + length + "):" + workspace + "/" + dataset_and_feature_class + ":  " + field_name + "(" + domain + ")")
            arcpy.AddField_management(workspace + "/" + dataset_and_feature_class,field_name,"SHORT",length,"#","#",alias,"NULLABLE","NON_REQUIRED",domain)
        except Exception as e:
            ExceptHandle(e)

    @staticmethod
    def add_field_text(workspace, dataset_and_feature_class, field_name, length, alias, domain):
        log("AddField_Text(" + length + "):" + workspace + "/" + dataset_and_feature_class + ":  " + field_name + "(" + domain + ")")
        arcpy.AddField_management(workspace + "/" + dataset_and_feature_class, field_name, "TEXT","#","#",length, alias, "NULLABLE","NON_REQUIRED", domain)

    @staticmethod
    def add_metadata_fields_two(workspace, target):
        log("Enabling Editor Tracking on {0}...".format(target));
        arcpy.EnableEditorTracking_management (workspace + "/" + target, "CREATEDBY", "CREATEDDATE", "MODIFIEDBY", "LASTMODIFIED", "ADD_FIELDS", "UTC")

    @staticmethod
    def add_range_value_domain(domain_name, comments, type):
        log("Add Range Value Domain:  Adding range value domain " + domain_name + "...")
        arcpy.CreateDomain_management(workspace, domain_name, comments, type, "RANGE")

    @staticmethod
    def add_metadata_fields(workspace, target):
        AddField_Text(workspace, target, "EVENTID", "38", "EventID", "#")
        AddField_Text(workspace, target, "CREATEDBY", "45", "Created By", "#")
        AddField_Date(os.path.join(workspace, target), "CREATEDDATE", "Created Date")
        AddField_Text(workspace, target, "MODIFIEDBY", "45", "Modified By", "#")
        AddField_Date(os.path.join(workspace, target), "LASTMODIFIED", "Last Modified")
        log("Enabling Editor Tracking on {0}...".format(target));
        arcpy.EnableEditorTracking_management (workspace + "/" + target, "CREATEDBY", "CREATEDDATE", "MODIFIEDBY", "LASTMODIFIED", "ADD_FIELDS", "UTC")

    @staticmethod
    def add_spatial_index(workspace,dataset_and_feature_class):
        log("Adding spatial index to " + workspace + " " + dataset_and_feature_class)
        addAction("Adding spatial index to " + workspace + " " + dataset_and_feature_class)
        arcpy.AddSpatialIndex_management(os.path.join(workspace,dataset_and_feature_class),)

    @staticmethod
    def alter_field(workspace, dataset_and_feature_class, field_name, new_field_name, new_field_alias):
        log("Alter Field:" + workspace + "/" + dataset_and_feature_class + " altering field: " + field_name + " adding alias: " + new_field_alias)
        arcpy.AlterField_management(workspace + "/" + dataset_and_feature_class,field_name, new_field_name, new_fiel_dalias)

    @staticmethod
    def append_managment(in_table, workspace, target):
        log("Appending data to  " + target)
        arcpy.Append_management (in_table, workspace + "/" + target, "NO_TEST", "#", "#")

    @staticmethod
    def assign_domain_to_field(workspace, dataset_and_feature_class, field_name, domain_name, sub_types): 
        log("Assign Domain To Field:  " + workspace + "/" + dataset_and_feature_class + ":  " + field_name + ", " + domain_name + "(sub_types: " + ', '.join(sub_types) + ")")
        arcpy.AssignDomainToField_management(workspace + "/" + dataset_and_feature_class, field_name, domain_name, sub_types)
        addAction("Assign Domain to field " + workspace + "/" + dataset_and_feature_class + ", field_name:" + field_name + ", Domain: " + domain_name)

    @staticmethod
    def create_relationship_class(origin_table, destination_table, out_relationship_class, forward_label, backward_label, message_direction, cardinality,
                                  origin_primary_key, origin_foreign_key):
        log("Creating Relationship Class " + out_relationship_class)
        arcpy.CreateRelationshipClass_management (workspace + "/" + origin_table, workspace + "/" + destination_table, workspace + "/" + out_relationship_class, "SIMPLE",
                                            forward_label, backward_label, message_direction, cardinality, "NONE", origin_primary_key, origin_foreign_key)

    @staticmethod
    def copy_feature_class(source, destination, register_as_versioned, default_privileges):
        log("Copy Feature Class:  " + source + " to " + destination + "...")
        log ("Register as versioned is : " + register_as_versioned)
        log ("Default Privs:  " + default_privileges)
        addAction("New feature class:  " + destination)
        arcpy.FeatureClassToFeatureClass_conversion(source, workspace, destination)     
        if default_privileges:
            arcpy.ChangePrivileges_management(workspace + "/" + destination, "GIS_VIEWER", "GRANT")
            arcpy.ChangePrivileges_management(workspace + "/" + destination, "GIS_EDITOR", "GRANT", "GRANT")
            arcpy.ChangePrivileges_management(workspace + "/" + destination, "GIS_WEB_VIEWER", "GRANT")
        else:
            arcpy.ChangePrivileges_management(workspace + "/" + destination, "GIS_VIEWER", "GRANT")
            arcpy.ChangePrivileges_management(workspace + "/" + destination, "GIS_WEB_VIEWER", "GRANT")
        if register_as_versioned == 'True':
            arcpy.register_as_versioned_management(workspace + "/" + destination, "NO_EDITS_TO_BASE") 

    @staticmethod
    def copy_table(source_db, dataset_and_feature_class, dest_db, dest_name):       
        log("Copy Table:  " + source_db + "dataset_and_feature_class"  + " to " + dest_db + " as "+ dest_name+"...")
        addAction("Copy Table:  " + dest_name)
        arcpy.TableToTable_conversion(os.path.join(source_db, dataset_and_feature_class), dest_db, dest_name)
      
    @staticmethod
    def hide_feature_class(workspace, feature_class):   # Important:  do not include GIS. in front of feature class
        log("Hiding Feature Class:  " + workspace +"\\" + feature_class)
        addAction("Hidden feature class:  " + feature_class)
        feature_class = feature_class.upper()
        sde_conn = arcpy.ArcSDESQLExecute(workspace)
        sql = "SELECT GRANTEE FROM table_privileges WHERE TABLE_NAME LIKE '" + feature_class + "' AND GRANTEE NOT IN ('CARTOPAC', 'GIS', 'SDE')"
        sde_return = sde_conn.execute(sql)
        if isinstance(sde_return, list):
            if len(sde_return) > 0:
                for role in sde_return:
                    arcpy.ChangePrivileges_management (workspace + "\\"+feature_class, str(role[0]), "REVOKE", "REVOKE")
                    log("Removing read and write priviliges for role: " + str(role[0]) + " on fc " + feature_class)
        else:
            log("No priviliges granted outside of Cartopac, GIS, or SDE for " + feature_class + " in the workspace " + workspace)

    @staticmethod
    def set_range_value_to_domain(workspace, domain_name, min_range, max_range):  #workspace - workspace parameter
        log("Set Range Value To Domain:  " + workspace + "/" + domain_name + ",Range Values " + "(" + str(min_range) + "-" + str(max_range) + ")")
        arcpy.SetValueForRangeDomain_management(workspace, domain_name, min_range, max_range)

    @staticmethod
    def sort_coded_value_domain_management(domain_name, workspace):
        log("Sort Coded Value Domain:  " + domain_name)
        arcpy.SortCodedValueDomain_management (workspace, domain_name, "DESCRIPTION", "ASCENDING")