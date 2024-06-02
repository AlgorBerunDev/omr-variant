project/
│
├── src/
│ ├── **init**.py
│ ├── main.py
│ ├── config.py
│ │
│ ├── consumer/
│ │ ├── **init**.py
│ │ ├── consumer.py
│ │
│ ├── image_processing/
│ │ ├── **init**.py
│ │ ├── a4_detection.py
│ │ ├── coordinate_analysis.py
│ │ ├── answer_analysis.py
│ │
│ ├── utils/
│ │ ├── **init**.py
│ │ ├── helpers.py
│ │
│ ├── minio/
│ │ ├── **init**.py
│ │ ├── minio_client.py
│ │
│ └── models/
│ ├── **init**.py
│ ├── student.py
│ ├── variant.py
│
├── tests/
│ ├── **init**.py
│ ├── test_consumer.py
│ ├── test_a4_detection.py
│ ├── test_coordinate_analysis.py
│ ├── test_answer_analysis.py
│ ├── test_helpers.py
│
├── .env # Файл с переменными окружения
├── requirements.txt
├── README.md
└── .gitignore

```python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
```
