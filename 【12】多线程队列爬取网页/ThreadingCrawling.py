from queue import Queue
import threading
from DownloadImagesHelper import ImagesHelper
# 多线程爬取图片：由2个线程抓取url到queue里边，10个线程从queue中下载图片
x = 0  # 标号
threadLock = threading.RLock()


class DownloadWorker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            global x
            try:
                link = self.queue.get(timeout=60)
            except Exception:
                break
            try:
                ImagesHelper.down_url(link, x)
            except Exception:
                continue
            finally:
                threadLock.acquire()  # 需要同步
                x += 1
                threadLock.release()
                self.queue.task_done()


class GetUrlWorker(threading.Thread):
    def __init__(self, queue, start, end):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start_p = start
        self.end_p = end

    def run(self):
        image_helper = ImagesHelper(self.queue, self.start_p, self.end_p)
        image_helper.get_urls()


def main():
    queue = Queue()
    # Create 10 worker threads
    for t in range(10):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    get_worker1 = GetUrlWorker(queue, 2100, 2103)
    get_worker1.daemon = True
    get_worker1.start()

    get_worker2 = GetUrlWorker(queue, 2103, 2105)
    get_worker2.daemon = True
    get_worker2.start()

    get_worker1.join()
    get_worker2.join()

    queue.join()
    print("over!")


if __name__ == '__main__':
    main()
