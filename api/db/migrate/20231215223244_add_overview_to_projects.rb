class AddOverviewToProjects < ActiveRecord::Migration[7.1]
  def change
    add_column :projects, :overview, :string
  end
end
