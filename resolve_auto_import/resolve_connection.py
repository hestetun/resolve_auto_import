import DaVinciResolveScript as dvrs


class ResolveConnection:

    def __init__(self):

        self.resolve_conn = dvrs.scriptapp("Resolve")
        if not self.resolve_conn:
            raise self.ResolveConnectionError("No open Resolve instance found")

    def load_project_manager(self):
        project_manager = self.resolve_conn.GetProjectManager()
        if not project_manager:
            raise self.ResolveConnectionError("No project manager found")
        return project_manager

    def load_project(self):

        project_manager = self.load_project_manager()

        project = project_manager.GetCurrentProject()
        if not project:
            raise self.ResolveConnectionError("No project loaded")
        return project

    def load_timeline(self):

        project = self.load_project()

        timeline = project.GetCurrentTimeline()
        if not timeline:
            raise self.ResolveConnectionError("No timeline loaded")
        return timeline

    def timeline_items(self):

        timeline = self.load_timeline()

        items = timeline.GetItemListInTrack('Video', 1)

        if not items:
            raise self.ResolveConnectionError("No items found in timeline")

        return items

    class ResolveConnectionError(Exception):

        def __init__(self, message):
            self.message = message

        def __str__(self):
            return self.message
