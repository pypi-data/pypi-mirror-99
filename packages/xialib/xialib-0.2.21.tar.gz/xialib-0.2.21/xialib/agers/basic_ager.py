from datetime import datetime
from xialib.ager import Ager


class BasicAger(Ager):
    """Basic Ager Use Python dictionary (No persistence) as Age data holder

    """
    data = {}

    def get_ready_key(self, key: str, start_key: int = 0, end_key: int = 0) -> int:
        if key not in self.data:
            self.logger.error("Target {} has not been initialized".format(key), extra=self.log_context)
            raise ValueError("XIA-000035")
        ager_dict = self.data[key].copy()

        frame_length = ager_dict.pop("frame_length", 0)
        schedule = ager_dict.pop("schedule", [])
        current_frame_id = self.get_frame_id(frame_length)
        current_frame_list = ager_dict.get(current_frame_id, [])

        all_list, last_ok_frame = [], ""
        for frame_id in sorted(ager_dict):
            for item in ager_dict[frame_id]:
                all_list = self.age_list_add_item(all_list, [int(item.split("-")[0]), int(item.split("-")[1])])
        old_end_key = all_list[0][-1]

        # Case 1: Just return the old key
        if start_key == 0 and end_key == 0:
            return old_end_key

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

        ready_key = all_list[0][-1] if all_list[0][-1] > old_end_key else 0

        if ready_key and current_frame_id not in schedule:
            schedule.append(current_frame_id)
            self.data[key]["schedule"] = schedule

        return ready_key if frame_length <= 1 else 0

    def key_init(self, key: str, start_key: int, frame_length: int = 0):
        if self.min_fram_length > 1 and frame_length % self.min_fram_length != 0:
            self.logger.error("Ager frame length not divisible by min length", extra=self.log_context)
            raise ValueError("XIA-000036")
        self.data[key] = {
            "frame_length": frame_length,
            self.get_frame_id(frame_length): [str(start_key) + "-" + str(start_key)]
        }

    def get_update_tasks(self, start_frame: int = 0, end_frame: int = 0) -> dict:
        # Case 1: Real-time only Ager
        if self.min_fram_length <= 1:
            return {}
        # Case 2: First Run => Update All
        if self.ctrl_key not in self.data:
            self.data[self.ctrl_key] = {"updated_frame_id": self.get_frame_id(self.min_fram_length), "tasks": {}}
            for key in [item for item in self.data if item != self.ctrl_key]:
                self.data[self.ctrl_key]["tasks"][key] = self.get_ready_key(key)
            return self.data[self.ctrl_key]["tasks"]
        # Case 3: Periodic Run => Partial Update
        update_dict = {}
        start_frame = start_frame if start_frame else self.data[self.ctrl_key]["updated_frame_id"]
        start_frame_ts = int(datetime.strptime(start_frame, "%Y%m%d%H%M%S").timestamp())
        current_frame_id = self.get_frame_id(self.min_fram_length)
        end_frame = end_frame if end_frame else current_frame_id
        end_frame_ts = int(datetime.strptime(end_frame, "%Y%m%d%H%M%S").timestamp())
        # Case 3.1 Iterate all not treated frame
        for frame_ts in range(start_frame_ts, end_frame_ts + 1, self.min_fram_length):
            frame = datetime.fromtimestamp(frame_ts).strftime("%Y%m%d%H%M%S")
            remain_keys = [item for item in self.data if item not in update_dict]
            for key in [item for item in remain_keys if frame in self.data[item].get("schedule", [])]:
                update_dict[key] = self.get_ready_key(key)
                self.data[key]["schedule"] = [t for t in self.data[key]["schedule"] if t > end_frame]
        # Case 3.2 Iterate for force updated item
        for key in [k for k, v in self.data[self.ctrl_key]["tasks"].items() if v is None and k not in update_dict]:
            update_dict[key] = self.get_ready_key(key)

        for key, frame_id in update_dict.copy().items():
            if not frame_id or self.data[self.ctrl_key]["tasks"].get(key, None) == frame_id:
                update_dict.pop(key)
        self.data[self.ctrl_key]["updated_frame_id"] = end_frame
        return update_dict
