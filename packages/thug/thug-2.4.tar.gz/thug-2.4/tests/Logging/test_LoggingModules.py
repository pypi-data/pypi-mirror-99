import thug.Logging.LoggingModules as log_modules


class TestLoggingModules:
    def test_json(self):
        assert log_modules.LoggingModules['json'] is log_modules.JSON.JSON

    def test_mongodb(self):
        assert log_modules.LoggingModules['mongodb'] is log_modules.MongoDB.MongoDB

    def test_elasticsearch(self):
        assert log_modules.LoggingModules['elasticsearch'] is log_modules.ElasticSearch.ElasticSearch
