class Api::V1::CourseTypesController < ApplicationController
  def index
    course_types = CourseType.all
    render json:course_types, status:200
  end

  def show
    course_types = CourseType.find(params[:id])
    if course_types
      render json:course_types, status:200
    else
      render json: {error: "Error finding course type"}, status:404
    end
  end

  def create
    course_types = CourseType.new(course_type_params)

    if course_types.save
      render json:course_types, status:200
    else
      render json: {error: "Error creating course type"}, status:400
    end
  end

  def update
    course_types = CourseType.find(params[:id])

    if course_types.update(course_type_params)
      render json:course_types, status:200
    else
      render json: {error: "Error creating course type"}, status:400
    end
  end

  private
    def course_type_params
      params.require(:course_type).permit(:name, :color)
    end
end
