Use to create CSV Imports of your data.

The csv tool will map headers to import functions:

    import csv_tool

    class UserImport(csv_tool.CsvImportTool):
        model = User

        # specify the fields you want to import without modification here
        fields = ["first_name", "last_name"]

        # specify alternate header names here
        # fields are automatically stripped and spaces are converted to "_" so
        # you don't need to alias that
        aliases = {"name": "first_name"}

        # customize your import with functions
        # just fill in the field name after "imports_"
        # including a like this will make "username" importable, you don't have
        # to add it to the fields list
        def import_username(self, instance, values, name):
            value = values.get(name, "")

            ... check the username ...

            instance.username = value

        # if you have m2m or other post save imported fields do them here
        # import_<fieldname>_after
        # this is called after this row's instance is saved
        def import_widgets_after(self, instance, values, name):
            ....


There are some other functions you can override to customize the behavior of your import:

    # called when getting a new object
    # you can fetch an existing object here
    def get_or_create(self, values)

    # called when all pre-save fields are imported
    def save_model(self, instance, values)

    # called when the object has been fully imported
    def finalize(self, instance, values)


Also included is a csv Export tool

    from csv_tool import CsvExportTool
    
    class MyExport(CsvExportTool):
        model = MyUser
        fields = ["custom", "id"]  # list fields here

        def export_custom(self, obj, fieldname):
            # custom logic
            return obj.custom

Unlike the Import, you need to explicitly list fields you want to export
even if they have a custom export function.

If you want to reuse a export method or use it multple times or with an 
alternate label/header use a tuple in the fields attribute of the class:

    from csv_tool import CsvExportTool
    
    class MyExport(CsvExportTool):
        fields = ["custom", ("id", "custom")] # export id the same as `custom`

        def export_custom(self, obj, fieldname): # fieldname will be "id"
            # custom logic
            return obj.custom