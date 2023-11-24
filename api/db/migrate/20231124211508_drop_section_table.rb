class DropSectionTable < ActiveRecord::Migration[7.1]
  def change
    drop_table :sections, force: :cascade
  end
end
