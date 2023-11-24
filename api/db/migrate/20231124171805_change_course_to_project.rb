class ChangeCourseToProject < ActiveRecord::Migration[7.1]
  def change
    rename_table :courses, :projects
    rename_table :course_types, :project_types
  end
end
