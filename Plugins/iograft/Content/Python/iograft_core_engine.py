# Copyright 2023 Fabrica Software, LLC

import os
import queue
import sys

import iograft
import unreal


IOGRAFT_UNREAL_CORE_NAME = "unreal"


@unreal.uclass()
class PythonCoreEngine(unreal.IograftCoreEngine):
    work_queue = queue.Queue()

    def execute_node_in_game_thread(self, func, *args):
        result_event = iograft._NodeProcessEvent()
        self.work_queue.put((func, args, result_event))
        self.execute_node_async()
        result_event.wait()

    @unreal.ufunction(override=True)
    def execute_queued_node(self):
        try:
            func, args, result_event = self.work_queue.get(False)
        except queue.Empty:
            return

        try:
            func(*args)
        except Exception:
            result_event.setException(sys.exc_info())

        result_event.set()
        self.work_queue.task_done()

    @unreal.ufunction(override=True)
    def get_core_name(self):
        return IOGRAFT_UNREAL_CORE_NAME

    @unreal.ufunction(override=True)
    def start_core(self):
        if not iograft.IsInitialized():
            iograft.Initialize()
            self.on_iograft_initialized()

        # Ensure there is an "unreal" Core object created and setup to
        # handle requests.
        core = iograft.GetCore(IOGRAFT_UNREAL_CORE_NAME)
        core.StartRequestHandler()
        core_address = core.GetClientAddress()

        message = "iograft Core: '{}' running at: {}".format(
                                                    IOGRAFT_UNREAL_CORE_NAME,
                                                    core_address)
        unreal.IograftBPLibrary.post_notification(message)
        unreal.log(message)

    @unreal.ufunction(override=True)
    def shutdown_core(self):
        if not iograft.IsInitialized():
            unreal.IograftBPLibrary.post_notification(
                    "The iograft API is not currently initialized.", True)
            return

        # Try to clear the "unreal" Core object and uninitialize iograft.
        try:
            iograft.UnregisterCore(IOGRAFT_UNREAL_CORE_NAME)
        except KeyError:
            pass

        iograft.Uninitialize()

        message = "The iograft API has been uninitialized."
        unreal.IograftBPLibrary.post_notification(message)
        unreal.log(message)

    @unreal.ufunction(override=True)
    def launch_ui(self):
        import subprocess
        if not iograft.IsInitialized():
            unreal.IograftBPLibrary.post_notification(
                    "The iograft API is not currently initialized.", True)
            return

        core_address = ""
        try:
            core = iograft.GetCore(IOGRAFT_UNREAL_CORE_NAME,
                                   create_if_needed=False)
            core_address = core.GetClientAddress()
        except KeyError:
            message = "No iograft Core: '{}' is currently running.".format(
                                                    IOGRAFT_UNREAL_CORE_NAME)
            unreal.IograftBPLibrary.post_notification(message, True)
            unreal.log_error(message)
            return

        # Sanitize the environment for the iograft_ui session; removing the
        # LD_LIBRARY_PATH and clearing the IOGRAFT_ENV environment variable
        # since the UI process will no longer be running under the Unreal
        # Python interpreter.
        subprocess_env = os.environ.copy()
        subprocess_env.pop("LD_LIBRARY_PATH", None)
        subprocess_env.pop("IOGRAFT_ENV", None)

        # Launch the iograft_ui subprocess.
        subprocess.Popen(["iograft_ui", "-c", core_address], env=subprocess_env)
        unreal.log("iograft_ui launched.")
