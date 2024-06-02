from consumer_base import ConsumerBase

class BlockIDAnalysisConsumer(ConsumerBase):
    def process_message(self, body, correlation_id):
        # Логика анализа блоков и кодов ID
        pass

if __name__ == "__main__":
    consumer = BlockIDAnalysisConsumer(queue='block_id_analysis_queue', routing_key='block_id_analysis')
    consumer.start_consuming()
