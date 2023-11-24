class ChangeCourseTypeIdtoProjectTypeId < ActiveRecord::Migration[7.1]
  def change
    rename_column :sections, :course_id, :project_id
    rename_column :projects, :course_type_id, :project_type_id
  end
end
