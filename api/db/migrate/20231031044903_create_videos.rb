class CreateVideos < ActiveRecord::Migration[7.1]
  def change
    create_table :videos do |t|
      t.string :name
      t.references :section, null: false, foreign_key: true
      t.binary :video
      t.boolean :completed

      t.timestamps
    end
  end
end
