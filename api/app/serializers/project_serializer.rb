class ProjectSerializer < ActiveModel::Serializer
  attributes :id, :name, :description, :completed
  belongs_to :project_type
end
