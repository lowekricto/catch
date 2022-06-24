import costrCatch
import threading


def costrrun():
    t1 = threading.Thread(target=costrCatch.getphoto, args=(2,))
    # t1.start()
    t2 = threading.Thread(target=costrCatch.getcoser, args=(2,))
    # t2.start()

    costrCatch.getcoser(2)


costrrun()
