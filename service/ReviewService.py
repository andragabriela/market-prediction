from repository.ReviewRepository import ReviewRepository

class ReviewService:
    def __init__(self):
        self.repository = ReviewRepository()

    def scrape_data(self):
        print("Service: Performing web scraping...")
        # Web scraping logic can go here, or delegate further to repo
        self.repository.scrape_data()

    def load_tabular_data(self):
        print("Service: Loading data from file...")
        # Loading data logic
        self.repository.load_tabular_data()

    def call_external_api(self):
        print("Service: Fetching data from external API...")
        # API calling logic
        self.repository.call_external_api()

    def create_visualization(self):
        print("Service: Generating visualizations...")
        # Visualization logic
        self.repository.create_visualization()

    def load_json_data(self, file):
        print("Service: Loading data from json...")
        # Loading data logic
        self.repository.load_json_data(file)

    def build_segmentation_model(self):
        self.repository.build_segmentation_model()