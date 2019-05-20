import tornado.ioloop
from app.application import LocationCodeApplication
import logging


if __name__ == "__main__":
    address, port = ('0.0.0.0', 8484)
    logging.basicConfig(level=logging.DEBUG)
    application = LocationCodeApplication()
    server = application.listen(port=port, address=address)
    logging.info(f'Listening http://{address}:{port}/')
    try:
        current_io_loop = tornado.ioloop.IOLoop.current()
        tornado.ioloop.PeriodicCallback(
            callback=application.run_daily,
            callback_time=86400000,  # Daily
            io_loop=current_io_loop,
        ).start()
        current_io_loop.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Exit due to keyboard interruption')
