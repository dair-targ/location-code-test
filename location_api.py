import tornado.web
import tornado.ioloop
from app.location_comparison_handler import LocationComparisonHandler
from app.location_data_handler import LocationHandler


def make_app():
    return tornado.web.Application([(r"/location-data/([a-zA-Z0-9]*)?", LocationHandler, {}),
                                    (r"/location-comparison/cities=\[(\S+)\]", LocationComparisonHandler, {})])

if __name__ == "__main__":
    application = make_app()
    application.listen(8484)
    tornado.ioloop.IOLoop.current().start()
