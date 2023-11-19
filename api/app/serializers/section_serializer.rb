class SectionSerializer < ActiveModel::Serializer
  attributes :id, :name, :videos
  has_many :videos
end
