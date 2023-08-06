import time

import redis
from locust import HttpUser, task, constant

from other.common.database.variable.storage import Storage


class Tester(HttpUser):
    wait_time = constant(5)
    token = None
    key = None
    user_id = None
    submission_id = None

    def on_start(self):
        # token = UCODE_STUDENT_USER_TOKEN[random.randint(0, len(UCODE_STUDENT_USER_TOKEN) - 1)]
        # self.client.headers.update({'access-token': token})
        redisClient = redis.StrictRedis(host='localhost',
                                        port=6379,
                                        db=0)
        while True:
            self.token = redisClient.lpop('tokens').decode('utf-8')
            self.client.headers.update({'access-token': self.token})
            user_info_res = self.client.get("/api/users/info", name='user_info')
            Storage.CURRENT_TOTAL_USER = Storage.CURRENT_TOTAL_USER + 1
            if user_info_res.status_code == 200:
                # self.token = UCODE_STUDENT_USER_TOKEN[Storage.CURRENT_TOTAL_USER]
                self.key = "test_user_draft_" + self.token
                self.user_id = user_info_res.json()['data']['id']
                contest_detail_res = self.client.get(f"/api/contests/gio-lap-trinh-mixed", name='contest_detail')
                if not contest_detail_res.json()['data']['current_submission']:
                    self.client.post(f"/api/learning/lesson/5090/submit-quiz",
                                     json={'list_answers': [], 'draft': True}, name='submit_draft')
                    contest_detail_res = self.client.get(f"/api/contests/gio-lap-trinh-mixed", name='contest_detail')
                self.submission_id = contest_detail_res.json()['data']['current_submission']
                user_data_draft_res = self.client.get(f"/api/user-data/draft?key={self.key}&user_id={self.user_id}",
                                                      name='user_draft')
                print(self.key, self.user_id , user_data_draft_res.json())
                return
            else:
                Storage.CURRENT_TOTAL_INVALID_USER = Storage.CURRENT_TOTAL_INVALID_USER + 1

    @task
    def run_contest(self):
        time.sleep(1000)
        # self.client.post(f"/api/learning/lesson/5090/submit-quiz",
        #                  json={'list_answers': [], 'draft': True}, name='submit_draft')

        # contest_detail_res = self.client.get(f"/api/contests/gio-lap-trinh-mixed", name='contest_detail')
        # self.submission_id = contest_detail_res.json()['data']['current_submission']

        # user_data_draft_res = self.client.get(f"/api/user-data/draft?key={self.key}&user_id={self.user_id}",
        #                                       name='user_draft')
        for i in range(25):
            user_data_draft2_res = self.client.post(f"/api/user-data/draft",
                                                    json={"key": self.key,
                                                          "value": "{\"46675\":{\"data\":1,\"status\":\"waiting\"},\"46691\":{\"data\":1,\"status\":\"waiting\"},\"46693\":{\"data\":1,\"status\":\"waiting\"},\"46694\":{\"data\":1,\"status\":\"waiting\"},\"46696\":{\"data\":3,\"status\":\"waiting\"},\"46697\":{\"data\":1,\"status\":\"waiting\"}}"},
                                                    name='user_draft')

            submit_draft_res = self.client.post(f"/api/learning/lesson/5090/submit-quiz",
                                                json={"list_answers": [{"question_id": 46675, "user_answer": "1"},
                                                                       {"question_id": 46691, "user_answer": "1"},
                                                                       {"question_id": 46693, "user_answer": "1"},
                                                                       {"question_id": 46694, "user_answer": "1"},
                                                                       {"question_id": 46696, "user_answer": "3"},
                                                                       {"question_id": 46697, "user_answer": "1"}],
                                                      "draft": True,
                                                      "submission_id": self.submission_id}, name='submit_draft')
            if submit_draft_res.status_code != 200:
                print(self.token, self.submission_id, submit_draft_res.status_code)
            time.sleep(1)

        res = self.client.post(f"/api/learning/lesson/5090/submit-quiz",
                               json={"list_answers": [{"question_id": 46675, "user_answer": "1"},
                                                      {"question_id": 46691, "user_answer": "1"},
                                                      {"question_id": 46693, "user_answer": "1"},
                                                      {"question_id": 46694, "user_answer": "1"},
                                                      {"question_id": 46696, "user_answer": "3"},
                                                      {"question_id": 46697, "user_answer": "1"}], "draft": False,
                                     "submission_id": self.submission_id}, name='submit')
        if res.status_code == 200:
            Storage.TOTAL_SUCCESS = Storage.TOTAL_SUCCESS + 1
        print(Storage.TOTAL_SUCCESS)
