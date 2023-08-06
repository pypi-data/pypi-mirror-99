import unittest

import pronotepy
import datetime

client = pronotepy.Client('https://demo.index-education.net/pronote/eleve.html', 'demonstration', 'pronotevs')


class TestClient(unittest.TestCase):
    global client

    def test__get_week(self):
        self.assertEqual(client.get_week(client.start_day + datetime.timedelta(days=8)), 2)

    def test_lessons(self):
        self.assertIsNotNone(
            client.lessons(client.start_day, client.start_day + datetime.timedelta(days=8)))

    def test_periods(self):
        self.assertIsNotNone(client.periods)

    def test_current_period(self):
        self.assertIsNotNone(client.current_period)

    def test_homework(self):
        self.assertIsNotNone(
            client.homework(client.start_day, client.start_day + datetime.timedelta(days=8)))

    def test_refresh(self):
        client.refresh()
        self.assertEqual(client.session_check(), True)


class TestPeriod(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        global client
        cls.period = client.current_period

    def test_grades(self):
        self.assertIsNotNone(self.period.grades)

    def test_averages(self):
        self.assertIsNotNone(self.period.averages)

    def test_overall_average(self):
        self.assertIsNotNone(self.period.overall_average)

    def test_evaluations(self):
        evaluations = self.period.evaluations
        self.assertIsNotNone(evaluations)
        for evaluation in evaluations:
            for acquisition in evaluation.acquisitions:
                self.assertIsNotNone(acquisition)


class TestLesson(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        global client
        cls.lesson = client.lessons(client.start_day+datetime.timedelta(days=4))[0]

    def test_normal(self):
        self.assertIsNotNone(self.lesson.normal)

    def test_content(self):
        self.assertIsInstance(self.lesson.content, pronotepy.LessonContent)


class TestLessonContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        global client
        cls.lessonContent = client.lessons(client.start_day+datetime.timedelta(days=4))[0].content

    def test_files(self):
        self.assertIsNotNone(self.lessonContent.files)


class TestParentClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = pronotepy.ParentClient('https://demo.index-education.net/pronote/parent.html', 'demonstration', 'pronotevs')

    def test_set_child(self):
        self.client.set_child(self.client.children[1])
        self.client.set_child('PARENT Fanny')

    def test_homework(self):
        self.assertIsNotNone(
            self.client.homework(self.client.start_day, self.client.start_day + datetime.timedelta(days=8)))


if __name__ == '__main__':
    unittest.main()
