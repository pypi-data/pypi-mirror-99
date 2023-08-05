import json
import os
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, Qt
from .compound_exercises_db import (fetch_preferred_lifts, fetch_lifts_for_reps, lift_difference,
                                    update_lift_history, update_lifts_for_reps)
from fitness_tracker.user_profile.profile_db import fetch_units

class UpdateLiftsForRepsWindow(QWidget):
  change_lifts_for_reps_signal = pyqtSignal(bool)
  history_signal = pyqtSignal(bool)

  def __init__(self, sqlite_connection, pg_connection):
    super().__init__()
    self.sqlite_connection = sqlite_connection
    self.sqlite_cursor = sqlite_connection.cursor()
    self.pg_connection = pg_connection
    self.pg_cursor = self.pg_connection.cursor()
    self.setStyleSheet("""
    QWidget{
      background-color: #322d2d;
      font-weight: bold;
      color:#c7c7c7;
    }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: center;
      padding-left: 5%;
      font-family: Montserrat;
    }
    QPushButton:hover:!pressed{
      border: 2px solid;
      border-color: #747474;
    }
    QPushButton:pressed{
      border: 2px solid;
      background-color: #323232;
    }
    """) 
    self.setWindowModality(Qt.ApplicationModal)
    self.units = "kg" if fetch_units(self.sqlite_cursor) == "metric" else "lb"
    self.preferred_lifts = json.loads(fetch_preferred_lifts(self.sqlite_cursor))
    self.setWindowTitle("Update Lifts For Reps")
    self.setLayout(self.create_panel())
    self.set_line_edit_values()

  def create_panel(self):
    form_layout = QFormLayout()
    
    exercise_label = QLabel("Exercise")
    header_layout = QHBoxLayout()
    reps_label = QLabel("Reps")
    weight_label = QLabel("Weight")
    header_layout.addWidget(reps_label)
    header_layout.addWidget(weight_label)

    horizontal_press_label = QLabel(self.preferred_lifts["Horizontal Press"])
    self.horizontal_press_reps_edit = QLineEdit()
    self.horizontal_press_reps_edit.setValidator(QIntValidator())
    x_label = QLabel("x")
    self.horizontal_press_edit = QLineEdit() 
    self.horizontal_press_edit.setValidator(QIntValidator())
    units_label = QLabel(self.units)
    hbox = QHBoxLayout()
    hbox.addWidget(self.horizontal_press_reps_edit)
    hbox.addWidget(x_label)
    hbox.addWidget(self.horizontal_press_edit)
    hbox.addWidget(units_label)

    floor_pull_label = QLabel(self.preferred_lifts["Floor Pull"])
    self.floor_pull_reps_edit = QLineEdit()
    self.floor_pull_reps_edit.setValidator(QIntValidator())
    x_label1 = QLabel("x")
    self.floor_pull_edit = QLineEdit()
    self.floor_pull_edit.setValidator(QIntValidator())
    units_label1 = QLabel(self.units)
    hbox1 = QHBoxLayout()
    hbox1.addWidget(self.floor_pull_reps_edit)
    hbox1.addWidget(x_label1)
    hbox1.addWidget(self.floor_pull_edit)
    hbox1.addWidget(units_label1)

    squat_label = QLabel(self.preferred_lifts["Squat"])
    self.squat_reps_edit = QLineEdit()
    self.squat_reps_edit.setValidator(QIntValidator())
    x_label2 = QLabel("x")
    self.squat_edit = QLineEdit()
    self.squat_edit.setValidator(QIntValidator())
    units_label2 = QLabel(self.units)
    hbox2 = QHBoxLayout()
    hbox2.addWidget(self.squat_reps_edit)
    hbox2.addWidget(x_label2)
    hbox2.addWidget(self.squat_edit)
    hbox2.addWidget(units_label2)

    vertical_press_label = QLabel("Overhead Press")
    self.vertical_press_reps_edit = QLineEdit()
    self.vertical_press_reps_edit.setValidator(QIntValidator())
    x_label3 = QLabel("x")
    self.vertical_press_edit = QLineEdit()
    self.vertical_press_edit.setValidator(QIntValidator())
    units_label3 = QLabel(self.units)
    hbox3 = QHBoxLayout()
    hbox3.addWidget(self.vertical_press_reps_edit)
    hbox3.addWidget(x_label3)
    hbox3.addWidget(self.vertical_press_edit)
    hbox3.addWidget(units_label3)

    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_lifts_for_reps())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_update_lifts_for_reps())
    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(cancel_button)  
    
    form_layout.addRow(exercise_label, header_layout)
    form_layout.addRow(horizontal_press_label, hbox)
    form_layout.addRow(floor_pull_label, hbox1)
    form_layout.addRow(squat_label, hbox2)
    form_layout.addRow(vertical_press_label, hbox3)
    
    main_layout = QVBoxLayout()
    main_layout.addLayout(form_layout)
    main_layout.addLayout(buttons_layout)
    
    return main_layout

  def save_lifts_for_reps(self):
    try:
      exercises = list(json.loads(fetch_lifts_for_reps(self.sqlite_cursor)).keys())
      horizontal_press_weight = str(int(self.horizontal_press_edit.text()))
      floor_pull_weight = str(int(self.floor_pull_edit.text()))
      squat_weight = str(int(self.squat_edit.text()))
      vertical_press_weight = str(int(self.vertical_press_edit.text()))

      horizontal_press_reps = str(int(self.horizontal_press_reps_edit.text()))      
      floor_pull_reps = str(int(self.floor_pull_reps_edit.text()))
      squat_reps = str(int(self.squat_reps_edit.text()))
      vertical_press_reps = str(int(self.vertical_press_reps_edit.text()))
    
      new_lifts_for_reps = {exercises[0]: [horizontal_press_reps, horizontal_press_weight],
                            exercises[1]: [floor_pull_reps, floor_pull_weight],
                            exercises[2]: [squat_reps, squat_weight],
                            exercises[3]: [vertical_press_reps, vertical_press_weight]}
      diff = lift_difference(new_lifts_for_reps, self.sqlite_cursor, lifts_reps=True)
      update_lift_history(diff, self.sqlite_connection, self.pg_connection)
      self.history_signal.emit(True)
      update_lifts_for_reps(new_lifts_for_reps, self.sqlite_connection, self.pg_connection)
      self.change_lifts_for_reps_signal.emit(True)
      self.set_line_edit_values()
      self.close()
    except ValueError:
      pass
  
  def close_update_lifts_for_reps(self):
    self.close()
    self.set_line_edit_values()

  def set_line_edit_values(self):
    lift_values = list(json.loads(fetch_lifts_for_reps(self.sqlite_cursor)).values())
    reps = [lift[0] for lift in lift_values]
    weight = [lift[1] for lift in lift_values]
    
    reps_line_edit = [self.horizontal_press_reps_edit,
                      self.floor_pull_reps_edit,
                      self.squat_reps_edit,
                      self.vertical_press_reps_edit]

    weight_line_edit = [self.horizontal_press_edit,
                        self.floor_pull_edit,
                        self.squat_edit,
                        self.vertical_press_edit]

    for i, line_edit in enumerate(reps_line_edit):
      line_edit.setText(reps[i])

    for i, line_edit in enumerate(weight_line_edit):
      line_edit.setText(weight[i])
