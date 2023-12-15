class RenameNameToTitle < ActiveRecord::Migration[7.1]
  def change
    rename_column :projects, :name, :title
  end
end
