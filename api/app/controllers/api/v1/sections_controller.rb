class Api::V1::SectionsController < ApplicationController
  def index
    sections = Section.all
    render json:sections, status:200
  end

  def show
    sections = Section.find(params[:id])
    if sections
      render json:sections, status:200
    else
      render json: {error: "Error finding section"}, status:404
    end
  end

  def create
    sections = Section.new(section_params)

    if sections.save
      render json:sections, status:200
    else
      render json: {error: "Error creating section"}, status:400
    end
  end

  def update
    sections = Section.find(params[:id])

    if sections.update(section_params)
      render json:sections, status:200
    else
      render json: {error: "Error updating section"}, status:400
    end
  end

  private
    def section_params
      params.require(:section).permit(:name, :course_id, :completed)
    end
end
