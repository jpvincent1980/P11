from locust import HttpUser, task


class ServerTest(HttpUser):

    @task
    def login(self):
        self.client.get("/")