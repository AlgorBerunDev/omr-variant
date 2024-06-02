from consumer_base import ConsumerBase

class CoordinateAnalysisConsumer(ConsumerBase):
    def process_message(self, body, correlation_id):
        # Логика анализа координат ответов
        pass

if __name__ == "__main__":
    consumer = CoordinateAnalysisConsumer(queue='coordinate_analysis_queue', routing_key='coordinate_analysis')
    consumer.start_consuming()
