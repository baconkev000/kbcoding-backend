class ProjectSerializer < ActiveModel::Serializer
  attributes :id, :title, :overview, :description, :completed
  belongs_to :project_type
end
