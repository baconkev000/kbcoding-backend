class CreateCourses < ActiveRecord::Migration[7.1]
  def change
    create_table :courses do |t|
      t.string :name
      t.string :description
      t.references :course_type, null: false, foreign_key: true
      t.boolean :completed

      t.timestamps
    end
  end
end
