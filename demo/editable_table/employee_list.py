import pandas as pd

# https://dash.plot.ly/datatable

df = pd.read_csv("demo/static/employees.csv").head(4)
df['id'] = df.index

# https://www.json-generator.com/
# [
#   '{{repeat(10, 10)}}',
#   {
#     'First name': '{{firstName()}}',
#     'Last name': '{{surname()}}',
#
#     'Office':  function (tags) {
#       var office = ['New York', 'San Francisco', 'Edinburgh'];
#       return office[tags.integer(0, office.length - 1)];
#     },
#
#     'Position':  function (tags) {
#       var position = ['Specialist', 'Senior Javascript Developer', 'Systems Administrator'];
#       return position[tags.integer(0, position.length - 1)];
#     },
#
#     'Start date': '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-dd")}}',
#     'Salary' : '{{integer(80000, 300000)}}'
#   }
# ]

index = 0

new_employees = [
  {
    "First name": "Essie",
    "Last name": "Atkins",
    "Office": "Edinburgh",
    "Position": "Senior Javascript Developer",
    "Start date": "2015-02-25",
    "Salary": 169982
  },
  {
    "First name": "Geneva",
    "Last name": "Mcconnell",
    "Office": "New York",
    "Position": "Specialist",
    "Start date": "2020-01-28",
    "Salary": 273367
  },
  {
    "First name": "Bernice",
    "Last name": "Ellison",
    "Office": "Edinburgh",
    "Position": "Specialist",
    "Start date": "2018-10-20",
    "Salary": 123144
  },
  {
    "First name": "Kline",
    "Last name": "Pittman",
    "Office": "Edinburgh",
    "Position": "Specialist",
    "Start date": "2018-06-20",
    "Salary": 262001
  },
  {
    "First name": "Zelma",
    "Last name": "Crawford",
    "Office": "New York",
    "Position": "Senior Javascript Developer",
    "Start date": "2018-07-21",
    "Salary": 157515
  },
  {
    "First name": "Newton",
    "Last name": "Phelps",
    "Office": "San Francisco",
    "Position": "Systems Administrator",
    "Start date": "2015-11-16",
    "Salary": 296607
  },
  {
    "First name": "Rosemary",
    "Last name": "Sweeney",
    "Office": "San Francisco",
    "Position": "Systems Administrator",
    "Start date": "2020-08-28",
    "Salary": 112018
  },
  {
    "First name": "Myra",
    "Last name": "Haley",
    "Office": "Edinburgh",
    "Position": "Systems Administrator",
    "Start date": "2020-03-19",
    "Salary": 107468
  },
  {
    "First name": "Melisa",
    "Last name": "Frederick",
    "Office": "San Francisco",
    "Position": "Specialist",
    "Start date": "2019-12-28",
    "Salary": 297174
  },
  {
    "First name": "Rochelle",
    "Last name": "Arnold",
    "Office": "New York",
    "Position": "Systems Administrator",
    "Start date": "2014-12-23",
    "Salary": 285163
  }
]

def new_employee(id):
    """Return dummy employee record"""
    global index
    employee = new_employees[index]
    employee['id'] = id
    index = (index + 1) % (len(new_employees) - 1)
    return employee
