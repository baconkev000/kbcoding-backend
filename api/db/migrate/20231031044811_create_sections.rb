class CreateSections < ActiveRecord::Migration[7.1]
  def change
    create_table :sections do |t|
      t.string :name
      t.references :course, null: false, foreign_key: true
      t.boolean :completed

      t.timestamps
    end
  end
end
