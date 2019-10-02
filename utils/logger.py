from timeutils import get_current_format_time
from configs import DEBUG


def log(pre, tag, message):
    now = get_current_format_time()
    print "%s %s\t\t%s:\t%s" % (pre, now, tag, message)


def log_d(tag, message):
    log("[+]", tag, message)


def log_e(tag, message):
    log("[-]", tag, message)


if __name__ == "__main__":
    log_d("Test", "Hello world")
    log_e("Test", "Hello world")
