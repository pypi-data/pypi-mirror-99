from os import path
import cv2

from ndu_gate_camera.api.video_source import VideoSource, log


class FileVideoSource(VideoSource):
    def __init__(self, source_config):
        """

        :param source_config:
        """
        super().__init__()
        log.info("source_config %s", source_config)
        self.__video_path = source_config.get("file_path", None)
        if self.__video_path is None:
            raise ValueError("Video file path is empty")

        if path.isfile(self.__video_path) is False:
            # TODO - get default installation path using OS
            self.__video_path = source_config.get("data_folder", "var/lib/ndu_gate_camera/data/".replace('/',
                                                                                                         path.sep)) + self.__video_path

        if path.isfile(self.__video_path) is False:
            raise ValueError("Video file is not exist : %s", self.__video_path)
        self._set_capture()

    def get_frames(self):
        log.debug("start video streaming..")
        count = 0
        # TODO - bitince başa sar?
        while self.__capture.isOpened():
            ret, frame = self.__capture.read()
            if ret is False:
                break

            yield count, frame
            count += 1

        log.debug("video finished..")
        self.__capture.release()
        cv2.destroyAllWindows()

        try:
            count = 0
            while self.__capture.isOpened():
                ok, frame = self.__capture.read()
                if not ok:
                    break
                yield count, frame
                count += 1
        except Exception as e:
            log.error(e)
        finally:
            log.debug("video finished..")
            self.__capture.release()
            cv2.destroyAllWindows()

    def reset(self):
        self._set_capture()

    def stop(self):
        # TODO
        pass

    def _set_capture(self):
        if path.isfile(self.__video_path) is False:
            raise ValueError("Video file is not exist")
        self.__capture = cv2.VideoCapture(self.__video_path)
