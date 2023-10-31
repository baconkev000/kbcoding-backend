class CourseSerializer < ActiveModel::Serializer
  attributes :id, :name, :description, :completed
  belongs_to :course_type
  has_many :sections
end
