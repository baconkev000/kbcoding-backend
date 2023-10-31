class Api::V1::CoursesController < ApplicationController
  def index
    courses = Course.all
    render json:courses, status:200
  end

  def show
    courses = Course.find(params[:id])
    if courses
      render json:courses, status:200
    else
      render json: {error: "Error finding course"}, status:404
    end
  end

  def create
    courses = Course.new(course_params)

    if courses.save
      render json:courses, status:200
    else
      render json: {error: "Error creating course"}, status:400
    end
  end

  def update
    courses = Course.find(params[:id])

    if courses.update(course_params)
      render json:courses, status:200
    else
      render json: {error: "Error updating course"}, status:400
    end
  end

  private
    def course_params
      params.require(:course).permit(:name, :description, :course_type_id, :completed)
    end
end
