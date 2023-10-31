class CourseTypeSerializer < ActiveModel::Serializer
  attributes :id, :name, :color
  has_many :courses
end
