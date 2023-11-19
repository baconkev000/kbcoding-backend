class Api::V1::VideosController < ApplicationController
  def index
    videos = Video.all
    render json:videos, status:200
  end

  def show
    videos = Video.find(params[:id])
    if videos
      render json:videos, status:200
    else
      render json: {error: "Error finding course"}, status:404
    end
  end

  def create
    videos = Video.new(video_params)

    if videos.save
      render json:videos, status:200
    else
      render json: {error: "Error creating course"}, status:400
    end
  end

  def update
    videos = Video.find(params[:id])

    if videos.update(video_params)
      render json:videos, status:200
    else
      render json: {error: "Error updating course"}, status:400
    end
  end

  private
    def video_params
      params.require(:video).permit(:name, :section_id, :video, :completed)
    end
end
