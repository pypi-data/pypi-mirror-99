from datetime import datetime
from xialib.controller import Controller


class BasicController(Controller):
    """Basic Controller Use Python dictionary (No persistence) as control data holder

    """
    data = {}

    def key_init(self, key: str, ctrl_info: dict, frame_length: int = 0):
        if self.min_fram_length > 1 and frame_length % self.min_fram_length != 0:
            self.logger.error("Ager frame length not divisible by min length", extra=self.log_context)
            raise ValueError("XIA-000036")
        ctrl_info.update({"status": "active", "key": key})
        self.data[key] = {
            "ctrl_info": ctrl_info,
            "frame_length": frame_length,
            self.get_frame_id(frame_length): ["1-1"]
        }

    def get_ready_task(self, key: str, start_key: int = 0, end_key: int = 0) -> dict:
        if key not in self.data:
            self.logger.error("Target {} has not been initialized".format(key), extra=self.log_context)
            raise ValueError("XIA-000035")
        ager_dict = self.data[key].copy()

        ctrl_info = ager_dict.pop("ctrl_info", {})
        frame_length = ager_dict.pop("frame_length", 0)
        schedule = ager_dict.pop("schedule", [])
        current_frame_id = self.get_frame_id(frame_length)
        current_frame_list = ager_dict.get(current_frame_id, [])

        all_list, last_ok_frame = [], ""
        for frame_id in sorted(ager_dict):
            for item in ager_dict[frame_id]:
                all_list = self.age_list_add_item(all_list, [int(item.split("-")[0]), int(item.split("-")[1])])
        old_ready_key = all_list[0][-1]

        # Case 1: Just return the old key (end key)
        if start_key == 0 and end_key == 0:
            return {"end_key": old_ready_key, "log_table_id": ctrl_info.get("log_table_id", ""),
                    "table_id": ctrl_info.get("table_id", ""), "field_list": ctrl_info.get("field_list", [])}

        current_frame_list.append(str(start_key) + "-" + str(end_key))
        self.data[key][current_frame_id] = current_frame_list
        all_list = self.age_list_add_item(all_list, [start_key, end_key])

        for frame_id in sorted(ager_dict):
            if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                last_ok_frame = frame_id

        # last_ok_frame could be empty if the ok frame contains gap
        if last_ok_frame:
            ager_dict[last_ok_frame].append(str(all_list[0][0]) + "-" + str(all_list[0][-1]))
            for frame_id in [id for id in sorted(ager_dict) if id < last_ok_frame]:
                if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                    self.data[key].pop(frame_id)

        ready_key = all_list[0][-1] if all_list[0][-1] > old_ready_key else 0

        if ready_key and current_frame_id not in schedule and frame_length > 1:
            schedule.append(current_frame_id)
            self.data[key]["schedule"] = schedule

        if frame_length > 1 or not ready_key:
            return {}
        return {"start_key": old_ready_key + 1, "end_key": ready_key, "log_table_id": ctrl_info.get("log_table_id", ""),
                "table_id": ctrl_info.get("table_id", ""), "field_list": ctrl_info.get("field_list", [])}

    def get_update_tasks(self, start_frame: int = 0, end_frame: int = 0) -> dict:
        update_dict, return_dict = {}, {}
        # Case 1: Real-time only Ager
        if self.min_fram_length <= 1:
            return {}
        # Case 2: First Run => Update All
        if self.ctrl_key not in self.data:
            self.data[self.ctrl_key] = {"updated_frame_id": self.get_frame_id(self.min_fram_length), "tasks": {}}
            for key in [id for id, value in self.data.items() if id != self.ctrl_key and value["frame_length"] > 1]:
                ready_task = self.get_ready_task(key)
                ready_task["start_key"] = 1
                self.data[self.ctrl_key]["tasks"][key] = ready_task["end_key"]
                return_dict[key] = ready_task.copy()
            return return_dict
        # Case 3: Periodic Run => Partial Update
        start_frame = start_frame if start_frame else self.data[self.ctrl_key]["updated_frame_id"]
        start_frame_ts = int(datetime.strptime(start_frame, "%Y%m%d%H%M%S").timestamp())
        current_frame_id = self.get_frame_id(self.min_fram_length)
        end_frame = end_frame if end_frame else current_frame_id
        end_frame_ts = int(datetime.strptime(end_frame, "%Y%m%d%H%M%S").timestamp())
        # Case 3.1 Iterate all not treated frame
        for frame_ts in range(start_frame_ts, end_frame_ts, self.min_fram_length):
            frame = datetime.fromtimestamp(frame_ts).strftime("%Y%m%d%H%M%S")
            remain_keys = [item for item in self.data if item not in update_dict]
            for key in [item for item in remain_keys if frame in self.data[item].get("schedule", [])]:
                update_dict[key] = self.get_ready_task(key)
                self.data[key]["schedule"] = [t for t in self.data[key]["schedule"] if t > end_frame]
        # Case 3.2 Iterate for force updated item
        for key in [k for k, v in self.data[self.ctrl_key]["tasks"].items() if v == 1 and k not in update_dict]:
            update_dict[key] = self.get_ready_task(key)

        for key, task_conf in update_dict.items():
            task_key = task_conf["end_key"]
            old_task_key = self.data[self.ctrl_key]["tasks"].get(key, 1)
            if task_key:
                if old_task_key != task_key:
                    task_conf["start_key"] = old_task_key + 1
                    return_dict[key] = task_conf.copy()
                self.data[self.ctrl_key]["tasks"][key] = task_key
        self.data[self.ctrl_key]["updated_frame_id"] = end_frame

        return return_dict

    def get_ctrl_info(self, key: str):
        return self.data.get(key, {}).get("ctrl_info", {})

    def get_table_info_all(self, table_id: str):
        return_dict = {}
        for key, value in self.data.items():
            ctrl_info = value.get("ctrl_info", {})
            if ctrl_info.get("table_id", "") == table_id and ctrl_info.get("status", "") == "active":
                segment_id = ctrl_info.get("segment_id", "")
                if segment_id not in return_dict:
                    return_dict[segment_id] = ctrl_info.copy()
                elif return_dict[segment_id].get("start_seq", "") < ctrl_info.get("start_seq", ""):
                    self.data[return_dict[segment_id]["key"]]["ctrl_info"]["status"] = "obsolete"
                    return_dict[segment_id] = ctrl_info.copy()
        return return_dict
