from kabaret import flow

import os
import fnmatch

from libreflow.baseflow.file import (
    FileFormat,
    Revision,
    TrackedFile, TrackedFolder,
    FileSystemMap,
    PublishFileAction,
    CreateTrackedFileAction, CreateFileAction,
    CreateTrackedFolderAction, CreateFolderAction,
    AddFilesFromExisting,
    FileRevisionNameChoiceValue,
)

from kabaret.flow_contextual_dict import get_contextual_dict

from .runners import (CHOICES, CHOICES_ICONS)


class FileFormat(flow.values.ChoiceValue):
    CHOICES = CHOICES





class CreateTrackedFileAction(CreateTrackedFileAction):

    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    _files = flow.Parent()
    _department = flow.Parent(2)

    file_name = flow.Param("")
    file_format = flow.Param("blend", FileFormat).ui(
        choice_icons=CHOICES_ICONS
    )

    def run(self, button):
        if button == "Cancel":
            return

        settings = get_contextual_dict(self, "settings")
        name = self.file_name.get()
        prefix = self._department._file_prefix.get()

        self.root().session().log_debug(
            "Creating file %s.%s" % (name, self.file_format.get())
        )

        self._files.add_tracked_file(name, self.file_format.get(), prefix + name)
        self._files.touch()

class CreateTrackedFolderAction(CreateTrackedFolderAction):
    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    _files = flow.Parent()
    _department = flow.Parent(2)


    folder_name = flow.Param("")


    def run(self, button):
        if button == "Cancel":
            return

        settings = get_contextual_dict(self, "settings")
        
        name = self.folder_name.get()
        prefix = self._department._file_prefix.get()

        self.root().session().log_debug(
            "Creating folder %s" % name
        )

        self._files.add_tracked_folder(name, prefix + name)
        self._files.touch()


class Revision(Revision):
    def compute_child_value(self, child_value):
        if child_value is self.file_name:
            name = "{filename}.{ext}".format(
                filename=self._file.complete_name.get(),
                ext=self._file.format.get(),
            )
            child_value.set(name)
        else:
            super(Revision, self).compute_child_value(child_value)


class PublishOKAction(flow.Action):

    _file = flow.Parent()
    _files = flow.Parent(2)
    comment = flow.SessionParam("")
    revision_name = flow.Param(None, FileRevisionNameChoiceValue).watched()
    upload_after_publish = flow.SessionParam(False).ui(editor="bool")

    def check_file(self):
        # In an ideal future, this method will check
        # the given revision of the file this action is parented to

        source_display_name = self._file.display_name.get()
        target_display_name = source_display_name.replace(".", "_ok.")
        msg = f"<h2>Publish in <font color=#fff>{target_display_name}</font></h2>"
        
        target_name, ext = self._target_name_and_ext()
        target_mapped_name = target_name + '_' + ext
        revision_name = self.revision_name.get()

        if self._files.has_mapped_name(target_mapped_name):
            target_file = self._files[target_mapped_name]

            if target_file.has_revision(revision_name):
                msg += (
                    "<font color=#D5000D>"
                    f"File {target_display_name} already has a revision {revision_name}."
                )
                self.message.set(msg)

                return False
        
        self.message.set((
            f"{msg}<font color='green'>"
            f"Revision {revision_name} of file {source_display_name} looks great !"
            "</font>"
        ))

        return True
    
    def allow_context(self, context):
        return context and self._file.enable_publish_ok.get()
    
    def child_value_changed(self, child_value):
        if child_value is self.revision_name:
            self.check_file()
    
    def _target_name_and_ext(self):
        split = self._file.name().split('_')
        name = '_'.join(split[:-1])
        ext = split[-1]

        return "%s_ok" % name, ext
    
    def get_buttons(self):
        self.check_file()
        return ["Publish", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return
        
        if not self.check_file():
            return self.get_result(close=False)

        target_name, ext = self._target_name_and_ext()
        target_mapped_name = target_name + '_' + ext
        revision_name = self.revision_name.get()
        
        # Create validation file if needed
        if not self._files.has_mapped_name(target_mapped_name):
            self._files.create_file.file_name.set(target_name)
            self._files.create_file.file_format.set(ext)
            self._files.create_file.run(None)
        
        target_file = self._files[target_mapped_name]

        self._file.publish_into_file.target_file.set(target_file)
        self._file.publish_into_file.source_revision_name.set(revision_name)
        self._file.publish_into_file.comment.set(self.comment.get())
        self._file.publish_into_file.upload_after_publish.set(self.upload_after_publish.get())
        self._file.publish_into_file.run(None)


class PublishFileAction(PublishFileAction):

    _files = flow.Parent(2)
    publish_ok = flow.SessionParam(False).ui(editor="bool")

    def get_buttons(self):
        self.publish_ok.revert_to_default()
        return super(PublishFileAction, self).get_buttons()

    def run(self, button):
        super(PublishFileAction, self).run(button)

        if not self._file.enable_publish_ok.get():
            return
        
        if self.publish_ok.get():
            self._file.publish_ok.comment.set(self.comment.get())
            self._file.publish_ok.revision_name.set(self._file.get_head_revision().name())
            
            return self.get_result(next_action=self._file.publish_ok.oid())


class PublishOKItem(flow.Object):

    enable_publish_ok = flow.Computed(cached=True)

    def name_to_match(self):
        raise NotImplementedError(
            "Must return the name used to check if publish OK is enabled."
        )

    def publish_ok_enabled(self):
        settings = self.root().project().admin.project_settings
        patterns = settings.publish_ok_files.get().split(",")

        if not patterns:
            return True

        for pattern in patterns:
            pattern = pattern.encode('unicode-escape').decode().replace(" ", "")
            if fnmatch.fnmatch(self.name_to_match(), pattern):
                return True
        
        return False


class TrackedFile(TrackedFile, PublishOKItem):

    publish_ok = flow.Child(PublishOKAction).ui(group='Advanced')

    def get_name(self):
        # Two remarks:
        # We redefined this method to lighten a bit tracked file's directory name for projects built with this flow.
        # Why the name of this method has been left totally confusing, is an excellent question.
        return self.name()
    
    def name_to_match(self):
        return self.display_name.get()
    
    def compute_child_value(self, child_value):
        if child_value is self.enable_publish_ok:
            self.enable_publish_ok.set(self.publish_ok_enabled())
        else:
            super(TrackedFile, self).compute_child_value(child_value)


class TrackedFolder(TrackedFolder, PublishOKItem):
    
    publish_ok = flow.Child(PublishOKAction).ui(group='Advanced')

    def name_to_match(self):
        return self.display_name.get()

    def compute_child_value(self, child_value):
        if child_value is self.enable_publish_ok:
            self.enable_publish_ok.set(self.publish_ok_enabled())
        else:
            super(TrackedFolder, self).compute_child_value(child_value)


class CreateFolderAction(CreateFolderAction):

    def allow_context(self, context):
        return False


class CreateFileAction(CreateFileAction):

    def allow_context(self, context):
        return False


class AddFilesFromExisting(AddFilesFromExisting):

    def allow_context(self, context):
        return False


class FileSystemMap(FileSystemMap):
    
    create_untracked_folder = flow.Child(CreateFolderAction)
    create_untracked_file = flow.Child(CreateFileAction)
    add_files_from_existing = flow.Child(AddFilesFromExisting)

    def add_tracked_file(self, name, extension, complete_name):
        key = "%s_%s" % (name, extension)
        file = self.add(key, object_type=TrackedFile)
        file.format.set(extension)
        file.complete_name.set(complete_name)

        # Create file folder
        try:
            self.root().session().log_debug(
                "Create file folder '{}'".format(file.get_path())
            )
            os.makedirs(file.get_path())
        except OSError:
            self.root().session().log_error(
                "Creation of file folder '{}' failed.".format(file.get_path())
            )
            pass

        # Create current revision folder
        current_revision_folder = os.path.join(file.get_path(), "current")

        try:
            self.root().session().log_debug(
                "Create current revision folder '{}'".format(
                    current_revision_folder
                )
            )
            os.mkdir(current_revision_folder)
        except OSError:
            self.root().session().log_error(
                "Creation of current revision folder '{}' failed".format(
                    current_revision_folder
                )
            )
            pass

        return file
    
    def add_tracked_folder(self, name, complete_name):
        folder = self.add(name, object_type=TrackedFolder)
        folder.format.set("zip")
        folder.complete_name.set(complete_name)

        # Create file folder
        try:
            self.root().session().log_debug(
                "Create tracked folder '{}'".format(folder.get_path())
            )
            os.makedirs(folder.get_path())
        except OSError:
            self.root().session().log_error(
                "Creation of tracked folder '{}' failed.".format(folder.get_path())
            )
            pass

        # Create current revision folder
        current_revision_folder = os.path.join(folder.get_path(), "current")

        try:
            self.root().session().log_debug(
                "Create current revision folder '{}'".format(
                    current_revision_folder
                )
            )
            os.mkdir(current_revision_folder)
        except OSError:
            self.root().session().log_error(
                "Creation of current revision folder '{}' failed".format(
                    current_revision_folder
                )
            )
            pass

        return folder
