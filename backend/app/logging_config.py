import logging

def setup_logging():
    logger = logging.getLogger('MAIN')
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()  # コンソールハンドラー
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger

# このモジュールがインポートされたときにsetup_loggingを呼び出してロギングを設定する
logger = setup_logging()

