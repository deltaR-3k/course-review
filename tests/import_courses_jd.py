#!/usr/bin/env python3
import sys
import uuid

from pymongo import MongoClient

sys.path.append('..')  # fix import directory

from app import app, db
from app.models import *
from datetime import datetime
import pickle

import dataclasses

import dataclasses
import pickle
from pathlib import Path
import pandas as pd

client = MongoClient('127.0.0.1', 27017, connectTimeoutMS=3000)
mongoclient = client['courses']
colall = mongoclient['all']  # offical+review
#
# mongoclient = client['test']
# colall = mongoclient['all_elective_courses']  # offical+review

import pandas as pd

df = pd.read_excel('courses.xlsx')
docs = dict()
for row in df.iterrows():
  name = row[1][1]
  docs[name] = {
    "课程号": "U10M11013",
    "课程名": "算法设计与分析",
    "学分": "2.0",
    "现在模块": "学科基础课程",
    "开课单位": "计算机学院",
    "类型": "必修",
    "授课教师": "王歧",
  }

dept_str_to_name = {
"航空学院": 1,
"航天学院": 2,
"航海学院": 3,
"材料学院": 4,
"机电学院": 5,
"力学与土木建筑学院": 6,
"动力与能源学院": 7,
"电子信息学院": 8,
"自动化学院": 9,
"计算机学院": 10,
"数学与统计学院": 11,
"物理科学与技术学院": 12,
"化学与化工学院": 13,
"管理学院": 14,
"公共政策与管理学院": 15,
"软件学院": 16,
"生命学院": 17,
"外国语学院": 18,
"教育实验学院": 19,
"国际教育学院": 20,
"马克思主义学院": 21,
"西北工业大学伦敦玛丽女王大学工程学院": 22,
"微电子学院": 23,
"网络空间安全学院": 24,
"民航学院": 25,
"生态环境学院": 26,
"DL": 27,
"体育部": 28,
"工程实践训练中心": 29,
"艺术教育中心": 30,
"继续教育学院": 31,
"医学研究院": 32,
"柔性电子研究院": 33,
"团委": 34,
"光电与智能研究院": 35,
"党委学生工作部（学生处、人民武装部）": 36,
"人民武装部": 37,
"无人系统技术研究院": 38,
}




@dataclasses.dataclass
class JDCourse:
  name: str
  id: str
  semester: str
  recommendation: str
  reviews: list
  optional_course_is_core: bool
  highest: float
  average: float
  lowest: float
  df_course: pd.DataFrame
  class_headcount: int


# jd = pickle.load(open('/tmp/courses.pickle', 'rb'))


depts_code_map = dict()
classes_map = dict()
majors_map = dict()
titles_map = dict()
teachers_id_map = dict()
teachers_name_map = dict()
# We should load all existing courses, because SQLAlchemy does not support .merge on non-primary-key,
# and we want to preserve course ID (primary key) for each (cno, term) pair.
course_classes_map = dict()
course_terms_map = dict()
courses_map = dict()


def load_courses(insert=True):
  for name, i in dept_str_to_name.items():
    dept = Dept()
    dept.code = i
    dept.name = name

    db.session.add(dept)
  db.session.commit()

  all_teachers = dict()
  for doc in colall.find():
    for teacher in doc['teachers']:
      if teacher not in all_teachers:
        t = Teacher()
        t.name = teacher
        db.session.add(t)
        all_teachers[teacher] = t
  db.session.commit()

  existing_depts = Dept.query.all()
  for dept in existing_depts:
    depts_code_map[dept.code] = dept
  print('%d existing departments loaded' % len(depts_code_map))

  existing_teachers = Teacher.query.all()
  print('%d existing teachers loaded' % len(existing_teachers))

  existing_courses = Course.query.all()
  print('%d existing courses loaded' % len(existing_courses))

  existing_course_classes = CourseClass.query.all()
  print('%d existing course classes loaded' % len(existing_course_classes))

  existing_course_terms = CourseTerm.query.all()
  print('%d existing course terms loaded' % len(existing_course_terms))

  new_teacher_count = 0
  new_course_count = 0
  new_term_count = 0
  new_class_count = 0
  new_dept_count = 0

  int_allow_empty = lambda string: int(string) if string.strip() else 0
  course_kcbh = {}
  print('Data loaded with %d courses' % colall.count_documents({}))

  user =  User.query.filter_by(username='initbot1').first()
  if user is None:
    user = User(username='initbot', email='initbot@xjtumen.nonexists', password=str(uuid.uuid4().hex))
    user.xjtumen_username = 'course_init_bot'

    user.role = 'Bot'
    user.save()
    user.confirm()

  for doc in colall.find():
    # print(doc)

    course = Course()
    course.name = doc['课程名']
    course.dept_id = dept_str_to_name[doc['开课单位']]

    if doc.get('备注') is not None:
      if doc.get('other_fields') is None or len(doc['other_fields']) == 0:
        doc['other_fields'] = doc.get('备注')
      else:
        doc['other_fields'] = doc.get('备注') + '\n' + doc['other_fields']
    if doc.get('选课要求') is not None:
      if doc.get('other_fields') is None or len(doc['other_fields']) == 0:
        doc['other_fields'] = doc.get('选课要求') + '\n' + doc['other_fields']
      else:
        doc['other_fields'] = doc.get('选课要求')
    course.introduction = doc['other_fields']
    db.session.add(course)
    this_course_teachers = set()
    course.teachers = [all_teachers[t] for t in set(doc['teachers'])]
    # print(set(doc['teachers']))
    db.session.commit()

    course_rate = CourseRate()
    course_rate.course = course
    db.session.add(course_rate)

    sem_cls_list = doc.get('semester_class_list')
    if sem_cls_list is None:
      continue

    if len(sem_cls_list) == 1 and sem_cls_list[0]['semester'] == '20771':
      course_term = CourseTerm()
      db.session.add(course_term)
      course_term.course = course
      course_term.term = '20772'
      course_term.courseries = doc['课程号']
      course_term.code = doc['课程号']
    for sem_cls in sem_cls_list:
      course_term = CourseTerm()
      db.session.add(course_term)
      mapping = {'核心课': '基础通识类核心课',
                 '选修课': '基础通识类选修课'}
      course_term.course_type = mapping[doc['类型']]

      if sem_cls.get('highest') is not None:
        course_term.grade_highest = sem_cls['highest']
        course_term.grade_lowest = sem_cls['lowest']
        course_term.grade_average = sem_cls['average']

      course_term.course = course
      course_term.join_type = doc['现在模块']  # 选课类别
      if doc.get('学时') is not None:
        course_term.hours = doc['学时']
      if doc.get('学分') is not None:
        course_term.credit = doc['学分']
      course_term.term = sem_cls['semester']
      if sem_cls.get('grade_range_student_count_list') is not None:
        course_term.has_grade_graph = True
        course_term.grade_u60 = sem_cls['grade_range_student_count_list'][0]
        course_term.grade_61_70 = sem_cls['grade_range_student_count_list'][1]
        course_term.grade_71_80 = sem_cls['grade_range_student_count_list'][2]
        course_term.grade_81_90 = sem_cls['grade_range_student_count_list'][3]
        course_term.grade_91_100 = sem_cls['grade_range_student_count_list'][4]
      else:
        course_term.has_grade_graph = False
      course_term.courseries = doc['课程号']
      course_term.code = doc['课程号']
      # course_term.class_numbers = '2'

      course_class = CourseClass()
      # update course class info
      course_class.course = course
      course_class.term = sem_cls['semester']

      # course_class.cno = '1'
      db.session.add(course_class)

      if doc['has_review_entry']:
        once = False
        for review_content in sem_cls['review_text_list']:
          review = Review()
          db.session.add(review)
          review.course = course

          review.term = sem_cls['semester']
          review.difficulty = 2
          review.homework = 2
          review.grading = 2
          review.gain = 2
          review.rate = 5
          review.author = user
          review.content = review_content
          if once:
            if (recomm := sem_cls.get('recommendation')) is not None:
              review.content = f'{recomm}\n{review.content}'
          review.update_time = datetime.utcnow()

          history = ReviewHistory()
          db.session.add(history)

          history.difficulty = review.difficulty
          history.homework = review.homework
          history.grading = review.grading
          history.gain = review.gain
          history.rate = review.rate
          history.content = review.content
          history.author_id = review.author_id
          history.course_id = review.course_id
          history.term = review.term
          history.publish_time = review.publish_time
          history.update_time = review.update_time
          history.is_anonymous = review.is_anonymous
          history.only_visible_to_student = review.only_visible_to_student
          history.is_hidden = review.is_hidden
          history.is_blocked = review.is_blocked

          history.review_id = review.id
          history.operation = 'create'
          history.operation_user_id = user.id

    db.session.commit()


with app.app_context():
  # we have merge now, do not drop existing data
  db.create_all()
  load_courses()
