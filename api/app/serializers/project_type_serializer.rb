class ProjectTypeSerializer < ActiveModel::Serializer
  attributes :id, :name, :color
  has_many :projects
end
