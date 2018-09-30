# Created by anmisra on 9/30/18
"""
This script you will automatically google forms
"""

from random import choice

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest


class GoogleForms(Spider):
    name = 'google_forms'
    start_urls = [
        'https://goo.gl/forms/SQi4L0GF9rvbFBvn1'
    ]  # Google form url
    comman_names = [{
        'name': 'Anurag Misra', 'age': '20-25', 'gender': 'Male'
    }]
    pre_define_question = ['Name', 'Gender', 'Age(in yrs)']

    def parse(self, response):
        questions_div = response.xpath(
            '//form//div[@role="listitem"]'
        )
        pre_define_answer = self.get_name_age()
        form_data = {}
        for question in questions_div:
            # Dictionary of questions and answers
            answer = self.get_question_answer(question, pre_define_answer)
            if answer:
                form_data.update(answer)

        yield FormRequest.from_response(
            response,
            formid='mG61Hd',
            formdata=form_data,
            callback=self.parse_form_submission
        )

    def parse_form_submission(self, response):
        if 'Your response has been recorded.' in response.body:
            print 'SUCCESSFUL'

    def get_question_answer(self, question, pre_define_answer):
        answer_dic = {}
        answer = None
        question_id = question.xpath('.//input/@name').extract_first()
        question_name = question.xpath(
            './/div[@role="heading"]/text()').extract_first(default='').strip()
        question_type = question.xpath(
            './/input[@name]/preceding-sibling::div/@role'
        ).extract_first()
        question_choice = question.xpath(
            './/content//label//div/@data-value'
        ).extract()
        # Adding Special for age, gender
        # Rest option filling any random choice
        if question_name in self.pre_define_question:
            if question_name == 'Name':
                answer = pre_define_answer[0]
            elif question_name == 'Age(in yrs)':
                answer = pre_define_answer[1]
            elif question_name == 'Gender':
                answer = pre_define_answer[2]
        else:
            # TODO: Add more question types
            if question_type == "radiogroup":
                answer = choice(question_choice)
        if answer:
            answer_dic[question_id] = answer
            return answer_dic

    def get_name_age(self):
        value = choice(self.comman_names)
        return value['name'], value['age'], value['gender']


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    })
    process.crawl(GoogleForms)
    process.start()
