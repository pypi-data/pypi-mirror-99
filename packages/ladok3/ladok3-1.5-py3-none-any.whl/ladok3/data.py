import csv
import datetime
import ladok3
import os
import sys

def extract_data_for_round(ladok, course_round):
  course_start = course_round.start
  course_length = course_round.end - course_start
  component = course_round.components()[0]
  results = ladok.search_reported_results_JSON(
    course_round.round_id, component.instance_id)

  for result in results:
    student = result["Student"]["Uid"]

    for component_result in result["ResultatPaUtbildningar"]:
      if component_result["HarTillgodoraknande"]:
        continue

      if "Arbetsunderlag" in component_result:
        result_data = component_result["Arbetsunderlag"]
      elif "SenastAttesteradeResultat" in component_result:
        result_data = component_result["SenastAttesteradeResultat"]
      else:
        continue
      matching_component = course_round.components(
        instance_id=result_data["UtbildningsinstansUID"])
      if len(matching_component) < 1:
        continue
      component_code = matching_component[0].code
      if "Betygsgradsobjekt" in result_data:
        grade = result_data["Betygsgradsobjekt"]["Kod"]
        date = datetime.date.fromisoformat(
          result_data["Examinationsdatum"])
        normalized_date = (date - course_start) / course_length
      else:
        grade = "-"
        normalized_date = None

      yield (student, component_code, grade, normalized_date)
def clean_data(data):
  data = list(data)
  students_to_remove = reregistered_students(data)
  return remove_students(students_to_remove, data)
def reregistered_students(data):
  students = set()
  for student, _, _, time in data:
    if time and time < 0:
      students.add(student)
  return students

def remove_students(students, data):
  for row in data:
    if row[0] not in students:
      yield row

def add_command_options(parser):
  data_parser = parser.add_parser("data",
    help="Returns course results data in CSV form")
  data_parser.set_defaults(func=command)
  data_parser.add_argument("course_code",
    help="The course code of the course for which to export data")

def command(ladok, args):
  data_writer = csv.writer(sys.stdout)
  course_rounds = ladok.search_course_rounds(code=args.course_code)

  data_writer.writerow([
    "Course", "Round", "Component", "Student", "Grade", "Time"
  ])
  for course_round in course_rounds:
    data = extract_data_for_round(ladok, course_round)
    data = clean_data(data)

    for student, component, grade, time in data:
      data_writer.writerow(
        [course_round.code, course_round.round_code, component,
          student, grade, time]
      )
