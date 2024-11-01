from service.ReviewService import ReviewService


class ReviewController:
    def __init__(self):
        self.service = ReviewService()

    def scrape_data(self):
        print("Controller: Starting data scraping...")
        self.service.scrape_data()

    def load_tabular_data(self):
        print("Controller: Loading tabular data...")
        self.service.load_tabular_data()

    def load_json_data(self, file):
        print("Controller: Loading json data...")
        self.service.load_json_data(file)

    def call_external_api(self):
        print("Controller: Calling external API...")
        self.service.call_external_api()

    def create_visualization(self):
        print("Controller: Creating visualizations...")
        self.service.create_visualization()

    def build_segmentation_model(self):
        self.service.build_segmentation_model()