import os
import random
import time
from threading import Thread
from os import path
from logging import getLogger

from simplejson import load
import cv2
import numpy as np

from ndu_gate_camera.api.video_source import VideoSourceType
from ndu_gate_camera.camera.roi_manager import ROIManager
from ndu_gate_camera.camera.video_sources.camera_video_source import CameraVideoSource
from ndu_gate_camera.camera.video_sources.file_video_source import FileVideoSource
from ndu_gate_camera.camera.video_sources.ip_camera_video_source import IPCameraVideoSource
from ndu_gate_camera.camera.video_sources.pi_camera_video_source import PiCameraVideoSource
from ndu_gate_camera.camera.video_sources.youtube_video_source import YoutubeVideoSource
from ndu_gate_camera.camera.video_sources.image_video_source import ImageVideoSource
from ndu_gate_camera.utility import constants, image_helper, string_helper
from ndu_gate_camera.utility.ndu_utility import NDUUtility

DEFAULT_RUNNERS = {
    # "drivermonitor": "DriverMonitorRunner",
    # "socialdistance": "SocialDistanceRunner",
    # "emotionanalysis": "EmotionAnalysisRunner",
}

log = getLogger("service")


class NDUCameraService(Thread):
    def __init__(self, instance=None, config_dir="", handler=None, is_main_thread=True, extension_folder=None):
        self.__is_main_thread = is_main_thread
        if instance is None:
            instance = {}
        super().__init__()
        self.__result_handler = handler
        self._ndu_gate_config_dir = config_dir
        self.__extension_folder = extension_folder
        self.RUNNERS = instance.get("runners", [])
        self.SOURCE_TYPE = VideoSourceType.CAMERA
        self.SOURCE_CONFIG = None

        if instance.get("source"):
            self.SOURCE_CONFIG = instance.get("source")
            type_str = self.SOURCE_CONFIG.get("type", "PI_CAMERA")
            if VideoSourceType[type_str]:
                self.SOURCE_TYPE = VideoSourceType[type_str]
            else:
                self.SOURCE_TYPE = VideoSourceType.PI_CAMERA

        self.__frame_send_interval = self.SOURCE_CONFIG.get("frame_send_interval", 1000)
        self.__motion_kernel = self.SOURCE_CONFIG.get("motion_kernel", None)
        self.__preview_show_motion_kernel = self.SOURCE_CONFIG.get("preview_show_motion_kernel", False)
        self.__preview_show = self.SOURCE_CONFIG.get("preview_show", False)
        if self.__preview_show:
            self.__preview_inited = False
            self.__last_preview_image = None
            self.__preview_show_debug_texts = self.SOURCE_CONFIG.get("preview_show_debug_texts", True)
            self.__preview_show_runner_info = self.SOURCE_CONFIG.get("preview_show_runner_info", True)
            self.__preview_show_score = self.SOURCE_CONFIG.get("preview_show_score", False)
            self.__preview_show_rect_name = self.SOURCE_CONFIG.get("preview_show_rect_name", True)
            self.__preview_show_track_id = self.SOURCE_CONFIG.get("preview_show_track_id", True)
            self.__preview_show_track_pnt = self.SOURCE_CONFIG.get("preview_show_track_pnt", False)
            if self.__preview_show_track_pnt:
                self._track_pnt_layer = None
                self._track_pnts = {}
            f = self.SOURCE_CONFIG.get("preview_show_rect_filter", None)
            if f is not None:
                if isinstance(f, str):
                    self.__preview_show_rect_filters = [f]
                elif isinstance(f, list):
                    self.__preview_show_rect_filters = f
                else:
                    raise Exception('Bad "preview_show_rect_filter" definition!')
            else:
                self.__preview_show_rect_filters = None

            self.__preview_write = self.SOURCE_CONFIG.get("preview_write", False)
            self.__preview_last_data = []
            self.__preview_last_data_show_times = []
            self.__preview_write_file_name = self.SOURCE_CONFIG.get("preview_write_file_name", "")
            self.__total_elapsed_times = []

        self._track_history = {}
        self._exit_requested = False
        self.__max_frame_dim = self.SOURCE_CONFIG.get("max_frame_dim", None)
        self.__min_frame_dim = self.SOURCE_CONFIG.get("min_frame_dim", None)
        self.__sleep = self.SOURCE_CONFIG.get("sleep", 0)
        self.__skip_frame = self.SOURCE_CONFIG.get("skip_frame", 0)
        self._skip = 0
        self.__color_toggle = None

        self.frame_sent = self.SOURCE_CONFIG.get("frame_sent", False)

        self.default_runners = DEFAULT_RUNNERS
        self.runners_configs = []
        self.runners_configs_by_key = {}
        self.implemented_runners = {}
        self.available_runners = {}

        self._load_runners()
        self._connect_with_runners()

        self.video_source = None
        self._steps = {}
        # self._start()

    # def run(self):
    #     self.start()

    def _load_runners(self):
        """
        config dosyasında belirtilen NDUCameraRunner imaplementasyonlarını bulur ve _implemented_runners içerisine ekler
        Aynı şekilde herbir runner için config dosyalarını bulur ve connectors_configs içerisine ekler
        """
        runners_configs_temp = {}
        last_priority = 1000000

        if self.RUNNERS:
            for runner in self.RUNNERS:
                log.debug("runner config : %s", runner)
                try:
                    if runner.get("status", 1) == 0:  # runner status default value is 1>>>
                        log.debug("runner is not active %s", runner)
                        continue

                    runner_type = runner.get("type", None)
                    if runner_type is None:
                        log.warning("type not found for %s", runner)
                        continue

                    class_name = self.default_runners.get(runner_type, runner.get("class", None))
                    if class_name is None:
                        log.warning("class name not found for %s", runner)
                        continue

                    runner_class = NDUUtility.check_and_import(runner_type, class_name,
                                                               package_uuids=runner.get("uuids", None), extension_folder=self.__extension_folder)
                    if runner_class is None:
                        log.warning("class name implementation not found for %s - %s", runner_type, class_name)
                        continue

                    runner_key = self.__get_runner_key(runner_type, class_name)
                    self.implemented_runners[runner_key] = runner_class

                    configuration_name = runner['configuration']
                    config_file = self._ndu_gate_config_dir + configuration_name

                    if path.isfile(config_file):
                        with open(config_file, 'r', encoding="UTF-8") as conf_file:
                            runner_conf = load(conf_file)
                            runner_conf["name"] = runner["name"]
                    else:
                        log.error("config file is not found %s", config_file)
                        runner_conf = {"name": runner["name"]}

                    roi_manager = None
                    roi_configuration_name = runner.get('roi_configuration', None)
                    if roi_configuration_name is not None:
                        roi_config_file = self._ndu_gate_config_dir + roi_configuration_name
                        try:
                            if path.isfile(roi_config_file):
                                with open(roi_config_file, 'r', encoding="UTF-8") as roi_conf_file:
                                    runner_roi_conf = load(roi_conf_file)
                                    roi_manager = ROIManager(runner_roi_conf, runner["name"])
                                    runner_conf["roi_manager"] = roi_manager
                            else:
                                log.error("roi config file is not found %s", roi_config_file)
                        except Exception as e1:
                            log.error("Error on loading runner roi config %s", roi_config_file)
                            log.exception(e1)

                    runner_custom_conf = {}
                    custom_config_file = self._ndu_gate_config_dir + runner_type + "_custom.json"
                    if path.isfile(custom_config_file):
                        with open(custom_config_file, 'r', encoding="UTF-8") as conf_file:
                            runner_custom_conf = load(conf_file)
                    else:
                        log.error("custom config file is not found %s", custom_config_file)

                    runner_conf["custom_config"] = runner_custom_conf

                    runner_unique_key = self.__get_runner_configuration_key(runner_type, class_name, configuration_name)

                    runner_priority = runner.get("priority", None)
                    if runner_priority is None:
                        runner_priority = last_priority
                        last_priority = last_priority + 100

                    rt = runners_configs_temp[runner_unique_key] = {
                        "name": runner["name"],
                        "type": runner_type,
                        "class": runner_class,
                        "configuration_name": configuration_name,
                        "config": runner_conf,
                        "priority": runner_priority,
                        "runner_key": runner_key,
                        "runner_unique_key": runner_unique_key,
                        "step_frame": runner.get("step_frame", None),
                        "step_sec": runner.get("step_sec", None)
                    }
                    if roi_manager is not None:
                        rt["roi_manager"] = roi_manager

                except Exception as e:
                    log.error("Error on loading runner config")
                    log.exception(e)

            runner_arr = []
            # add all configs to array
            for key in runners_configs_temp:
                runner_arr.append(runners_configs_temp[key])

            self.runners_configs_by_key = runners_configs_temp
            self.runners_configs = sorted(runner_arr, key=lambda x: x["priority"], reverse=False)
        else:
            log.error("Runners - not found! Check your configuration!")

    def _connect_with_runners(self):
        """
        runners_configs içindeki configleri kullanarak sırayla yüklenen runner sınıflarının instance'larını oluşturur
        oluşturulan bu nesneleri available_runners içerisine ekler.
        """
        for runner_config in self.runners_configs:
            runner = None
            try:
                runner_key = runner_config["runner_key"]
                runner_type = runner_config["type"]
                runner_unique_key = runner_config["runner_unique_key"]

                if runner_config["config"] is None:
                    log.warning("Config not found for %s", runner_key)
                    continue

                if self.implemented_runners[runner_key] is None:
                    log.error("Implemented runner not found for %s", runner_key)
                else:
                    runner = self.implemented_runners[runner_key](runner_config["config"], runner_type)
                    # runner.setName(runner_config["name"])
                    self.available_runners[runner_unique_key] = runner

            except Exception as e:
                log.exception(e)
                if runner is not None and NDUUtility.has_method(runner, 'close'):
                    runner.close()

    def _set_video_source(self):
        """
        SOURCE_TYPE değerine göre video_source değişkenini oluşturur.
        """
        try:
            if self.SOURCE_TYPE is VideoSourceType.VIDEO_FILE:
                self.SOURCE_CONFIG["test_data_path"] = path.dirname(
                    path.dirname(path.abspath(__file__))) + '/data/'.replace('/', path.sep)
                self.video_source = FileVideoSource(self.SOURCE_CONFIG)
                pass
            elif self.SOURCE_TYPE is VideoSourceType.PI_CAMERA:
                self.video_source = PiCameraVideoSource(show_preview=True)
            elif self.SOURCE_TYPE is VideoSourceType.VIDEO_URL:
                # TODO
                pass
            elif self.SOURCE_TYPE is VideoSourceType.IP_CAMERA:
                self.video_source = IPCameraVideoSource(self.SOURCE_CONFIG)
                pass
            elif self.SOURCE_TYPE is VideoSourceType.CAMERA:
                self.video_source = CameraVideoSource(self.SOURCE_CONFIG)
            elif self.SOURCE_TYPE is VideoSourceType.YOUTUBE:
                self.video_source = YoutubeVideoSource(self.SOURCE_CONFIG)
            elif self.SOURCE_TYPE is VideoSourceType.IMAGE_FILE:
                self.video_source = ImageVideoSource(self.SOURCE_CONFIG)
            else:
                log.error("Video source type is not supported : %s ", self.SOURCE_TYPE.value)
                # exit(101)
        except Exception as e:
            log.error("Error during setting up video source")
            log.error(e)

    def exit_signal(self):
        self._exit_requested = True

    # main thread tarafından çağırılabilir
    def check_for_preview(self):
        if self.__is_main_thread:
            raise Exception('Main thread does not need to call check_for_preview!')
        if self.__preview_show:
            return self._show_preview()

    def _show_preview(self):
        if not self.__preview_inited:
            self._winname = self.SOURCE_CONFIG.get("device", "ndu_gate_camera preview")
            pos = self.SOURCE_CONFIG.get("preview_show_win_pos", [40, 30])
            self._pause = False
            cv2.namedWindow(self._winname)  # Create a named window
            cv2.moveWindow(self._winname, pos[0], pos[1])
            self.__preview_inited = True

        preview = self.__last_preview_image
        if preview is not None:
            self.__last_preview_image = None
            cv2.imshow(self._winname, preview)
            # while True:
            #     k = cv2.waitKey(100) & 0xFF
            #     print(k)
            while True:
                k = cv2.waitKey(1) & 0xFF
                if k == ord("q"):
                    self._exit_requested = True
                    break
                elif k == ord("s"):
                    self._skip = 30
                elif k == 32:  # space key
                    self._pause = not self._pause
                if not self._pause:
                    break
            if self.__preview_write:
                self._write_frame(preview)

    def finish_preview(self):
        if self.__preview_show and self.__preview_write and self.__out is not None:
            self.__out.release()
            import ffmpeg  # pip3 install ffmpeg-python & brew install ffmpeg
            try:
                # daha az sıkışmış, quicktime çalabiliyor
                fn = self.__preview_write_file_name
                ffmpeg.input(fn).output(fn + '_ffmpeg.mp4').run(capture_stdout=True, capture_stderr=True)

                # # # süper sıkışmış ama quicktime çalamıyor. Benim denemelerimde yarım yamalak kaydedebildi!
                # ffmpeg.input(fn) \
                #     .output(fn + '2.mp4', vcodec='libx265', crf=24, t=5) \
                #     .run(capture_stdout=True, capture_stderr=True)
                # # os.remove(fn)
            except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e
            finally:
                self.__out = None

    def run(self):
        self._set_video_source()
        if self.video_source is None:
            log.error("video source is not set!")
            return
            # exit(102)
        start_total = None
        # TODO - çalıştırma sırasına göre sonuçlar bir sonraki runnera aktarılabilir
        # TODO - runner dependency ile kimin çıktısı kimn giridisi olacak şeklinde de olabilir

        try:
            for runner_unique_key in self.available_runners:
                runner_conf = self.runners_configs_by_key[runner_unique_key]
                step_sec = runner_conf.get("step_sec", None)
                step_frame = runner_conf.get("step_frame", None)
                if step_sec is not None or step_frame is not None:
                    self._steps[runner_unique_key] = [step_sec, 0, step_frame]

            device = self.SOURCE_CONFIG.get("device", None)
            i = -1
            last_thresh = last_gray = None
            has_motion_kernel = self.__motion_kernel is not None
            results_for_preview = None
            for _frame_index, frame in self.video_source.get_frames():
                if self._exit_requested:
                    break
                i += 1
                if self.__skip_frame > 1 and i % self.__skip_frame != 0:
                    continue
                if has_motion_kernel:
                    gray = image_helper.resize(frame, width=500, interpolation=cv2.INTER_NEAREST)
                    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (self.__motion_kernel, self.__motion_kernel), 0)
                    if last_gray is not None:
                        frame_delta = cv2.absdiff(last_gray, gray)
                        last_thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                        no_zero = cv2.countNonZero(last_thresh)
                        if self.__preview_show_motion_kernel:
                            image_helper.put_text(last_thresh, str(no_zero), [50, 50])
                        # cv2.imshow("last_thresh", last_thresh)
                        # cv2.waitKey(1)
                        if no_zero <= 1:
                            continue
                    last_gray = gray

                if i % 500 == 0:
                    log.debug("frame count %s ", i)
                    print("Source Device : {} - frame {}".format(device, i))

                if i % self.__frame_send_interval == 0:
                    try:
                        camera_capture_base64 = image_helper.frame2base64(frame)
                        log.info("CAMERA_CAPTURE size : %s", len(camera_capture_base64))
                        print("CAMERA_CAPTURE size : {}".format(len(camera_capture_base64)))
                        if self.frame_sent:
                            self.__result_handler.save_result([{"data": {"CAMERA_CAPTURE": camera_capture_base64}}], device=device, data_type='attribute')
                        self.__result_handler.save_result([{"data": {"FRAME_COUNT": i}}], device=device, data_type='attribute')
                        self.frame_sent = True
                    except Exception as e:
                        log.exception(e)
                        log.error("can not create CAMERA_CAPTURE")

                if self.__max_frame_dim is not None:
                    frame = image_helper.resize_if_larger(frame, self.__max_frame_dim)
                if self.__min_frame_dim is not None:
                    frame = image_helper.resize_if_smaller(frame, self.__min_frame_dim)

                if self.__preview_show:
                    results_for_preview = []
                if self._skip <= 0:
                    if self.__preview_show:
                        start_total = time.time()
                    extra_data = {
                        constants.EXTRA_DATA_KEY_RESULTS: {}
                    }
                    extra_data_results = extra_data[constants.EXTRA_DATA_KEY_RESULTS]
                    empty_resulted_runners = []
                    # TODO - check runner settings before send the frame to runner
                    for runner_unique_key in self.available_runners:
                        try:
                            start_time = time.time()
                            step = self._steps.get(runner_unique_key, None)
                            if step is not None:
                                step_sec = step[0]
                                last_time = step[1]
                                step_frame = step[2]
                                if step_frame is not None and i % step_frame != 0:
                                    continue
                                if step_sec is not None:
                                    diff = (start_time - last_time)
                                    if diff <= step_sec:
                                        continue
                                    else:
                                        step[1] = start_time

                            runner_conf = self.runners_configs_by_key[runner_unique_key]
                            if "roi_manager" in runner_conf:
                                roi_manager = runner_conf.get("roi_manager", None)
                                frame = roi_manager.forward(frame)
                                results = self.available_runners[runner_unique_key].process_frame(frame, extra_data=extra_data)
                                frame, results = roi_manager.reverse(frame, results)
                            else:
                                results = self.available_runners[runner_unique_key].process_frame(frame, extra_data=extra_data)

                            if results is not None and len(results) > 0:
                                extra_data_results[runner_unique_key] = results
                                log.debug("result : %s", results)
                            else:
                                empty_resulted_runners.append(runner_unique_key)
                            if self.__preview_show:
                                elapsed = time.time() - start_time
                                results_for_preview.append({"elapsed_time": '{}: {:.4f}sn fps:{:.0f}'.format(runner_conf["type"], elapsed, 1.0 / max(elapsed, 0.001))})

                        except Exception as e:
                            log.exception(e)

                    def check_results(runner_unique_key_, results_, device_, results_for_preview_):
                        self.__result_handler.save_result(results_, device=device_, runner_name=self.runners_configs_by_key[runner_unique_key_]["name"])
                        if self.__preview_show:
                            results_for_preview_.extend(results_)

                    delete_required_keys = []
                    for runner_unique_key, results in extra_data_results.items():
                        results = self._check_track(runner_unique_key, results)
                        if results is not None and len(results) > 0:
                            check_results(runner_unique_key, results, device, results_for_preview)
                        else:
                            delete_required_keys.append(runner_unique_key)
                    for runner_unique_key in delete_required_keys:
                        del extra_data_results[runner_unique_key]
                    for runner_unique_key in empty_resulted_runners:
                        results = self._check_track(runner_unique_key, None)
                        if results is not None and len(results) > 0:
                            extra_data_results[runner_unique_key] = results
                            check_results(runner_unique_key, results, device, results_for_preview)

                self._age_track_history()
                if self.__preview_show:
                    if self._skip > 0:
                        self._skip -= 1
                        preview = frame
                    else:
                        total_elapsed_time = time.time() - start_total
                        self.__total_elapsed_times.append(total_elapsed_time)
                        len_times = len(self.__total_elapsed_times)
                        total_elapsed_time = sum(self.__total_elapsed_times) / len_times
                        if len_times > 10000:
                            self.__total_elapsed_times = []
                        results_for_preview.append({"total_elapsed_time": '{:.0f}msec fps:{:.0f}'.format(total_elapsed_time * 1000, (1.0 / max(total_elapsed_time, 0.001)))})
                        preview = self._get_preview(frame, results_for_preview)
                        if self.__preview_show_motion_kernel and last_thresh is not None:
                            th = image_helper.resize(last_thresh, preview.shape[1], preview.shape[0], interpolation=cv2.INTER_NEAREST)
                            th = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
                            preview = cv2.addWeighted(preview, 1, th, 1, 0)

                    self.__last_preview_image = preview
                    if self.__is_main_thread:
                        self._show_preview()

                    # # write frames
                    # fn = "C:/_koray/temp/sc19_{}.jpg".format(str(i))
                    # cv2.imwrite(fn, frame)

                if self.__sleep > 0 and self._skip <= 0:
                    time.sleep(self.__sleep)

            if self.__preview_show and self.__is_main_thread:
                self.finish_preview()

            # TODO - set camera_perspective
        except Exception as e:
            log.exception(e)

        log.info("Video source is finished")

    def _check_track(self, runner_unique_key, results):
        res = []
        if results is not None:
            for result in results:
                if constants.RESULT_KEY_TRACK_ID in result:
                    if runner_unique_key not in self._track_history:
                        self._track_history[runner_unique_key] = {}
                    history = self._track_history[runner_unique_key]
                    track_id = result[constants.RESULT_KEY_TRACK_ID]
                    if track_id != -1:
                        if track_id not in history:
                            history[track_id] = {"result": result, "age": 0}
                        else:
                            result0 = history[track_id]["result"]
                            history[track_id]["age"] = 0
                            score = result.get(constants.RESULT_KEY_SCORE, 0.9)
                            score0 = result0.get(constants.RESULT_KEY_SCORE, 0.9)
                            if score < score0:
                                for key in [constants.RESULT_KEY_DATA, constants.RESULT_KEY_CLASS_NAME, constants.RESULT_KEY_DEBUG]:
                                    if key in result0:
                                        result[key] = result0[key]
                                result[constants.RESULT_KEY_SCORE] = score0
                            else:
                                history[track_id]["result"] = result
                        if constants.RESULT_KEY_DATA in result:
                            result = result.copy()
                            del result[constants.RESULT_KEY_DATA]
                    elif constants.RESULT_KEY_DATA in result:
                        result = result.copy()
                        del result[constants.RESULT_KEY_DATA]
                    res.append(result)
                else:
                    res.append(result)

        for i, (runner_unique_key, history) in enumerate(self._track_history.items()):
            del_lst = []
            for track_id, h in history.items():
                if h["age"] > 30:
                    result = history[track_id]["result"]
                    res.append(result)
                    del_lst.append(track_id)
            for track_id in del_lst:
                del history[track_id]
        return res

    def _age_track_history(self):
        for i, (runner_unique_key, history) in enumerate(self._track_history.items()):
            for track_id, h in history.items():
                h["age"] += 1

    def _write_frame(self, frame):
        def get_free_file_name(fn):
            if os.path.exists(fn):
                filename, file_extension = os.path.splitext(fn)
                i = 1
                while os.path.exists(fn):
                    # sil fn = f"{filename}{i}{file_extension}"
                    fn = "{}{}{}".format(filename, i, file_extension)
                    i += 1
            return fn

        try:
            self.__out.write(frame)
        except:
            shape = frame.shape[1], frame.shape[0]
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            # fourcc = cv2.VideoWriter_fourcc(*'AVC1')
            # fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.__preview_write_file_name = get_free_file_name(self.__preview_write_file_name)
            self.__out = cv2.VideoWriter(self.__preview_write_file_name, fourcc, 24.0, shape)
            self.__out.write(frame)

    def _new_color(self):
        if self.__color_toggle is None:
            self.__color_toggle = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]
            return self.__color_toggle
        else:
            c = self.__color_toggle
            self.__color_toggle = None
            return [max(50, 255 - c[0]), max(50, 255 - c[1]), max(50, 255 - c[2])]

    def _get_preview(self, image, results):
        def get_color(obj, class_preview_key_, color=None):
            if color is None:
                color = [255, 255, 255]
                if class_preview_key_ is not None:
                    if not hasattr(obj, "__colors"):
                        setattr(obj, "__colors", {})
                    dic = getattr(obj, "__colors")
                    if class_preview_key_ in dic:
                        color = dic[class_preview_key_]
                    else:
                        color = dic[class_preview_key_] = self._new_color()
            return color

        def draw_rect(obj, img, c1_, c2_, class_preview_key_, color=None):
            if color is None:
                color = get_color(obj, class_preview_key_, color)
            cv2.rectangle(img, (c1_[0], c1_[1]), (c2_[0], c2_[1]), color=[1, 1, 1], thickness=3)
            cv2.rectangle(img, (c1_[0], c1_[1]), (c2_[0], c2_[1]), color=color, thickness=2)

        show_debug_texts = self.__preview_show_debug_texts
        show_runner_info = self.__preview_show_runner_info
        show_score = self.__preview_show_score
        rect_filters = self.__preview_show_rect_filters
        show_rect_name = self.__preview_show_rect_name
        show_track_id = self.__preview_show_track_id
        show_track_pnt = self.__preview_show_track_pnt

        h, w, *_ = image.shape
        line_height = 20
        font_scale = 0.4
        current_line = [20, 0]
        current_line_bottom = [20, h]
        data_added = []
        if results is not None:
            for result in results:
                debug_texts = []
                text_type = ""
                has_data = False

                if show_runner_info:
                    total_elapsed_time = result.get("total_elapsed_time", None)
                    if total_elapsed_time is not None:
                        image_helper.put_text(image, total_elapsed_time, [w - 150, h - 30], color=[200, 200, 128], font_scale=0.4)
                        continue

                values = {}
                elapsed_time = values["elapsed_time"] = result.get("elapsed_time", None)
                class_name = values[constants.RESULT_KEY_CLASS_NAME] = result.get(constants.RESULT_KEY_CLASS_NAME, None)
                class_preview_key = values[constants.RESULT_KEY_PREVIEW_KEY] = result.get(constants.RESULT_KEY_PREVIEW_KEY, class_name)
                score = values[constants.RESULT_KEY_SCORE] = result.get(constants.RESULT_KEY_SCORE, None)
                rect = values[constants.RESULT_KEY_RECT] = result.get(constants.RESULT_KEY_RECT, None)
                rect_debug_text = values[constants.RESULT_KEY_RECT_DEBUG_TEXT] = result.get(constants.RESULT_KEY_RECT_DEBUG_TEXT, None)
                data = values[constants.RESULT_KEY_DATA] = result.get(constants.RESULT_KEY_DATA, None)
                debug_text = values[constants.RESULT_KEY_DEBUG] = result.get(constants.RESULT_KEY_DEBUG, None)

                if debug_text is not None:
                    debug_texts.append(debug_text)

                def _get_score_txt(text_, score_):
                    res = "%{:.2f} ".format(score_ * 100) if isinstance(score_, float) else score_
                    if text_ is not None and len(text_) > 0:
                        return "{}- {} ".format(text_, res)
                    else:
                        return res

                text = ""
                if class_name is not None:
                    text = NDUUtility.debug_conv_turkish(class_name) + " "
                    if show_score and score is not None:
                        text = _get_score_txt(text, score)
                elif show_score and score is not None:
                    text = _get_score_txt(None, score)

                if data is not None:
                    add_txt = " data: " + str(data)
                    data_added.append(add_txt)
                    text = text + add_txt
                    has_data = True
                if rect is not None:
                    c = np.array(rect[:4], dtype=np.int32)
                    c1, c2 = [c[1], c[0]], (c[3], c[2])
                    color_rect = get_color(self, class_preview_key, result.get(constants.RESULT_KEY_RECT_COLOR, None))
                    show_rect = True
                    if rect_filters is not None:
                        show_rect = False
                        for rect_filter in rect_filters:
                            if string_helper.wildcard(class_name, rect_filter):
                                show_rect = True
                                break
                    if show_rect:
                        draw_rect(self, image, c1, c2, class_preview_key, color_rect)
                    else:
                        text = ""
                    if show_rect and show_rect_name and len(text) > 0:
                        # c1[1] = c1[1] + line_height
                        c1[1] -= 10
                        if rect_debug_text is not None:
                            text += " - " + rect_debug_text
                        image_helper.put_text(image, text, c1)
                        text = ""
                    if show_rect and show_track_id:
                        track_id = result.get(constants.RESULT_KEY_TRACK_ID, None)
                        if track_id is not None:
                            # c1[1] -= line_height * 1.5
                            c1[1] -= 15
                            image_helper.put_text(image, "{}".format(track_id), c1)
                    if show_track_pnt:
                        track_id = result.get(constants.RESULT_KEY_TRACK_ID, None)
                        if track_id is not None:
                            if self._track_pnt_layer is None:
                                h, w = image_helper.image_h_w(image)
                                self._track_pnt_layer = np.zeros((h, w, 3), np.uint8)
                            self._track_pnt_layer = image_helper.change_brightness(self._track_pnt_layer, -1)
                            y1, x1, y2, x2 = tuple(rect)
                            pnt = (int(x1 + (x2 - x1) * 0.5), int(y2))
                            pnts_key = str(track_id)
                            pnts = self._track_pnts.get(pnts_key, [])
                            pnts.append(pnt)
                            self._track_pnts[pnts_key] = pnts
                            if len(pnts) > 1:
                                pts = np.array(pnts, np.int32)
                                # cv2.polylines(self._track_pnt_layer, [pts], False, color, 5)
                                # cv2.polylines(image, [pts], False, color_rect, 5)
                                thickness = 10
                                for i in range(len(pnts) - 1, 0, -1):
                                    p0 = pnts[i]
                                    p1 = pnts[i - 1]
                                    cv2.line(image, p0, p1, color_rect, thickness)
                                    if i % 10 == 0:
                                        thickness -= 1
                                        if thickness < 1:
                                            # pnts = pnts[i: len(pnts)]
                                            break

                            # color = [255,255,255]
                            # cv2.circle(self._track_pnt_layer, pnt, 1, color, 8)
                            # image = cv2.addWeighted(image, 1, self._track_pnt_layer, 1,)
                            # ret, mask = cv2.threshold(self._track_pnt_layer, 1, 255, cv2.THRESH_BINARY)
                            # mask = cv2.bitwise_not(mask)
                            # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                            # image = cv2.bitwise_and(image, image, mask=mask)
                            # image = cv2.addWeighted(image, 1, self._track_pnt_layer, 0.1, 1)
                            # image += self._track_pnt_layer
                            # image = self._track_pnt_layer.copy()

                if elapsed_time is not None:
                    text_type = elapsed_time + " " + text_type
                if len(text) > 0:
                    text_type = text_type + text + " "
                if show_runner_info and len(text_type) > 0:
                    current_line[1] += line_height
                    if show_runner_info:
                        if not has_data:
                            image_helper.put_text(image, text_type, current_line, font_scale=font_scale)
                        else:
                            image_helper.put_text(image, text_type, current_line, color=[0, 0, 255], font_scale=font_scale)
                if show_debug_texts and len(debug_texts) > 0:
                    for debug_text in debug_texts:
                        current_line_bottom[1] -= line_height * 2
                        image_helper.put_text(image, debug_text, current_line_bottom, color=[255, 250, 99], font_scale=font_scale * 2.75, thickness=2, back_color=[1, 1, 1])

        if show_runner_info:
            if len(data_added) > 0:
                show_last_data_frame_time = time.time()
                for data in data_added:
                    if data not in self.__preview_last_data:
                        self.__preview_last_data.append(data)
                        self.__preview_last_data_show_times.append(show_last_data_frame_time)
                    else:
                        self.__preview_last_data_show_times[self.__preview_last_data.index(data)] = show_last_data_frame_time
            for i in reversed(range(len(self.__preview_last_data))):
                elapsed = time.time() - self.__preview_last_data_show_times[i]
                if elapsed > 5:
                    del self.__preview_last_data_show_times[i]
                    del self.__preview_last_data[i]
            for last_data in self.__preview_last_data:
                current_line[1] += line_height
                image_helper.put_text(image, last_data, current_line, color=[0, 255, 255])

        return image

    @staticmethod
    def __get_runner_configuration_key(runner_type, class_name, configuration):
        if configuration is None:
            configuration = runner_type + ".json"
        return runner_type + "_" + class_name + "_" + configuration

    @staticmethod
    def __get_runner_key(type, class_name):
        return type + "_" + class_name


if __name__ == '__main__':
    NDUCameraService(constants.DEFAULT_NDU_GATE_CONF.replace('/', path.sep))
