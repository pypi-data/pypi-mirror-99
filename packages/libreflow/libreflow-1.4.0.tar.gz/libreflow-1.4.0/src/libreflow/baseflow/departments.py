import os
import getpass
import re
from collections import defaultdict

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict

from .file import FileSystemMap
from .users import ToggleBookmarkAction


class CreateDefaultFileSystemItemsAction(flow.Action):

    _department = flow.Parent()

    def allow_context(self, context):
        return context and context.endswith(".inline")

    def _compute_names_and_extensions(self, names_as_string, separator, args):
        formatted_names = names_as_string.split(separator)
        names_and_extensions = []

        for formatted_name in formatted_names:
            formatted_name, extension = tuple(os.path.splitext(formatted_name))
            tracked = "@" not in formatted_name
            formatted_name = formatted_name.replace("@", "")
            name = formatted_name.format_map(defaultdict(str))
            name = re.sub("-", "_", name)
            # name = re.sub('\A_|_\Z', '', name)
            while name.startswith("_"):
                name = name[1:]
            while name.endswith("_"):
                name = name[:-1]

            complete_name = formatted_name.format(**args)
            if extension:
                extension = extension[1:]

            names_and_extensions.append((name, complete_name, extension, tracked))

        return names_and_extensions

    def get_buttons(self):
        self.message.set("<h3>Create default files</h3>")

        settings = get_contextual_dict(self._department, "settings")
        context = settings["context"]
        department = settings["department"]
        default_items = "default_%s_%s_files" % (context, department)

        try:
            default_names_as_string = settings[default_items].replace(" ", "")
        except KeyError:
            msg = self.message.get()
            msg += (
                "<font color=#D5000D>Not default files for %s %s department</font>"
                % (context, department)
            )
            self.message.set(msg)

            return ["Cancel"]

        self._default_names_and_extensions = self._compute_names_and_extensions(
            default_names_as_string, ",", settings
        )

        msg = self.message.get()
        msg += "The following items will be created:<br><br>"

        for (
            name,
            complete_name,
            extension,
            tracked,
        ) in self._default_names_and_extensions:
            msg += "  %s%s" % ("" if tracked else "@", name)
            if extension:
                msg += ".%s" % extension
            msg += " (%s)<br>" % complete_name

        self.message.set(msg)

        return ["Confirm", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        settings = get_contextual_dict(self._department, "settings")
        settings = defaultdict(str, settings)

        for (
            name,
            complete_name,
            extension,
            tracked,
        ) in self._default_names_and_extensions:
            try:
                if extension:  # File
                    if tracked:
                        self._department.files.add_tracked_file(
                            name, extension, complete_name
                        )
                    else:
                        self._department.files.add_file(name, extension)
                else:  # Folder
                    if tracked:
                        self._department.files.add_tracked_folder(name, complete_name)
                    else:
                        self._department.files.add_folder(name)
            except ValueError:
                # Item has already been created manually
                pass

        self._department.files.touch()


class Department(flow.Object):

    _parent = flow.Parent()

    toggle_bookmark = flow.Child(ToggleBookmarkAction)

    settings = flow.Child(ContextualView).ui(hidden=True)
    files = (
        flow.Child(FileSystemMap)
        .injectable()
        .ui(expanded=True, action_submenus=True, items_action_submenus=True)
    )
    auto_current = flow.BoolParam(True).ui(hidden=True)

    create_defaults = flow.Child(CreateDefaultFileSystemItemsAction).ui(
        label="Create default files"
    )
    path = flow.Computed(cached=True).ui(hidden=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                department=self.name(),
                context=self._parent.__class__.__name__.lower(),
            )
    
    def compute_child_value(self, child_value):
        if child_value is self.path:
            settings = get_contextual_dict(self, "settings")
            file_category = settings["file_category"]
            if file_category == "PROD":
                path = os.path.join(
                    file_category,
                    settings["sequence"],
                    settings["shot"],
                    settings["department"],
                )
            elif file_category == "LIB":
                path = os.path.join(
                    file_category,
                    settings["asset_name"],
                    settings["department"],
                )

            child_value.set(path)
