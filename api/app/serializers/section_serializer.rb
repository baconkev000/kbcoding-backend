class SectionSerializer < ActiveModel::Serializer
  attributes :id, :name
  has_many :videos
end
