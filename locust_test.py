from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8000"  # Замените на адрес вашего сервиса с портом
    wait_time = between(0.001, 0.001)  # Устанавливаем минимальное время ожидания между запросами

    @task
    def index(self):
        self.client.get("/api/v1/currency_pair/}?currency_pair=bitcoin-usd")
