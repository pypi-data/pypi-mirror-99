from datetime import datetime
from typing import List
from google.cloud import firestore
from xialib.controller import Controller

class FirestoreController(Controller):
    """Ager By Using Firestore database


    """
    def __init__(self, collection: str, db: firestore.Client, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(db, firestore.Client):
            self.logger.error("FirestoreDepositor db must be type of Firestore Client", extra=self.log_context)
            raise TypeError("XIA-010003")
        else:
            self.db = db
            self.collection = db.collection(collection)

    def key_init(self, key: str, ctrl_info: dict, frame_length: int = 0):
        if self.min_fram_length > 1 and frame_length % self.min_fram_length != 0:
            self.logger.error("Ager frame length not divisible by min length", extra=self.log_context)
            raise ValueError("XIA-000036")

        ctrl_info.update({"status": "active", "key": key})
        ager_ref = self.collection.document(key).get()
        ager_ref.reference.set({
            "ctrl_info": ctrl_info,
            "frame_length": frame_length,
            self.get_frame_id(frame_length): ["1-1"]
        })

    def get_ready_task(self, key: str, start_key: int = 0, end_key: int = 0, ager_ref=None) -> dict:
        """Adding age range and get the last ready age

        Attributes:
            key (:obj:`str`): object key (key should contains Target Topic, Target Table, Segment ID)
            start_key (:obj:`int`): new input start merge key
            end_key (:obj:`int`): new input end merge key

        Return:
            :obj:`int`: The end age number which is ready to be loaded (No GAP from beginning)
        """
        ager_ref = self.collection.document(key).get() if not ager_ref else ager_ref
        key = ager_ref.id if ager_ref else key
        if not ager_ref.exists:
            raise ValueError("Target {} has not been initialized".format(key))
        ager_dict = ager_ref.to_dict()

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

        # Case 1: Just return the old key
        if start_key == 0 and end_key == 0:
            return {"end_key": old_ready_key, "log_table_id": ctrl_info.get("log_table_id", ""),
                    "table_id": ctrl_info.get("table_id", ""), "field_list": ctrl_info.get("field_list", [])}

        current_frame_list.append(str(start_key) + "-" + str(end_key))
        ager_dict[current_frame_id] = current_frame_list
        all_list = self.age_list_add_item(all_list, [start_key, end_key])

        for frame_id in sorted(ager_dict):
            if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                last_ok_frame = frame_id
        update_task = {current_frame_id: firestore.ArrayUnion([str(start_key) + "-" + str(end_key)])}

        # last_ok_frame could be empty if the ok frame contains gap
        if last_ok_frame:
            update_task[last_ok_frame] = firestore.ArrayUnion([str(all_list[0][0]) + "-" + str(all_list[0][-1])])
            for frame_id in [id for id in sorted(ager_dict) if id < last_ok_frame]:
                if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                    update_task[frame_id] = firestore.DELETE_FIELD

        ready_key = all_list[0][-1] if all_list[0][-1] > old_ready_key else 0
        if ready_key and current_frame_id not in schedule and frame_length > 1:
            update_task["schedule"] = firestore.ArrayUnion([current_frame_id])

        # Incremental Updates
        ager_ref.reference.update(update_task)

        if frame_length > 1 or not ready_key:
            return {}
        return {"start_key": old_ready_key + 1, "end_key": ready_key, "log_table_id": ctrl_info.get("log_table_id", ""),
                "table_id": ctrl_info.get("table_id", ""), "field_list": ctrl_info.get("field_list", [])}

    def get_update_tasks(self, start_frame: int = 0, end_frame: int = 0)-> dict:
        # Case 1: Real-time only Ager
        if self.min_fram_length <= 1:
            return {}
        # Case 2: First Run => Update All
        ctrl_ref = self.collection.document(self.ctrl_key).get()
        if not ctrl_ref.exists:
            ctrl_dict = {"updated_frame_id": self.get_frame_id(self.min_fram_length), "tasks": {}}
            task_dict, return_dict = {}, {}
            ctrl_ref.reference.set({"updated_frame_id": self.get_frame_id(self.min_fram_length), "tasks": {}})
            for ager_ref in self.collection.where("frame_length", ">", 1).stream():
                ready_task = self.get_ready_task('', ager_ref=ager_ref)
                ready_task["start_key"] = 1
                task_dict[ager_ref.id] = ready_task["end_key"]
                return_dict[ager_ref.id] = ready_task.copy()
            ctrl_dict.update({"tasks": task_dict})
            ctrl_ref.reference.set(ctrl_dict)
            return return_dict
        # Case 3: Periodic Run => Partial Update
        ctrl_dict = ctrl_ref.to_dict()
        update_dict, return_dict = {}, {}
        start_frame = start_frame if start_frame else ctrl_dict["updated_frame_id"]
        start_frame_ts = int(datetime.strptime(start_frame, "%Y%m%d%H%M%S").timestamp())
        current_frame_id = self.get_frame_id(self.min_fram_length)
        end_frame = end_frame if end_frame else current_frame_id
        end_frame_ts = int(datetime.strptime(end_frame, "%Y%m%d%H%M%S").timestamp())
        # Case 3.1 Iterate all not treated frame
        for frame_ts in range(start_frame_ts, end_frame_ts, self.min_fram_length):
            frame = datetime.fromtimestamp(frame_ts).strftime("%Y%m%d%H%M%S")
            for ager_ref in self.collection.where("schedule", "array_contains", frame).stream():
                update_dict[ager_ref.id] = self.get_ready_task('', ager_ref=ager_ref)
                ager_dict = ager_ref.to_dict()
                remove_list = [item for item in ager_dict.get("schedule") if item <= end_frame]
                ager_ref.reference.update({"schedule": firestore.ArrayRemove(remove_list)})
        # Case 3.2 Iterate for force updated item
        for key in [k for k, v in ctrl_dict["tasks"].items() if v == 1 and k not in update_dict]:
            update_dict[key] = self.get_ready_task(key)

        for key, task_conf in update_dict.items():
            task_key = task_conf["end_key"]
            old_task_key = ctrl_dict["tasks"].get(key, 1)
            if task_key:
                if old_task_key != task_key:
                    task_conf["start_key"] = old_task_key + 1
                    return_dict[key] = task_conf.copy()
                ctrl_dict["tasks"][key] = task_key
        ctrl_dict["updated_frame_id"] = end_frame
        ctrl_ref.reference.set(ctrl_dict)
        return return_dict

    def get_ctrl_info(self, key: str):
        ctrl_info = self.collection.document(key).get({"ctrl_info"})
        return ctrl_info.to_dict()["ctrl_info"] if ctrl_info.exists else {}

    def get_table_info_all(self, table_id: str):
        return_dict = {}
        for ager_ref in self.collection \
            .where("ctrl_info.table_id", "==", table_id) \
            .where("ctrl_info.status", "==", "active") \
            .stream():
            ctrl_info = ager_ref.to_dict()["ctrl_info"]
            segment_id = ctrl_info.get("segment_id", "")
            if segment_id not in return_dict:
                return_dict[segment_id] = ctrl_info.copy()
            elif return_dict[segment_id].get("start_seq", "") < ctrl_info.get("start_seq", ""):
                self.collection.document(return_dict[segment_id]["key"]).update({
                    "ctrl_info.status": "obsolete"
                })
                return_dict[segment_id] = ctrl_info.copy()
        return return_dict


