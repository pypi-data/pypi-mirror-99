import arcpy

class Eliminations:

    @staticmethod
    def delete_coded_value_from_domain(workspace, domain_name, code):
        log("Delete Coded Value From Domain: %s %s %s" %(workspace, domain_name, code))
        #USAGE: DeleteCodedValueFromDomain_management (in_workspace, domain_name, code)
        arcpy.DeleteCodedValueFromDomain_management (workspace, domain_name, code)

    @staticmethod
    def delete_domain(workspace, domain_name):
        log("Delete domain:  " + workspace + ":" + domain_name)
        arcpy.DeleteDomain_management (workspace, domain_name)

    @staticmethod
    def delete_feature_class(workspace, dataset_and_feature_class):
        log("Delete Feature Class:  " + workspace + "/" + dataset_and_feature_class)
        addAction("Deleted feature class:  " + dataset_and_feature_class)
        arcpy.Delete_management (workspace + "/" + dataset_and_feature_class)

    @staticmethod
    def delete_rows(workspace, in_table):
        log("Deletin gRows " + in_table)
        arcpy.DeleteRows_management(workspace + "/" + in_table)

    @staticmethod
    def remove_domain_from_field(workspace, target, field_name, subtype):
        target = workspace + "/" + target
        log("Remove Domain From Field: %s %s %s" %(target, field_name, subtype))
        #USAGE:  RemoveDomainFromField_management (in_table, field_name, {subtype_code})
        arcpy.RemoveDomainFromField_management (target, field_name, subtype)

    @staticmethod
    def truncate_table(in_table, workspace):
        log("Truncating  " + in_table)	
        arcpy.TruncateTable_management (workspace + "/" + in_table)