import arcpy

class Versioning:
    @staticmethod
    def reconcile_versions(input_database, target_version, edit_version, abort_if_conflicts, conflict_definitiion, 
                           conflict_resolution, with_post, with_delete):
        log('Reconcile/posting from GIS.GPS_QA to GIS.DRAFTING_QA using GIS user...')
        arcpy.ReconcileVersions_management(input_database,"ALL_VERSIONS", target_version, edit_version,"LOCK_ACQUIRED",abort_if_conflicts, 
        conflict_definitiion, conflict_resolution, with_post, with_delete,"#")

    @staticmethod
    def register_as_versioned(target, workspace):
        log("Register As Versioned:  " + target)
        arcpy.RegisterAsVersioned_management(workspace + "/" + target, "NO_EDITS_TO_BASE")

    @staticmethod
    def unregister_as_versioned_management(workspace):
        # KEEP_EDIT will trigger an error if there are edits in delta tables.
        # Since DMC's are run at compress state 0, this will be a further safe guard to lost data.
        arcpy.UnregisterAsVersioned_management (workspace, "KEEP_EDIT","#")