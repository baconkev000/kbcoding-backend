class VideoSerializer < ActiveModel::Serializer
  attributes :id, :name, :video, :completed
end
