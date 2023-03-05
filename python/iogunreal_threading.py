# Copyright 2023 Fabrica Software, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import unreal


def unreal_game_thread(func):
    """
    Decorator to execute a node in the Unreal Game Thread. All Unreal nodes
    that access Editor or Game data that must run in the game thread should
    apply this decorator to their Process() function:
        @unreal_game_thread
        def Process(self, data):
            ...
    """
    @functools.wraps(func)
    def launch_in_game_thread(*args):
        # If the IograftBPLibrary module does not exist, call the function
        # directly.
        # NOTE: This is required for backwards compatibility with Unreal 4.
        if not hasattr(unreal, "IograftBPLibrary"):
            func(*args)
        elif unreal.IograftBPLibrary.is_running_in_game_thread():
            # Check if we are already in the game thread. If so, we can call
            # the function directly.
            func(*args)
        else:
            # Otherwise, pass the node to the iograft Unreal Core Engine to
            # execute the node on the game thread.
            core_engine = unreal.IograftBPLibrary.get_iograft_core_engine()
            core_engine.execute_node_in_game_thread(func, *args)

    return launch_in_game_thread
